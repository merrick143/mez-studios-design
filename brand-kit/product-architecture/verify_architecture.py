#!/usr/bin/env python3
"""Validate the non-canonical product architecture review surface."""

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent


def main() -> int:
    failures: list[str] = []
    required = [HERE / name for name in ("manifest.json", "index.html", "styles.css", "app.js")]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty: {path.name}")

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("studyId") != "MEZ-PRODUCT-ARCHITECTURE-GRADIENT-ASSIGNMENT-01":
        failures.append("unexpected study ID")
    if manifest.get("productionAuthority") is not False or manifest.get("mutatesCanonicalAuthority") is not False:
        failures.append("review surface must remain non-canonical")
    if manifest.get("finishProfile") != "deep":
        failures.append("Deep Mineral must be the review finish")

    products = manifest.get("products", [])
    if len(products) != 5:
        failures.append("the review must contain exactly five products")
    names = [row.get("publicName") for row in products]
    expected_names = ["AI OS", "Context Engine", "AI Ads System", "Claude Code OS", "Organic Content OS"]
    if names != expected_names:
        failures.append(f"unexpected public roster: {names}")
    ids = [row.get("productId") for row in products]
    if len(ids) != len(set(ids)) or any(not value for value in ids):
        failures.append("stable product IDs must be present and unique")

    library = json.loads((BRAND_KIT / "gradient-library/library-manifest.json").read_text(encoding="utf-8"))
    active = set(library.get("activeIds", []))
    for product in products:
        options = product.get("gradientOptions", [])
        option_ids = {option.get("id") for option in options}
        if product.get("recommendedGradient") not in option_ids:
            failures.append(f"{product.get('publicName')} recommendation missing from options")
        if not option_ids <= active:
            failures.append(f"{product.get('publicName')} uses inactive or unknown gradient IDs")
    context = next((row for row in products if row.get("publicName") == "Context Engine"), {})
    if len(context.get("gradientOptions", [])) < 5 or context.get("recommendedGradient") != "MZ-G01":
        failures.append("Context Engine must show five source-backed choices with MZ-G01 recommended")

    legacy = manifest.get("legacyMappings", [])
    if [row.get("legacyName") for row in legacy] != ["Aurora", "Forge", "Prism"]:
        failures.append("legacy mapping set must be Aurora, Forge and Prism")
    if len(legacy) != 3:
        failures.append("exactly three legacy mappings are required")

    html = (HERE / "index.html").read_text(encoding="utf-8")
    app = (HERE / "app.js").read_text(encoding="utf-8")
    for phrase in ("Five products.", "One clean handover.", "Zero production authority", "One export closes the human gate"):
        if phrase not in html:
            failures.append(f"review page missing: {phrase}")
    if "mountLivingCores" not in app or "data-mz-core" not in app:
        failures.append("review must use the shared Living Core renderer")
    if "/api/product-architecture-decisions" not in app:
        failures.append("review must save through the isolated decision endpoint")

    if failures:
        print("PRODUCT ARCHITECTURE REVIEW: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PRODUCT ARCHITECTURE REVIEW: PASS")
    print("- five public products and stable machine IDs")
    print("- source-backed gradient choices under Deep Mineral")
    print("- historical Aurora, Forge and Prism disposition")
    print("- one shared renderer and zero production authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
