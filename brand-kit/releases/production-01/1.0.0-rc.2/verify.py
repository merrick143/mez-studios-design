#!/usr/bin/env python3
"""Dependency-free verifier for the isolated CERT-01 rc.2 package."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def load(path: Path, failures: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        failures.append(f"invalid JSON {path}: {error}")
        return {}


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    failures: list[str] = []
    baseline = root / "verify_baseline.py"
    if not baseline.is_file():
        failures.append("package baseline verifier is missing")
    else:
        run = subprocess.run(
            [sys.executable, "-I", "-B", str(baseline)],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        if run.returncode != 0:
            failures.append("rc.1 baseline contract failed after the rc.2 overlay: " + (run.stdout + run.stderr).strip())

    package = load(root / "package.json", failures)
    manifest = load(root / "manifest.json", failures)
    source = load(root / "certification/certification.source.json", failures)
    scope = load(root / "certification/scope.json", failures)
    build_boundary = load(root / "certification/BUILD-BOUNDARY.json", failures)
    figma = load(root / "mirrors/figma/approval.json", failures)
    ui = load(root / "product-ui/contract/approval.json", failures)
    health = load(root / "certification/health-checks.json", failures)
    transfer = load(root / "certification/benchmarks/transfer-results.json", failures)

    def expect(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    expect(package.get("name") == "@mez-systems/design-system-web", "wrong package name")
    expect(package.get("version") == manifest.get("version") == "1.0.0-rc.2", "rc.2 identity mismatch")
    expect(package.get("status") == manifest.get("status") == "candidate", "package must remain candidate")
    expect(package.get("productionAuthority") is False, "package claims production authority")
    expect(manifest.get("productionAuthority") is False, "manifest claims production authority")
    expect(manifest.get("taskId") == "TASK-CERT-01-SYSTEM-CERTIFICATION", "manifest task mismatch")
    expect(manifest.get("gateId") == "H-CERT-01-SYSTEM-CERTIFICATION", "manifest gate mismatch")
    expect(source.get("status") == "candidate-awaiting-human", "certification source is not awaiting human")
    expect(source.get("humanGate", {}).get("status") == "pending", "H-CERT-01 must remain pending inside candidate")
    expect(source.get("authorityBoundary", {}).get("deferredChannelsCertified") is False, "deferred channels were certified")
    expect(len(scope.get("explicitlyUncertified", [])) == 9, "exact deferred-channel scope is absent")
    expect(scope.get("productionAuthority") is False, "scope claims production authority")
    expect(build_boundary.get("frozenPredecessorManifestSha256") == "c9b5074b79c3f13450b7d826e938b31deda129fc5992ac70b4bafea90e5c4df8", "frozen rc.1 identity missing")
    expect(build_boundary.get("consumerIntegrationAuthority") is False, "candidate claims consumer authority")
    expect(figma.get("verdict") == "approved" and figma.get("canonicalAuthority") is False, "Figma mirror boundary widened")
    expect(ui.get("verdict") == "approved" and ui.get("canonicalAuthority") is False, "Product UI boundary widened")
    expect(ui.get("productionAuthority") is False, "Product UI claims production authority")
    expect(health.get("failurePolicy") == "fail-closed", "health-check failure policy is not fail-closed")
    expect(transfer.get("result") in {"pass", "pass-with-auth-limitation"}, "model-transfer result is not an honest pass state")

    required = [
        "product-ui/index.html",
        "product-ui/fixtures/system-proof.json",
        "mirrors/figma/approval.json",
        "certification/certification.source.json",
        "certification/scope.json",
        "certification/audits/authority.json",
        "certification/audits/accessibility.json",
        "certification/audits/portability.json",
        "certification/audits/onboarding.json",
        "certification/audits/release-governance.json",
        "certification/benchmarks/contract-replay.json",
        "certification/benchmarks/transfer-results.json",
    ]
    for relative in required:
        expect((root / relative).is_file(), f"required rc.2 artifact missing: {relative}")

    manifest_path = root / "manifest.json"
    listed = {row.get("path") for row in manifest.get("artifacts", [])}
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path != manifest_path and "__pycache__" not in path.parts
    }
    expect(listed == actual, "rc.2 manifest file set mismatch")
    rows = []
    for row in manifest.get("artifacts", []):
        relative = row.get("path", "")
        path = root / relative
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expect(row.get("sha256") == digest, f"artifact hash mismatch: {relative}")
        expect(row.get("bytes") == path.stat().st_size, f"artifact size mismatch: {relative}")
        rows.append({"path": relative, "bytes": path.stat().st_size, "sha256": digest})
    rows.sort(key=lambda item: item["path"])
    content_hash = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    expect(manifest.get("contentSha256") == content_hash, "manifest content hash mismatch")

    if failures:
        print("MEZ CERTIFIED RELEASE CANDIDATE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MEZ CERTIFIED RELEASE CANDIDATE: PASS")
    print(f"- {package['name']} {package['version']} ({manifest['contentSha256'][:12]})")
    print(f"- {manifest['artifactCount']} manifest-bound artifacts")
    print("- rc.1 baseline, Figma mirror, Product UI and current-scope certification boundaries agree")
    print("- H-CERT-01, publication, deployment and consumer integration remain pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
