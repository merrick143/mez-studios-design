#!/usr/bin/env python3
"""Verify the Product UI Foundation candidate against its running contract.

The verifier intentionally reads the fixture's named authority sources and
greps the browser implementation for the behaviours promised by the source
contract. A polished JSON claim cannot pass while the interface omits it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parent
WORKBENCH = BRAND_KIT / "workbench" / "product-ui"
SOURCE = ROOT / "product-ui-foundation.source.json"
SCHEMA = ROOT / "product-ui-foundation.schema.json"
REVIEW = ROOT / "review.json"
APPROVAL = ROOT / "approval.json"
FIXTURE = WORKBENCH / "fixtures" / "system-proof.json"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
JS = WORKBENCH / "product-ui.js"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def finish(failures: list[str]) -> int:
    if failures:
        print("PRODUCT UI FOUNDATION CONTRACT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PRODUCT UI FOUNDATION CONTRACT: PASS")
    print("- H-UI-01-approved foundation direction; no canonical or production product authority is claimed")
    print("- every fixture record and visible summary resolves to named repository evidence")
    print("- implementation contains the seven states, three densities, roving navigation, sort, filter, selection and dialog behaviours promised by the contract")
    print("- semantic table, aria-sort, live announcements and a complete chart text alternative are present")
    return 0


def main() -> int:
    failures: list[str] = []
    for path in (SOURCE, SCHEMA, REVIEW, APPROVAL, FIXTURE, HTML, CSS, JS):
        if not path.exists():
            failures.append(f"missing artifact: {path.relative_to(BRAND_KIT.parent)}")
    if failures:
        return finish(failures)

    source, schema, review, approval, fixture = map(load, (SOURCE, SCHEMA, REVIEW, APPROVAL, FIXTURE))
    html = HTML.read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.S)
    js = JS.read_text(encoding="utf-8")

    for error in Draft202012Validator(schema).iter_errors(source):
        location = ".".join(str(part) for part in error.path) or "root"
        failures.append(f"source schema {location}: {error.message}")

    if source["status"] != "approved" or source["productionAuthority"] is not False:
        failures.append("UI-01 must be approved with productionAuthority false")
    if source["decisionIds"] or source["approval"]["decisionId"] is not None:
        failures.append("approved direction must not invent a canonical decision ID")
    if source["approval"]["state"] != "approved-foundation-direction" or source["approval"]["approvedAt"] != "2026-07-28":
        failures.append("source contract does not record the exact H-UI-01 approval state")
    if review.get("productionAuthority") is not False or review.get("outputStatus") != "approved" or review.get("verdict") != "approved":
        failures.append("review must record approved non-production authority")
    if approval.get("gateId") != "H-UI-01-PRODUCT-UI-FOUNDATION" or approval.get("verdict") != "approved" or approval.get("approvedBy") != "Olli":
        failures.append("approval record does not close the exact H-UI-01 gate through Olli")
    if approval.get("humanEvidence") != ["approved"]:
        failures.append("approval record must preserve the exact human evidence")
    if approval.get("productionAuthority") is not False or approval.get("canonicalAuthority") is not False or approval.get("decisionId") is not None:
        failures.append("H-UI-01 approval must remain non-production, non-canonical and decision-ID-free")
    if fixture.get("notProductionProductData") is not True:
        failures.append("fixture must explicitly deny production product-data authority")
    if fixture.get("scopeLabel") != source["dataTruth"]["scopeLabel"]:
        failures.append("fixture scope label differs from the source contract")

    records = fixture.get("records", [])
    if len(records) != 7 or len({item["id"] for item in records}) != 7:
        failures.append("review fixture must contain the seven unique bounded evidence records")
    required_record_fields = {"id", "name", "type", "status", "updated", "source", "detail"}
    for record in records:
        if set(record) != required_record_fields:
            failures.append(f"{record.get('id', 'unknown')}: record fields do not match the bounded shape")
        source_path = BRAND_KIT / record.get("source", "")
        if not source_path.exists():
            failures.append(f"{record.get('id')}: named source is missing: {record.get('source')}")

    # Cross-check every claim that can drift against its authoritative file.
    products = load(BRAND_KIT / "registry" / "products.json")["products"]
    registry_summary = fixture.get("registrySummary", {})
    if registry_summary != {
        "products": len(products),
        "live": sum(item["availability"] == "live" for item in products),
        "comingSoon": sum(item["availability"] == "coming-soon" for item in products),
    }:
        failures.append("registry summary does not match registry/products.json")

    figma = load(BRAND_KIT / "figma-companion" / "phase-04-functional-components.json")
    expected_figma = {
        "totalComponentSets": figma["liveAudit"]["componentSets"],
        "functionalComponentSets": figma["componentSummary"]["componentSets"],
        "functionalVariants": figma["componentSummary"]["variants"],
    }
    if fixture.get("figmaSummary") != expected_figma:
        failures.append(f"Figma summary does not match Phase 4 evidence: expected {expected_figma}")

    source_by_record = {
        "navigation": "components/global-navigation/global-navigation.source.json",
        "portrait": "components/halftone-portrait/halftone-portrait.source.json",
        "testimonials": "components/testimonial-marquee/testimonial-marquee.source.json",
        "product-ui": "product-ui/product-ui-foundation.source.json",
    }
    by_id = {item["id"]: item for item in records}
    for record_id, relative in source_by_record.items():
        authority = load(BRAND_KIT / relative)
        if by_id[record_id]["status"] != authority["status"]:
            failures.append(f"{record_id}: fixture status differs from {relative}")
    if by_id["product-registry"]["status"] != "canonical" or load(BRAND_KIT / "registry/products.json")["authorityState"] != "canonical-active":
        failures.append("product registry fixture record does not match canonical registry authority")

    distribution = fixture.get("distribution", [])
    actual_counts: dict[str, int] = {}
    for record in records:
        actual_counts[record["status"]] = actual_counts.get(record["status"], 0) + 1
    declared_counts = {item["status"]: item["count"] for item in distribution}
    if declared_counts != actual_counts:
        failures.append(f"distribution {declared_counts} does not match record statuses {actual_counts}")

    # Implementation-level assertions: the contract must exist in the code.
    for state in source["states"]:
        if state not in html and state not in js:
            failures.append(f"implementation omits promised state: {state}")
    for density in source["densityModes"]:
        css_declared = f'data-density="{density}"' in css or (density == "comfortable" and 'data-density="comfortable"' in html)
        if f'data-density-value="{density}"' not in html or not css_declared:
            failures.append(f"implementation omits promised density: {density}")
    for token in ("ArrowDown", "ArrowUp", "Home", "End", "aria-current", "tabIndex=-1"):
        if token not in js:
            failures.append(f"roving navigation implementation omits {token}")
    for token in ("viewIncludes", 'activeView=button.dataset.view', 'record.type==="Registry"', 'record.type==="Runtime component"'):
        if token not in js:
            failures.append(f"workspace navigation implementation omits real view behaviour: {token}")
    for token in ("data-sort", "aria-sort", "data-filter", "data-select", "aria-live", 'role="dialog"'):
        if token not in html and token not in js:
            failures.append(f"interaction or accessibility contract missing from implementation: {token}")
    for token in ('setAttribute("inert"', 'setAttribute("aria-hidden"', 'event.key==="Tab"', "event.shiftKey", "returnFocus"):
        if token not in js:
            failures.append(f"modal focus-management contract missing from implementation: {token}")
    if '<table>' not in html or "<caption>" not in html or 'scope="col"' not in html:
        failures.append("ledger must remain a semantic table with caption and column headers")
    if "<noscript>" not in html or "Open the complete seven-record source fixture" not in html:
        failures.append("JavaScript-disabled output must preserve purpose and a route to the complete fixture")
    if 'data-status-alternative' not in html or 'aria-label="Text alternative for status distribution"' not in html:
        failures.append("status visualisation requires a complete adjacent text alternative")
    if "fixture.distribution.map" not in js or 'setAttribute("aria-label"' not in js:
        failures.append("status visualisation values must generate both visual and spoken labels from one fixture")
    if "prefers-reduced-motion:reduce" not in css or "transition-duration:.001ms" not in css:
        failures.append("reduced motion must remove control transitions")
    if "@media(max-width:1023px)" not in css or "@media(max-width:639px)" not in css:
        failures.append("implementation lacks declared tablet and narrow recomposition boundaries")
    if 'content:attr(data-label)' not in css.replace(" ", ""):
        failures.append("narrow ledger must expose persistent field labels")

    banned_css = ("backdrop-filter", "box-shadow", "#000000", "#000", "purple")
    for banned in banned_css:
        if banned in css.lower():
            failures.append(f"banned Product UI CSS: {banned}")
    if re.search(r"\b(revenue|customers?|conversion rate|monthly active|arr)\b", json.dumps(fixture), re.I):
        failures.append("fixture contains a production-style business metric or customer claim")

    return finish(failures)


if __name__ == "__main__":
    raise SystemExit(main())
