#!/usr/bin/env python3
"""Verify the GOLD-01 Round 17 candidate: the authored-split-card reinvention of the
editorial sections (S02 Problem, S03 Principle, S04 Built-on-ourselves), the S05
Operating-proof rebuild, the S06 AI-OS Wings centring + bottom-card pair (orbital /
2x2 index), the S07 ecosystem card simplification, and the family header-alignment
fix — with the locked hero, canonical motion and honest evidence states carried
forward, and the S03 rented-brand logos removed for good."""

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
SECTION_REVIEW = ROOT / "round-16-section-review-feedback.json"
HERO_LOCK = ROOT / "round-14-feedback.json"
HERO_MOTION_REVIEW = ROOT / "hero-motion.review.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    required = (
        HTML, CSS, JS, MOBILE, SOURCE, SCHEMA, REVIEW,
        SECTION_REVIEW, HERO_LOCK, HERO_MOTION_REVIEW,
    )
    for path in required:
        if not path.exists():
            failures.append(f"missing Round 17 artifact: {path.relative_to(BRAND_KIT.parent)}")
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

    # --- Ten reviewable regions, ordered ---
    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if section_ids != [f"GH-S{index:02d}" for index in range(1, 11)]:
        failures.append(f"section ids are not the ordered GH-S01..GH-S10 sequence: {section_ids}")
    for expected in (
        'data-review-id="GH-S02" data-review-title="The problem"',
        'data-review-id="GH-S03" data-review-title="The Mez Systems principle"',
        'data-review-id="GH-S04" data-review-title="Built on ourselves first"',
        'data-review-id="GH-S05" data-review-title="Operating proof"',
        'data-review-id="GH-S06" data-review-title="Available now: AI OS"',
        'data-review-id="GH-S07" data-review-title="The Mez Systems ecosystem"',
        'data-review-id="GH-S08" data-review-title="Proof from the first Mez System"',
        'data-review-id="GH-S09" data-review-title="Final route"',
        'data-review-id="GH-S10" data-review-title="Footer"',
    ):
        if expected not in html:
            failures.append(f"reviewable region missing/renamed: {expected}")

    # --- R17 authored-split-card family (shared editorial grammar) ---
    if ".split-card {" not in css:
        failures.append("the shared .split-card family (S02/S03/S04) is missing from CSS")
    for family_part in (".split-card__editorial", ".split-card__viz", ".split-chips", ".split-badge"):
        if family_part not in css:
            failures.append(f"split-card family part missing: {family_part}")
    if html.count('class="split-card"') != 3:
        failures.append("exactly three editorial sections (S02/S03/S04) must use the split card")

    # S02 Problem — charcoal fragmentation field, not the old drifting tiles
    for token in ("frag-field", "frag-void", "problem-consequences"):
        if token not in html:
            failures.append(f"S02 problem rebuild missing: {token}")
    for banned in ("problem-tile", "problem-fragments", "tool-pile", "tool-window"):
        if banned in html:
            failures.append(f"superseded S02 markup must not remain: {banned}")

    # S03 Principle — abstract swap-slots over an owned base; NO rented-brand logos
    for token in ("intel-slot", "intel-base__wings", "Interchangeable intelligence"):
        if token not in html:
            failures.append(f"S03 principle rebuild missing: {token}")
    for banned_logo in ("data-intelligence", "principle-logo", "ownership-instrument", "instrument-rented"):
        if banned_logo in html:
            failures.append(f"S03 must not reintroduce the rented-brand logo mechanism: {banned_logo}")

    # S04 Built-on-ourselves — the operating loop keeps its sequence wiring
    if "method-loop" not in html or javascript.count("data-method-sequence") < 1:
        failures.append("S04 operating-loop (method-loop / data-method-sequence) is missing")
    if len(re.findall(r"data-method-step", html)) != 5:
        failures.append("S04 operating loop must expose exactly five stages")
    for banned in ("origin-ledger", "method-console", "origin-lines"):
        if banned in html:
            failures.append(f"superseded S04 markup must not remain: {banned}")

    # S05 Operating proof — honest charcoal redacted-screen placeholders (was unstyled)
    if "op-grid" not in html or "op-screen" not in html:
        failures.append("S05 operating-proof rebuild (op-grid / op-screen) is missing")
    if len(re.findall(r'class="op-screen"', html)) != 3:
        failures.append("operating proof must expose exactly three redacted-screen records")
    if "proof-record" in html:
        failures.append("the unstyled S05 proof-record markup must be replaced")
    if ".op-grid" not in css:
        failures.append("S05 operating-proof was previously unstyled; the .op-grid CSS must exist now")

    # S06 AI OS — Wings centred + enlarged; bottom pair rebuilt (orbital + 2x2 index)
    wings_block = re.search(r"\.aios-material__wings\s*\{([^}]*)\}", css)
    if not wings_block or "left: 50%" not in wings_block.group(1) or "translate(-50%, -50%)" not in wings_block.group(1):
        failures.append("the AI OS card Wings must be centred on the material (left/translate centring)")
    for token in ("aios-panel--how", "aios-orbit", "aios-orbit__core", "aios-panel--features", "aios-featuregrid"):
        if token not in html:
            failures.append(f"S06 bottom-card pair rebuild missing: {token}")
    if len(re.findall(r'class="aios-feat"', html)) != 4:
        failures.append("the Features panel must expose exactly four capability cells")
    for banned in ("aios-col", "aios-flow"):
        if banned in html:
            failures.append(f"superseded S06 split markup must not remain: {banned}")

    # S07 Ecosystem — Wings + name + Coming soon; NO waitlist / extended / job
    if len(re.findall(r'class="eco-card"', html)) != 4:
        failures.append("ecosystem must expose exactly four coming-soon cards")
    if len(re.findall(r'class="eco-card__status"', html)) != 4:
        failures.append("each ecosystem card must carry a 'Coming soon' status")
    for banned in ("data-eco-waitlist", "eco-card__ext", "eco-card__job", "Join waitlist"):
        if banned in html:
            failures.append(f"S07 must be simplified to Wings + name + Coming soon; found: {banned}")

    # --- Family header-alignment fix (the reintroduced 'why is the title indented' bug) ---
    for head in (".problem-head", ".principle-head", ".why-head", ".op-head"):
        block = re.search(re.escape(head) + r"\s*\{([^}]*)\}", css)
        if not block:
            failures.append(f"family header rule missing: {head}")
        elif "max-width" in block.group(1):
            failures.append(f"{head} must not carry a container max-width (it centres/indents the header)")
    why_h2 = re.search(r"\.why-head h2\s*\{([^}]*)\}", css)
    if not why_h2 or "max-width" not in why_h2.group(1):
        failures.append("the header measure must live on the text (.why-head h2 cap), not the container")

    # --- Locked copy carried forward (tags stripped: some headings split a grey
    #     prefix into a <span class="head-quiet">, so check the rendered text) ---
    plain = re.sub(r"<[^>]+>", "", html)
    for phrase in (
        "The operating systems AI-native businesses run on.",
        "Too many tools. Too many middlemen.",
        "Use the best intelligence. Own the layer around it.",
        "We run Mez Studios on the systems we sell.",
        "Operating proof",
        "Give AI a business to understand.",
        "Specialised systems for the work AI-native businesses do.",
        "Built to be used, not admired.",
        "Explore the Systems",
    ):
        if phrase not in plain:
            failures.append(f"locked homepage phrase missing from workbench: {phrase}")

    # --- Foundations, registry-driven hero, canonical Wings ---
    if '../../../releases/foundations/dist/index.css' not in html:
        failures.append("canonical foundation release is not loaded")
    if 'registry/products.json' not in javascript or "products.map" not in javascript:
        failures.append("hero family is not generated from the canonical product registry")
    if "brightness(0) invert(1)" not in css:
        failures.append("canonical white Wings treatment is missing")
    if "entry-armed" not in javascript or "entry-armed" not in css:
        failures.append("section entry must be armed by JavaScript so content survives without it")

    # --- Hero unchanged (locked at V01) + Round 11/12 consistency guards ---
    if "hero-core-layer" in (html + css + javascript):
        failures.append("collapsed hero-core-layer mount pattern must not return")
    if javascript.count("renderer.mount(material") != 1:
        failures.append("hero must mount cores directly on sized material elements in one bounded loop")
    if ".hero-card .hero-card__material::after" in css:
        failures.append("hero cards must not fork the shared material overlay (Round 11 guard)")
    if "--card-outline: var(--mz-border-default)" not in css:
        failures.append("card outline must stay bound to the canonical token (Round 12)")
    if "rgba(25, 25, 25, .42)" in css:
        failures.append("the bespoke harsh card outline value must stay removed")
    hero_identity_block = re.search(r"\.hero-card \.material-identity\s*\{([^}]*)\}", css)
    if not hero_identity_block or "align-items: center" not in hero_identity_block.group(1):
        failures.append("Round 11 centred hero identity mark must remain")

    # --- Motion contract ---
    motion = source.get("motion", {})
    if (
        motion.get("heroMotionTreatment") != "phase-a-canonical-automatic"
        or motion.get("heroRestSpeed") != 1
        or motion.get("heroHoverSpeed") != 1.85
        or motion.get("ordinaryMaximumLivePageCores") != 1
    ):
        failures.append("canonical-automatic hero motion contract must be unchanged")
    if motion.get("eligibleSections") != ["GH-S01", "GH-S06", "GH-S09"]:
        failures.append("motion eligibleSections must stay [GH-S01, GH-S06, GH-S09]")
    if len(source.get("sections", [])) != 10:
        failures.append("the section contract must list exactly ten reviewable regions")

    # --- Honest proof states ---
    if html.count("Evidence pending") != 3:
        failures.append("all three operating screens must remain honest 'Evidence pending' slots")
    if "consent verification pending" not in html.lower():
        failures.append("testimonial section must expose pending consent verification")

    # --- Compact proof (no horizontal swipe) ---
    if "overflow-x: auto" in css or "scroll-snap-type" in css:
        failures.append("compact composition must not depend on horizontal swiping")
    if "390px" not in mobile:
        failures.append("compact 390px vertical family proof is missing")

    # --- Portability ---
    for token in ("/Users/", "/private/", "file://", "http://"):
        for path, text in ((HTML, html), (CSS, css), (JS, javascript), (SOURCE, SOURCE.read_text())):
            if token in text:
                failures.append(f"absolute or non-portable dependency in {path.name}: {token}")

    if 'candidateRevision: "golden-homepage-01-r17"' not in javascript:
        failures.append("review export does not identify the Round 17 candidate")
    if javascript.count("data-review-item") < 1 or "reviewPayload" not in javascript:
        failures.append("section-level keep/revise/kill review tooling is missing")

    heading_levels = [int(level) for level in re.findall(r"<h([1-3])(?:\s|>)", html)]
    if not heading_levels or heading_levels[0] != 1 or heading_levels.count(1) != 1:
        failures.append("homepage must contain one leading h1")

    # --- Governance traces ---
    review = read_json(REVIEW)
    if (
        review.get("verdict") != "pending"
        or review.get("candidateRevision") != "golden-homepage-01-r17"
        or review.get("productionAuthority") is not False
    ):
        failures.append("Round 17 review record must be pending, r17, non-production")
    if review.get("heroSectionLock", {}).get("locked") is not True:
        failures.append("the provisional GH-S01 hero lock must carry forward")
    if source.get("version") != "0.17.0-candidate" or source.get("candidateRevision") != "golden-homepage-01-r17":
        failures.append("source contract must be stamped 0.17.0-candidate / r17")

    section_review = read_json(SECTION_REVIEW)
    verdicts = {s.get("id"): s.get("verdict") for s in section_review.get("sections", [])}
    if verdicts.get("GH-S02") != "revise" or verdicts.get("GH-S03") != "revise" or verdicts.get("GH-S01") != "keep":
        failures.append("the r15 section-review feedback trace (driving R17) is incomplete")

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
        print("MEZ GOLDEN HOMEPAGE ROUND 17: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GOLDEN HOMEPAGE ROUND 17: PASS")
    print("- S02/S03/S04 reinvented on one authored split-card family (light editorial + charcoal generative)")
    print("- S03 rented-brand logos removed for good; interchangeable intelligence shown as abstract swap-slots")
    print("- S05 operating proof rebuilt from unstyled text into honest charcoal 'Evidence pending' screens")
    print("- S06 Wings centred + enlarged; bottom pair rebuilt as an orbital diagram + a divided 2x2 index")
    print("- S07 ecosystem simplified to Wings + name + Coming soon (waitlist removed)")
    print("- family header indent fixed; locked hero, canonical motion and honest states carried forward")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
