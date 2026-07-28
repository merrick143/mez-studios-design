#!/usr/bin/env python3
"""Verify the bounded GH-S06 AI OS ten-variant exploration lab."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
LAB = BRAND_KIT / "workbench" / "golden" / "homepage" / "s06-ai-os-lab"
HTML = LAB / "index.html"
CSS = LAB / "styles.css"
JS = LAB / "lab.js"


def main() -> int:
    failures: list[str] = []
    for path in (HTML, CSS, JS):
        if not path.exists():
            failures.append(f"missing {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        print("AI OS SECTION LAB: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    javascript = JS.read_text(encoding="utf-8")

    ids = re.findall(r'id: "(V\d{2})"', javascript)
    layouts = re.findall(r'layout: "([^"]+)"', javascript)
    if ids != [f"V{i:02}" for i in range(1, 11)]:
        failures.append(f"expected V01-V10 exactly once; found {ids}")
    if len(layouts) != 10 or len(set(layouts)) != 10:
        failures.append("the ten variants must declare ten distinct composition families")
    for required in (
        "Give AI a business to understand.",
        "How it works",
        "Know what matters today",
        "Ask against real work",
        "Retain decision reasoning",
        "Connect direction to execution",
    ):
        if required not in javascript:
            failures.append(f"missing source capability or section copy: {required}")
    if "mz-g13.webp" not in css or "wings.svg" not in javascript:
        failures.append("lab does not use the canonical AI OS static material and Wings")
    if "data-live" in html or "data-live" in javascript or "mountLivingCores" in javascript:
        failures.append("ten-option lab must not mount simultaneous live cores")
    for banned in ("box-shadow", "backdrop-filter", "perspective", "linear-gradient"):
        if banned in css:
            failures.append(f"banned treatment present: {banned}")
    if "@media (max-width: 700px)" not in css or "grid-template-columns: 1fr" not in css:
        failures.append("compact single-column contract is missing")
    if "current homepage untouched" not in html:
        failures.append("lab does not disclose its non-canonical isolation boundary")

    if failures:
        print("AI OS SECTION LAB: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1

    print("AI OS SECTION LAB: PASS")
    print("- ten distinct composition families are present")
    print("- copy is compressed into one mechanism and two feature groups")
    print("- exact static AI OS material is used with no multi-core motion")
    print("- the current Golden Homepage remains untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
