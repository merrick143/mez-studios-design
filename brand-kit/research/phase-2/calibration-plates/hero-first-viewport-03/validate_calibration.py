#!/usr/bin/env python3
"""Validate hero and first viewport calibration 03."""

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
        ROOT / "hero-first-viewport-03-review.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-HERO-FIRST-VIEWPORT-03":
        errors.append("Manifest must identify hero calibration 03")
    if manifest.get("status") != "human-review-complete-direction-approved-mobile-revision-required" or manifest.get("decisionCount") != 6:
        errors.append("Hero calibration 03 must preserve its completed six-decision human review")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Hero calibration 03 must preserve zero authority")
    if manifest.get("calibrationException", {}).get("productionDefaultUnchanged") != "one-living-core-per-viewport":
        errors.append("The multi-core calibration must preserve the production motion default")

    feedback = json.loads((ROOT / "hero-first-viewport-03-review.json").read_text())
    feedback_decisions = feedback.get("decisions", {})
    approved = [key for key, value in feedback_decisions.items() if value.get("decision") == "approve"]
    edited = [key for key, value in feedback_decisions.items() if value.get("decision") == "edit"]
    if approved != ["overallDirection", "messageHierarchy", "cardStackComposition", "animationUse", "productFamilyRead"]:
        errors.append("Hero calibration 03 must preserve all five approved direction decisions")
    if edited != ["mobileOpening"]:
        errors.append("Hero calibration 03 must preserve mobile opening as the only edit")
    if feedback.get("productionAuthority") is not False or feedback.get("sourceExpressionApproved") is not False:
        errors.append("Hero review must preserve zero authority")

    family = manifest.get("productFamily", [])
    if len(family) != 5 or sum(item.get("expression", "").startswith("living-card") for item in family) != 4:
        errors.append("Hero calibration 03 must expose four living cards and one neutral card")
    context = next((item for item in family if item.get("name") == "Context Engine"), {})
    if context.get("core") is not None or context.get("expression") != "neutral-static-card":
        errors.append("Context Engine must remain visibly unassigned")

    hero = (ROOT / "hero.html").read_text()
    for text in ["The systems AI-native businesses run on.", "AI OS", "Context Engine", "AI Ads System", "Claude Code OS", "Organic Content OS"]:
        if text not in hero:
            errors.append(f"Missing approved hero content: {text}")
    if hero.count('class="product-card ') != 5:
        errors.append("Hero must show exactly five equal product cards")
    for core_id in ["MZ-G13", "MZ-G20", "MZ-G15", "MZ-G06"]:
        if f'data-mz-core="{core_id}"' not in hero:
            errors.append(f"Missing Living Core surface: {core_id}")
    if hero.count("design-system-export/assets/wings.svg") < 6:
        errors.append("Hero must use canonical Wings in the lockup and all five cards")

    styles = (ROOT / "hero.css").read_text()
    for contract in ['font-family: "Geist Display"', 'font-family: "Mez Inter"', "aspect-ratio: 3 / 4", "border-radius: 14px", "--mz-r-control: 12px", "min-height: 48px", "@media (max-width: 599px)", "@media (prefers-reduced-motion: reduce)"]:
        if contract not in styles:
            errors.append(f"Missing hero system contract: {contract}")
    for rejected in ["text-transform: uppercase", "filter: blur(", "grid-template-columns: repeat(5"]:
        if rejected in styles:
            errors.append(f"Hero carries a rejected visual habit: {rejected}")

    script = (ROOT / "hero.js").read_text()
    if "mountLivingCores(document)" not in script:
        errors.append("Hero must use the shared Living Core renderer")

    review = (ROOT / "review.js").read_text()
    if "MEZ-HERO-FIRST-VIEWPORT-03" not in review or "productionAuthority: false" not in review:
        errors.append("Review export must preserve study identity and zero authority")

    prose = "\n".join(path.read_text() for path in [ROOT / "README.md", ROOT / "index.html", ROOT / "hero.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in customer-visible or active calibration prose")

    if errors:
        print("HERO AND FIRST VIEWPORT CALIBRATION 03: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("HERO AND FIRST VIEWPORT CALIBRATION 03: PASS")
    print("- centred proposition and equal-size five-card fan")
    print("- four exact Living Core textures and one neutral unassigned card")
    print("- canonical Wings and approved card anatomy")
    print("- authored desktop and mobile compositions")
    print("- six-decision human gate complete: five approved, mobile revision required")
    print("- calibration-only multi-core exception with zero production authority")
    return 0


if __name__ == "__main__":
    sys.exit(main())
