#!/usr/bin/env python3
"""Verify the canonical Mez colour and surfaces foundation."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "colour.source.json"
SCHEMA = ROOT / "colour.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "foundations" / "colour"
PROTECTED = [BRAND_KIT / "registry" / "gradients.json", BRAND_KIT / "gradient-library" / "approval.json", BRAND_KIT / "gradient-library" / "palettes.json"]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA), format_checker=jsonschema.FormatChecker()).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")

    if source.get("status") != "canonical":
        failures.append("FND-02 must be canonical after approval")
    if source.get("candidateGateId") != "H-FND-02-SURFACE-PROOF":
        failures.append("human gate identity drift")
    if source.get("candidateRevision") != "final-lock-02":
        failures.append("FND-02 candidate revision is not the final lock revision")
    if "DEC-COLOUR-FOUNDATION-001" not in source.get("decisionIds", []):
        failures.append("canonical colour implementation decision is not applied")
    if review.get("verdict") != "approve" or review.get("gateId") != "H-FND-02-SURFACE-PROOF":
        failures.append("canonical status is not backed by the approved human gate")
    if review.get("candidateRevision") != source.get("candidateRevision") or review.get("resultingStatus") != "canonical":
        failures.append("approval record does not resolve the final-lock candidate to canonical")
    mode_roles = [set(mode.get("roles", {})) for mode in source.get("modes", {}).values()]
    if not mode_roles or any(roles != mode_roles[0] for roles in mode_roles[1:]):
        failures.append("semantic role parity differs between modes")
    for mode_name, mode in source.get("modes", {}).items():
        for role, reference in mode.get("roles", {}).items():
            if reference not in source.get("primitives", {}):
                failures.append(f"unresolved primitive: {mode_name}:{role} -> {reference}")

    protected_before = {path: sha256(path) for path in PROTECTED}
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_colour.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    if protected_before != {path: sha256(path) for path in PROTECTED}:
        failures.append("gradient or Living Core authority changed during colour build")

    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("manifest artifact count mismatch")
    for artifact in manifest.get("artifacts", []):
        relative = Path(artifact["path"])
        if relative.is_absolute() or ".." in relative.parts:
            failures.append(f"manifest path escapes package: {artifact['path']}")
            continue
        path = DIST / relative
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")

    report = read_json(DIST / "contrast-report.json") if (DIST / "contrast-report.json").is_file() else {}
    if report.get("failureCount") != 0:
        failures.append(f"contrast report has {report.get('failureCount')} failures")
    expected_checks = len(source.get("modes", {})) * len(source.get("contrastPairs", []))
    if report.get("checkCount") != expected_checks:
        failures.append("contrast report check count mismatch")

    css = (DIST / "tokens.css").read_text(encoding="utf-8") if (DIST / "tokens.css").is_file() else ""
    for phrase in ('data-mz-mode="dark"', 'data-mz-mode="email"', 'data-mz-mode="document"', '@media print', 'forced-colors: active'):
        if phrase not in css:
            failures.append(f"generated CSS missing: {phrase}")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("reviewGateId") != "H-FND-02-SURFACE-PROOF":
        failures.append("canonical package loses its bounded production authority or review gate")
    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "colour"
        shutil.copytree(DIST, isolated)
        if not all((isolated / name).is_file() for name in package.get("entrypoints", {}).values()):
            failures.append("isolated package is missing an entrypoint")

    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in ("Canvas decision", "Identity inheritance", "Canonical", "Approval record", "Contained dark", "Email", "Document", "Print", "Functional feedback", "Failure modes", "H-FND-02-SURFACE-PROOF"):
        if phrase not in html:
            failures.append(f"human proof missing: {phrase}")
    if "http://" in html or "https://" in html:
        failures.append("human proof must not load external runtime assets")
    if not (WORKBENCH / "styles.css").is_file() or not (WORKBENCH / "review.js").is_file():
        failures.append("human proof styles or review interaction missing")

    if failures:
        print("MEZ COLOUR FOUNDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ COLOUR FOUNDATION: PASS")
    print(f"- {len(source['primitives'])} primitives and {len(mode_roles[0])} semantic roles agree across five modes")
    print(f"- {report['checkCount']} contrast pairs pass with zero hidden channel overrides")
    print("- canonical portable package rebuilds without drift and protected gradient authority is unchanged")
    print("- canonical status is backed by approved H-FND-02-SURFACE-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
