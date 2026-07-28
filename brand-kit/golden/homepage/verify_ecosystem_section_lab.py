#!/usr/bin/env python3
"""Verify the bounded GH-S07 expression-led product-family lab."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
LAB = BRAND_KIT / "workbench" / "golden" / "homepage" / "s07-ecosystem-lab"
HTML = LAB / "index.html"
CSS = LAB / "styles.css"
JS = LAB / "lab.js"
MOBILE = LAB / "mobile-proof.html"


def main() -> int:
    failures: list[str] = []
    for path in (HTML, CSS, JS, MOBILE):
        if not path.exists():
            failures.append(f"missing {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        print("ECOSYSTEM SECTION LAB: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    javascript = JS.read_text(encoding="utf-8")

    ids = re.findall(r'id: "(V\d{2})"', javascript)
    layouts = re.findall(r'layout: "([^"]+)"', javascript)
    if ids != ["V01", "V02", "V03", "V04", "V05"]:
        failures.append(f"expected V01-V05 exactly once; found {ids}")
    if len(layouts) != 5 or len(set(layouts)) != 5:
        failures.append("the five variants must use five distinct composition families")

    required_copy = (
        "Coming next",
        "Specialised systems for the work AI-native businesses do.",
        "Coming soon",
    )
    for required in required_copy:
        if required not in javascript:
            failures.append(f"missing locked section or product copy: {required}")

    if "registry/products.json" not in javascript:
        failures.append("lab does not read the canonical product registry")
    if "gradient-library/assets/static" not in javascript or "const twin" not in javascript:
        failures.append("lab does not resolve exact static twins from canonical IDs")
    if "wings.svg" not in javascript:
        failures.append("canonical Wings are missing")
    for shape in ('"disc"', '"sphere"', '"wings"'):
        if shape not in javascript:
            failures.append(f"missing requested expression shape: {shape}")
    if "mountLivingCores" not in javascript or "let activeHost = null" not in javascript:
        failures.append("shared one-live renderer allocation is missing")
    if "unmountActive()" not in javascript or "renderer.surfaces?.delete(activeHost)" not in javascript:
        failures.append("hover-live cleanup contract is missing")
    if "prefers-reduced-motion: reduce" not in javascript or "forceStatic" not in javascript:
        failures.append("reduced-motion exact-static allocation is missing")

    for banned in ("box-shadow", "backdrop-filter", "perspective", "linear-gradient"):
        if banned in css:
            failures.append(f"banned treatment present: {banned}")
    if "#1b1b19" in css or "eco-stage" in css:
        failures.append("the rejected combined dark stage is present")
    if "@media (max-width: 720px)" not in css or "grid-template-columns: 1fr" not in css:
        failures.append("compact single-column contract is missing")
    if "homepage untouched" not in html:
        failures.append("lab does not disclose its non-canonical isolation boundary")

    if failures:
        print("ECOSYSTEM SECTION LAB: FAIL")
        print("\n".join(f"- {item}" for item in failures))
        return 1

    print("ECOSYSTEM SECTION LAB: PASS")
    print("- five expression-led compositions are present")
    print("- the rejected combined dark stage is absent")
    print("- canonical registry data, exact static twins and canonical Wings are used")
    print("- one shared renderer mounts only the hovered or focused expression")
    print("- current Golden Homepage GH-S07 remains untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
