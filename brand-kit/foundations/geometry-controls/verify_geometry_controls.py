#!/usr/bin/env python3
"""Verify the canonical Mez geometry, depth, and controls foundation."""

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
SOURCE = ROOT / "geometry-controls.source.json"
SCHEMA = ROOT / "geometry-controls.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "foundations" / "geometry-controls"
PROTECTED = [
    BRAND_KIT / "foundations" / "typography" / "dist" / "package.json",
    BRAND_KIT / "foundations" / "colour" / "dist" / "package.json",
    BRAND_KIT / "foundations" / "space-layout" / "dist" / "package.json",
    BRAND_KIT / "registry" / "gradients.json",
    BRAND_KIT / "gradient-library" / "approval.json",
]


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
        failures.append("FND-04 must be canonical after approval")
    if source.get("candidateGateId") != "H-FND-04-CONTROL-PROOF" or source.get("candidateRevision") != "control-lock-01":
        failures.append("FND-04 gate or candidate revision drifted")
    if "DEC-GEOMETRY-CONTROLS-FOUNDATION-001" not in source.get("decisionIds", []):
        failures.append("canonical geometry-controls decision is not applied")
    if review.get("gateId") != source.get("candidateGateId") or review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        failures.append("canonical status is not backed by the approved human gate")
    if review.get("candidateRevision") != source.get("candidateRevision") or review.get("resultingStatus") != "canonical":
        failures.append("approval record does not resolve control-lock-01 to canonical")
    radii = source.get("radii", {})
    if radii.get("control") != 12 or list(radii.values())[:-1] != sorted(set(list(radii.values())[:-1])):
        failures.append("radius scale must be ascending with the approved twelve-pixel control role")
    scale = source.get("controlScale", {})
    if [scale.get(name, {}).get("height") for name in ("compact", "default", "prominent")] != [40, 48, 52]:
        failures.append("approved control heights must remain 40, 48 and 52 pixels")
    if source.get("motion", {}).get("hoverLift") != -1 or source.get("focus", {}).get("width") != 3:
        failures.append("approved micro-lift or focus contract drifted")
    required_states = {"rest", "hover", "focusVisible", "active", "loading", "disabled", "error", "destructiveConfirmation"}
    if set(source.get("stateContracts", {})) != required_states:
        failures.append("control state contract is incomplete")
    policies = " ".join(source.get("policies", {}).values()).lower()
    for phrase in ("glow", "forced-colour", "reduced motion", "one primary", "full rounding"):
        if phrase not in policies:
            failures.append(f"control policies missing boundary: {phrase}")
    protected_before = {path: sha256(path) for path in PROTECTED}
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_geometry_controls.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    if protected_before != {path: sha256(path) for path in PROTECTED}:
        failures.append("canonical dependency or gradient authority changed during control build")
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("manifest artifact count mismatch")
    for artifact in manifest.get("artifacts", []):
        relative = Path(artifact["path"])
        path = DIST / relative
        if relative.is_absolute() or ".." in relative.parts or not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("reviewGateId") != "H-FND-04-CONTROL-PROOF":
        failures.append("canonical package loses its bounded production authority or review gate")
    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "geometry-controls"
        shutil.copytree(DIST, isolated)
        if not all((isolated / name).is_file() for name in package.get("entrypoints", {}).values()):
            failures.append("isolated package is missing an entrypoint")
    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in ("Quiet pressure", "Shape grammar", "Border grammar", "Depth is conditional", "State matrix", "Field system", "Dark surface", "Mobile hierarchy", "Accessibility contract", "Failure modes", "H-FND-04-CONTROL-PROOF"):
        if phrase not in html:
            failures.append(f"human proof missing: {phrase}")
    if "http://" in html or "https://" in html:
        failures.append("human proof must not load external runtime assets")
    if not (WORKBENCH / "styles.css").is_file() or not (WORKBENCH / "review.js").is_file():
        failures.append("human proof styles or review interaction missing")
    if failures:
        print("MEZ GEOMETRY + CONTROLS FOUNDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GEOMETRY + CONTROLS FOUNDATION: PASS")
    print(f"- {len(radii)} named radii preserve the approved twelve-pixel control role")
    print(f"- {len(source['variants'])} variants and {len(source['stateContracts'])} complete state contracts validate")
    print("- canonical portable package rebuilds without drift and dependency authority is unchanged")
    print("- canonical status is backed by approved H-FND-04-CONTROL-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
