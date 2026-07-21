#!/usr/bin/env python3
"""Verify integrity, isolation, authority and proof coverage for FND-05."""

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
SOURCE = ROOT / "release.source.json"
SCHEMA = ROOT / "release.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "foundations" / "release"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_bytes(path: Path) -> dict[str, bytes]:
    return {item.relative_to(path).as_posix(): item.read_bytes() for item in path.rglob("*") if item.is_file()}


def main() -> int:
    failures: list[str] = []
    source = read_json(SOURCE)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")

    expected_keys = ["typography", "colour", "space-layout", "geometry-controls"]
    if [item.get("key") for item in source.get("packages", [])] != expected_keys:
        failures.append("source package sequence must remain typography, colour, space-layout, geometry-controls")
    if source.get("productionAuthority") is not True or source.get("status") != "canonical" or source.get("version") != "1.0.0":
        failures.append("approved unified release is not canonical 1.0.0 with bounded production authority")
    review = read_json(REVIEW)
    if review.get("gateId") != "H-FND-05-FOUNDATION-RELEASE" or review.get("candidateRevision") != "foundation-release-01":
        failures.append("release review record does not identify the bounded gate and revision")
    if review.get("verdict") != "approve" or review.get("productionAuthority") is not True or review.get("resultingStatus") != "canonical":
        failures.append("canonical release is not backed by an approved human record")
    if review.get("decisionId") != "DEC-FOUNDATION-RELEASE-001" or "DEC-FOUNDATION-RELEASE-001" not in source.get("decisionIds", []):
        failures.append("canonical foundation release decision is missing")

    protected = []
    for declared in source.get("packages", []):
        source_dist = BRAND_KIT / "foundations" / declared["key"] / "dist"
        for name, key in (("package.json", "packageSha256"), ("manifest.json", "manifestSha256")):
            path = source_dist / name
            protected.append(path)
            if not path.is_file() or sha256(path) != declared[key]:
                failures.append(f"source integrity drift: {declared['key']}/{name}")
        package = read_json(source_dist / "package.json") if (source_dist / "package.json").is_file() else {}
        review_path = source_dist / "review.json"
        package_review = read_json(review_path) if review_path.is_file() else {}
        if package.get("status") != "canonical" or package.get("version") != "1.0.0" or package.get("productionReadyForScope") is not True:
            failures.append(f"source package is not canonical and production-ready: {declared['key']}")
        if package_review.get("verdict") != "approve" or package_review.get("productionAuthority") is not True:
            failures.append(f"source approval missing: {declared['key']}")

    protected_before = {path: sha256(path) for path in protected if path.is_file()}
    before = tree_bytes(DIST) if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_foundation_release.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = tree_bytes(DIST) if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated release output")
    if protected_before != {path: sha256(path) for path in protected if path.is_file()}:
        failures.append("release build changed a canonical source package")

    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("productionAuthority") is not True or package.get("status") != "canonical":
        failures.append("canonical dist loses production readiness or bounded authority")
    if manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("release manifest artifact count mismatch")
    for artifact in manifest.get("artifacts", []):
        relative = Path(artifact["path"])
        path = DIST / relative
        if relative.is_absolute() or ".." in relative.parts or not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"release manifest drift: {artifact['path']}")

    index_css = (DIST / "index.css").read_text(encoding="utf-8") if (DIST / "index.css").is_file() else ""
    imports = re.findall(r'@import url\("([^"]+)"\);', index_css)
    if imports != source.get("loadOrder"):
        failures.append("single CSS entrypoint does not preserve declared load order")
    for relative in imports:
        if not (DIST / relative).is_file():
            failures.append(f"CSS import does not resolve: {relative}")
    licences = read_json(DIST / "licences.json") if (DIST / "licences.json").is_file() else {}
    if len(licences.get("licences", [])) != 4:
        failures.append("font licence inventory must retain four OFL records")

    for declared in source.get("packages", []):
        nested = DIST / "packages" / declared["key"]
        source_dist = BRAND_KIT / "foundations" / declared["key"] / "dist"
        if tree_bytes(nested) != tree_bytes(source_dist):
            failures.append(f"nested package is not a byte-for-byte canonical copy: {declared['key']}")
        nested_package = read_json(nested / "package.json") if (nested / "package.json").is_file() else {}
        for entrypoint in nested_package.get("entrypoints", {}).values():
            if not (nested / entrypoint).is_file():
                failures.append(f"nested entrypoint missing: {declared['key']}/{entrypoint}")

    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "mez-foundations"
        shutil.copytree(DIST, isolated)
        for relative in imports:
            if not (isolated / relative).is_file():
                failures.append(f"isolated release import missing: {relative}")
        font_urls = []
        typography_css = (isolated / "packages" / "typography" / "tokens.css").read_text(encoding="utf-8")
        font_urls.extend(re.findall(r'url\("?([^"\)]+)"?\)', typography_css))
        for relative in font_urls:
            if relative.startswith(("http:", "https:", "data:")) or not (isolated / "packages" / "typography" / relative).resolve().is_file():
                failures.append(f"isolated font URL does not resolve locally: {relative}")
        runtime_text = index_css + typography_css
        if "http://" in runtime_text or "https://" in runtime_text or str(BRAND_KIT) in runtime_text:
            failures.append("isolated runtime CSS depends on an external or canonical-checkout path")

    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    required_phrases = (
        "One import. Four locked foundations.", "Release audit", "Loading order", "Integrated specimen",
        "Light and dark", "Responsive profiles", "Controls and fields", "Isolated portability",
        "Migration boundary", "Failure modes", "H-FND-05-FOUNDATION-RELEASE",
    )
    for phrase in required_phrases:
        if phrase not in html:
            failures.append(f"release proof missing: {phrase}")
    if '../../../releases/foundations/dist/index.css' not in html:
        failures.append("release proof does not consume the unified CSS entrypoint")
    for forbidden in ("../../../foundations/typography", "../../../foundations/colour", "../../../foundations/space-layout", "../../../foundations/geometry-controls", "http://", "https://"):
        if forbidden in html:
            failures.append(f"release proof contains forbidden runtime dependency: {forbidden}")
    if not (WORKBENCH / "styles.css").is_file() or not (WORKBENCH / "review.js").is_file():
        failures.append("release proof styles or review interaction missing")
    docs = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in ("README.md", "MIGRATION.md"))
    for phrase in ("0.1.0-alpha.1", "one CSS entrypoint", "No production consumer", "H-FND-05-FOUNDATION-RELEASE"):
        if phrase not in docs:
            failures.append(f"release guidance missing boundary: {phrase}")

    if failures:
        print("MEZ FOUNDATION RELEASE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ FOUNDATION RELEASE: PASS")
    print("- four canonical packages match declared hashes and approval gates")
    print("- deterministic build preserves every source package byte-for-byte")
    print("- one ordered CSS entrypoint, local fonts and four licence records resolve in isolation")
    print("- canonical 1.0.0 authority is backed by approved H-FND-05-FOUNDATION-RELEASE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
