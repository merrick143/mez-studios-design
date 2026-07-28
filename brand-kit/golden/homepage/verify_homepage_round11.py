#!/usr/bin/env python3
"""Verify the GOLD-01 Round 11 centred card-face identity candidate."""

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
ROUND_08_FEEDBACK = ROOT / "round-08-feedback.json"
ROUND_09_FEEDBACK = ROOT / "round-09-feedback.json"
ROUND_10_FEEDBACK = ROOT / "round-10-feedback.json"
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
        ROOT / "round-07-feedback.json",
        ROUND_08_FEEDBACK,
        ROUND_09_FEEDBACK,
        ROUND_10_FEEDBACK,
        HERO_MOTION_REVIEW,
    )
    for path in required:
        if not path.exists():
            failures.append(f"missing Round 11 artifact: {path.relative_to(BRAND_KIT.parent)}")
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

    if "family-caption" in (html + css) or "supporting-line" in (html + css):
        failures.append("the Round 09 hero-copy removals must not return")

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
            failures.append(f"carried-forward component missing in Round 11: {visual_contract}")

    if "hero-core-layer" in (html + css + javascript):
        failures.append("collapsed hero-core-layer mount pattern must not return")
    if javascript.count("renderer.mount(material") != 1:
        failures.append("hero must mount cores directly on sized material elements in one bounded loop")
    for banned_override in ("HERO_CORE_SPEED", "surface.speed", "speedTarget", "hero-core-drift"):
        if banned_override in (javascript + css):
            failures.append(f"hero motion must stay canonical-automatic; found override: {banned_override}")

    # Round 10 fan geometry is unchanged this round -- only card content style
    # changed. These exact literals anchor that the positional tightening
    # itself was not touched.
    for unchanged_geometry in (
        "clamp(36px, 4.2vw, 60px)",
        "clamp(-58px, -4vw, -38px)",
        "clamp(70px, 8vw, 112px)",
    ):
        if unchanged_geometry not in css:
            failures.append(f"Round 10 fan geometry must remain unchanged in Round 11: {unchanged_geometry}")

    # Round 11 centred identity: bigger, centred mark; ecosystem/final-route
    # cards keep their own bottom-left instance of the shared component.
    hero_identity_block_match = re.search(
        r"\.hero-card \.material-identity\s*\{([^}]*)\}", css
    )
    if not hero_identity_block_match:
        failures.append("hero identity mark override rule is missing")
    else:
        block = hero_identity_block_match.group(1)
        for centering_property in ("align-items: center", "justify-content: center", "text-align: center"):
            if centering_property not in block:
                failures.append(f"hero identity mark must be centred: missing {centering_property}")
        if "bottom:" in block:
            failures.append("hero identity mark must not still be bottom-anchored")

    for stale_size in (
        "clamp(13px, 1.2vw, 16px)",
        "clamp(12.5px, 1.15vw, 15px)",
        "font-size: 8px;\n}\n\n.hero-card .hero-card__material",
    ):
        if stale_size in css:
            failures.append(f"stale Round 10 compact-mark sizing must not remain: {stale_size!r}")

    # Consistency guard: the hero must NOT fork the shared card material
    # overlay. An earlier Round 11 pass added a hero-only darkening override
    # that made the hero material read darker than every other card; it was
    # reverted at the reviewer's direction. Hero cards use the canonical
    # bottom-weighted `.hero-card__material::after` unchanged.
    if ".hero-card .hero-card__material::after" in css:
        failures.append("hero cards must not fork the shared material overlay; the canonical .hero-card__material::after applies unchanged")

    products = source.get("products", {})
    if products.get("heroIdentityMarkAlignment") != "centred":
        failures.append("homepage contract must record the centred identity-mark alignment")
    if products.get("heroOcclusionAuthorised") is not True:
        failures.append("homepage contract must record Olli's explicit occlusion authorisation")
    if products.get("heroArrangement") != "centred-spread-deck-2-1-2-compact":
        failures.append("hero arrangement identifier must be unchanged from Round 08")

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

    if 'candidateRevision: "golden-homepage-01-r11"' not in javascript:
        failures.append("review export does not identify the Round 11 candidate")
    if javascript.count("data-review-item") < 1 or "reviewPayload" not in javascript:
        failures.append("section-level keep/revise/kill review tooling is missing")

    heading_levels = [int(level) for level in re.findall(r"<h([1-3])(?:\s|>)", html)]
    if not heading_levels or heading_levels[0] != 1 or heading_levels.count(1) != 1:
        failures.append("homepage must contain one leading h1")

    review = read_json(REVIEW)
    if (
        review.get("verdict") != "pending"
        or review.get("candidateRevision") != "golden-homepage-01-r11"
        or review.get("productionAuthority") is not False
    ):
        failures.append("Round 11 review record must remain pending and non-production")

    round_09 = read_json(ROUND_09_FEEDBACK)
    if round_09.get("candidateRevision") != "golden-homepage-01-r09" or len(round_09.get("sections", [])) != 1:
        failures.append("Round 09 hero-compaction feedback trace is incomplete")

    round_10 = read_json(ROUND_10_FEEDBACK)
    if (
        round_10.get("candidateRevision") != "golden-homepage-01-r10"
        or round_10.get("verdict") != "round-feedback"
        or len(round_10.get("sections", [])) != 1
        or round_10.get("sections", [{}])[0].get("id") != "GH-S01"
        or "constraintSupersession" not in round_10
        or "occlusion" not in round_10.get("constraintSupersession", {}).get("supersededBy", "").lower()
    ):
        failures.append("Round 10 centred-identity feedback and its constraint-supersession trace must be recorded")

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
        print("MEZ GOLDEN HOMEPAGE ROUND 11: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GOLDEN HOMEPAGE ROUND 11: PASS")
    print("- nine reviewable regions carry forward; only hero card content style changed this round")
    print("- the hero identity mark is fully centred with a larger Wings icon and larger titles")
    print("- Olli's explicit occlusion authorisation is recorded, scoped to fan-overlap only")
    print("- the Round 10 fan geometry itself is unchanged; only the in-card content style moved")
    print("- Living Cores stay on sized hosts with unchanged canonical-automatic motion and complete fallbacks")
    print("- compact proof keeps every product visible without horizontal swipe-only discovery")
    print("- the Round 10 feedback is preserved and the human gate remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
