#!/usr/bin/env python3
"""Validate button and control system calibration 01."""

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
        ROOT / "controls.css",
        ROOT / "controls.js",
        ROOT / "review.js",
        ROOT / "calibration-manifest.json",
        ROOT / "calibration-review.schema.json",
        ROOT / "button-control-system-01-review.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-BUTTON-CONTROL-SYSTEM-01":
        errors.append("Manifest must identify the control-system study")
    if manifest.get("status") != "human-review-complete-approved-direction" or manifest.get("decisionCount") != 7:
        errors.append("Control calibration must preserve the completed seven-decision review")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Control calibration must preserve zero authority")
    if manifest.get("approvedInputs", {}).get("typographyDecision") != "DEC-TYPE-001":
        errors.append("Control calibration must consume the approved typography decision")
    if len(manifest.get("contextsTested", [])) != 7 or len(manifest.get("statesTested", [])) != 7:
        errors.append("Control calibration must test seven contexts and seven states")
    if manifest.get("approvedDecision") != "DEC-CONTROL-001":
        errors.append("Control calibration must link the approved control direction")
    progress = manifest.get("reviewProgress", {})
    if progress.get("completedDecisionCount") != 7 or progress.get("remaining") != []:
        errors.append("Control calibration must record all seven completed decisions")

    review = json.loads((ROOT / "button-control-system-01-review.json").read_text())
    expected = {
        "shape": "moderate-12",
        "hierarchy": "solid-outline-text",
        "depth": "micro-lift",
        "scale": "48-default",
        "iconPolicy": "selective-directional",
        "darkSurface": "white-primary-outline-secondary",
        "mobileBehaviour": "primary-full-secondary-link",
    }
    actual = {key: value.get("decision") for key, value in review.get("decisions", {}).items()}
    if review.get("complete") is not True or actual != expected:
        errors.append("Control review must preserve the seven approved recommended behaviours")
    if review.get("productionAuthority") is not False or review.get("sourceExpressionApproved") is not False:
        errors.append("Control review must preserve zero authority")

    html = (ROOT / "index.html").read_text()
    for required_text in [
        "The click should feel inevitable.",
        "Rounded, not inflated.",
        "One action leads.",
        "Pressure, not theatre.",
        "A button is not finished until every state is.",
        "One thumb. One obvious next step.",
        "Pay $99 and get AI OS",
    ]:
        if required_text not in html:
            errors.append(f"Missing required specimen: {required_text}")

    styles = (ROOT / "controls.css").read_text()
    for contract in [
        "--control-radius: 12px",
        "--control-height: 48px",
        "translateY(-1px)",
        "@media (prefers-reduced-motion: reduce)",
        ":focus-visible",
    ]:
        if contract not in styles:
            errors.append(f"Missing candidate contract: {contract}")

    script = (ROOT / "review.js").read_text()
    if "MEZ-BUTTON-CONTROL-SYSTEM-01" not in script or "productionAuthority: false" not in script:
        errors.append("Review export must preserve study identity and zero authority")

    prose = "\n".join(path.read_text() for path in [ROOT / "README.md", ROOT / "index.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in control calibration prose")

    if errors:
        print("BUTTON AND CONTROL SYSTEM CALIBRATION 01: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("BUTTON AND CONTROL SYSTEM CALIBRATION 01: PASS")
    print("- seven bounded design decisions")
    print("- seven real contexts and seven interaction states")
    print("- approved Geist and Inter role split")
    print("- responsive and reduced-motion contracts")
    print("- DEC-CONTROL-001 records the approved direction with zero direct production authority")
    return 0


if __name__ == "__main__":
    sys.exit(main())
