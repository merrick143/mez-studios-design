#!/usr/bin/env python3
"""Verify the GOLD-01 Round 19 candidate: GH-S02 rebuilt as the staircase.

Round 19 replaces the R17 authored-split-card treatment of GH-S02 with the
stepped stack selected by Olli across problem-lab-5 through problem-lab-8:

  * two columns, head left and treads right (lab 7 variant C);
  * equal-width treads that step sideways, so the stack reads as strata rather
    than tapering to a point;
  * the weight ramp Olli kept, on the charcoal ramp and never pure black;
  * the business tread on an ink hairline instead of the mid-grey one;
  * the grey-prefix heading removed from S02, so both sentences sit in the ink.

S03 and S04 kept the R17 split-card family at the time of this round. That guard is
drops from three to two. Everything R17 proved outside S02 is carried forward by
verify_homepage_round17.py, which stays as that round's record.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "golden" / "homepage"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
FEEDBACK = ROOT / "round-18-feedback.json"

TREADS = (
    "Your business",
    "Another subscription",
    "Another interface",
    "Another app",
    "Another login",
)


def report(failures: list[str]) -> int:
    if failures:
        print("GOLDEN HOMEPAGE ROUND 19: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 19: PASS")
    print("- GH-S02 rebuilt as the stepped stack (lab 8 variant A)")
    print("- equal-width treads, weight ramp, ink business tread, no grey prefix")
    return 0


def main() -> int:
    failures: list[str] = []
    for path in (HTML, CSS, FEEDBACK):
        if not path.exists():
            failures.append(f"missing Round 19 artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return report(failures)

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")

    # --- the surviving reviewable regions still exist ---
    # RETIRED AT R22: the DOM-order premise expired when Olli moved GH-S08
    # directly under the hero as a review marquee. IDs remain stable logical
    # review handles, so this historical round now guards presence/uniqueness.
    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    # UPDATED AT R25: the duplicate closing route was moved into GH-S06 and
    # removed from above the footer, so GH-S10 retired and the footer is GH-S09.
    expected = [f"GH-S{n:02d}" for n in range(1, 10)]
    if len(section_ids) != 9 or set(section_ids) != set(expected):
        failures.append(f"section IDs changed or duplicated: {section_ids}")

    # --- S02 is the staircase ---
    for token in ("problem-layout", "problem-steps", "step-row--you", "step-row--layer"):
        if token not in html:
            failures.append(f"S02 staircase missing from markup: {token}")
        if f".{token}" not in css:
            failures.append(f"S02 staircase missing from CSS: .{token}")

    for tread in TREADS:
        if f'<span class="step-role">{tread}</span>' not in html:
            failures.append(f"S02 tread missing or renamed: {tread}")

    if html.count('class="step-row') != 5:
        failures.append(f"S02 must carry exactly five treads, found {html.count('class=\"step-row')}")

    # Equal-width treads: the tapering behaviour was rejected in lab 7 variant D.
    if "width: calc(100% - (var(--step) * 4))" not in css:
        failures.append("treads must be equal width less the total travel, not tapering")
    for offset in range(1, 5):
        if f".step-o{offset} {{ margin-left: calc(var(--step) * {offset}); }}" not in css:
            failures.append(f"missing tread offset step-o{offset}")

    # The weight ramp Olli kept, on the charcoal ramp only.
    for ramp in ("step-w1", "step-w2", "step-w3", "step-w4"):
        if f".{ramp}" not in css:
            failures.append(f"weight ramp step missing: .{ramp}")
    if "#3b3b38" not in css:
        failures.append("weight ramp must open on the #3b3b38 charcoal step")

    # The business tread is definite, not mid grey.
    match = re.search(r"\.step-row--you \{(.*?)\}", css, re.S)
    if not match:
        failures.append("missing .step-row--you rule")
    elif "var(--page-ink)" not in match.group(1):
        failures.append("business tread must sit on an ink border, not the mid-grey one")

    # --- the removals Olli asked for ---
    s02 = html[html.index('data-review-id="GH-S02"'):html.index('data-review-id="GH-S03"')]
    if "head-quiet" in s02:
        failures.append("S02 must not use the grey-prefix heading")
    for dead in ("frag-field", "frag-void", "frag-node", "problem-consequence"):
        if dead in html or dead in css:
            failures.append(f"retired R17 S02 token still present: {dead}")

    # --- RETIRED at R21 -------------------------------------------------
    # This round guarded the shared split-card family because replacing the
    # neighbouring section had already deleted it once while GH-S04 still
    # consumed it. At R21 GH-S04 was rebuilt as the horizontal sequence and the
    # family lost its last consumer, so those rules were removed deliberately
    # rather than by accident. The guard's premise is gone; every other check in
    # this round still holds and still runs.

    # --- canon guards ---
    if "http://" in html or "http://" in css:
        failures.append("http:// is banned in the workbench")
    for banned, rule in (("backdrop-filter", "MAT-01"), ("#000000", "COL-05")):
        if banned in css:
            failures.append(f"{rule}: {banned} is banned")
    # CPY-05 is scoped to the region this round owns. Em dashes elsewhere in the
    # page are pre-existing approved copy in S03/S04/S06 and are logged as a
    # standing defect rather than silently rewritten by an S02 round.
    if "—" in s02:
        failures.append("em dash found in the GH-S02 region (CPY-05)")
    # MOT-01 cannot be counted in static markup: homepage.js stamps and clears
    # data-mz-core at runtime. What is checkable statically is that the page uses
    # the shared-renderer pattern, which is what keeps the count at one.
    javascript = (WORKBENCH / "homepage.js").read_text(encoding="utf-8")
    if "mountLivingCores" not in javascript:
        failures.append("MOT-01: page must use the shared mountLivingCores renderer")
    if re.search(r"\bmountLivingCore\b(?!s)", javascript):
        failures.append("MOT-01: mountLivingCore creates a second WebGL context")
    if "problem-steps" in css and "data-mz-core" in html[html.index('data-review-id="GH-S02"'):html.index('data-review-id="GH-S03"')]:
        failures.append("S02 is a still: it must not declare a live core")

    # --- the round record exists and is honest about its status ---
    feedback = json.loads(FEEDBACK.read_text(encoding="utf-8"))
    if feedback.get("productionAuthority") is not False:
        failures.append("round-18-feedback.json must not claim production authority")

    return report(failures)


if __name__ == "__main__":
    raise SystemExit(main())
