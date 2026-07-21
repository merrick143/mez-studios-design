#!/usr/bin/env python3
"""Validate the hero and first viewport calibration artefact."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    """Validate required files, authority boundaries and source references."""
    required = [
        "README.md",
        "calibration-manifest.json",
        "calibration-review.schema.json",
        "hero.html",
        "hero.js",
        "index.html",
        "plate.css",
        "review.js",
        "hero-first-viewport-01-review.json",
    ]
    missing = [name for name in required if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"FAIL missing calibration files: {', '.join(missing)}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-HERO-FIRST-VIEWPORT-01":
        raise SystemExit("FAIL incorrect studyId")
    if manifest.get("productionAuthority") is not False:
        raise SystemExit("FAIL calibration must not claim production authority")
    if manifest.get("sourceExpressionApproved") is not False:
        raise SystemExit("FAIL calibration must not claim source expression approval")
    if manifest.get("decisionCount") != 5:
        raise SystemExit("FAIL expected five bounded decisions")
    if manifest.get("status") != "composition-rejected-foundation-slices-deferred":
        raise SystemExit("FAIL hero disposition must preserve the rejected composition")

    review_record = json.loads((ROOT / "hero-first-viewport-01-review.json").read_text())
    expected_decisions = {
        "overallDirection": "edit",
        "heroComposition": "reject",
        "typography": "advance",
        "controls": "edit",
        "mobileOpening": "edit",
    }
    actual_decisions = {
        key: value.get("decision")
        for key, value in review_record.get("decisions", {}).items()
    }
    if actual_decisions != expected_decisions:
        raise SystemExit("FAIL hero review decisions do not match the recorded export")
    if review_record.get("productionAuthority") is not False:
        raise SystemExit("FAIL hero review must preserve zero production authority")

    hero = (ROOT / "hero.html").read_text()
    review = (ROOT / "index.html").read_text()
    styles = (ROOT / "plate.css").read_text()
    required_copy = [
        "The systems AI-native businesses run on.",
        "Explore the AI OS",
        "See what we're building",
        "The intelligence is rented.",
        "The operating layer is yours.",
    ]
    absent_copy = [value for value in required_copy if value not in hero]
    if absent_copy:
        raise SystemExit(f"FAIL approved copy missing: {', '.join(absent_copy)}")

    for required_reference in ["DEC-MOTION-002", "VT-01", "VT-05", "VT-06"]:
        if required_reference not in json.dumps(manifest):
            raise SystemExit(f"FAIL missing source reference {required_reference}")

    if "data-mz-core=\"MZ-G13\"" not in hero:
        raise SystemExit("FAIL hero does not use the approved AI OS Living Core")
    if "design-system-export/assets/wings.svg" not in hero:
        raise SystemExit("FAIL hero does not use the canonical Wings asset")
    if "gradient" in hero.lower().replace("living-core", ""):
        raise SystemExit("FAIL hero introduces unreviewed gradient copy or structure")
    if "iframe src=\"hero.html\"" not in review:
        raise SystemExit("FAIL review page does not render the clean hero expression")
    if "border-radius: var(--candidate-radius-control)" not in styles:
        raise SystemExit("FAIL candidate control radius is not applied through one variable")

    print("PASS hero and first viewport calibration structure and authority checks")


if __name__ == "__main__":
    main()
