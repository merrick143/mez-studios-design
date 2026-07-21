#!/usr/bin/env python3
"""Validate hero and first viewport calibration 02."""

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
        ROOT / "studio.css",
        ROOT / "hero.html",
        ROOT / "hero.css",
        ROOT / "hero.js",
        ROOT / "review.js",
        ROOT / "calibration-manifest.json",
        ROOT / "calibration-review.schema.json",
        ROOT / "hero-first-viewport-02-direct-feedback.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-HERO-FIRST-VIEWPORT-02":
        errors.append("Manifest must identify hero calibration 02")
    if manifest.get("status") != "direct-feedback-revision-requested" or manifest.get("decisionCount") != 5:
        errors.append("Hero calibration 02 must preserve five decisions and its direct revision request")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Hero calibration 02 must preserve zero authority")
    expected_inputs = ["DEC-MOTION-002", "DEC-TYPE-001", "DEC-CONTROL-001", "DEC-FAMILY-001"]
    inputs = manifest.get("approvedInputs", {})
    actual_inputs = [inputs.get("motionDecision"), inputs.get("typographyDecision"), inputs.get("controlDecision"), inputs.get("familyDecision")]
    if actual_inputs != expected_inputs:
        errors.append("Hero calibration 02 must inherit the four approved foundation decisions")
    if manifest.get("previousVisualExecutionInherited") is not False:
        errors.append("Hero calibration 02 must not inherit the family plate visual execution")

    family = manifest.get("productFamily", [])
    if len(family) != 5 or family[0].get("core") != "MZ-G13":
        errors.append("Hero calibration 02 must preserve the five-product roster and locked AI OS core")
    context = next((item for item in family if item.get("name") == "Context Engine"), {})
    if context.get("core") is not None or context.get("coreState") != "unassigned":
        errors.append("Context Engine must remain visibly unassigned")

    hero = (ROOT / "hero.html").read_text()
    for text in [
        "The systems AI-native businesses run on.",
        "Explore the AI OS",
        "See what we're building",
        "The intelligence is rented.",
        "The operating layer is yours.",
        "AI OS",
        "Context Engine",
        "AI Ads System",
        "Claude Code OS",
        "Organic Content OS",
    ]:
        if text not in hero:
            errors.append(f"Missing approved hero content: {text}")
    if hero.count("product-core") != 5:
        errors.append("Hero must show exactly five product cores")
    if hero.count("design-system-export/assets/wings.svg") < 6:
        errors.append("Hero must use the canonical Wings in the lockup and all five cores")

    styles = (ROOT / "hero.css").read_text()
    for contract in [
        'font-family: "Geist Display"',
        'font-family: "Mez Inter"',
        "grid-template-columns: repeat(5",
        "--mz-r-control: 12px",
        "min-height: 48px",
        "width: 50%",
        "@media (max-width: 599px)",
        "@media (prefers-reduced-motion: reduce)",
        "mz-g13.webp",
        "mz-g20.webp",
        "mz-g15.webp",
        "mz-g06.webp",
    ]:
        if contract not in styles:
            errors.append(f"Missing hero system contract: {contract}")
    for rejected in ["linear-gradient(", "radial-gradient(", "filter: blur(", "text-transform: uppercase"]:
        if rejected in styles:
            errors.append(f"Hero carries a rejected visual habit: {rejected}")

    review = (ROOT / "review.js").read_text()
    if "MEZ-HERO-FIRST-VIEWPORT-02" not in review or "productionAuthority: false" not in review:
        errors.append("Review export must preserve study identity and zero authority")

    prose = "\n".join(path.read_text() for path in [ROOT / "README.md", ROOT / "index.html", ROOT / "hero.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in customer-visible or active calibration prose")

    if errors:
        print("HERO AND FIRST VIEWPORT CALIBRATION 02: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("HERO AND FIRST VIEWPORT CALIBRATION 02: PASS")
    print("- centred proposition and aligned five-product opening")
    print("- approved Geist, tuned Inter and 12px control system")
    print("- exact gradient textures and canonical Wings")
    print("- static repeated cores with Context Engine unassigned")
    print("- authored desktop and mobile compositions")
    print("- direct feedback preserved and revision requested")
    print("- zero production authority")
    return 0


if __name__ == "__main__":
    sys.exit(main())
