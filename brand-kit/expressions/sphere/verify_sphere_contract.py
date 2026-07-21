#!/usr/bin/env python3
"""Verify the canonical Mez sphere and its immutable dependencies."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "sphere.source.json"
SCHEMA = ROOT / "sphere.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "expressions" / "sphere"

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
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")
    if review.get("gateId") != source.get("candidateGateId") or review.get("candidateRevision") != source.get("candidateRevision"):
        failures.append("review gate or revision drifted")
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True:
        failures.append("sphere must be canonical 1.0.0")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-SPHERE-EXPRESSION-001" or review.get("resultingStatus") != "canonical" or review.get("productionAuthority") is not True:
        failures.append("canonical status is not backed by the approved human gate")
    if "DEC-SPHERE-EXPRESSION-001" not in source.get("decisionIds", []):
        failures.append("canonical sphere decision is not applied")
    geometry = source.get("geometry", {})
    expected = {"shape": "sphere", "aspectRatio": 1, "edge": "hard circular mask", "overflow": "hidden", "border": "none", "cssShadow": "none", "externalHalo": False, "externalGlow": False, "depthSource": "approved renderer sphere branch only", "distortion": "never"}
    if geometry != expected:
        failures.append("sphere geometry or depth boundary drifted")
    finish = source.get("finish", {})
    decision = read_json(BRAND_KIT / "gradient-library" / "calibration" / "depth-light-01" / "decision.json")
    if finish.get("profileId") != "deep" or finish.get("values") != decision.get("values"):
        failures.append("Deep Mineral values drifted from the approved decision")
    wings = source.get("wings", {})
    if wings.get("widthRatio") != 0.39 or wings.get("colour") != "#FFFFFF" or "completely visible" not in wings.get("cropPolicy", ""):
        failures.append("canonical Wings or crop rule drifted")
    bands = source.get("scaleBands", [])
    if [(band.get("minimumPx"), band.get("maximumPx")) for band in bands] != [(360, 639), (640, 959), (960, None)]:
        failures.append("feature, hero and immersive bands are incomplete")
    allocation = source.get("allocation", {})
    if allocation.get("maximumLivePerViewport") != 1 or "Below 360px" not in json.dumps(bands):
        failures.append("single-live or disc-below-360 rule drifted")
    policy = json.dumps({"geometry": geometry, "finish": finish, "allocation": allocation, "fallback": source.get("fallback"), "accessibility": source.get("accessibility")}).lower()
    for phrase in ("external cloud", "never grows", "exact colour fallback; depth removed", "never stretch into an ellipse"):
        if phrase not in policy:
            failures.append(f"sphere policy missing boundary: {phrase}")
    protected: list[Path] = []
    for dependency in source.get("dependencies", {}).values():
        path = BRAND_KIT / dependency["path"].removeprefix("brand-kit/")
        protected.append(path)
        if not path.is_file() or sha256(path) != dependency["sha256"]:
            failures.append(f"immutable dependency drift: {dependency['path']}")
    product = source.get("proofProduct", {})
    for key, hash_key in (("sourcePath", "sourceSha256"), ("staticTwinPath", "staticTwinSha256")):
        path = BRAND_KIT / product.get(key, "missing").removeprefix("brand-kit/")
        protected.append(path)
        if not path.is_file() or sha256(path) != product.get(hash_key):
            failures.append(f"proof product asset drift: {product.get(key)}")
    protected.append(BRAND_KIT / wings.get("assetPath", "missing").removeprefix("brand-kit/"))
    if not protected[-1].is_file() or sha256(protected[-1]) != wings.get("sha256"):
        failures.append("canonical Wings asset drifted")
    protected_before = {path: sha256(path) for path in protected if path.is_file()}
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_sphere_contract.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    if protected_before != {path: sha256(path) for path in protected_before}:
        failures.append("a canonical dependency changed during the sphere build")
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if manifest.get("productionAuthority") is not True or package.get("productionReadyForScope") is not True or package.get("productionAuthority") is not True:
        failures.append("canonical package loses bounded production authority")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in ("One dimensional focal state", "Not under review", "Same core", "Depth", "Scale + crop", "Exact colour fallback", "H-EXP-02-SPHERE-PROOF"):
        if phrase not in html:
            failures.append(f"human proof missing: {phrase}")
    if "http://" in html or "https://" in html:
        failures.append("human proof must not load external runtime assets")
    if html.count("data-mz-core") != 1 or 'data-shape="sphere"' not in html:
        failures.append("human proof must contain exactly one sphere runtime mount")
    css = (WORKBENCH / "styles.css").read_text(encoding="utf-8") if (WORKBENCH / "styles.css").is_file() else ""
    for phrase in ("var(--mz-font-display)", "var(--mz-font-body)"):
        if phrase not in css:
            failures.append(f"workbench typography mapping missing: {phrase}")
    script = (WORKBENCH / "sphere.js").read_text(encoding="utf-8") if (WORKBENCH / "sphere.js").is_file() else ""
    for phrase in ("forceStatic", "disableWebGL", "mountLivingCores", "prefers-reduced-motion"):
        if phrase not in script:
            failures.append(f"workbench runtime missing proof control: {phrase}")
    if failures:
        print("MEZ SPHERE CONTRACT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ SPHERE CONTRACT: PASS")
    print("- approved depth is the only identity variable added to the canonical disc")
    print("- feature, hero and immersive bands preserve a 1:1 sphere and visible Wings")
    print("- one live focal object and exact-colour depthless fallback are explicit")
    print("- canonical 1.0.0 authority is backed by approved H-EXP-02-SPHERE-PROOF")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
