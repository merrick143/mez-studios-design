#!/usr/bin/env python3
"""Validate the approved, non-canonical product architecture record."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
EXPECTED_ASSIGNMENTS = {
    "AI OS": "MZ-G13",
    "Context Engine": "MZ-G12",
    "AI Ads System": "MZ-G06",
    "Claude Code OS": "MZ-G15",
    "Organic Content OS": "MZ-G20",
}


def main() -> int:
    failures: list[str] = []
    required = [HERE / name for name in ("manifest.json", "review.json", "index.html", "styles.css", "app.js")]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty: {path.name}")

    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    review = json.loads((HERE / "review.json").read_text(encoding="utf-8"))
    if manifest.get("studyId") != "MEZ-PRODUCT-ARCHITECTURE-GRADIENT-ASSIGNMENT-01":
        failures.append("unexpected study ID")
    if manifest.get("status") != "human-review-complete-approved":
        failures.append("product architecture gate must be approved")
    if manifest.get("productionAuthority") is not False or manifest.get("mutatesCanonicalAuthority") is not False:
        failures.append("approved review must remain non-canonical until cutover")
    if manifest.get("finishProfile") != "deep":
        failures.append("Deep Mineral must be the approved finish")

    products = manifest.get("products", [])
    assignments = {row.get("publicName"): row.get("gradientId") for row in products}
    if assignments != EXPECTED_ASSIGNMENTS:
        failures.append(f"approved assignment drift: {assignments}")
    ids = [row.get("productId") for row in products]
    if len(products) != 5 or len(ids) != len(set(ids)) or any(not value for value in ids):
        failures.append("five unique stable product IDs are required")

    library = json.loads((BRAND_KIT / "gradient-library/library-manifest.json").read_text(encoding="utf-8"))
    active = set(library.get("activeIds", []))
    if not set(assignments.values()) <= active:
        failures.append("approved assignments must use active source-backed gradients")

    if review.get("verdict") != "approve" or review.get("complete") is not True:
        failures.append("tracked review must be complete and approved")
    if review.get("productionAuthority") is not False or review.get("sourceExpressionApproved") is not True:
        failures.append("review must approve the source expressions without claiming cutover authority")
    if review.get("historicalNames") != [] or manifest.get("namingPolicy") != "Use literal public product names. Aurora, Forge and Prism are not product names, aliases or active migration keys.":
        failures.append("literal-name-only policy must remove every historical alias")
    review_assignments = {row.get("publicName"): row.get("gradientId") for row in review.get("products", [])}
    if review_assignments != EXPECTED_ASSIGNMENTS:
        failures.append("review and manifest assignments disagree")

    html = (HERE / "index.html").read_text(encoding="utf-8")
    app = (HERE / "app.js").read_text(encoding="utf-8")
    visible_text = html + app
    for retired in ("Aurora", "Forge", "Prism", "Historical names"):
        if retired in visible_text:
            failures.append(f"active review still exposes retired naming: {retired}")
    for phrase in ("Five products.", "One clean handover.", "Human gate closed", "The identity kernel"):
        if phrase not in html:
            failures.append(f"approved page missing: {phrase}")
    if "mountLivingCores" not in app or "data-mz-core" not in app:
        failures.append("approved record must use the shared Living Core renderer")

    if failures:
        print("PRODUCT ARCHITECTURE REVIEW: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PRODUCT ARCHITECTURE REVIEW: PASS")
    print("- literal five-product family with zero historical aliases")
    print("- MZ-G13 / G12 / G06 / G15 / G20 assignments approved")
    print("- exact sources, Deep Mineral motion and tracked review agree")
    print("- production authority remains unchanged until cutover")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
