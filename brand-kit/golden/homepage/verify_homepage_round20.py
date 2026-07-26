#!/usr/bin/env python3
"""Verify the GOLD-01 Round 20 candidate: GH-S03 rebuilt as the concentric orbit.

Round 20 replaces the R17 authored-split-card treatment of GH-S03 with the
composition Olli selected from principle-lab-8 variant A:

  * three radii of one object, not three stacked bands: business connections on
    the outer ring, harnesses on the inner, the product core at the centre;
  * two registers of third-party mark, because a harness is not a plugin;
  * the core mounted as a canonical disc expression;
  * the core cycling every product in the registry, cross-faded through the exact
    static twins so only one WebGL context ever exists;
  * the grey-prefix heading gone, matching the correction already made in S02.

S04 kept the shared split-card family at the time of this round. Those rules were rebuilt
because the previous S03 block owned them and this workbench is untracked, so
this file guards them against a second loss.
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
JS = WORKBENCH / "homepage.js"
MARKS = BRAND_KIT / "assets" / "third-party-marks" / "registry.json"


def report(failures: list[str]) -> int:
    if failures:
        print("GOLDEN HOMEPAGE ROUND 20: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 20: PASS")
    print("- GH-S03 rebuilt as the concentric orbit (principle-lab-8 variant A)")
    print("- two mark registers, disc core, product cycle across the static twins")
    return 0


def main() -> int:
    failures: list[str] = []
    for path in (HTML, CSS, JS, MARKS):
        if not path.exists():
            failures.append(f"missing Round 20 artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return report(failures)

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    javascript = JS.read_text(encoding="utf-8")

    section_ids = re.findall(r'data-review-id="(GH-S\d{2})"', html)
    if section_ids != [f"GH-S{n:02d}" for n in range(1, 11)]:
        failures.append(f"section order changed: {section_ids}")

    s03 = html[html.index('data-review-id="GH-S03"'):html.index('data-review-id="GH-S04"')]

    # --- the orbit ---
    for token in ("conc__ring--outer", "conc__ring--inner", "conc__core", "conc__veil"):
        if f".{token}" not in css:
            failures.append(f"orbit part missing from CSS: .{token}")
    for token in ('data-orbit="connections"', 'data-orbit="harnesses"'):
        if token not in s03:
            failures.append(f"orbit ring missing from S03 markup: {token}")
    if 'data-core-shape="disc"' not in s03:
        failures.append("the S03 core must mount as a canonical disc expression")

    # Counter-rotation must be the base transform, not only the animation's first
    # keyframe, or every mark sits tilted under reduced motion.
    upright = re.search(r"\.conc__upright \{(.*?)\}", css, re.S)
    if not upright:
        failures.append("missing .conc__upright rule")
    elif "transform: rotate(calc(var(--a) * -1))" not in upright.group(1):
        failures.append("mark counter-rotation must be a base transform, not only a keyframe")

    # A percentage inset resolves per axis and collapses the disc to an ellipse.
    core = re.search(r"\.conc__core \{(.*?)\}", css, re.S)
    if core and "aspect-ratio: 1" not in core.group(1):
        failures.append("the core must be squared by aspect-ratio, not by a percentage inset")

    # --- two registers of mark ---
    for register in (".conc__mark--harness", ".conc__mark--tool"):
        if register not in css:
            failures.append(f"mark register missing: {register}")

    # Every mark used must be a freestanding symbol in the registry.
    registry = json.loads(MARKS.read_text(encoding="utf-8"))
    symbols = {b["slug"] for b in registry["brands"] if b.get("form") == "symbol"}
    used = set(re.findall(r'\["([a-z0-9-]+)",\s*"[^"]+"\]', javascript))
    known = {b["slug"] for b in registry["brands"]}
    for slug in sorted(used & known):
        if slug not in symbols:
            failures.append(f"{slug} is not form:symbol and must not sit in a ring of peers")

    # --- the product cycle ---
    if "renderer.setCore" not in javascript:
        failures.append("the product cycle must swap the mounted core, not remount it")
    if "conc__veil" not in javascript:
        failures.append("the cycle must cross-fade through the static twin")
    if re.search(r"\bmountLivingCore\b(?!s)", javascript):
        failures.append("MOT-01: mountLivingCore creates a second WebGL context")

    # --- removals ---
    if "head-quiet" in s03:
        failures.append("S03 must not use the grey-prefix heading")
    for dead in ("intel-slot", "intel-spine", "intel-base", "intel-diagram"):
        if dead in html or dead in css:
            failures.append(f"retired R17 S03 token still present: {dead}")

    # --- RETIRED at R21 -------------------------------------------------
    # This round guarded the shared split-card family because replacing the
    # neighbouring section had already deleted it once while GH-S04 still
    # consumed it. At R21 GH-S04 was rebuilt as the horizontal sequence and the
    # family lost its last consumer, so those rules were removed deliberately
    # rather than by accident. The guard's premise is gone; every other check in
    # this round still holds and still runs.

    # --- the thesis block S03 closes on ---
    for part in (".principle-thesis", ".thesis-serif", ".thesis-close"):
        if part not in css:
            failures.append(f"principle thesis style missing: {part}")

    # --- canon guards ---
    if "http://" in html or "http://" in css:
        failures.append("http:// is banned in the workbench")
    if "backdrop-filter" in css:
        failures.append("MAT-01: backdrop-filter is banned")
    if "—" in s03:
        failures.append("em dash found in the GH-S03 region (CPY-05)")

    return report(failures)


if __name__ == "__main__":
    raise SystemExit(main())
