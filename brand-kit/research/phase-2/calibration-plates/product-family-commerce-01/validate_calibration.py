#!/usr/bin/env python3
"""Validate product family and commerce calibration 01."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    errors: list[str] = []
    required = [
        ROOT / "README.md",
        ROOT / "index.html",
        ROOT / "family.css",
        ROOT / "family.js",
        ROOT / "review.js",
        ROOT / "calibration-manifest.json",
        ROOT / "calibration-review.schema.json",
        ROOT / "product-family-commerce-01-review.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-PRODUCT-FAMILY-COMMERCE-01":
        errors.append("Manifest must identify the product-family and commerce study")
    if manifest.get("status") != "human-review-complete-behaviour-approved-visual-execution-not-approved" or manifest.get("decisionCount") != 7:
        errors.append("Calibration must record seven completed behaviour decisions without visual approval")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Calibration must preserve zero authority")
    inputs = manifest.get("approvedInputs", {})
    if [inputs.get("motionDecision"), inputs.get("typographyDecision"), inputs.get("controlDecision")] != ["DEC-MOTION-002", "DEC-TYPE-001", "DEC-CONTROL-001"]:
        errors.append("Calibration must inherit the three approved foundation decisions")
    roster = manifest.get("researchRoster", [])
    if len(roster) != 5 or roster[0].get("core") != "MZ-G13" or roster[0].get("coreState") != "locked":
        errors.append("Research roster must contain five products and preserve the locked AI OS core")
    if not any(item.get("coreState") == "unassigned" for item in roster):
        errors.append("Calibration must disclose at least one unresolved future core")
    if len(manifest.get("contextsTested", [])) != 7:
        errors.append("Calibration must test seven product and commerce contexts")
    if manifest.get("approvedDecision") != "DEC-FAMILY-001" or manifest.get("visualExecutionApproved") is not False:
        errors.append("Calibration must link DEC-FAMILY-001 and explicitly withhold visual-execution approval")
    progress = manifest.get("reviewProgress", {})
    if progress.get("completedDecisionCount") != 7 or progress.get("remaining") != []:
        errors.append("Calibration must record all seven completed human decisions")

    review = json.loads((ROOT / "product-family-commerce-01-review.json").read_text())
    expected = {
        "publicRoster": "homepage-five",
        "familyChassis": "aligned-catalogue",
        "territoryMethod": "gradient-and-copy",
        "expressionMode": "static-core-only",
        "availabilityHierarchy": "equal-family",
        "commerceSequence": "live-first-bundle-later",
        "mobileBehaviour": "vertical-catalogue-sticky-summary",
    }
    actual = {key: value.get("decision") for key, value in review.get("decisions", {}).items()}
    if review.get("complete") is not True or actual != expected:
        errors.append("Review must preserve all seven approved family and commerce behaviours")
    if review.get("productionAuthority") is not False or review.get("sourceExpressionApproved") is not False:
        errors.append("Review must preserve zero production and source-expression authority")

    html = (ROOT / "index.html").read_text()
    for text in [
        "A family,",
        "One baseline.",
        "Same spine.",
        "Sell what exists.",
        "A bundle is a decision,",
        "One product.",
        "Vertical, legible,",
        "Pay $99 and get AI OS",
    ]:
        if text not in html:
            errors.append(f"Missing required context: {text}")
    for product in ["AI OS", "Context Engine", "AI Ads System", "Claude Code OS", "Organic Content OS"]:
        if product not in html:
            errors.append(f"Missing research product: {product}")
    if html.count("product-cell") < 6:
        errors.append("Aligned family catalogue must contain five product cells")

    styles = (ROOT / "family.css").read_text()
    for contract in ["grid-template-columns:repeat(5", "min-height:48px", "border-radius:12px", "@media(max-width:680px)", "@media(prefers-reduced-motion:reduce)"]:
        if contract not in styles:
            errors.append(f"Missing family contract: {contract}")

    script = (ROOT / "review.js").read_text()
    if "MEZ-PRODUCT-FAMILY-COMMERCE-01" not in script or "productionAuthority: false" not in script:
        errors.append("Review export must preserve study identity and zero authority")

    prose = "\n".join(path.read_text() for path in [ROOT / "README.md", ROOT / "index.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in calibration prose")

    if errors:
        print("PRODUCT FAMILY AND COMMERCE CALIBRATION 01: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PRODUCT FAMILY AND COMMERCE CALIBRATION 01: PASS")
    print("- five-product research roster with explicit core conflict")
    print("- seven contextual product and commerce behaviours approved")
    print("- visual execution explicitly not approved")
    print("- approved type, motion and control inputs preserved")
    print("- current purchase and future bundle scenario remain distinct")
    print("- zero production authority")
    return 0


if __name__ == "__main__":
    sys.exit(main())
