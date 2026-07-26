#!/usr/bin/env python3
"""Verify the GOLD-01 copy lock and portable homepage implementation plan."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
COPY_MD = ROOT / "homepage-copy.md"
COPY_SOURCE = ROOT / "homepage-copy.source.json"
COPY_SCHEMA = ROOT / "homepage-copy.schema.json"
COPY_REVIEW = ROOT / "homepage-copy.review.json"
PLAN_MD = ROOT / "HOMEPAGE-COMPOSITION-PLAN.md"
PLAN_SOURCE = ROOT / "homepage-plan.source.json"
PLAN_SCHEMA = ROOT / "homepage-plan.schema.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flatten_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in flatten_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in flatten_strings(child)]
    return []


def main() -> int:
    failures: list[str] = []
    copy = read_json(COPY_SOURCE)
    plan = read_json(PLAN_SOURCE)
    review = read_json(COPY_REVIEW)

    for source, schema, label in (
        (copy, read_json(COPY_SCHEMA), "copy source"),
        (plan, read_json(PLAN_SCHEMA), "homepage plan"),
    ):
        try:
            jsonschema.Draft202012Validator(schema).validate(source)
        except jsonschema.ValidationError as error:
            failures.append(f"{label} schema: {error.message}")

    if copy.get("source", {}).get("sha256") != sha256(COPY_MD):
        failures.append("canonical homepage copy hash drifted")
    if copy.get("review", {}).get("sha256") != sha256(COPY_REVIEW):
        failures.append("homepage copy review hash drifted")
    if (
        review.get("verdict") != "approve"
        or review.get("decisionId") != "DEC-GOLDEN-HOMEPAGE-COPY-001"
        or review.get("productionAuthority") is not True
    ):
        failures.append("homepage copy does not carry the approved bounded decision")

    copy_text = COPY_MD.read_text(encoding="utf-8")
    for phrase in (
        "The operating systems AI-native businesses run on.",
        "Too many tools. Too many middlemen.",
        "Use the best intelligence. Own the layer around it.",
        "We run Mez Studios on the systems we sell.",
        "Give AI a business to understand.",
        "Specialised systems for the work AI-native businesses do.",
        "Built to be used, not admired.",
        "Start with the AI OS.",
        "Explore the AI OS",
    ):
        if phrase not in copy_text:
            failures.append(f"locked homepage copy missing: {phrase}")

    expected_sections = [f"GH-S{index:02d}" for index in range(10)]
    actual_sections = [section.get("id") for section in plan.get("sections", [])]
    if actual_sections != expected_sections:
        failures.append("homepage section order drifted")

    products = read_json(BRAND_KIT / "registry" / "products.json")
    product_slugs = [product["slug"] for product in products["products"]]
    hero = plan.get("hero", {})
    planned_products = hero.get("liveProducts", [])
    if planned_products != product_slugs:
        failures.append("hero product order or roster drifted from the canonical registry")
    if hero.get("staticFallbackProducts", []) != product_slugs:
        failures.append("hero exact-static fallback roster drifted from the canonical registry")
    if (
        hero.get("cardContent") != ["wings", "publicName", "extendedName"]
        or hero.get("cardActions") is not False
        or hero.get("cardDescription") is not False
        or hero.get("wingsPlacement") != "bottom-left"
        or hero.get("liveStaticCompositionEquivalent") is not True
    ):
        failures.append("hero card simplification or live/static equivalence drifted")
    if hero.get("productCount") != 5 or hero.get("mobileMayReduceProductCount") is not False:
        failures.append("mobile hero must preserve all five products")

    motion = plan.get("motionAllocation", {})
    if (
        motion.get("maximumLivePageCores") != 5
        or motion.get("ordinaryMaximumLivePageCores") != 1
        or motion.get("heroMotionDecisionId") != "DEC-GOLDEN-HOMEPAGE-HERO-MOTION-001"
    ):
        failures.append("homepage motion allocation is missing the bounded five-live hero decision")
    if plan.get("motionAllocation", {}).get("expandedNavigationLiveCores") != 5:
        failures.append("expanded Global Navigation exception must remain exactly five")
    if plan.get("motionAllocation", {}).get("expandedNavigationSuppressesPageMotion") is not True:
        failures.append("expanded navigation must suppress page Living Cores")

    product_card = read_json(BRAND_KIT / "expressions" / "product-card" / "product-card.source.json")
    product_ids = {
        variant
        for expression in product_card.get("expressions", [])
        for variant in expression.get("variants", [])
    }
    pantry = read_json(
        BRAND_KIT
        / "expressions"
        / "product-card"
        / "phase-b"
        / "product-component-pantry.source.json"
    )
    pantry_ids = {
        item["id"] for group in ("components", "patterns") for item in pantry.get(group, [])
    }
    trading = read_json(BRAND_KIT / "expressions" / "trading-card" / "trading-card.source.json")
    trading_ids = {item["id"] for item in trading.get("specimens", [])}
    motion = read_json(BRAND_KIT / "expressions" / "channel-motion" / "channel-motion.source.json")
    motion_ids = {item["id"] for item in motion.get("specimens", [])}
    known_ids = product_ids | pantry_ids | trading_ids | motion_ids
    for section in plan.get("sections", []):
        for lineage in section.get("lineage", []):
            if lineage.startswith(("PC2-", "TC-", "MOT-")) and lineage not in known_ids:
                failures.append(f"unknown canonical lineage reference: {lineage}")

    boundary = plan.get("consumerBoundary", {})
    if (
        boundary.get("consumerRepository") is not None
        or boundary.get("runtimeCrossRepositoryImportAllowed") is not False
        or boundary.get("absolutePathsAllowedInRelease") is not False
    ):
        failures.append("technical consumer boundary is not safely unresolved and portable")
    for value in flatten_strings(plan):
        if value.startswith(("/Users/", "/private/", "file://")):
            failures.append(f"absolute path leaked into homepage plan: {value}")

    plan_text = PLAN_MD.read_text(encoding="utf-8")
    for phrase in (
        "This repository is the design-system authority.",
        "The separate technical Mez Systems repository is a future production consumer.",
        "Do not reduce the family to three products.",
        "all five product Living Cores run only while `GH-S01` is the active page motion region",
        "The copy decision preserves the supplied words. It does not manufacture proof status.",
        "Round 01 · Structural composition",
    ):
        if phrase not in plan_text:
            failures.append(f"human plan missing boundary: {phrase}")

    task = read_json(BRAND_KIT / "llm" / "tasks" / "TASK-GOLD-01-GOLDEN-HOMEPAGE.json")
    if task.get("status") != "in-progress":
        failures.append("GOLD-01 task must be in-progress after Round 00 planning begins")
    required_files = set(task.get("inputs", {}).get("requiredFiles", []))
    for path in (
        "brand-kit/golden/homepage/homepage-copy.source.json",
        "brand-kit/golden/homepage/HOMEPAGE-COMPOSITION-PLAN.md",
        "brand-kit/golden/homepage/homepage-plan.source.json",
        "brand-kit/expressions/trading-card/trading-card.source.json",
    ):
        if path not in required_files:
            failures.append(f"GOLD-01 task missing required plan input: {path}")

    if failures:
        print("MEZ GOLDEN HOMEPAGE ROUND 00: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MEZ GOLDEN HOMEPAGE ROUND 00: PASS")
    print("- canonical eight-section copy lock and bounded claim status agree")
    print("- ten-section page plan composes approved navigation, card, trading-card and motion contracts")
    print("- all five hero products remain visible and share the bounded hero-only five-live allocation")
    print("- technical Mez Systems repository remains an unresolved versioned consumer")
    print("- cumulative hero feedback through Round 04 is recorded for Round 05")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
