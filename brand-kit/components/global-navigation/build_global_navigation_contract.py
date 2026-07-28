#!/usr/bin/env python3
"""Build the deterministic canonical CMP-01 Global Navigation package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
DIST = ROOT / "dist"
RELEASE = BRAND_KIT / "releases" / "components" / "global-navigation" / "1.0.0"
ROOT_FILES = ("global-navigation.source.json", "global-navigation.schema.json", "review.json", "README.md")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(source: Path, relative: str) -> None:
    destination = DIST / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> int:
    source = json.loads((ROOT / ROOT_FILES[0]).read_text(encoding="utf-8"))
    review = json.loads((ROOT / "review.json").read_text(encoding="utf-8"))
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True:
        raise SystemExit("CMP-01 build requires canonical 1.0.0 authority")
    if review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        raise SystemExit("CMP-01 build requires the approved human gate")
    if review.get("decisionId") not in source.get("decisionIds", []):
        raise SystemExit("approved Global Navigation decision is missing from the source contract")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for name in ROOT_FILES:
        copy_file(ROOT / name, name)
    for name in ("mez-global-navigation.js", "mez-global-navigation.css"):
        copy_file(ROOT / name, f"components/global-navigation/{name}")
    for path in (ROOT / "fixtures").iterdir():
        if path.is_file():
            copy_file(path, f"components/global-navigation/fixtures/{path.name}")
    copy_file(BRAND_KIT / "registry/products.json", "registry/products.json")
    copy_file(BRAND_KIT / "gradient-library/catalogue.json", "gradient-library/catalogue.json")
    product_gradients = json.loads((BRAND_KIT / "registry/products.json").read_text(encoding="utf-8"))["products"]
    for product in product_gradients:
        name = f"{product['gradientId'].lower()}.webp"
        copy_file(BRAND_KIT / "gradient-library/assets/static" / name, f"gradient-library/assets/static/{name}")
    copy_file(BRAND_KIT / "source-pack/design-system-export/mz-core.js", "source-pack/design-system-export/mz-core.js")
    copy_file(BRAND_KIT / "source-pack/design-system-export/assets/wings.svg", "source-pack/design-system-export/assets/wings.svg")
    foundations = BRAND_KIT / "releases/foundations/dist"
    for path in foundations.rglob("*"):
        if path.is_file():
            copy_file(path, f"releases/foundations/dist/{path.relative_to(foundations).as_posix()}")
    package = {
        "schemaVersion":"1.0.0",
        "name":"@mez-systems/global-navigation",
        "version":source["version"],
        "status":source["status"],
        "candidateRevision":source["candidateRevision"],
        "reviewGateId":source["gateId"],
        "decisionId":review["decisionId"],
        "productionReadyForScope":True,
        "productionAuthority":True,
        "entrypoints":{
            "element":"components/global-navigation/mez-global-navigation.js",
            "styles":"components/global-navigation/mez-global-navigation.css",
            "contract":"global-navigation.source.json",
            "schema":"global-navigation.schema.json",
            "review":"review.json",
            "htmlFixture":"components/global-navigation/fixtures/static-html.html",
            "reactFixture":"components/global-navigation/fixtures/react.jsx"
        }
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    paths = sorted(path for path in DIST.rglob("*") if path.is_file() and path.name != "manifest.json")
    manifest = {
        "schemaVersion":"1.0.0",
        "componentId":source["componentId"],
        "version":source["version"],
        "status":source["status"],
        "decisionId":review["decisionId"],
        "productionAuthority":True,
        "artifactCount":len(paths),
        "artifacts":[{"path":path.relative_to(DIST).as_posix(),"bytes":path.stat().st_size,"sha256":sha256(path)} for path in paths]
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if RELEASE.exists():
        shutil.rmtree(RELEASE)
    RELEASE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DIST, RELEASE)
    print("MEZ GLOBAL NAVIGATION 1.0.0: BUILT")
    print(f"- {len(paths)} portable artifacts")
    print("- canonical release mirrored to brand-kit/releases/components/global-navigation/1.0.0")
    print("- H-CMP-01-GLOBAL-NAVIGATION-PROOF closed by DEC-GLOBAL-NAVIGATION-COMPONENT-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
