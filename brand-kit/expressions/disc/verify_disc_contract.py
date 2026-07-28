#!/usr/bin/env python3
"""Verify the canonical Mez product-disc contract and immutable dependencies."""

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
SOURCE = ROOT / "disc.source.json"
SCHEMA = ROOT / "disc.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "expressions" / "disc"


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
        failures.append("review gate or candidate revision drifted")
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True:
        failures.append("disc expression must be canonical 1.0.0 after approval")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-DISC-EXPRESSION-001" or review.get("resultingStatus") != "canonical" or review.get("productionAuthority") is not True:
        failures.append("canonical status is not backed by the approved human gate")
    if "DEC-DISC-EXPRESSION-001" not in source.get("decisionIds", []):
        failures.append("canonical disc decision is not applied")
    geometry = source.get("geometry", {})
    expected_geometry = {"shape": "circle", "aspectRatio": 1, "edge": "hard", "overflow": "hidden", "border": "none", "shadow": "none", "insetTile": False, "halo": False, "glow": False, "sphereShading": False}
    if geometry != expected_geometry:
        failures.append("disc geometry is not the approved flat hard-edged circle")
    wings = source.get("wings", {})
    if wings.get("widthRatio") != 0.39 or wings.get("minimumMarkedDiscPx") != 48 or wings.get("colour") != "#FFFFFF":
        failures.append("Wings scale, minimum marked size or colour drifted")
    bands = source.get("scaleBands", [])
    if [(band.get("minimumPx"), band.get("maximumPx")) for band in bands] != [(24, 47), (48, 127), (128, 359), (360, 639), (640, None)]:
        failures.append("contextual scale bands are incomplete or overlapping")
    allocation = source.get("allocation", {})
    if allocation.get("staticDefault") is not True or allocation.get("maximumLivePerViewport") != 1:
        failures.append("static default or one-live-per-viewport rule drifted")
    policy_text = json.dumps({"geometry": geometry, "allocation": allocation, "surfaces": source.get("surfaces"), "accessibility": source.get("accessibility")}).lower()
    for phrase in ("no glow", "reduced motion", "webgl failure", "perfect circle", "layout shift", "equal disc geometry"):
        if phrase not in policy_text:
            failures.append(f"disc policy missing boundary: {phrase}")
    products_registry = read_json(BRAND_KIT / "registry" / "products.json")
    gradients_registry = read_json(BRAND_KIT / "registry" / "gradients.json")
    registered_products = {item["productId"]: item for item in products_registry["products"]}
    registered_gradients = {item["id"]: item for item in gradients_registry["gradients"]}
    if len(source.get("products", [])) != 5:
        failures.append("exactly five approved product cores are required")
    protected_paths = [
        BRAND_KIT / source["dependencies"]["foundationManifest"]["path"].removeprefix("brand-kit/"),
        BRAND_KIT / source["dependencies"]["renderer"]["path"].removeprefix("brand-kit/"),
        BRAND_KIT / wings["assetPath"].removeprefix("brand-kit/"),
        BRAND_KIT / "registry" / "products.json",
        BRAND_KIT / "registry" / "gradients.json",
    ]
    for product in source.get("products", []):
        registered = registered_products.get(product["productId"], {})
        gradient = registered_gradients.get(product["gradientId"], {})
        if registered.get("publicName") != product["publicName"] or registered.get("gradientId") != product["gradientId"] or registered.get("identityState") != "locked":
            failures.append(f"product assignment drift: {product['productId']}")
        if gradient.get("source", {}).get("sha256") != product["sourceSha256"] or gradient.get("staticTwin", {}).get("sha256") != product["staticTwinSha256"]:
            failures.append(f"source or exact static twin drift: {product['gradientId']}")
        static_path = BRAND_KIT / product["staticTwinPath"].removeprefix("brand-kit/")
        protected_paths.extend([BRAND_KIT / gradient.get("source", {}).get("path", "missing"), static_path])
        if not static_path.is_file() or sha256(static_path) != product["staticTwinSha256"]:
            failures.append(f"static twin file mismatch: {product['gradientId']}")
    declared_hashes = {
        protected_paths[0]: source["dependencies"]["foundationManifest"]["sha256"],
        protected_paths[1]: source["dependencies"]["renderer"]["sha256"],
        protected_paths[2]: wings["sha256"],
    }
    for path, declared in declared_hashes.items():
        if not path.is_file() or sha256(path) != declared:
            failures.append(f"declared immutable dependency drift: {path.relative_to(BRAND_KIT)}")
    protected_before = {path: sha256(path) for path in protected_paths if path.is_file()}
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_disc_contract.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    if protected_before != {path: sha256(path) for path in protected_before}:
        failures.append("a canonical dependency changed during the disc build")
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if manifest.get("productionAuthority") is not True or manifest.get("artifactCount") != len(manifest.get("artifacts", [])):
        failures.append("canonical manifest authority or count is invalid")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    if package.get("productionReadyForScope") is not True or package.get("productionAuthority") is not True or package.get("reviewGateId") != "H-EXP-01-DISC-PROOF":
        failures.append("canonical package loses bounded authority or its gate")
    with tempfile.TemporaryDirectory() as temporary:
        isolated = Path(temporary) / "disc"
        shutil.copytree(DIST, isolated)
        if not all((isolated / entrypoint).is_file() for entrypoint in package.get("entrypoints", {}).values()):
            failures.append("isolated metadata package is missing an entrypoint")
    html_path = WORKBENCH / "index.html"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    for phrase in ("One chassis", "Exact static", "Scale bands", "One live", "Five products", "Surface proof", "Failure proof", "Channel allocation", "H-EXP-01-DISC-PROOF"):
        if phrase not in html:
            failures.append(f"human proof missing: {phrase}")
    if "http://" in html or "https://" in html:
        failures.append("human proof must not load external runtime assets")
    if html.count("data-mz-core") != 1:
        failures.append("human proof must contain exactly one animated Living Core mount")
    script = (WORKBENCH / "disc.js").read_text(encoding="utf-8") if (WORKBENCH / "disc.js").is_file() else ""
    for phrase in ("forceStatic", "disableWebGL", "mountLivingCores", "prefers-reduced-motion"):
        if phrase not in script:
            failures.append(f"workbench runtime missing proof control: {phrase}")
    if failures:
        print("MEZ DISC CONTRACT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ DISC CONTRACT: PASS")
    print("- one hard circular chassis, 0.39 Wings ratio and five contextual scale bands validate")
    print("- five locked products retain their exact source and static-twin hashes")
    print("- one live focal core and static repeated allocation are visible in the proof")
    print("- canonical 1.0.0 authority is backed by approved H-EXP-01-DISC-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
