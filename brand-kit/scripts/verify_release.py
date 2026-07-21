#!/usr/bin/env python3
"""Verify a self-contained Mez Systems migration snapshot using stdlib only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Mez Systems migration release")
    parser.add_argument("--release", type=Path, help="Release directory; defaults to this script's directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release = (args.release or Path(__file__).resolve().parent).resolve()
    failures: list[str] = []
    manifest = read_json(release / "release.json")
    artifacts = read_json(release / "artifact-manifest.json")
    products = read_json(release / "data/products.json")
    gradients = read_json(release / "data/gradients.json")
    assets = read_json(release / "data/assets.json")
    decisions = read_json(release / "data/decisions.json")

    if manifest.get("version") != "0.1.0-alpha.1" or manifest.get("stage") != "migration-snapshot":
        failures.append("release identity or stage drift")
    if manifest.get("productionReady") is not False:
        failures.append("migration alpha must not claim foundation-complete production readiness")
    if artifacts.get("artifactCount") != len(artifacts.get("artifacts", [])):
        failures.append("artifact count mismatch")
    for row in artifacts.get("artifacts", []):
        path = release / row["path"]
        if not path.is_file():
            failures.append(f"missing artifact: {row['path']}")
        elif path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            failures.append(f"artifact drift: {row['path']}")

    expected = {
        "AI OS": "MZ-G13",
        "Context Engine": "MZ-G12",
        "AI Ads System": "MZ-G06",
        "Claude Code OS": "MZ-G15",
        "Organic Content OS": "MZ-G20",
    }
    actual = {row["publicName"]: row["gradientId"] for row in products.get("products", [])}
    if actual != expected or len({row["productId"] for row in products.get("products", [])}) != 5:
        failures.append(f"product identity kernel drift: {actual}")
    retired_names = {"Aurora", "Forge", "Prism"}
    if retired_names.intersection(actual):
        failures.append("retired alternate product names leaked into canonical products")

    rows = gradients.get("gradients", [])
    if len(rows) != 43 or gradients.get("activeCount") != 33 or len(gradients.get("aliases", {})) != 10:
        failures.append("gradient source or alias counts drift")
    if gradients.get("qualityExceptions") != ["MZ-G01"]:
        failures.append("MZ-G01 approved source exception missing")
    for row in rows:
        source = release / row["source"]["path"]
        static = release / row["staticTwin"]["path"]
        if not source.is_file() or sha256(source) != row["source"]["sha256"]:
            failures.append(f"source authority drift: {row['id']}")
        if not static.is_file() or sha256(static) != row["staticTwin"]["sha256"]:
            failures.append(f"static twin drift: {row['id']}")
        if len(row.get("runtime", {}).get("anchors", [])) != 4 or row.get("approximation") is not True:
            failures.append(f"runtime core contract drift: {row['id']}")

    asset_rows = assets.get("assets", [])
    if len(asset_rows) != 88:
        failures.append(f"expected 88 registered assets, found {len(asset_rows)}")
    for row in asset_rows:
        path = release / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            failures.append(f"asset registry drift: {row['assetId']}")

    renderer = (release / "runtime/mz-core.js").read_text(encoding="utf-8")
    if renderer.count('getContext("webgl"') != 1:
        failures.append("Living Core must allocate exactly one WebGL context")
    if "prefers-reduced-motion" not in renderer or "setStaticSurface" not in renderer:
        failures.append("Living Core exact-static fallback contract missing")
    if sha256(release / "assets/wings.svg") != "e6475e216a77a39dda11a634e9cae18e54fff7f5386252f56344492d4d358a33":
        failures.append("canonical Wings hash drift")

    decision_ids = {row["id"] for row in decisions.get("decisions", [])}
    required_decisions = {
        "DEC-MOTION-002",
        "DEC-GRADIENT-LIBRARY-001",
        "DEC-LIVING-CORE-FINISH-001",
        "DEC-MIGRATION-SEQUENCE-001",
        "DEC-PRODUCT-ARCHITECTURE-001",
    }
    if not required_decisions.issubset(decision_ids):
        failures.append("required decision history missing")
    schemas = {path.name for path in (release / "schemas").glob("*.schema.json")}
    expected_schemas = {f"{name}.schema.json" for name in ("product", "gradient", "asset", "decision", "release", "authority")}
    if schemas != expected_schemas:
        failures.append(f"schema set drift: {sorted(schemas)}")

    states = {manifest.get("authorityState"), products.get("authorityState"), gradients.get("authorityState"), assets.get("authorityState")}
    if len(states) != 1 or states.pop() not in {"prepared", "canonical-active"}:
        failures.append("release authority state is inconsistent")

    if failures:
        print("MEZ MIGRATION RELEASE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ MIGRATION RELEASE: PASS")
    print("- literal five-product identity kernel and assignments agree")
    print("- 43 source IDs, 33 active cores and ten aliases agree")
    print("- exact sources, static twins, canonical Wings and shared renderer hashes agree")
    print("- release is self-contained and production readiness remains false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
