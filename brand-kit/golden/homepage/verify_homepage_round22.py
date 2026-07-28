#!/usr/bin/env python3
"""Verify GOLD-01 Round 22: proof rail, centred sequence and S02 copy cut.

Round 22 is intentionally bounded to Olli's 27 July review:

* GH-S08 moves directly below the locked hero and becomes a simple, static
  testimonial-proof rail using the three existing attributed review excerpts;
* GH-S04 keeps its locked workflow-sequence family, but every marker is centred
  in its grid column so the complete rail is optically centred;
* GH-S02 loses the complete two-part closing line that Olli found out of place.

Run with --self-test to mutate each owned contract in memory. This proves the
verifier fails for the regressions it claims to catch without touching the
worktree.
"""

from __future__ import annotations

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
FEEDBACK = ROOT / "round-22-feedback.json"

EXPECTED_DOM_ORDER = [
    "GH-S01", "GH-S08", "GH-S02", "GH-S03", "GH-S04",
    "GH-S05", "GH-S06", "GH-S07", "GH-S09", "GH-S10",
]
REVIEW_NAMES = ("Kayvon Jafarzadeh", "Omar Zeineddine", "Daniel Leung")
REMOVED_PROBLEM_COPY = (
    "External tools can create real value",
    "Dependency without ownership",
    "Your business needs an operating layer it controls.",
)


def validate(
    html: str,
    css: str,
    javascript: str,
    source: dict,
    review: dict,
    feedback: dict,
) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    # --- candidate identity and receipt ---
    # R23 legitimately advanced the shared candidate after the R22 contract
    # landed. The R22 receipt itself remains fixed; live source/review metadata
    # may identify either the original round or its direct successor.
    if source.get("candidateRevision") not in {"golden-homepage-01-r22", "golden-homepage-01-r23", "golden-homepage-01-r24"}:
        fail("META", "source does not identify the R22 to R24 lineage")
    if review.get("candidateRevision") not in {"golden-homepage-01-r22", "golden-homepage-01-r23", "golden-homepage-01-r24"}:
        fail("META", "review does not identify the R22 to R24 lineage")
    if feedback.get("candidateRevision") != "golden-homepage-01-r22":
        fail("META", "Round 22 feedback no longer identifies its own candidate")
    if source.get("version") not in {"0.22.0-candidate", "0.23.0-candidate", "0.24.0-candidate"}:
        fail("META", "homepage.source.json version is outside the R22 to R24 lineage")
    if not any(round_label in html for round_label in ("Round 22", "Round 23", "Round 24")) or not any(
        revision in javascript for revision in ("golden-homepage-01-r22", "golden-homepage-01-r23", "golden-homepage-01-r24")
    ):
        fail("META", "workbench title or review export predates Round 22")
    if feedback.get("productionAuthority") is not False:
        fail("META", "Round 22 feedback must remain non-production")

    # --- the review rail leads the argument directly under the hero ---
    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if section_ids != EXPECTED_DOM_ORDER:
        fail("ORDER", f"expected hero, proof, problem order; found {section_ids}")
    source_ids = [section.get("id") for section in source.get("sections", [])]
    if source_ids != EXPECTED_DOM_ORDER:
        fail("ORDER", f"source contract does not mirror DOM order: {source_ids}")

    s08_start = html.find('data-review-id="GH-S08"')
    s02_start = html.find('data-review-id="GH-S02"')
    if s08_start < 0 or s02_start < 0 or s08_start > s02_start:
        fail("ORDER", "GH-S08 must sit between the hero and GH-S02")
        s08 = ""
    else:
        s08 = html[s08_start:s02_start]

    if 'class="review-marquee__track"' not in s08:
        fail("MARQUEE", "GH-S08 is missing the testimonial-proof rail")
    if s08.count('class="review-marquee__item"') != 3:
        fail("MARQUEE", "the rail must carry exactly three real review excerpts")
    for name in REVIEW_NAMES:
        if name not in s08:
            fail("TRUTH", f"existing attributed reviewer missing: {name}")
    for retired in ("proof-voices", "proof-voice", "proof-sphere"):
        if retired in html or f".{retired}" in css:
            fail("MARQUEE", f"retired testimonial-card token remains: {retired}")
    if "Consent verification pending" not in s08:
        fail("TRUTH", "the moved reviews must retain the pending-consent state")

    marquee_css = css[css.find(".review-marquee__head"):]
    marquee_end = marquee_css.find("/* ---- R16 · final ---- */")
    marquee_css = marquee_css[:marquee_end] if marquee_end >= 0 else marquee_css
    if "grid-template-columns: repeat(3, minmax(0, 1fr))" not in marquee_css:
        fail("MARQUEE", "desktop review rail is not one simple three-part strip")
    if re.search(r"animation(?:-name)?\s*:", marquee_css):
        fail("MOTION", "MOT-04: review type or layout must not auto-move")
    if "<marquee" in html.lower():
        fail("MOTION", "deprecated moving marquee markup is forbidden")

    # --- the complete GH-S02 closing line is gone ---
    s02 = html[html.find('data-review-id="GH-S02"'):html.find('data-review-id="GH-S03"')]
    for phrase in REMOVED_PROBLEM_COPY:
        if phrase in s02:
            fail("PROBLEM-COPY", f"removed GH-S02 close returned: {phrase}")
    if "problem-close" in s02 or ".problem-close" in css:
        fail("PROBLEM-COPY", "the empty GH-S02 closing wrapper or its styling remains")

    # --- the workflow rail itself is centred, not manually offset ---
    mseq = re.search(r"\.mseq \{(.*?)\}", css, re.S)
    marker = re.search(r"\.mseq__marker \{(.*?)\}", css, re.S)
    connector = re.search(r"\.mseq li:not\(:last-child\)::before \{(.*?)\}", css, re.S)
    if not mseq or "width: min(1040px, 100%)" not in mseq.group(1) or "margin: 0 auto" not in mseq.group(1):
        fail("SEQUENCE-CENTRE", "the sequence group needs a bounded, centred width")
    if not marker or "justify-items: center" not in marker.group(1) or "width: 100%" not in marker.group(1):
        fail("SEQUENCE-CENTRE", "each marker must sit at the centre of its grid column")
    if not connector or "left: 50%" not in connector.group(1):
        fail("SEQUENCE-CENTRE", "each connector must start from its column centre")
    if "nth-last-child(2)" in css:
        fail("SEQUENCE-CENTRE", "the old left-aligned special-case connector must stay retired")

    # --- neighbours and honesty survive the bounded change ---
    # Retired in R23: Olli supplied four real operating screenshots, so the
    # honest neighbour state advanced from three evidence-intake placeholders
    # to real pixels with an explicit public-redaction gate.
    if html.count("Evidence pending") not in (0, 3):
        fail("NEIGHBOUR", "GH-S05 is neither the R22 intake state nor the R23 supplied-evidence state")
    if (
        html.count("Evidence pending") == 0
        and "Production redaction pending" not in html
        and source.get("proof", {}).get("operatingStatus") != "evidence-supplied-redaction-pending"
    ):
        fail("NEIGHBOUR", "supplied GH-S05 evidence must retain its internal redaction gate")
    for phrase in ("The operating layer is yours.", "Build the system. Rent the model."):
        if phrase not in html:
            fail("NEIGHBOUR", f"GH-S03 closing thesis changed: {phrase}")
    if html.count('data-review-id="GH-S01"') != 1 or html.count('data-review-id="GH-S10"') != 1:
        fail("NEIGHBOUR", "hero or footer review boundary changed")

    # --- scoped canon guards ---
    for banned, code in (("backdrop-filter", "MAT-01"), ("<marquee", "MOT-04")):
        if banned in html.lower() or banned in css.lower():
            fail("CANON", f"{code}: {banned} is banned")
    if "http://" in html or "http://" in css:
        fail("PORTABILITY", "http:// is forbidden in workbench artifacts")

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
    cases = (
        (
            "ORDER",
            html.replace('data-review-id="GH-S08"', 'data-review-id="GH-S18"', 1),
            css,
        ),
        (
            "PROBLEM-COPY",
            html.replace(
                "</section>\n\n<!-- GH-S03",
                "<p>External tools can create real value.</p></section>\n\n<!-- GH-S03",
                1,
            ),
            css,
        ),
        (
            "SEQUENCE-CENTRE",
            html,
            css.replace("justify-items: center;\n  width: 100%;", "justify-items: start;\n  width: 100%;", 1),
        ),
        (
            "MOTION",
            html,
            css.replace(".review-marquee__track {", ".review-marquee__track {\n  animation: drift 10s linear infinite;", 1),
        ),
        (
            "TRUTH",
            html.replace("Consent verification pending", "", 1),
            css,
        ),
    )
    misses: list[str] = []
    for expected_code, mutated_html, mutated_css in cases:
        failures = validate(mutated_html, mutated_css, javascript, source, review, feedback)
        if not any(item.startswith(f"{expected_code}:") for item in failures):
            misses.append(expected_code)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 22 SELF-TEST: FAIL")
        for code in misses:
            print(f"  - mutation was not caught: {code}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 22 SELF-TEST: PASS")
    print("- order, copy, centring, motion and truth regressions all fail in memory")
    return 0


def main() -> int:
    required = (HTML, CSS, JS, SOURCE, REVIEW, FEEDBACK)
    missing = [path for path in required if not path.exists()]
    if missing:
        print("GOLDEN HOMEPAGE ROUND 22: FAIL")
        for path in missing:
            print(f"  - missing artifact: {path.relative_to(BRAND_KIT.parent)}")
        return 1

    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)

    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 22: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("GOLDEN HOMEPAGE ROUND 22: PASS")
    print("- GH-S08 is a static testimonial-proof rail directly below the hero")
    print("- GH-S04 marker centres are symmetric around the page axis")
    print("- the complete out-of-place GH-S02 close is removed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
