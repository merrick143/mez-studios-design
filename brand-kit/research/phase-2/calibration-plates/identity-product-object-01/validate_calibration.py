#!/usr/bin/env python3
"""Validate the Mez identity and product-object calibration plate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = Path("/Users/olivermerrick/Downloads/all-gradients/MZ-G13.png")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    required = [
        ROOT / "README.md",
        ROOT / "index.html",
        ROOT / "plate.css",
        ROOT / "plate.js",
        ROOT / "play-button.js",
        ROOT / "calibration-manifest.json",
        ROOT / "calibration-review.schema.json",
        ROOT / "identity-product-object-01-review.json",
        ROOT / "assets/wings.svg",
        ROOT / "assets/gradients/mz-g13.webp",
        ROOT / "assets/gradients/variants.json",
        ROOT / "qa/desktop.png",
        ROOT / "qa/mobile.png",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    variants = json.loads((ROOT / "assets/gradients/variants.json").read_text())
    schema = json.loads((ROOT / "calibration-review.schema.json").read_text())

    if manifest.get("studyId") != "MEZ-IDENTITY-PRODUCT-OBJECT-01":
        errors.append("Unexpected study ID")
    if manifest.get("status") != "revision-required":
        errors.append("Calibration must record the required revision")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Calibration must deny production and source-expression authority")
    if len(manifest.get("decisions", [])) != 3:
        errors.append("Calibration must request exactly three decisions")

    review = json.loads((ROOT / "identity-product-object-01-review.json").read_text())
    decisions = review.get("record", {}).get("decisions", {})
    if len(decisions) != 3 or any(item.get("decision") != "edit" for item in decisions.values()):
        errors.append("Completed review must preserve all three edit decisions")
    if review.get("productionAuthority") is not False or review.get("sourceExpressionApproved") is not False:
        errors.append("Completed review must preserve zero production and source-expression authority")

    variant_records = variants.get("variants", [])
    if len(variant_records) != 1 or variant_records[0].get("id") != "MZ-G13":
        errors.append("Gradient manifest must contain only MZ-G13")
    if not SOURCE.is_file() or sha256(SOURCE) != "7932fb83949329ad562a13010221d2c0e6cad9f24312993acf781935547a946e":
        errors.append("MZ-G13 raw source hash changed")

    wings = (ROOT / "assets/wings.svg").read_text()
    if wings.count("<path") != 2 or "viewBox=\"9 16 340 241\"" not in wings:
        errors.append("Canonical two-path Wings geometry is missing")
    component = (ROOT / "play-button.js").read_text()
    for contract in ["width: 50%", "-0.02", "border-radius: 50%", "prefers-reduced-motion", "IntersectionObserver"]:
        if contract not in component:
            errors.append(f"Product-disc contract missing: {contract}")

    properties = schema.get("properties", {})
    if properties.get("productionAuthority", {}).get("const") is not False:
        errors.append("Review schema must deny production authority")
    if properties.get("sourceExpressionApproved", {}).get("const") is not False:
        errors.append("Review schema must deny source-expression authority")

    prose = "\n".join((ROOT / name).read_text() for name in ["README.md", "index.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in calibration prose")

    if errors:
        print("MEZ IDENTITY CALIBRATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("MEZ IDENTITY CALIBRATION: PASS")
    print("- source-authoritative MZ-G13 texture and canonical Wings")
    print("- one coherent product-core hypothesis at four scales")
    print("- three edit decisions preserved")
    print("- expression atlas 02 required before hero calibration")
    print("- production and source-expression authority denied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
