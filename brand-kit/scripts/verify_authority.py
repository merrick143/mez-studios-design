#!/usr/bin/env python3
"""Validate the Mez Systems authority handshake and dated migration evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
VERSION = "0.1.0-alpha.1"
CUTOVER_ID = "CUTOVER-2026-07-21-01"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    authority = read_json(BRAND_KIT / "authority/authority.json")
    rollback = read_json(BRAND_KIT / "authority/rollback.json")
    proof_path = BRAND_KIT / "authority/clean-clone-proof.json"
    proof = read_json(proof_path) if proof_path.is_file() else None
    activation_proof_path = BRAND_KIT / "authority/activation-proof.json"
    activation_proof = read_json(activation_proof_path) if activation_proof_path.is_file() else None
    dated = read_json(BRAND_KIT / "authority/artifact-manifest-2026-07-21.json")
    source = read_json(BRAND_KIT / "source-manifest.json")
    status = read_json(BRAND_KIT / "data/status.json")
    release = read_json(BRAND_KIT / f"releases/{VERSION}/release.json")
    products = read_json(BRAND_KIT / "registry/products.json")
    gradients = read_json(BRAND_KIT / "registry/gradients.json")
    assets = read_json(BRAND_KIT / "registry/assets.json")

    if authority.get("cutoverId") != CUTOVER_ID or authority.get("activeRelease") != VERSION:
        failures.append("authority cutover or release identity drift")
    state = authority.get("status")
    if state not in {"prepared", "canonical-active"}:
        failures.append(f"invalid authority state: {state}")
    expected_production = state == "canonical-active"
    if authority.get("productionAuthority") is not expected_production:
        failures.append("authority production flag disagrees with state")
    if authority.get("rank") != (1 if expected_production else None):
        failures.append("authority rank disagrees with state")
    if rollback.get("cutoverId") != CUTOVER_ID or rollback.get("restore", {}).get("commit") != "822aa91":
        failures.append("rollback record does not preserve the frozen internal checkpoint")
    if proof is None or proof.get("status") != "passed" or proof.get("validatedCommit") != "698152ede765958e0e35323652a0dccc0470afde":
        failures.append("prepared clean-clone proof is missing or does not pin commit 698152e")
    if expected_production and not authority.get("previousAuthority", {}).get("transitionCommit"):
        failures.append("active authority must name the internal transfer commit")
    if expected_production:
        if activation_proof is None or activation_proof.get("status") != "passed":
            failures.append("active authority must preserve the clean-clone activation proof")
        elif activation_proof.get("validatedCommit") != "19f1570fd8943c4aa7a031f3d5c65c203346366b":
            failures.append("activation proof must pin canonical activation commit 19f1570")

    for registry in (products, gradients, assets):
        if registry.get("authorityState") != state or registry.get("productionAuthority") is not expected_production:
            failures.append(f"registry authority mismatch: {registry.get('registryId')}")
    if release.get("authorityState") != state or release.get("canonicalSnapshot") is not expected_production:
        failures.append("release authority state mismatch")
    if release.get("productionReady") is not False:
        failures.append("migration alpha must not claim foundation-complete production readiness")

    if expected_production:
        if source.get("workbenchStatus") != "canonical-control-plane" or source.get("productionAuthority") is not True:
            failures.append("source manifest must identify the active canonical control plane")
        if status.get("canonicalRepositoryTransferred") is not True:
            failures.append("programme status must record completed repository transfer")
    else:
        if source.get("workbenchStatus") != "non-canonical-migration-proof" or source.get("productionAuthority") is not False:
            failures.append("prepared snapshot must not override the internal authority")
        if status.get("canonicalRepositoryTransferred") is not False:
            failures.append("prepared programme status must not claim transfer")

    if dated.get("cutoverId") != CUTOVER_ID or dated.get("authorityState") != state:
        failures.append("dated migration manifest state drift")
    if dated.get("artifactCount") != len(dated.get("artifacts", [])):
        failures.append("dated migration artifact count mismatch")
    for row in dated.get("artifacts", []):
        path = BRAND_KIT / row["path"]
        if not path.is_file() or path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            failures.append(f"dated migration artifact drift: {row['path']}")

    verifier = subprocess.run(
        [sys.executable, str(BRAND_KIT / f"releases/{VERSION}/verify.py")],
        cwd=BRAND_KIT / f"releases/{VERSION}",
        text=True,
        capture_output=True,
        check=False,
    )
    if verifier.returncode:
        failures.append("self-contained release verifier failed: " + verifier.stdout.strip())

    if failures:
        print("MEZ AUTHORITY GATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ AUTHORITY GATE: PASS")
    print(f"- cutover {CUTOVER_ID} is {state}")
    print(f"- release {VERSION}, registries and dated artifacts agree")
    print("- prepared commit 698152e passed clean-clone and deterministic rebuild proof")
    if expected_production:
        print("- activation commit 19f1570 passed canonical clean-clone proof")
    print("- rollback to internal commit 822aa91 remains explicit")
    print("- migration alpha remains distinct from production readiness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
