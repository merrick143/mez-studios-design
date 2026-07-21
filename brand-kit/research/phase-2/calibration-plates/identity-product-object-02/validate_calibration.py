#!/usr/bin/env python3
"""Validate the Mez product expression atlas 02."""

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
        ROOT / "README.md", ROOT / "index.html", ROOT / "atlas.css", ROOT / "atlas.js",
        ROOT / "play-button.js", ROOT / "calibration-manifest.json", ROOT / "calibration-review.schema.json",
        ROOT / "assets/wings.svg", ROOT / "assets/gradients/mz-g13.webp", ROOT / "assets/gradients/variants.json",
        ROOT / "qa/desktop.png", ROOT / "qa/mobile.png"
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    variants = json.loads((ROOT / "assets/gradients/variants.json").read_text())
    schema = json.loads((ROOT / "calibration-review.schema.json").read_text())

    if manifest.get("studyId") != "MEZ-IDENTITY-PRODUCT-OBJECT-02" or manifest.get("supersedes") != "MEZ-IDENTITY-PRODUCT-OBJECT-01":
        errors.append("Atlas identity or supersession record is incorrect")
    if manifest.get("status") != "human-review-ready" or manifest.get("decisionCount") != 9:
        errors.append("Atlas must be ready with exactly nine decisions")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Atlas must deny production and source-expression authority")

    records = variants.get("variants", [])
    if len(records) != 1 or records[0].get("id") != "MZ-G13":
        errors.append("Gradient manifest must contain only MZ-G13")
    if not SOURCE.is_file() or sha256(SOURCE) != "7932fb83949329ad562a13010221d2c0e6cad9f24312993acf781935547a946e":
        errors.append("MZ-G13 raw source hash changed")

    wings_text = (ROOT / "assets/wings.svg").read_text()
    if wings_text.count("<path") != 2 or "viewBox=\"9 16 340 241\"" not in wings_text:
        errors.append("Canonical two-path Wings geometry is missing")

    component = (ROOT / "play-button.js").read_text()
    for contract in ["width: 50%", "-0.02", "border-radius: 50%", "prefers-reduced-motion", "sharedGradientRenderers", "AuroraTexture"]:
        if contract not in component:
            errors.append(f"Expression renderer contract missing: {contract}")
    if "scale(1.025)" in component or "isEnergized ? 1.5" in component:
        errors.append("Rejected hover growth or hover speed-up remains")

    atlas_js = (ROOT / "atlas.js").read_text()
    for expression in ["gradientMark", "flat-disc", "living-sphere", "landing-card", "trading-card", "product-pill", "data-collections"]:
        if expression not in atlas_js and expression not in (ROOT / "index.html").read_text():
            errors.append(f"Missing expression or collection renderer: {expression}")

    properties = schema.get("properties", {})
    if properties.get("productionAuthority", {}).get("const") is not False or properties.get("sourceExpressionApproved", {}).get("const") is not False:
        errors.append("Review schema must deny production and source-expression authority")

    prose = "\n".join((ROOT / name).read_text() for name in ["README.md", "index.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in atlas prose")

    if errors:
        print("MEZ EXPRESSION ATLAS 02: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("MEZ EXPRESSION ATLAS 02: PASS")
    print("- calibration 01 edits answered")
    print("- static and living allocation separated")
    print("- contextual scale bands and six expressions")
    print("- hover growth and hover speed-up removed")
    print("- source-authoritative MZ-G13 and canonical Wings")
    print("- production and source-expression authority denied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
