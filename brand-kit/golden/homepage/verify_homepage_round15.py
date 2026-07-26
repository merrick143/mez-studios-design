#!/usr/bin/env python3
"""Verify the GOLD-01 Round 15 candidate: the S04 split into two sections plus the
header-alignment fix, with every prior contract carried forward and the hero unchanged."""

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
SECTION_REVIEW = ROOT / "round-14-section-review-feedback.json"
HERO_LOCK = ROOT / "round-14-feedback.json"
HERO_MOTION_REVIEW = ROOT / "hero-motion.review.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    required = (
        HTML, CSS, JS, MOBILE, SOURCE, SCHEMA, REVIEW,
        SECTION_REVIEW, HERO_LOCK, HERO_MOTION_REVIEW,
        ROOT / "round-13-feedback.json",
    )
    for path in required:
        if not path.exists():
            failures.append(f"missing Round 15 artifact: {path.relative_to(BRAND_KIT.parent)}")
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

    # --- Ten reviewable regions after the split ---
    for section_id in [f"GH-S{index:02d}" for index in range(1, 11)]:
        if f'data-review-id="{section_id}"' not in html:
            failures.append(f"missing reviewable page region: {section_id}")

    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if section_ids != [f"GH-S{index:02d}" for index in range(1, 11)]:
        failures.append(f"section ids are not the ordered GH-S01..GH-S10 sequence: {section_ids}")

    # --- The S04 split: two distinct sections ---
    if 'data-review-id="GH-S04" data-review-title="Built on ourselves first"' not in html:
        failures.append("GH-S04 must be retitled 'Built on ourselves first' after the split")
    if 'data-review-id="GH-S05" data-review-title="Operating proof"' not in html:
        failures.append("GH-S05 must be the new 'Operating proof' section")
    if 'class="operating-proof review-target"' not in html or 'id="operating-proof"' not in html:
        failures.append("the Operating proof section wrapper is missing")
    # AI OS / ecosystem / final / footer shifted down by one
    for expected in (
        'data-review-id="GH-S06" data-review-title="Available now: AI OS"',
        'data-review-id="GH-S07" data-review-title="The Mez Systems ecosystem"',
        'data-review-id="GH-S08" data-review-title="Proof from the first Mez System"',
        'data-review-id="GH-S09" data-review-title="Final route"',
        'data-review-id="GH-S10" data-review-title="Footer"',
    ):
        if expected not in html:
            failures.append(f"renumbered region missing after the split: {expected}")

    # --- Header-alignment fix on .why-head (shared by both split sections) ---
    why_head_block = re.search(r"\.why-head\s*\{([^}]*)\}", css)
    if not why_head_block:
        failures.append("the .why-head rule is missing")
    else:
        body = why_head_block.group(1)
        if "max-width: 860px" in body:
            failures.append("the .why-head max-width:860px centring (the indent bug) must be removed")
        if "align-items: flex-start" not in body:
            failures.append("the .why-head must left-align its children to the section edge")
    if ".why-head h2 { max-width: 680px; }" not in css:
        failures.append("the header measure must move onto the text (.why-head h2 cap) so alignment holds")

    # --- Locked copy carried forward (both split headings included) ---
    for phrase in (
        "The operating systems AI-native businesses run on.",
        "Too many tools. Too many middlemen.",
        "Use the best intelligence. Own the layer around it.",
        "We run Mez Studios on the systems we sell.",
        "Operating proof",
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
        "product-deck--arc", "hero-card__material", ".hero-card .material-identity",
        "tool-pile", "ownership-instrument", "method-console", "proof-record",
        "identity-event", "ecosystem-card__field", "testimonial-disc", "final-installed",
    ):
        if visual_contract not in (html + css + javascript):
            failures.append(f"carried-forward component missing in Round 15: {visual_contract}")

    # --- Hero unchanged (locked at r14/V01); the lifted fan geometry must remain ---
    for lifted_geometry in (
        "clamp(12px, 1.6vw, 24px)",
        "clamp(-80px, -5.6vw, -58px)",
        "clamp(40px, 4.6vw, 72px)",
    ):
        if lifted_geometry not in css:
            failures.append(f"locked hero fan geometry missing: {lifted_geometry}")
    for stale_geometry in ("clamp(22px, 2.6vw, 38px)", "clamp(-74px, -5.2vw, -52px)"):
        if stale_geometry in css:
            failures.append(f"stale hero fan geometry must not remain: {stale_geometry}")

    if "hero-core-layer" in (html + css + javascript):
        failures.append("collapsed hero-core-layer mount pattern must not return")
    if javascript.count("renderer.mount(material") != 1:
        failures.append("hero must mount cores directly on sized material elements in one bounded loop")
    for banned_override in ("HERO_CORE_SPEED", "surface.speed", "speedTarget", "hero-core-drift"):
        if banned_override in (javascript + css):
            failures.append(f"hero motion must stay canonical-automatic; found override: {banned_override}")
    if ".hero-card .hero-card__material::after" in css:
        failures.append("hero cards must not fork the shared material overlay (Round 11 consistency guard)")
    if "--card-outline: var(--mz-border-default)" not in css:
        failures.append("card outline must stay bound to the canonical token (Round 12)")
    if "rgba(25, 25, 25, .42)" in css:
        failures.append("the bespoke harsh card outline value must stay removed")
    hero_identity_block = re.search(r"\.hero-card \.material-identity\s*\{([^}]*)\}", css)
    if not hero_identity_block or "align-items: center" not in hero_identity_block.group(1):
        failures.append("Round 11 centred hero identity mark must remain")

    products = source.get("products", {})
    if (
        products.get("heroArrangement") != "centred-spread-deck-2-1-2-compact"
        or products.get("heroIdentityMarkAlignment") != "centred"
        or products.get("heroOcclusionAuthorised") is not True
        or products.get("cardOutlineToken") != "--mz-border-default"
    ):
        failures.append("carried-forward hero contract fields must be unchanged")

    motion = source.get("motion", {})
    if (
        motion.get("heroMotionTreatment") != "phase-a-canonical-automatic"
        or motion.get("heroRestSpeed") != 1
        or motion.get("heroHoverSpeed") != 1.85
        or motion.get("coreMountHostsIntrinsicallySized") is not True
    ):
        failures.append("canonical-automatic hero motion contract must be unchanged")
    if motion.get("eligibleSections") != ["GH-S01", "GH-S06", "GH-S09"]:
        failures.append("motion eligibleSections must track the renumber (GH-S01, GH-S06, GH-S09)")

    if len(source.get("sections", [])) != 10:
        failures.append("the section contract must list exactly ten reviewable regions")

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

    if 'candidateRevision: "golden-homepage-01-r15"' not in javascript:
        failures.append("review export does not identify the Round 15 candidate")
    if javascript.count("data-review-item") < 1 or "reviewPayload" not in javascript:
        failures.append("section-level keep/revise/kill review tooling is missing")

    heading_levels = [int(level) for level in re.findall(r"<h([1-3])(?:\s|>)", html)]
    if not heading_levels or heading_levels[0] != 1 or heading_levels.count(1) != 1:
        failures.append("homepage must contain one leading h1")

    review = read_json(REVIEW)
    if (
        review.get("verdict") != "pending"
        or review.get("candidateRevision") != "golden-homepage-01-r15"
        or review.get("productionAuthority") is not False
    ):
        failures.append("Round 15 review record must remain pending and non-production")
    if review.get("heroSectionLock", {}).get("locked") is not True:
        failures.append("the provisional GH-S01 hero lock must carry forward")

    section_review = read_json(SECTION_REVIEW)
    verdicts = {s.get("id"): s.get("verdict") for s in section_review.get("sections", [])}
    if verdicts.get("GH-S01") != "keep" or verdicts.get("GH-S04") != "revise":
        failures.append("the r14 section-review feedback trace is incomplete")

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
        print("MEZ GOLDEN HOMEPAGE ROUND 15: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GOLDEN HOMEPAGE ROUND 15: PASS")
    print("- ten reviewable regions: 'Why Mez Systems' split into 'Built on ourselves first' + 'Operating proof'")
    print("- the .why-head indent is fixed (header left-aligns with its body; the centred 860px block is gone)")
    print("- AI OS, ecosystem, proof, final route and footer renumbered; motion eligibility tracks the shift")
    print("- the locked V01 hero, centred identity, outline token, no-overlay-fork guard and canonical motion are unchanged")
    print("- honest evidence-intake and consent-pending states, compact no-swipe proof and one h1 all hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
