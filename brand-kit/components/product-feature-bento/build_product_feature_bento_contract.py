#!/usr/bin/env python3
"""Build the deterministic PC2-B-C04 Product Feature Bento package.

This mirrors the CMP-01 Global Navigation build and, like it, refuses to run
without an approved human gate. Today it refuses by design: the component is a
candidate, review.json records awaiting-human-review, and no decision exists in
governance/decisions.json. That is the correct state, not a bug. An agent may
build the component; only Olli can promote it.

Once a decision exists, set status canonical, productionAuthority true, record
the decision ID in both the contract and the review, and this will produce
dist/ and the matching release directory.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
DIST = ROOT / "dist"
RELEASE = BRAND_KIT / "releases" / "components" / "product-feature-bento"
ROOT_FILES = (
    "product-feature-bento.source.json",
    "product-feature-bento.schema.json",
    "review.json",
    "README.md",
)
DECISIONS = BRAND_KIT / "governance" / "decisions.json"


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

    if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        raise SystemExit(
            "PC2-B-C04 is a candidate. A release requires canonical authority, which requires "
            "Olli's approval. Nothing was built."
        )
    if review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        raise SystemExit("PC2-B-C04 build requires the approved human gate. Nothing was built.")

    decision = review.get("decisionId")
    if not decision or decision not in source.get("decisionIds", []):
        raise SystemExit("the approved bento decision is missing from the contract. Nothing was built.")
    approved = {entry.get("decisionId") for entry in json.loads(DECISIONS.read_text(encoding="utf-8")).get("decisions", [])}
    if decision not in approved:
        raise SystemExit(f"{decision} is not recorded in governance/decisions.json. Nothing was built.")

    version = source["version"]
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for name in ROOT_FILES:
        copy_file(ROOT / name, name)
    for name in ("mez-product-feature-bento.js", "mez-product-feature-bento.css"):
        copy_file(ROOT / name, f"components/product-feature-bento/{name}")
    for path in sorted((ROOT / "fixtures").iterdir()):
        if path.is_file():
            copy_file(path, f"components/product-feature-bento/fixtures/{path.name}")

    copy_file(BRAND_KIT / "registry/products.json", "registry/products.json")
    copy_file(BRAND_KIT / "gradient-library/catalogue.json", "gradient-library/catalogue.json")
    for product in json.loads((BRAND_KIT / "registry/products.json").read_text(encoding="utf-8"))["products"]:
        name = f"{product['gradientId'].lower()}.webp"
        copy_file(BRAND_KIT / "gradient-library/assets/static" / name, f"gradient-library/assets/static/{name}")
    copy_file(BRAND_KIT / "source-pack/design-system-export/mz-core.js", "source-pack/design-system-export/mz-core.js")
    copy_file(BRAND_KIT / "source-pack/design-system-export/assets/wings.svg", "source-pack/design-system-export/assets/wings.svg")
    for path in (BRAND_KIT / "releases/foundations/dist").rglob("*"):
        if path.is_file():
            copy_file(path, f"foundations/{path.relative_to(BRAND_KIT / 'releases/foundations/dist')}")

    manifest = {
        "componentId": source["componentId"],
        "pantryId": source["pantryId"],
        "version": version,
        "decisionId": decision,
        "files": {
            str(path.relative_to(DIST)): sha256(path)
            for path in sorted(DIST.rglob("*")) if path.is_file()
        },
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    target = RELEASE / version
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(DIST, target)
    print(f"PC2-B-C04 {version} built: {len(manifest['files'])} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
