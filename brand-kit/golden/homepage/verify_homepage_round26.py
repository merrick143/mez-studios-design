#!/usr/bin/env python3
"""Verify GOLD-01 Round 26: selected unboxed ecosystem disc rail."""

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
FEEDBACK = ROOT / "round-26-feedback.json"

PRODUCTS = {
    "context-engine": ("Context Engine", "MZ-G12", "mz-g12.webp"),
    "ai-ads-system": ("AI Ads System", "MZ-G06", "mz-g06.webp"),
    "claude-code-os": ("Claude Code OS", "MZ-G15", "mz-g15.webp"),
    "organic-content-os": ("Organic Content OS", "MZ-G20", "mz-g20.webp"),
}


def validate(html: str, css: str, javascript: str, source: dict, review: dict, feedback: dict) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    for label, value in (
        ("source", source.get("candidateRevision")),
        ("review", review.get("candidateRevision")),
        ("feedback", feedback.get("candidateRevision")),
    ):
        if value != "golden-homepage-01-r26":
            fail("META", f"{label} does not identify golden-homepage-01-r26")
    if source.get("version") != "0.26.0-candidate" or "Round 26" not in html:
        fail("META", "workbench or source still identifies an older round")
    if feedback.get("productionAuthority") is not False or feedback.get("verdict") != "direction-selected":
        fail("META", "the human direction record must remain a non-production selection")

    section_start = html.find('data-review-id="GH-S07"')
    section_end = html.find('data-review-id="GH-S09"')
    ecosystem = html[section_start:section_end] if 0 <= section_start < section_end else ""
    if not ecosystem:
        fail("BOUNDARY", "GH-S07 is missing or not directly before the footer")
    for required in (
        "Coming next",
        "Specialised systems for the work AI-native businesses do.",
        'class="eco-grid"',
        "ecosystem-rule",
        "Different systems. Same rule.",
        'class="shell eco-stage"',
    ):
        if required not in ecosystem:
            fail("COMPOSITION", f"selected ecosystem composition missing: {required}")

    for slug, (name, gradient, static_twin) in PRODUCTS.items():
        for required in (
            f'data-product="{slug}"',
            name,
            f'data-gradient-id="{gradient}"',
            static_twin,
        ):
            if required not in ecosystem:
                fail("PRODUCT", f"canonical ecosystem product truth missing: {required}")
    if ecosystem.count('class="eco-card"') != 4 or ecosystem.count("Coming soon") != 4:
        fail("PRODUCT", "the selected rail must expose four equal coming-soon products")
    if ecosystem.count('tabindex="0"') != 4:
        fail("ACCESS", "all four hover-live product objects need a keyboard focus equivalent")

    stage_rule = re.search(r"\.eco-stage\s*\{([^}]*)\}", css, re.S)
    card_rule = re.search(r"\.eco-card\s*\{([^}]*)\}", css, re.S)
    field_rule = re.search(r"\.eco-card__field\s*\{([^}]*)\}", css, re.S)
    if not stage_rule or any(token in stage_rule.group(1) for token in ("background", "padding", "border-radius")):
        fail("UNBOXED", "the ecosystem stage must have no shared fill, padding tray or rounded chassis")
    if not card_rule or any(token in card_rule.group(1) for token in ("background", "border:", "border-radius", "padding:")):
        fail("UNBOXED", "ecosystem siblings must not restore a card chassis")
    if not field_rule:
        fail("DISC", "the selected disc field rule is missing")
    else:
        field_css = field_rule.group(1)
        for required in (
            "width: clamp(116px, 11.5vw, 164px)",
            "aspect-ratio: 1",
            "border-radius: var(--mz-radius-full)",
        ):
            if required not in field_css:
                fail("DISC", f"smaller canonical disc rule missing: {required}")
    if ".eco-card__field { width: 88px; }" not in css:
        fail("RESPONSIVE", "compact product discs must resolve to 88px")
    if "justify-items: center" not in card_rule.group(1) or "text-align: center" not in card_rule.group(1):
        fail("ALIGNMENT", "desktop product objects must centre the disc, name and status as one stack")

    if 'renderer.mount(field, field.dataset.gradientId, { shape: "disc", radius: 0, profile: "deep" })' not in javascript:
        fail("MOTION", "ecosystem hover must mount the canonical disc shape")
    hover_start = javascript.find("const activateEcoField")
    hover_end = javascript.find("const releaseEcoField", hover_start)
    for required in ("unmountSingleCore();", "unmountSequence();", "unmountHeroCores();"):
        if required not in javascript[hover_start:hover_end]:
            fail("MOTION", f"one-live-core guard missing before ecosystem mount: {required}")
    for event_name in ("pointerenter", "pointerleave", "focusin", "focusout"):
        if f'card.addEventListener("{event_name}"' not in javascript:
            fail("ACCESS", f"ecosystem interaction missing: {event_name}")

    lock = review.get("ecosystemSectionLock", {})
    if not lock.get("locked") or lock.get("lockedRevision") != "golden-homepage-01-r26":
        fail("LOCK", "review state does not preserve Olli's provisional GH-S07 selection")
    selected = feedback.get("selected", {})
    if selected.get("direction") != "V02 Unboxed disc rail" or "116–164px" not in selected.get("desktopDiscBand", ""):
        fail("LOCK", "feedback does not record the selected direction and smaller disc band")

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
    old_source["candidateRevision"] = "golden-homepage-01-r25"
    cases = (
        ("META", html, css, javascript, old_source, review, feedback),
        ("UNBOXED", html, css.replace(".eco-stage {\n  margin-top", ".eco-stage {\n  background: #1b1b19;\n  margin-top", 1), javascript, source, review, feedback),
        ("DISC", html, css.replace("width: clamp(116px, 11.5vw, 164px)", "width: clamp(116px, 11.5vw, 250px)", 1), javascript, source, review, feedback),
        ("MOTION", html, css, javascript.replace('renderer.mount(field, field.dataset.gradientId, { shape: "disc"', 'renderer.mount(field, field.dataset.gradientId, { shape: "rect"', 1), source, review, feedback),
        ("PRODUCT", html.replace("mz-g20.webp", "missing.webp", 1), css, javascript, source, review, feedback),
    )
    misses: list[str] = []
    for expected, *case in cases:
        failures = validate(*case)
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 26 SELF-TEST: FAIL")
        print("- missed mutations: " + ", ".join(misses))
        return 1
    print("GOLDEN HOMEPAGE ROUND 26 SELF-TEST: PASS")
    print("- metadata, unboxed composition, disc scale, motion and product regressions fail in memory")
    return 0


def main() -> int:
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 26: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1
    print("GOLDEN HOMEPAGE ROUND 26: PASS")
    print("- GH-S07 uses the selected unboxed four-disc rail")
    print("- the standard-width rail centres 116–164px desktop discs and resolves to 88px compact discs")
    print("- exact static twins and one hover-live canonical disc are enforced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
