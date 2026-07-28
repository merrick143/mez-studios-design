#!/usr/bin/env python3
"""Verify the canonical Mez space, layout, and responsive foundation."""

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
SOURCE = ROOT / "space-layout.source.json"
SCHEMA = ROOT / "space-layout.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "foundations" / "space-layout"
PROTECTED = [
    BRAND_KIT / "foundations" / "typography" / "dist" / "package.json",
    BRAND_KIT / "foundations" / "colour" / "dist" / "package.json",
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
        failures.append("FND-03 must be canonical after approval")
    if source.get("candidateGateId") != "H-FND-03-SPATIAL-PROOF" or source.get("candidateRevision") != "spatial-lock-01":
        failures.append("FND-03 gate or candidate revision drifted")
    if "DEC-SPACE-LAYOUT-FOUNDATION-001" not in source.get("decisionIds", []):
        failures.append("canonical space-layout implementation decision is not applied")
    if review.get("gateId") != source.get("candidateGateId") or review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        failures.append("canonical status is not backed by the approved human gate")
    if review.get("candidateRevision") != source.get("candidateRevision") or review.get("resultingStatus") != "canonical":
        failures.append("approval record does not resolve spatial-lock-01 to canonical")
    if any(value % source.get("baseUnit", 1) for value in source.get("space", {}).values()):
        failures.append("spacing scale contains a value outside the four-pixel rhythm")
    widths = list(source.get("contentWidths", {}).values())
    if widths != sorted(set(widths)):
        failures.append("content widths must be unique and ascending")
    breakpoints = list(source.get("breakpoints", {}).values())
    if breakpoints != sorted(set(breakpoints)):
        failures.append("breakpoints must be unique and ascending")
    profiles = source.get("responsiveProfiles", {})
    for name, profile in profiles.items():
        if profile.get("minWidth") != source.get("breakpoints", {}).get(name):
            failures.append(f"responsive profile does not match breakpoint: {name}")
        for field in ("pageGutter", "gridGap", "sectionCompact", "sectionDefault", "sectionSpacious", "heroTop"):
            if profile.get(field, 1) % source.get("baseUnit", 1):
                failures.append(f"responsive value leaves base rhythm: {name}:{field}")
        if not profile.get("sectionCompact", 0) < profile.get("sectionDefault", 0) < profile.get("sectionSpacious", 0):
            failures.append(f"section rhythm is not ordered: {name}")
    for name, density in source.get("densityModes", {}).items():
        for field in ("componentGap", "componentPadding", "rowMinHeight"):
            if density.get(field, 1) % source.get("baseUnit", 1):
                failures.append(f"density value leaves base rhythm: {name}:{field}")
    protected_before = {path: sha256(path) for path in PROTECTED}
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_space_layout.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    if protected_before != {path: sha256(path) for path in PROTECTED}:
        failures.append("canonical dependency or gradient authority changed during spatial build")
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("manifest artifact count mismatch")
    for artifact in manifest.get("artifacts", []):
        relative = Path(artifact["path"])
        path = DIST / relative
        if relative.is_absolute() or ".." in relative.parts or not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("reviewGateId") != "H-FND-03-SPATIAL-PROOF":
        failures.append("canonical package loses its bounded production authority or review gate")
    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "space-layout"
        shutil.copytree(DIST, isolated)
        if not all((isolated / name).is_file() for name in package.get("entrypoints", {}).values()):
            failures.append("isolated package is missing an entrypoint")
    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in ("Spatial audit", "Three widths", "Responsive profiles", "Density modes", "Source order", "Intentional break", "Channel layouts", "Failure modes", "H-FND-03-SPATIAL-PROOF"):
        if phrase not in html:
            failures.append(f"human proof missing: {phrase}")
    if "http://" in html or "https://" in html:
        failures.append("human proof must not load external runtime assets")
    if not (WORKBENCH / "styles.css").is_file() or not (WORKBENCH / "review.js").is_file():
        failures.append("human proof styles or review interaction missing")
    if failures:
        print("MEZ SPACE + LAYOUT FOUNDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ SPACE + LAYOUT FOUNDATION: PASS")
    print(f"- {len(source['space'])} four-pixel spacing steps and three named content widths agree")
    print(f"- {len(profiles)} responsive profiles and {len(source['densityModes'])} receiver-led density modes validate")
    print("- canonical portable package rebuilds without drift and dependency authority is unchanged")
    print("- canonical status is backed by approved H-FND-03-SPATIAL-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
