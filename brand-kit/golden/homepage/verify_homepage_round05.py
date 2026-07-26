#!/usr/bin/env python3
"""Verify the GOLD-01 Round 05 visibly animated hero candidate."""

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
ROUND_01_FEEDBACK = ROOT / "round-01-feedback.json"
ROUND_02_HERO_FEEDBACK = ROOT / "round-02-hero-feedback.json"
ROUND_03_HERO_FEEDBACK = ROOT / "round-03-hero-feedback.json"
ROUND_04_HERO_FEEDBACK = ROOT / "round-04-hero-feedback.json"
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
        ROUND_01_FEEDBACK,
        ROUND_02_HERO_FEEDBACK,
        ROUND_03_HERO_FEEDBACK,
        ROUND_04_HERO_FEEDBACK,
        HERO_MOTION_REVIEW,
    )
    for path in required:
        if not path.exists():
            failures.append(f"missing Round 05 artifact: {path.relative_to(BRAND_KIT.parent)}")
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
    ):
        if phrase not in html:
            failures.append(f"locked homepage phrase missing from workbench: {phrase}")

    if '../../../releases/foundations/dist/index.css' not in html:
        failures.append("canonical foundation release is not loaded")
    if '../../../components/global-navigation/mez-global-navigation.css' not in html:
        failures.append("canonical Global Navigation stylesheet is not loaded")
    if 'components/global-navigation/mez-global-navigation.js' not in javascript:
        failures.append("canonical Global Navigation component is not imported")
    if 'registry/products.json' not in javascript or "products.map" not in javascript:
        failures.append("hero family is not generated from the canonical product registry")
    if "comingProducts" not in javascript or "data-ecosystem-stage" not in html:
        failures.append("future product family is not generated as a composed four-product deck")
    for visual_contract in (
        "hero-family--fan",
        "ownership-instrument",
        "method-instrument",
        "ai-os-pair",
        "ecosystem-composition",
        "testimonial-ledger",
        "final-system--installed",
    ):
        if visual_contract not in html:
            failures.append(f"Round 05 visual contract missing: {visual_contract}")

    if javascript.count("renderer.mount(liveLayer") != 1:
        failures.append("ordinary page regions must have exactly one allocator mount call")
    if javascript.count("renderer.mount(layer") != 1:
        failures.append("hero must have exactly one bounded multi-surface allocator loop")
    for contract in (
        'expandedNavigationSuppressesPageMotion',
        "unmountAllPageCores",
        "mountHeroCores",
        "unmountHeroCores",
        "mez-navigation-open",
    ):
        if contract not in (json.dumps(source) + javascript):
            failures.append(f"motion allocator contract missing: {contract}")
    motion = source.get("motion", {})
    if (
        motion.get("maximumLivePageCores") != 5
        or motion.get("ordinaryMaximumLivePageCores") != 1
        or motion.get("heroLivePageCores") != 5
        or motion.get("heroFiveLiveException") is not True
        or motion.get("heroMotionDecisionId") != "DEC-GOLDEN-HOMEPAGE-HERO-MOTION-001"
        or motion.get("heroMotionLegibleAtRest") is not True
        or motion.get("heroRestSpeed") != 3.2
        or motion.get("heroHoverSpeed") != 4
        or motion.get("heroMaterialDriftSeconds") != 6.4
    ):
        failures.append("bounded five-live hero allocation is incomplete")
    if javascript.count("data-hero-core-layer") < 2 or "heroLayers" not in javascript:
        failures.append("five-card hero Living Core layer generation is missing")
    for simplified_contract in (
        "hero-product__copy .material-wings",
        "position: static",
        "rgba(25, 25, 25, .42)",
    ):
        if simplified_contract not in (javascript + css):
            failures.append(f"simplified outlined card contract missing: {simplified_contract}")
    if "hero-product__action" in javascript or "hero-product__copy p" in css:
        failures.append("hero cards must not contain actions or descriptive copy")
    for motion_contract in (
        "HERO_CORE_SPEED",
        "rest: 3.2",
        "hover: 4",
        "surface.speed = HERO_CORE_SPEED.rest",
        "surface.speedTarget = HERO_CORE_SPEED.rest",
        'interactionTarget.addEventListener("pointerenter"',
        'interactionTarget.addEventListener("pointerleave"',
    ):
        if motion_contract not in javascript:
            failures.append(f"visible hero motion contract missing: {motion_contract}")
    for drift_contract in (
        "@keyframes hero-core-drift",
        "animation: hero-core-drift 6.4s",
        "translate3d(-3.5%, -1.5%, 0) scale(1.12)",
        "translate3d(3.5%, 1.5%, 0) scale(1.16)",
    ):
        if drift_contract not in css:
            failures.append(f"visible hero material drift missing: {drift_contract}")

    if "overflow-x: auto" in css or "scroll-snap-type" in css:
        failures.append("compact hero must not depend on horizontal swiping")
    if "grid-template-columns: 1fr;" not in css or "390px" not in mobile:
        failures.append("compact vertical composition proof is missing")
    if 'src="./?static=1"' not in mobile:
        failures.append("compact proof must exercise the exact static fallback")

    if len(re.findall(r'class="proof-record(?:\s|")', html)) != 3:
        failures.append("operating proof must expose exactly three governed records")
    if "consent verification pending" not in html.lower():
        failures.append("testimonial section must expose pending consent verification")
    if html.count("Evidence intake") < 3:
        failures.append("all operating screenshots must remain honest evidence-intake slots")

    for token in ("/Users/", "/private/", "file://"):
        for path, text in ((HTML, html), (CSS, css), (JS, javascript), (SOURCE, SOURCE.read_text())):
            if token in text:
                failures.append(f"absolute dependency in {path.name}: {token}")

    if "candidateRevision: \"golden-homepage-01-r05\"" not in javascript:
        failures.append("review export does not identify the Round 05 candidate")
    if javascript.count('data-review-item') < 1 or "reviewPayload" not in javascript:
        failures.append("section-level keep/revise/kill review tooling is missing")

    heading_levels = [int(level) for level in re.findall(r"<h([1-3])(?:\\s|>)", html)]
    if not heading_levels or heading_levels[0] != 1 or heading_levels.count(1) != 1:
        failures.append("homepage must contain one leading h1")

    review = read_json(REVIEW)
    if (
        review.get("verdict") != "pending"
        or review.get("candidateRevision") != "golden-homepage-01-r05"
        or review.get("productionAuthority") is not False
    ):
        failures.append("Round 05 review record must remain pending and non-production")

    feedback = read_json(ROUND_01_FEEDBACK)
    if (
        feedback.get("candidateRevision") != "golden-homepage-01-r01"
        or feedback.get("verdict") != "round-feedback"
        or len(feedback.get("sections", [])) != 9
    ):
        failures.append("Round 01 human feedback trace is incomplete")

    hero_feedback = read_json(ROUND_02_HERO_FEEDBACK)
    if (
        hero_feedback.get("candidateRevision") != "golden-homepage-01-r02"
        or hero_feedback.get("verdict") != "round-feedback"
        or not any("QC04" in reference for reference in hero_feedback.get("references", []))
    ):
        failures.append("Round 02 hero redirect is incomplete")

    simplification_feedback = read_json(ROUND_03_HERO_FEEDBACK)
    if (
        simplification_feedback.get("candidateRevision") != "golden-homepage-01-r03"
        or simplification_feedback.get("verdict") != "round-feedback"
        or "No buttons" not in simplification_feedback.get("sections", [{}])[0].get("feedback", "")
    ):
        failures.append("Round 03 hero simplification feedback is incomplete")

    motion_feedback = read_json(ROUND_04_HERO_FEEDBACK)
    if (
        motion_feedback.get("candidateRevision") != "golden-homepage-01-r04"
        or motion_feedback.get("verdict") != "round-feedback"
        or "do not read as animated" not in motion_feedback.get("sections", [{}])[0].get("feedback", "")
    ):
        failures.append("Round 04 hero motion-legibility feedback is incomplete")

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
        print("MEZ GOLDEN HOMEPAGE ROUND 05: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GOLDEN HOMEPAGE ROUND 05: PASS")
    print("- nine reviewable regions compose one complete locked-copy homepage")
    print("- five outlined full-field cards contain only bottom-left Wings and two-line identity")
    print("- every hero material is visibly animated at rest while card structure remains static")
    print("- five hero Living Cores yield to one page core elsewhere and to five navigation spheres")
    print("- compact proof preserves every product without horizontal swipe-only discovery")
    print("- cumulative feedback through Round 04 and the bounded motion decision are preserved")
    print("- human golden approval remains open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
