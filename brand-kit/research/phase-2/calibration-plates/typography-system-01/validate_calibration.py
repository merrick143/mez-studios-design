#!/usr/bin/env python3
"""Validate typography system calibration 01."""

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
        ROOT / "typography.css",
        ROOT / "review.js",
        ROOT / "calibration-manifest.json",
        ROOT / "calibration-review.schema.json",
        ROOT / "typography-system-01-review.json",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty output: {path}")

    manifest = json.loads((ROOT / "calibration-manifest.json").read_text())
    if manifest.get("studyId") != "MEZ-TYPOGRAPHY-SYSTEM-01":
        errors.append("Manifest must identify the typography study")
    if manifest.get("status") != "human-review-complete-approved-direction" or manifest.get("decisionCount") != 6:
        errors.append("Typography calibration must expose six decisions")
    if manifest.get("productionAuthority") is not False or manifest.get("sourceExpressionApproved") is not False:
        errors.append("Typography calibration must preserve zero authority")
    if len(manifest.get("candidates", [])) != 3:
        errors.append("Typography calibration must compare three candidates")
    if len(manifest.get("rolesTested", [])) < 8:
        errors.append("Typography calibration must test the full role system")
    progress = manifest.get("reviewProgress", {})
    if progress:
        decisions = progress.get("decisions", {})
        if decisions.get("displayFamily", {}).get("decision") != "geist":
            errors.append("Recorded display direction must be Geist")
        if decisions.get("bodyFamily", {}).get("decision") != "inter-tuned":
            errors.append("Recorded body direction must be tuned Inter")
        if progress.get("completedDecisionCount") != 6 or progress.get("remaining") != []:
            errors.append("Typography review progress must record six completed decisions")

    review = json.loads((ROOT / "typography-system-01-review.json").read_text())
    expected = {
        "primaryFamily": "inter-tuned",
        "displayFamily": "geist",
        "bodyFamily": "inter-tuned",
        "serifPolicy": "contextual-only",
        "monoPolicy": "keep-ibm-plex",
        "mobileType": "edit",
    }
    actual = {
        key: value.get("decision")
        for key, value in review.get("decisions", {}).items()
    }
    if actual != expected or review.get("complete") is not True:
        errors.append("Completed typography review must preserve all six approved decisions")
    if review.get("productionAuthority") is not False or review.get("sourceExpressionApproved") is not False:
        errors.append("Completed typography review must preserve zero authority")

    html = (ROOT / "index.html").read_text()
    for required_text in [
        "Tuned Inter",
        "Instrument Sans",
        "Geist",
        "390-pixel stress test",
        "Serif policy",
        "Mono and data policy",
        "The systems AI-native businesses run on.",
    ]:
        if required_text not in html:
            errors.append(f"Missing required specimen: {required_text}")

    script = (ROOT / "review.js").read_text()
    if "MEZ-TYPOGRAPHY-SYSTEM-01" not in script or "productionAuthority: false" not in script:
        errors.append("Review export must preserve study identity and zero authority")

    prose = "\n".join(path.read_text() for path in [ROOT / "README.md", ROOT / "index.html"])
    if "—" in prose:
        errors.append("Prohibited em dash in typography calibration prose")

    if errors:
        print("TYPOGRAPHY SYSTEM CALIBRATION 01: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("TYPOGRAPHY SYSTEM CALIBRATION 01: PASS")
    print("- three complete family territories")
    print("- eight real typography roles")
    print("- desktop and 390-pixel mobile specimens")
    print("- serif and mono policies separated")
    print("- six approved role and policy decisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
