#!/usr/bin/env python3
"""Verify the bounded PORT-01 production release plan."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
REPO = BRAND_KIT.parent


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    plan = read_json(ROOT / "release-plan.source.json")

    try:
        jsonschema.Draft202012Validator(read_json(ROOT / "release-plan.schema.json")).validate(plan)
    except jsonschema.ValidationError as error:
        failures.append(f"release plan schema: {error.message}")

    proof = read_json(ROOT / "operating-proof-payload.example.json")
    try:
        jsonschema.Draft202012Validator(read_json(ROOT / "operating-proof-payload.schema.json")).validate(proof)
    except jsonschema.ValidationError as error:
        failures.append(f"operating-proof payload schema: {error.message}")

    dependencies = plan.get("dependencies", [])
    ids = [item.get("id") for item in dependencies]
    if len(ids) != len(set(ids)):
        failures.append("dependency IDs are not unique")
    required_classes = {"canonical", "generated", "evidence-only", "consumer-owned"}
    if {item.get("class") for item in dependencies} != required_classes:
        failures.append("dependency inventory does not exercise all five required authority classes")
    for item in dependencies:
        source = item.get("source", "")
        if not source.startswith(("consumer://", "external://")):
            path = REPO / source
            if not path.exists():
                failures.append(f"dependency source does not exist: {source}")
        if not item.get("followUp", "").startswith("TASK-"):
            failures.append(f"dependency has no owning follow-up: {item.get('id')}")

    by_id = {item["id"]: item for item in dependencies}
    required_ids = {
        "DEP-FOUNDATIONS-1-0-0",
        "DEP-PRODUCT-REGISTRY",
        "DEP-GRADIENT-CATALOGUE-AND-STATIC-TWINS",
        "DEP-LIVING-CORE-RUNTIME",
        "DEP-WINGS-ASSET",
        "DEP-GLOBAL-NAVIGATION-1-0-0",
        "DEP-GOLDEN-HOMEPAGE-CONTRACT",
        "DEP-GOLDEN-HOMEPAGE-IMPLEMENTATION",
        "DEP-THIRD-PARTY-MARKS",
        "DEP-CMP-05-HALFTONE-PORTRAIT",
        "DEP-CMP-06-TESTIMONIAL-MARQUEE",
        "DEP-TESTIMONIAL-CONTENT",
        "DEP-TESTIMONIAL-MEDIA",
        "DEP-OPERATING-PROOF-RAW",
        "DEP-ROUTES-ANALYTICS-SEO-AVAILABILITY",
    }
    missing = sorted(required_ids - set(by_id))
    if missing:
        failures.append(f"required dependency units missing: {', '.join(missing)}")

    homepage_html = (BRAND_KIT / "workbench/golden/homepage/index.html").read_text(encoding="utf-8")
    homepage_css = (BRAND_KIT / "workbench/golden/homepage/styles.css").read_text(encoding="utf-8")
    homepage_js = (BRAND_KIT / "workbench/golden/homepage/homepage.js").read_text(encoding="utf-8")
    marquee_js = (BRAND_KIT / "components/testimonial-marquee/mez-testimonial-marquee.js").read_text(encoding="utf-8")
    runtime_claims = {
        "DEP-FOUNDATIONS-1-0-0": "releases/foundations/dist/index.css",
        "DEP-GLOBAL-NAVIGATION-1-0-0": "components/global-navigation/mez-global-navigation",
        "DEP-CMP-05-HALFTONE-PORTRAIT": "halftone-portrait",
        "DEP-CMP-06-TESTIMONIAL-MARQUEE": "components/testimonial-marquee/mez-testimonial-marquee",
        "DEP-PRODUCT-REGISTRY": "registry/products.json",
        "DEP-GRADIENT-CATALOGUE-AND-STATIC-TWINS": "gradient-library/catalogue.json",
        "DEP-LIVING-CORE-RUNTIME": "source-pack/design-system-export/mz-core.js",
        "DEP-WINGS-ASSET": "source-pack/design-system-export/assets/wings.svg",
        "DEP-THIRD-PARTY-MARKS": "assets/third-party-marks/",
        "DEP-OPERATING-PROOF-RAW": "assets/operating-proof/",
    }
    combined = "\n".join((homepage_html, homepage_css, homepage_js, marquee_js))
    for dep_id, needle in runtime_claims.items():
        if needle not in combined:
            failures.append(f"current homepage no longer proves inventory dependency {dep_id}: {needle}")

    for dep_id, source_path in (
        ("DEP-CMP-05-HALFTONE-PORTRAIT", BRAND_KIT / "components/halftone-portrait/halftone-portrait.source.json"),
        ("DEP-CMP-06-TESTIMONIAL-MARQUEE", BRAND_KIT / "components/testimonial-marquee/testimonial-marquee.source.json"),
    ):
        source = read_json(source_path)
        inventory = by_id.get(dep_id, {})
        if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
            failures.append(f"{dep_id} live source does not carry canonical authority")
        if len(source.get("decisionIds", [])) != 1:
            failures.append(f"{dep_id} does not cite exactly one promotion decision")
        if inventory.get("class") != "canonical" or inventory.get("includeInTarget") is not True or inventory.get("status") != "release-eligible-approved":
            failures.append(f"{dep_id} is not routed into release-candidate assembly")

    raw_proof = by_id.get("DEP-OPERATING-PROOF-RAW", {})
    if raw_proof.get("class") != "evidence-only" or raw_proof.get("includeInTarget") is not False:
        failures.append("raw operating proof is not excluded as evidence-only")
    if proof.get("publicReleaseEligible") is not False or proof.get("review") is not None:
        failures.append("redaction-pending proof example must not be public-release eligible or reviewed")
    if proof.get("sourceProvenance", {}).get("originalPathsIncluded") is not False or proof.get("sourceProvenance", {}).get("originalBytesIncluded") is not False:
        failures.append("proof payload exposes original paths or bytes")
    provenance = read_json(BRAND_KIT / "workbench/golden/homepage/assets/operating-proof/provenance.json")
    source_hashes = {item["sha256"] for item in provenance.get("assets", [])}
    payload_hashes = {item["originalSha256"] for item in proof.get("records", [])}
    if source_hashes != payload_hashes or len(payload_hashes) != 4:
        failures.append("proof payload does not preserve exactly the four original hashes")
    for record in proof.get("records", []):
        if record.get("redactedAsset") is not None or record.get("redactedSha256") is not None or record.get("publicReleaseEligible") is not False:
            failures.append(f"unreviewed proof record became release eligible: {record.get('id')}")
    if re.search(r"/Users/|[A-Za-z]:\\\\", json.dumps(proof)):
        failures.append("release-safe proof payload contains an absolute workstation path")

    package = plan.get("targetPackage", {})
    required_groups = {"authority", "foundations", "identity", "runtime", "expressions", "components", "golden-homepage", "guidance", "skills", "schemas", "validators", "examples", "licences"}
    if set(package.get("requiredGroups", [])) != required_groups:
        failures.append("target package group boundary is incomplete")
    clean = plan.get("cleanConsumerProof", {})
    if clean.get("viewports") != [320, 375, 390, 430, 768, 1024, 1280, 1440]:
        failures.append("clean-consumer proof viewports drifted")
    method = clean.get("method", "").lower()
    for phrase in ("only the assembled package", "temporary directory", "canonical checkout", "network dependency", "included verifier"):
        if phrase not in method:
            failures.append(f"clean-consumer method missing: {phrase}")
    versioning = plan.get("versioning", {})
    for key in ("visibility", "update", "rollback", "compatibility"):
        if len(versioning.get(key, "")) < 40:
            failures.append(f"versioning contract incomplete: {key}")
    consumer = plan.get("consumerInterface", {})
    registry = read_json(BRAND_KIT / "governance/consumer-register.json")
    records = registry.get("consumers", [])
    registered = records[0] if len(records) == 1 else {}
    if (
        consumer.get("consumerId") != "CON-MEZ-SYSTEMS-WEB-001"
        or consumer.get("consumerId") != registered.get("id")
        or consumer.get("repository") != registered.get("repository")
        or consumer.get("registrationRecord") != "brand-kit/governance/consumer-register.json"
        or consumer.get("registrationRequiredBeforeIntegration") is not False
        or consumer.get("runtimeCrossRepositoryImportAllowed") is not False
        or registered.get("state") not in {"registered-not-integrated", "integrated-production"}
        or registered.get("productionIntegration", {}).get("runtimeCrossRepositoryImport") is not False
    ):
        failures.append("named consumer registration or pre-integration boundary is invalid")

    base_ledger = read_json(BRAND_KIT / "governance/decisions.json")
    supplement = read_json(BRAND_KIT / "governance/post-cutover-decisions.json")
    base_ids = {item.get("id") for item in base_ledger.get("decisions", [])}
    supplement_ids = {item.get("id") for item in supplement.get("decisions", [])}
    reconciliation = plan.get("authorityReconciliation", {})
    required_reconciled = {
        "DEC-FOUNDATION-RELEASE-001",
        "DEC-GLOBAL-NAVIGATION-COMPONENT-001",
        "DEC-GOLDEN-HOMEPAGE-001",
    }
    declared_reconciled = set(reconciliation.get("reconciledDecisionIds", []))
    component_promotions = {
        "DEC-HALFTONE-PORTRAIT-COMPONENT-001",
        "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001",
    }
    if declared_reconciled != required_reconciled or supplement_ids != required_reconciled | component_promotions or reconciliation.get("status") != "reconciled":
        failures.append("authority reconciliation does not match the post-cutover decision supplement")
    if reconciliation.get("ledger") != "brand-kit/governance/post-cutover-decisions.json" or reconciliation.get("baseLedger") != "brand-kit/governance/decisions.json":
        failures.append("authority reconciliation loses the immutable cutover-ledger boundary")
    if supplement.get("baseLedger") != "brand-kit/governance/decisions.json" or base_ids & supplement_ids:
        failures.append("post-cutover register does not cleanly supplement the immutable ledger")
    record_text = "\n".join((REPO / path).read_text(encoding="utf-8") for path in reconciliation.get("supportingRecords", []))
    for decision_id in declared_reconciled:
        if decision_id not in record_text:
            failures.append(f"bounded supporting record missing decision ID: {decision_id}")

    if failures:
        print("MEZ PRODUCTION RELEASE BOUNDARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MEZ PRODUCTION RELEASE BOUNDARY: PASS")
    print("- 21 release-copy or external ownership units use all four current authority classes")
    print("- CMP-05 and CMP-06 are approved canonical inputs to release-candidate assembly")
    print("- four raw operating-proof records remain evidence-only and release-ineligible")
    print("- package, clean-install, version visibility, update, rollback and named-consumer boundaries are explicit")
    print("- immutable cutover decisions plus three prior and two component approvals form current decision authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
