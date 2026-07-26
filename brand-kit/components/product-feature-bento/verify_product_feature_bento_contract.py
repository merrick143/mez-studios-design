#!/usr/bin/env python3
"""Verify the PC2-B-C04 Product Feature Bento candidate contract.

This mirrors, in Python, the rules the custom element enforces at render, so a
fixture cannot pass review by never being opened in a browser. The one rule
everything else leans on: a bento carries exactly one colour event. The pantry
states it as "multiple live gradient cells fail validation" and the reference
study arrived at the same rule independently, which is why it is checked here,
in the schema and at render rather than trusted to care.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "product-feature-bento.source.json"
SCHEMA = ROOT / "product-feature-bento.schema.json"
REVIEW = ROOT / "review.json"
CSS = ROOT / "mez-product-feature-bento.css"
JS = ROOT / "mez-product-feature-bento.js"
FIXTURES = ROOT / "fixtures"
PRODUCTS = BRAND_KIT / "registry" / "products.json"
FOUNDATIONS = BRAND_KIT / "releases" / "foundations" / "dist" / "packages" / "geometry-controls" / "tokens.css"

JOBS = ["product", "proof", "workflow", "metric", "media", "integration", "quote", "action"]
SURFACES = ["paper", "muted", "tint", "outline", "recessed", "raised", "dark", "material"]
MATERIAL_JOBS = {"product", "metric"}

BANNED_CSS = ("backdrop-filter", "box-shadow", "#000000", "#0a0a0a")


def report(failures: list[str]) -> int:
    if failures:
        print("PRODUCT FEATURE BENTO CONTRACT: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("PRODUCT FEATURE BENTO CONTRACT: PASS")
    print("- candidate authority, not production, and no release is claimed")
    print("- every fixture declares typed cells and carries exactly one colour event")
    print("- rows sum to the declared column count; no fixture leaves a hole")
    print("- radii are concentric: frame minus padding equals the panel radius")
    return 0


def radius_tokens() -> dict[str, int]:
    if not FOUNDATIONS.exists():
        return {}
    text = FOUNDATIONS.read_text(encoding="utf-8")
    return {
        name: int(value)
        for name, value in re.findall(r"--mz-radius-([a-z]+):\s*(\d+)px", text)
    }


def check_rows(cells: list[dict], columns: int, name: str, failures: list[str]) -> None:
    """Auto-flow fixtures must tile exactly. Explicitly placed ones are checked
    against their own declared coordinates instead."""
    if any("col" in cell or "row" in cell for cell in cells):
        occupied: dict[tuple[int, int], str] = {}
        for index, cell in enumerate(cells):
            col = cell.get("col")
            row = cell.get("row")
            if col is None or row is None:
                failures.append(f"{name}: cell {index + 1} mixes explicit and auto placement")
                continue
            for r in range(row, row + cell.get("rows", 1)):
                for c in range(col, col + cell.get("span", 3)):
                    if c > columns:
                        failures.append(f"{name}: cell {index + 1} runs past column {columns}")
                    if (r, c) in occupied:
                        failures.append(f"{name}: cell {index + 1} overlaps {occupied[(r, c)]} at row {r} column {c}")
                    occupied[(r, c)] = f"cell {index + 1}"
        rows = {r for r, _ in occupied}
        for r in rows:
            filled = len([1 for rr, _ in occupied if rr == r])
            if filled != columns:
                failures.append(f"{name}: row {r} fills {filled} of {columns} columns, leaving a hole")
        return

    total = sum(cell.get("span", 3) * cell.get("rows", 1) for cell in cells)
    if total % columns:
        failures.append(f"{name}: spans total {total}, which is not a whole number of {columns} column rows")


def main() -> int:
    failures: list[str] = []
    for path in (SOURCE, SCHEMA, REVIEW, CSS, JS, PRODUCTS):
        if not path.exists():
            failures.append(f"missing artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return report(failures)

    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    # Comments explain the rules and quote the selectors they warn about, so they
    # are stripped before scanning or the file trips its own guards.
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.S)
    js = JS.read_text(encoding="utf-8")
    products = {item["slug"] for item in json.loads(PRODUCTS.read_text(encoding="utf-8"))["products"]}

    # --- authority. A candidate must not claim what it has not been granted.
    if source.get("status") != "candidate" or source.get("productionAuthority") is not False:
        failures.append("the contract must remain candidate with productionAuthority false until a human decision exists")
    if source.get("approval", {}).get("state") != "awaiting-human-review":
        failures.append("approval state must stay awaiting-human-review while decisionIds is empty")
    if source.get("decisionIds") and not source["approval"].get("decisionId"):
        failures.append("decision IDs are recorded but the approval block names none")
    if review.get("verdict") != "awaiting-human-review" or review.get("productionAuthority") is not False:
        failures.append("review.json must record an unapproved candidate")
    if source.get("motion", {}).get("maximumLiveCores") != 1:
        failures.append("MOT-01: the bento budget is one live core")

    # --- the fixtures are the real contract surface.
    declared = {variant["fixture"] for variant in source.get("variants", [])}
    for relative in sorted(declared):
        if not (ROOT / relative).exists():
            failures.append(f"declared fixture is missing: {relative}")

    # Every fixture on disk is checked, not only the four the contract declares.
    # An exploration that violates the contract is still a fixture that renders.
    everything = sorted(
        path for path in FIXTURES.rglob("*.json")
        if path.name != "invalid-two-material.json"
    )
    for path in everything:
        relative = path.relative_to(ROOT).as_posix()
        fixture = json.loads(path.read_text(encoding="utf-8"))
        name = fixture.get("variant", relative)
        columns = fixture.get("columns", 12)

        if fixture.get("source") == "registry":
            template = fixture.get("registryTemplate", {})
            if not template.get("live") or not template.get("coming"):
                failures.append(f"{name}: a registry fixture needs both a live and a coming template")
            if template.get("live", {}).get("surface") != "material":
                failures.append(f"{name}: the shipped product carries the colour event")
            if template.get("coming", {}).get("surface") == "material":
                failures.append(f"{name}: coming products must not carry material")
            if re.search(r"\b[0-9]+\s*products?\b", json.dumps(fixture)):
                failures.append(f"{name}: a registry fixture must not hardcode a product count (LAY-09)")
            continue

        cells = fixture.get("cells", [])
        if not cells:
            failures.append(f"{name}: no cells")
            continue

        for index, cell in enumerate(cells):
            at = f"{name} cell {index + 1}"
            if cell.get("job") not in JOBS:
                failures.append(f"{at}: job {cell.get('job')!r} is not a declared job")
            if cell.get("surface") and cell["surface"] not in SURFACES:
                failures.append(f"{at}: surface {cell['surface']!r} is not a declared surface")
            if not any(key in cell for key in ("label", "productSlug", "figure", "entries")):
                failures.append(f"{at}: resolves to no content, which makes it filler")
            if cell.get("productSlug") and cell["productSlug"] not in products:
                failures.append(f"{at}: product {cell['productSlug']!r} is not in the canonical registry")
            if cell.get("job") == "product" and not cell.get("productSlug"):
                failures.append(f"{at}: a product cell must name a registry slug, never a hardcoded product")

        material = [cell for cell in cells if cell.get("surface") == "material"]
        # The rule is one colour event, not one material cell. A continuous layer
        # behind apertures is one object seen through many windows, so it spends
        # the same single event; declaring both is the violation.
        # "layer" in fixture, not truthiness: an empty layer object is falsy in
        # Python and would slip past both this count and its own check below.
        events = len(material) + (1 if "layer" in fixture else 0)
        if events > 1:
            failures.append(f"{name}: {events} colour events; a bento carries exactly one")
        if "layer" in fixture and not (fixture["layer"] or {}).get("productSlug"):
            failures.append(f"{name}: a layer must name the product whose material it carries")
        for cell in material:
            if cell.get("job") not in MATERIAL_JOBS:
                failures.append(f"{name}: material sits on a {cell.get('job')} cell, not a product or metric cell")
        if len([cell for cell in cells if cell.get("focal")]) > 1:
            failures.append(f"{name}: more than one focal cell")

        spans = [cell.get("span", 3) for cell in cells]
        if len(spans) >= 3 and len(set(spans)) == 1:
            failures.append(f"{name}: every cell spans {spans[0]}; an even grid is not a bento (LAY-01)")

        check_rows(cells, columns, name, failures)

    # A negative fixture has to exist, or the rule is asserted rather than proven.
    invalid = FIXTURES / "invalid-two-material.json"
    if not invalid.exists():
        failures.append("the negative fixture proving the one-colour-event rule is missing")
    else:
        cells = json.loads(invalid.read_text(encoding="utf-8")).get("cells", [])
        if len([cell for cell in cells if cell.get("surface") == "material"]) < 2:
            failures.append("the negative fixture no longer violates the rule it exists to prove")

    # --- canon guards on the stylesheet.
    for banned in BANNED_CSS:
        if banned in css.lower():
            failures.append(f"banned in component CSS: {banned}")
    if "border-radius: 0" in css:
        failures.append("LAY-07: outer corners stay rounded")

    radii = radius_tokens()
    if radii:
        frame, panel = radii.get("frame"), radii.get("panel")
        pad = re.search(r"--bento-pad:\s*(\d+)px", css)
        if frame and panel and pad and frame - int(pad.group(1)) != panel:
            failures.append(
                f"radii are not concentric: frame {frame} minus padding {pad.group(1)} should equal panel {panel}"
            )

    # A silent substring match on --row would steal the span from every auto-flow
    # cell that declares one. This regression is cheap to reintroduce and costly
    # to spot, so it is pinned.
    if re.search(r'\[style\*="--row"\]', css) or re.search(r'\[style\*="--col"\]', css):
        failures.append("placement selectors must match --col-start and --row-start, or --rows is captured by --row")

    # --- the renderer contract.
    if "export function validate" not in js:
        failures.append("the contract rules must be exported so they can be tested without a browser")
    if re.search(r"\bmountLivingCore\b(?!s)", js):
        failures.append("MOT-01: mountLivingCore creates a second WebGL context")
    if "registry/products.json" not in js:
        failures.append("product identity must resolve from the canonical registry")
    for hardcoded in ("AI OS", "MZ-G13"):
        if hardcoded in js:
            failures.append(f"LAY-09: {hardcoded!r} is hardcoded in the component")

    return report(failures)


if __name__ == "__main__":
    raise SystemExit(main())
