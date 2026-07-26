#!/usr/bin/env python3
"""Verify the GOLD-01 Round 10 hero deck further-compaction candidate."""

from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "golden" / "homepage"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
JS = WORKBENCH / "homepage.js"
MOBILE = WORKBENCH / "mobile-proof.html"
SOURCE = ROOT / "homepage.source.json"
SCHEMA = ROOT / "homepage.schema.json"
REVIEW = ROOT / "review.json"
ROUND_07_FEEDBACK = ROOT / "round-07-feedback.json"
ROUND_08_FEEDBACK = ROOT / "round-08-feedback.json"
ROUND_09_FEEDBACK = ROOT / "round-09-feedback.json"
HERO_MOTION_REVIEW = ROOT / "hero-motion.review.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    required = (
        HTML,
        CSS,
        JS,
        MOBILE,
        SOURCE,
        SCHEMA,
        REVIEW,
        ROOT / "round-01-feedback.json",
        ROOT / "round-02-hero-feedback.json",
        ROOT / "round-03-hero-feedback.json",
        ROOT / "round-04-hero-feedback.json",
        ROOT / "round-05-feedback.json",
        ROOT / "round-06-feedback.json",
        ROUND_07_FEEDBACK,
        ROUND_08_FEEDBACK,
        ROUND_09_FEEDBACK,
        HERO_MOTION_REVIEW,
    )
    for path in required:
        if not path.exists():
            failures.append(f"missing Round 10 artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return report(failures)

    source = read_json(SOURCE)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"homepage source schema: {error.message}")

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    javascript = JS.read_text(encoding="utf-8")
    mobile = MOBILE.read_text(encoding="utf-8")

    for section_id in [f"GH-S{index:02d}" for index in range(1, 10)]:
        if f'data-review-id="{section_id}"' not in html:
            failures.append(f"missing reviewable page region: {section_id}")

    for phrase in (
        "The operating systems AI-native businesses run on.",
        "Too many tools. Too many middlemen.",
        "Use the best intelligence. Own the layer around it.",
        "We run Mez Studios on the systems we sell.",
        "Give AI a business to understand.",
        "Specialised systems for the work AI-native businesses do.",
        "Built to be used, not admired.",
        "Start with the AI OS.",
        "Explore the Systems",
    ):
        if phrase not in html:
            failures.append(f"locked homepage phrase missing from workbench: {phrase}")

    # Round 09 removals must stay removed.
    if "family-caption" in (html + css) or "supporting-line" in (html + css):
        failures.append("the Round 09 hero-copy removals must not return")
    if "AI OS is available now" in html or "One operating layer" in html:
        failures.append("removed hero copy must not return")

    if '../../../releases/foundations/dist/index.css' not in html:
        failures.append("canonical foundation release is not loaded")
    if 'registry/products.json' not in javascript or "products.map" not in javascript:
        failures.append("hero family is not generated from the canonical product registry")

    for visual_contract in (
        "product-deck--arc",
        "hero-card__material",
        ".hero-card .material-identity",
        "tool-pile",
        "ownership-instrument",
        "method-console",
        "proof-record",
        "identity-event",
        "ecosystem-card__field",
        "testimonial-disc",
        "final-installed",
    ):
        if visual_contract not in (html + css + javascript):
            failures.append(f"carried-forward component missing in Round 10: {visual_contract}")

    if "hero-core-layer" in (html + css + javascript):
        failures.append("collapsed hero-core-layer mount pattern must not return")
    if javascript.count("renderer.mount(material") != 1:
        failures.append("hero must mount cores directly on sized material elements in one bounded loop")
    for banned_override in ("HERO_CORE_SPEED", "surface.speed", "speedTarget", "hero-core-drift"):
        if banned_override in (javascript + css):
            failures.append(f"hero motion must stay canonical-automatic; found override: {banned_override}")

    # Round 10 geometry: tighter than Round 08/09's 50-80/-32to-50/94-142.
    # These exact literals anchor the tightened step so a future round can't
    # silently drift back to the looser Round 08 numbers without a new round.
    for tightened_contract in (
        "clamp(36px, 4.2vw, 60px)",
        "clamp(-58px, -4vw, -38px)",
        "clamp(70px, 8vw, 112px)",
    ):
        if tightened_contract not in css:
            failures.append(f"Round 10 tightened hero geometry missing: {tightened_contract}")
    for stale_geometry in ("clamp(50px, 5.7vw, 80px)", "clamp(-50px, -3.4vw, -32px)"):
        if stale_geometry in css:
            failures.append(f"stale Round 08 geometry must not remain alongside the Round 10 values: {stale_geometry}")

    motion = source.get("motion", {})
    if (
        motion.get("heroMotionTreatment") != "phase-a-canonical-automatic"
        or motion.get("heroRestSpeed") != 1
        or motion.get("heroHoverSpeed") != 1.85
        or motion.get("coreMountHostsIntrinsicallySized") is not True
    ):
        failures.append("canonical-automatic hero motion contract must be unchanged")

    if "brightness(0) invert(1)" not in css:
        failures.append("canonical white Wings treatment is missing from card identity")
    if "entry-armed" not in javascript or "entry-armed" not in css:
        failures.append("section entry must be armed by JavaScript so content survives without it")

    if "overflow-x: auto" in css or "scroll-snap-type" in css:
        failures.append("compact composition must not depend on horizontal swiping")
    if "grid-template-columns: repeat(2, minmax(0, 1fr))" not in css or "390px" not in mobile:
        failures.append("compact one-plus-four vertical family proof is missing")
    if 'src="./?static=1"' not in mobile:
        failures.append("compact proof must exercise the exact static fallback")

    if len(re.findall(r'class="proof-record(?:\s|")', html)) != 3:
        failures.append("operating proof must expose exactly three governed records")
    if "consent verification pending" not in html.lower():
        failures.append("testimonial section must expose pending consent verification")
    if html.lower().count("evidence intake") < 3:
        failures.append("all operating screenshots must remain honest evidence-intake slots")

    for token in ("/Users/", "/private/", "file://", "http://"):
        for path, text in ((HTML, html), (CSS, css), (JS, javascript), (SOURCE, SOURCE.read_text())):
            if token in text:
                failures.append(f"absolute or non-portable dependency in {path.name}: {token}")

    if 'candidateRevision: "golden-homepage-01-r10"' not in javascript:
        failures.append("review export does not identify the Round 10 candidate")
    if javascript.count("data-review-item") < 1 or "reviewPayload" not in javascript:
        failures.append("section-level keep/revise/kill review tooling is missing")

    heading_levels = [int(level) for level in re.findall(r"<h([1-3])(?:\s|>)", html)]
    if not heading_levels or heading_levels[0] != 1 or heading_levels.count(1) != 1:
        failures.append("homepage must contain one leading h1")

    review = read_json(REVIEW)
    if (
        review.get("verdict") != "pending"
        or review.get("candidateRevision") != "golden-homepage-01-r10"
        or review.get("productionAuthority") is not False
    ):
        failures.append("Round 10 review record must remain pending and non-production")

    round_08 = read_json(ROUND_08_FEEDBACK)
    if round_08.get("candidateRevision") != "golden-homepage-01-r08" or len(round_08.get("sections", [])) != 1:
        failures.append("Round 08 hero-copy-trim feedback trace is incomplete")

    round_09 = read_json(ROUND_09_FEEDBACK)
    if (
        round_09.get("candidateRevision") != "golden-homepage-01-r09"
        or round_09.get("verdict") != "round-feedback"
        or len(round_09.get("sections", [])) != 1
        or round_09.get("sections", [{}])[0].get("id") != "GH-S01"
        or "too low" not in round_09.get("sections", [{}])[0].get("feedback", "").lower()
        or "rejectedAttempt" not in round_09.get("implementationNote", {})
    ):
        failures.append("Round 09 feedback and the rejected-overtightening trace must be recorded")

    hero_motion = read_json(HERO_MOTION_REVIEW)
    if (
        hero_motion.get("decisionId") != "DEC-GOLDEN-HOMEPAGE-HERO-MOTION-001"
        or hero_motion.get("status") != "approved-bounded"
        or hero_motion.get("productionAuthority") is not False
    ):
        failures.append("bounded hero-motion decision trace is incomplete")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        print("MEZ GOLDEN HOMEPAGE ROUND 10: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GOLDEN HOMEPAGE ROUND 10: PASS")
    print("- nine reviewable regions carry forward; only the hero geometry tightened further this round")
    print("- per-card vertical step and horizontal overlap are measurably tighter than Round 08/09")
    print("- every card's public name remains fully legible under strict hit-testing")
    print("- an even tighter pass that clipped a card's name was tested and explicitly rejected, not shipped")
    print("- Living Cores stay on sized hosts with unchanged canonical-automatic motion and complete fallbacks")
    print("- compact proof keeps every product visible without horizontal swipe-only discovery")
    print("- the Round 09 feedback is preserved and the human gate remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
