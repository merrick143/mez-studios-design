#!/usr/bin/env python3
"""Verify GOLD-01 Round 27: remove the ecosystem coda and add the FAQ close."""

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
SOURCE = ROOT / "homepage.source.json"
REVIEW = ROOT / "review.json"
FEEDBACK = ROOT / "round-27-feedback.json"

QUESTIONS = (
    "What is a Mez System?",
    "What is the AI OS?",
    "Do I have to replace ChatGPT, Claude or Notion AI?",
    "Why not use one AI product for everything?",
    "Who is the AI OS for?",
    "What is coming next?",
)


def validate(html: str, css: str, source: dict, review: dict, feedback: dict) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    for label, value in (
        ("source", source.get("candidateRevision")),
        ("review", review.get("candidateRevision")),
        ("feedback", feedback.get("candidateRevision")),
    ):
        if value != "golden-homepage-01-r27":
            fail("META", f"{label} does not identify golden-homepage-01-r27")
    if source.get("version") != "0.27.0-candidate" or "Round 27" not in html:
        fail("META", "workbench or source still identifies an older round")
    if feedback.get("productionAuthority") is not False:
        fail("META", "the FAQ revision must remain non-production")

    ecosystem_start = html.find('data-review-id="GH-S07"')
    faq_review = html.find('data-review-id="GH-S09"')
    faq_start = html.rfind("<section", ecosystem_start, faq_review + 1)
    footer_start = html.find('data-review-id="GH-S10"')
    if not (0 <= ecosystem_start < faq_start <= faq_review < footer_start):
        fail("ORDER", "ecosystem, FAQ and footer must remain in source order")
    ecosystem_tail = html[ecosystem_start:faq_start]
    for removed in (
        "ecosystem-rule",
        "Different systems. Same rule.",
        "Every Mez System is:",
        "Able to improve without rebuilding the business around a new tool",
    ):
        if removed in ecosystem_tail:
            fail("REMOVAL", f"deleted ecosystem coda content returned: {removed}")
    if "Explore the AI OS" in ecosystem_tail:
        fail("REMOVAL", "the deleted bottom AI OS action returned")

    faq = html[faq_start:footer_start] if 0 <= faq_start < footer_start else ""
    for required in (
        'class="faq review-target"',
        'id="faq"',
        "Questions, answered",
        "What operators usually ask first.",
        'class="faq-list"',
    ) + QUESTIONS:
        if required not in faq:
            fail("FAQ", f"FAQ composition missing: {required}")
    if faq.count('<details class="faq-item">') != 6 or faq.count("<summary>") != 6:
        fail("FAQ", "FAQ must expose six native disclosure rows")

    for required in (
        ".faq-layout",
        ".faq-item summary",
        ".faq-item[open] .faq-item__toggle::after",
        "grid-template-columns: minmax(260px, .78fr) minmax(0, 1.22fr)",
        "@media (max-width: 820px)",
        "@media (prefers-reduced-motion: reduce)",
    ):
        if required not in css:
            fail("DESIGN", f"FAQ design contract missing: {required}")

    sections = source.get("sections", [])
    if len(sections) != 10:
        fail("SOURCE", "homepage source must register ten reviewable sections")
    if not any(item.get("id") == "GH-S09" and item.get("title") == "Frequently asked questions" for item in sections):
        fail("SOURCE", "FAQ source record is missing")
    if not any(item.get("id") == "GH-S10" and item.get("title") == "Footer" for item in sections):
        fail("SOURCE", "footer was not moved to GH-S10")

    return failures


def load() -> tuple[str, str, dict, dict, dict]:
    return (
        HTML.read_text(encoding="utf-8"),
        CSS.read_text(encoding="utf-8"),
        json.loads(SOURCE.read_text(encoding="utf-8")),
        json.loads(REVIEW.read_text(encoding="utf-8")),
        json.loads(FEEDBACK.read_text(encoding="utf-8")),
    )


def self_test(data: tuple[str, str, dict, dict, dict]) -> int:
    html, css, source, review, feedback = data
    old_source = copy.deepcopy(source)
    old_source["candidateRevision"] = "golden-homepage-01-r26"
    cases = (
        ("META", html, css, old_source, review, feedback),
        ("REMOVAL", html.replace('</section>\n\n      <!-- GH-S09', '<div class="ecosystem-rule">Different systems. Same rule.</div></section>\n\n      <!-- GH-S09', 1), css, source, review, feedback),
        ("FAQ", html.replace("What is a Mez System?", "", 1), css, source, review, feedback),
        ("DESIGN", html, css.replace("grid-template-columns: minmax(260px, .78fr) minmax(0, 1.22fr)", "grid-template-columns: 1fr", 1), source, review, feedback),
        ("SOURCE", html, css, {**source, "sections": source["sections"][:-1]}, review, feedback),
    )
    misses: list[str] = []
    for expected, *case in cases:
        failures = validate(*case)
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 27 SELF-TEST: FAIL")
        print("- missed mutations: " + ", ".join(misses))
        return 1
    print("GOLDEN HOMEPAGE ROUND 27 SELF-TEST: PASS")
    print("- metadata, coda removal, FAQ composition, design and source-order regressions fail in memory")
    return 0


def main() -> int:
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 27: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1
    print("GOLDEN HOMEPAGE ROUND 27: PASS")
    print("- the ecosystem rule coda and bottom AI OS action are absent")
    print("- a six-question native FAQ now closes the page before GH-S10 footer")
    print("- the FAQ reflows to one column and preserves reduced-motion behaviour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
