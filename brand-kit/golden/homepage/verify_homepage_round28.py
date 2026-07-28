#!/usr/bin/env python3
"""Verify GOLD-01 Round 28 mobile hero, principle and process refinements."""

from __future__ import annotations

import copy
import json
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
FEEDBACK = ROOT / "round-28-feedback.json"


def validate(html: str, css: str, javascript: str, source: dict, review: dict, feedback: dict) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    for label, value in (
        ("source", source.get("candidateRevision")),
        ("review", review.get("candidateRevision")),
        ("feedback", feedback.get("candidateRevision")),
    ):
        if value != "golden-homepage-01-r28":
            fail("META", f"{label} does not identify golden-homepage-01-r28")
    if source.get("version") not in {"0.28.0-candidate", "1.0.0"} or "Round 28" not in html or "Round 28" not in css:
        fail("META", "workbench or source still identifies an older round")
    if "Review Round 28" not in html or "Round 28 review" not in html or "homepage.js?v=0.28.1" not in html:
        fail("META", "visible review controls or script cache key still identify an older round")
    if 'candidateRevision: "golden-homepage-01-r28"' not in javascript:
        fail("META", "review payload does not identify Round 28")

    hero = html[html.find('data-review-id="GH-S01"'):html.find('data-review-id="GH-S08"')]
    if hero.count("<h1>") != 1 or hero.count('class="hero-lead"') != 1:
        fail("HERO", "hero must expose exactly one H1 and one subtitle")
    if "hero-proof" in hero or "Every Mez System is built inside Mez Studios first" in hero:
        fail("HERO", "the duplicate second subtitle returned")
    for token in (
        ".hero-copy h1",
        "max-width: 17ch",
        "display: flex",
        "width: clamp(98px, 30vw, 118px)",
        "margin-inline: clamp(-33px, -8vw, -25px)",
    ):
        if token not in css:
            fail("HERO", f"compact flare contract missing: {token}")

    for token in (
        "width: min(300px, 100%)",
        ".conc__core { width: 26%; }",
        "width: 28px",
        "height: auto",
        ".conc__product {\n    display: none",
    ):
        if token not in css:
            fail("PRINCIPLE", f"compact principle sizing missing: {token}")

    for token in (
        "--mseq-mobile-gap",
        "grid-template-columns: var(--mseq-disc) minmax(0, 1fr)",
        "grid-row: 1 / 3",
        "left: calc(var(--mseq-disc) / 2 - var(--mseq-rule) / 2)",
        "width: var(--mseq-rule)",
    ):
        if token not in css:
            fail("PROCESS", f"vertical process guide missing: {token}")

    responsive = source.get("responsive", {})
    expected = {
        "heroCopyStructure": "one-h1-one-subtitle",
        "mobileHeroArrangement": "centred-five-card-flare",
        "principleOrbitCompactMaximum": 300,
        "mobileProcessGuide": "left-aligned-vertical",
    }
    for key, value in expected.items():
        if responsive.get(key) != value:
            fail("SOURCE", f"responsive.{key} is not {value!r}")

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
    old_source = copy.deepcopy(source)
    old_source["candidateRevision"] = "golden-homepage-01-r27"
    cases = (
        ("META", html, css, javascript, old_source, review, feedback),
        ("HERO", html.replace('</h1>', '</h1><p class="hero-proof">Duplicate</p>', 1), css, javascript, source, review, feedback),
        ("PRINCIPLE", html, css.replace("width: min(300px, 100%)", "width: 100%", 1), javascript, source, review, feedback),
        ("PROCESS", html, css.replace("--mseq-mobile-gap", "--removed-mobile-gap"), javascript, source, review, feedback),
        ("SOURCE", html, css, javascript, {**source, "responsive": {**source["responsive"], "mobileProcessGuide": "none"}}, review, feedback),
    )
    misses: list[str] = []
    for expected, *case in cases:
        failures = validate(*case)
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 28 SELF-TEST: FAIL")
        print("- missed mutations: " + ", ".join(misses))
        return 1
    print("GOLDEN HOMEPAGE ROUND 28 SELF-TEST: PASS")
    print("- metadata, hero hierarchy, compact orbit, vertical process and source regressions fail in memory")
    return 0


def main() -> int:
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 28: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1
    print("GOLDEN HOMEPAGE ROUND 28: PASS")
    print("- hero has one H1, one subtitle and a compact five-card mobile flare")
    print("- the compact principle core uses an undistorted, mark-only Wings treatment on mobile")
    print("- the mobile Build-to-Package sequence uses a left-aligned vertical guide")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
