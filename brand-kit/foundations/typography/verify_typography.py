#!/usr/bin/env python3
"""Verify the licensed, generated and reviewable Mez typography foundation."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "typography.source.json"
SCHEMA = ROOT / "typography.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "foundations" / "typography"


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
    schema = read_json(SCHEMA)
    try:
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")

    expected_families = {
        "display": "Geist",
        "body": "Inter",
        "editorial": "Instrument Serif",
        "technical": "IBM Plex Mono",
    }
    actual_families = {key: value.get("name") for key, value in source.get("families", {}).items()}
    if actual_families != expected_families:
        failures.append(f"family policy drift: {actual_families}")
    if source.get("status") != "canonical":
        failures.append("foundation status must be canonical after approval")
    if "DEC-TYPE-001" not in source.get("decisionIds", []):
        failures.append("DEC-TYPE-001 is not applied")
    if "DEC-TYPE-FOUNDATION-001" not in source.get("decisionIds", []):
        failures.append("canonical implementation decision is not applied")
    review = read_json(REVIEW) if REVIEW.is_file() else {}
    if review.get("verdict") != "approve" or review.get("gateId") != "H-FND-01-TYPE-PROOF":
        failures.append("approved human gate record is missing")

    font_paths: set[Path] = set()
    for family_id, family in source.get("families", {}).items():
        licence_path = ROOT / family["licencePath"]
        if not licence_path.is_file():
            failures.append(f"missing licence for {family_id}")
        elif "SIL OPEN FONT LICENSE Version 1.1" not in licence_path.read_text(encoding="utf-8"):
            failures.append(f"invalid OFL notice for {family_id}")
        for asset in family.get("web", []) + family.get("authoring", []):
            path = ROOT / asset["path"]
            font_paths.add(path)
            if not path.is_file():
                failures.append(f"missing font asset: {asset['path']}")
                continue
            magic = path.read_bytes()[:4]
            if asset["format"] == "woff2" and magic != b"wOF2":
                failures.append(f"invalid WOFF2 signature: {asset['path']}")
            if asset["format"] == "ttf" and magic not in {b"\x00\x01\x00\x00", b"true"}:
                failures.append(f"invalid TTF signature: {asset['path']}")

    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run(
        [sys.executable, str(ROOT / "build_typography.py")],
        cwd=BRAND_KIT.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")

    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("manifest artifact count mismatch")
    for artifact in manifest.get("artifacts", []):
        relative = Path(artifact["path"])
        if relative.is_absolute() or ".." in relative.parts:
            failures.append(f"manifest path escapes package: {artifact['path']}")
            continue
        path = DIST / relative
        if not path.is_file():
            failures.append(f"manifest path missing: {artifact['path']}")
        elif path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")

    tokens = read_json(DIST / "tokens.json") if (DIST / "tokens.json").is_file() else {}
    if set(tokens.get("typography", {})) != set(source.get("roles", {})):
        failures.append("generated token roles do not match source roles")
    css = (DIST / "tokens.css").read_text(encoding="utf-8") if (DIST / "tokens.css").is_file() else ""
    if css.count("@font-face") != 6:
        failures.append("generated CSS must declare six approved font faces")
    if "../" in css:
        failures.append("generated CSS escapes the portable package")
    for url in re.findall(r'url\("([^\"]+)"\)', css):
        if not (DIST / url).resolve().is_file():
            failures.append(f"portable CSS asset is missing: {url}")
    for role in source.get("roles", {}):
        if f".mz-type-{role.replace('.', '-')}" not in css:
            failures.append(f"generated CSS missing role: {role}")
    for font_path in font_paths:
        if font_path.suffix == ".woff2" and font_path.name not in css:
            failures.append(f"web font is not referenced by generated CSS: {font_path.name}")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("scope") != "typography-foundation":
        failures.append("portable package does not declare its production-ready scope")
    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "typography"
        shutil.copytree(DIST, isolated)
        isolated_css = (isolated / "tokens.css").read_text(encoding="utf-8")
        for url in re.findall(r'url\("([^\"]+)"\)', isolated_css):
            if not (isolated / url).resolve().is_file():
                failures.append(f"isolated package cannot resolve: {url}")

    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in (
        "Marketing",
        "Commerce",
        "Document",
        "Email",
        "Dense UI",
        "H-FND-01-TYPE-PROOF",
        "Approval record",
        "130% copy",
        "Fallbacks",
    ):
        if phrase not in html:
            failures.append(f"review proof missing: {phrase}")
    for role in source.get("roles", {}):
        if f"mz-type-{role.replace('.', '-')}" not in html:
            failures.append(f"review proof does not show role: {role}")
    if "http://" in html or "https://" in html:
        failures.append("review proof must not load external runtime assets")
    if not (WORKBENCH / "styles.css").is_file() or not (WORKBENCH / "review.js").is_file():
        failures.append("review proof styles or review interaction missing")

    if failures:
        print("MEZ TYPOGRAPHY FOUNDATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MEZ TYPOGRAPHY FOUNDATION: PASS")
    print(f"- {len(expected_families)} licensed families and {len(source['roles'])} semantic roles agree")
    print("- self-contained CSS, fonts, authoring files, licences and artifact hashes rebuild without drift")
    print("- marketing, commerce, document, email and dense-UI proof fixtures are present")
    print(f"- {source['status']} status is backed by approved H-FND-01-TYPE-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
