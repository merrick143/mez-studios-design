#!/usr/bin/env python3
"""Verify GOLD-01 Round 25: move and simplify the dark AI OS route."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "golden" / "homepage"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
JS = WORKBENCH / "homepage.js"
SOURCE = ROOT / "homepage.source.json"
REVIEW = ROOT / "review.json"
FEEDBACK = ROOT / "round-25-feedback.json"

EXPECTED_IDS = ["GH-S01", "GH-S08", "GH-S02", "GH-S03", "GH-S04", "GH-S05", "GH-S06", "GH-S07", "GH-S09"]
REMOVED_COPY = (
    "The models will keep improving.",
    "Installed first",
    "Four focused systems extend the same operating layer",
)
REMOVED_BENTO = (
    "aios-shell",
    "aios-card",
    "aios-split",
    "aios-panel",
    "aios-orbit",
    "aios-featuregrid",
    "aios-feat",
    "aios-route",
)


def validate(html: str, css: str, javascript: str, source: dict, review: dict, feedback: dict) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    for label, value in (("source", source.get("candidateRevision")), ("review", review.get("candidateRevision")), ("feedback", feedback.get("candidateRevision"))):
        if value != "golden-homepage-01-r25":
            fail("META", f"{label} does not identify golden-homepage-01-r25")
    if source.get("version") != "0.25.0-candidate" or "Round 25" not in html or "golden-homepage-01-r25" not in javascript:
        fail("META", "workbench or source still identifies an older round")
    if feedback.get("productionAuthority") is not False:
        fail("META", "the human direction record must remain non-production")

    ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if ids != EXPECTED_IDS:
        fail("STRUCTURE", f"expected the nine-region moved-route order; found {ids}")
    source_ids = [section.get("id") for section in source.get("sections", [])]
    if source_ids != EXPECTED_IDS:
        fail("STRUCTURE", f"source section order does not match the rendered page: {source_ids}")
    if 'data-review-id="GH-S09" data-review-title="Footer"' not in html or "GH-S10" in html:
        fail("STRUCTURE", "footer must become GH-S09 after the duplicate closing route is removed")

    s06_review = html.find('data-review-id="GH-S06"')
    s06_start = html.rfind("<section", 0, s06_review) if s06_review >= 0 else -1
    s07_start = html.find('data-review-id="GH-S07"')
    s06 = html[s06_start:s07_start] if 0 <= s06_start < s07_start else ""
    if not s06:
        fail("BOUNDARY", "GH-S06 is missing or not directly before GH-S07")
    for required in (
        'class="final-route ai-os review-target"',
        'id="ai-os"',
        'data-mz-mode="dark"',
        "Start here",
        "Start with the AI OS.",
        'class="final-card hero-card__material"',
        'data-live-anchor="ai-os"',
        'data-gradient-id="MZ-G13"',
        'data-consumer-route="ai-os"',
    ):
        if required not in s06:
            fail("COMPOSITION", f"simplified dark AI OS route missing: {required}")
    if html.count('class="final-route ai-os review-target"') != 1 or html.count('class="final-card hero-card__material"') != 1:
        fail("COMPOSITION", "the moved dark route and AI OS material must each appear exactly once")

    for removed in REMOVED_COPY:
        if removed in html:
            fail("SIMPLICITY", f"removed copy has returned: {removed}")
    for removed in REMOVED_BENTO:
        if removed in s06:
            fail("SIMPLICITY", f"old bento markup remains in GH-S06: {removed}")
    if "data-final-products" in html or "data-final-products" in javascript or "final-extension" in javascript:
        fail("SIMPLICITY", "the removed four-system extension rail is still authored")
    if 'id="start"' in html or 'document.querySelector("#start")' in javascript:
        fail("STRUCTURE", "the former duplicate closing-route anchor still exists")

    motion = source.get("motion", {})
    if motion.get("eligibleSections") != ["GH-S01", "GH-S06"]:
        fail("MOTION", "motion allocation must remove the deleted GH-S09 route")
    if javascript.count('dataset.liveAnchor === "ai-os"') != 1:
        fail("MOTION", "the moved AI OS card must be the single GH-S06 live anchor")

    route_rule = re.search(r"\.final-route\s*\{([^}]*)\}", css, re.S)
    if not route_rule or "background: var(--page-dark)" not in route_rule.group(1):
        fail("CONTRAST", "the selected dark section background is missing")
    if 'width: min(340px, 100%)' not in css:
        fail("SIMPLICITY", "the moved AI OS portrait card is not compacted to the selected size")
    for banned in ("box-shadow", "perspective", "backdrop-filter"):
        section_css_start = css.find("GH-S06 · Simplified dark AI OS")
        section_css = css[section_css_start:] if section_css_start >= 0 else ""
        if banned in section_css:
            fail("CANON", f"simplified section introduces banned treatment: {banned}")

    return failures


def load() -> tuple[str, str, str, dict, dict, dict]:
    return (
        HTML.read_text(encoding="utf-8"),
        CSS.read_text(encoding="utf-8"),
        JS.read_text(encoding="utf-8"),
        json.loads(SOURCE.read_text(encoding="utf-8")),
        json.loads(REVIEW.read_text(encoding="utf-8")),
        json.loads(FEEDBACK.read_text(encoding="utf-8")),
    )


def self_test(data: tuple[str, str, str, dict, dict, dict]) -> int:
    html, css, javascript, source, review, feedback = data
    bad_motion = copy.deepcopy(source)
    bad_motion["motion"]["eligibleSections"].append("GH-S09")
    cases = (
        ("META", html.replace("Round 25", "Round 24"), css, javascript, source),
        ("SIMPLICITY", html.replace("Start with the AI OS.", "Start with the AI OS.</h2><p>Installed first</p>", 1), css, javascript, source),
        ("STRUCTURE", html.replace('data-review-id="GH-S09"', 'data-review-id="GH-S10"', 1), css, javascript, source),
        ("MOTION", html, css, javascript, bad_motion),
        ("CONTRAST", html, css.replace(".final-route {\n  background: var(--page-dark);", ".final-route {\n  background: var(--page-paper);", 1), javascript, source),
    )
    misses: list[str] = []
    for expected, mutated_html, mutated_css, mutated_js, mutated_source in cases:
        failures = validate(mutated_html, mutated_css, mutated_js, mutated_source, review, feedback)
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 25 SELF-TEST: FAIL")
        print("- missed mutations: " + ", ".join(misses))
        return 1
    print("GOLDEN HOMEPAGE ROUND 25 SELF-TEST: PASS")
    print("- structure, simplification, contrast and motion regressions all fail in memory")
    return 0


def main() -> int:
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 25: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1
    print("GOLDEN HOMEPAGE ROUND 25: PASS")
    print("- the dark Start here route replaces the old AI OS bento in GH-S06")
    print("- the former footer-adjacent duplicate and its extension rail are removed")
    print("- the selected copy deletions and compact AI OS card are enforced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
