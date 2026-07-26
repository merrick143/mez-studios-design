#!/usr/bin/env python3
"""Verify the GOLD-01 Round 21 candidate: GH-S04 rebuilt as the sequence.

Round 21 replaces the R17 authored-split-card treatment of GH-S04, and the
five-step console inside it, with the composition Olli locked:

  * a horizontal workflow sequence, because GH-S02 owns the vertical staircase
    and repeating it two sections later fails the repetition test;
  * four charcoal dots and one small material disc, all on one baseline, so the
    terminus is the last step rather than a different kind of object;
  * exactly one colour event in the section, on the thing that ships;
  * a blend between two live cores rather than a fade through a static twin,
    because a still frame in the middle of the transition is what reads as a
    freeze.

Two guards here exist because of mistakes already made in this file's history.
The R21 rewrite deleted GH-S03's closing thesis along with the S04 block, the
same class of regression Round 20 was written to catch, so the thesis is checked
again from this round. And the connector is checked for a colour token that
actually resolves on this page: it was first written against --page-line-strong,
which this stylesheet does not define, so the line rendered fully transparent
while every geometric measurement passed.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "golden" / "homepage"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
JS = WORKBENCH / "homepage.js"

STAGES = ("Build", "Run", "Break", "Refine", "Package")


def report(failures: list[str]) -> int:
    if failures:
        print("GOLDEN HOMEPAGE ROUND 21: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 21: PASS")
    print("- GH-S04 rebuilt as the horizontal sequence")
    print("- four charcoal dots, one small material disc, one colour event")
    print("- the blend runs live core to live core, never through a still")
    print("- GH-S03's thesis and the neighbouring sections are intact")
    return 0


def main() -> int:
    failures: list[str] = []
    for path in (HTML, CSS, JS):
        if not path.exists():
            failures.append(f"missing Round 21 artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return report(failures)

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    javascript = JS.read_text(encoding="utf-8")

    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if section_ids != [f"GH-S{n:02d}" for n in range(1, 11)]:
        failures.append(f"section order changed: {section_ids}")

    s04 = html[html.index('data-review-id="GH-S04"'):html.index('data-review-id="GH-S05"')]

    # --- the composition ---
    if 'class="mseq"' not in s04:
        failures.append("GH-S04 must carry the sequence")
    for stage in STAGES:
        if f"<strong>{stage}</strong>" not in s04:
            failures.append(f"sequence stage missing: {stage}")
    dots = s04.count('class="mseq__dot"')
    if dots != 4:
        failures.append(f"expected four charcoal dots, found {dots}")
    if s04.count("data-sequence-core") != 1:
        failures.append("exactly one marker carries material")
    if s04.count('class="mseq__core"') != 2:
        failures.append("the terminus needs two core layers to blend between")

    # --- the retired treatment ---
    for dead in ("split-card", "method-loop", "method-step", "method-return", "method-line"):
        if dead in s04:
            failures.append(f"retired R17 S04 token still present in the section: {dead}")
    if "data-method-sequence" in javascript:
        failures.append("the five-step console script outlived the markup it drove")

    # --- geometry that only holds if it is derived, not typed ---
    if "--mseq-disc" not in css or "--mseq-dot" not in css:
        failures.append("the marker sizes must be variables the connector can be derived from")
    if "nth-last-child(2)" not in css:
        failures.append("the last connector must be sized for the disc, not for a dot")
    if "var(--mseq-disc) / 2" not in css:
        failures.append("the connector must reach the disc centre from the same variable that sizes it")

    # The connector was first written against a token this page does not define,
    # so it rendered transparent while every measurement still passed.
    connector = re.search(r"\.mseq li:not\(:last-child\)::before \{(.*?)\}", css, re.S)
    if not connector:
        failures.append("missing the .mseq connector rule")
    else:
        colour = re.search(r"background:\s*([^;]+);", connector.group(1))
        if not colour:
            failures.append("the connector has no colour")
        else:
            for token in re.findall(r"var\((--[a-z0-9-]+)", colour.group(1)):
                if f"{token}:" not in css and "--mz-" not in token:
                    failures.append(f"the connector uses {token}, which this stylesheet never defines")

    # --- MOT-03: never mount on an absolutely positioned empty layer ---
    core_rule = re.search(r"\.mseq__core \{(.*?)\}", css, re.S)
    if core_rule and "position: absolute" in core_rule.group(1):
        failures.append("MOT-03: mount() stamps position:relative and would collapse an absolute core layer")
    if core_rule and "grid-area" not in core_rule.group(1):
        failures.append("the two core layers must stack in a grid cell, not by positioning")

    # --- the blend ---
    if "advanceSequence" not in javascript:
        failures.append("the terminus must blend rather than cut")
    if "staticTwin" in javascript and "veil" in javascript.lower() and "sequence" in javascript.lower():
        if re.search(r"sequenceVeil|sequence.*veil", javascript, re.I):
            failures.append("the sequence must not fade through a static twin; that is the freeze")
    if re.search(r"\bmountLivingCore\b(?!s)", javascript):
        failures.append("MOT-01: mountLivingCore creates a second WebGL context")
    if "productGradients" not in javascript:
        failures.append("LAY-09: the blend must read gradients from the canonical registry")
    for hardcoded in ("MZ-G13", "MZ-G12", "MZ-G06"):
        if f'"{hardcoded}"' in javascript:
            failures.append(f"LAY-09: {hardcoded} is hardcoded rather than read from the registry")

    # --- the neighbours this rewrite could have damaged ---
    for part in (".principle-thesis", ".thesis-serif", ".thesis-close"):
        if part not in css:
            failures.append(f"GH-S03 thesis style lost to the S04 rewrite: {part}")
    for part in (".problem-layout", ".step-row"):
        if part not in css:
            failures.append(f"GH-S02 staircase style lost to the S04 rewrite: {part}")
    if 'class="conc"' not in html:
        failures.append("GH-S03's concentric orbit lost to the S04 rewrite")

    # --- canon guards ---
    if "http://" in html or "http://" in css:
        failures.append("http:// is banned in the workbench")
    if "backdrop-filter" in css:
        failures.append("MAT-01: backdrop-filter is banned")
    mseq_css = css[css.index(".mseq {"):] if ".mseq {" in css else ""
    if "box-shadow" in mseq_css[:mseq_css.find("@media")] if mseq_css else False:
        failures.append("MAT-03: the sequence carries no shadow")

    return report(failures)


if __name__ == "__main__":
    raise SystemExit(main())
