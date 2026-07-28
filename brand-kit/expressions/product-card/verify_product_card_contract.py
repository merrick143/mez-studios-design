#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND = ROOT.parents[1]
DIST = ROOT / "dist"
WORKBENCH = BRAND / "workbench" / "expressions" / "product-card"
EXPRESSION_IDS = [f"F{number}" for number in range(1, 5)]
FAMILY_NAMES = ("Landing Plates", "Product Cards", "Bundles and Packs", "Website Sections")
SPECIMEN_IDS = [
    "QC01", "QC02", "QC03", "QC04", "ES02", "ES04", "IC01", "IC02", "IC03",
    "HL01", "HL02", "HL04", "QF01", "QF03",
    "FC01", "FC02", "PO01", "PO02",
    "ST01", "ST02", "SG01", "FN01", "BX01", "BX02",
    "SH01", "SH02", "SH03", "FS01", "FS02", "EX02", "BO01", "BO02",
]
KILLED_R08_IDS = ("ES01", "ES03", "HL03", "QF02", "CR01", "CR02", "KY01", "KY02", "FD01", "FD02", "FN02", "GR01", "GR02", "HR01", "HR02", "EX01")
KILLED_R09_IDS = ("MN01", "MN02", "HS01", "HS02")


def read(path: Path):
    return json.loads(path.read_text())


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    failures = []
    source = read(ROOT / "product-card.source.json")
    review = read(ROOT / "review.json")
    receipt_r08 = read(ROOT / "round-08-feedback.json")
    receipt = read(ROOT / "round-09-feedback.json")
    receipt_r10 = read(ROOT / "round-10-feedback.json")
    registry = read(BRAND / "registry" / "products.json")
    try:
        jsonschema.Draft202012Validator(read(ROOT / "product-card.schema.json")).validate(source)
    except jsonschema.ValidationError as error:
        failures.append("schema: " + error.message)

    if source.get("candidateRevision") != "product-card-02-phase-a-r10" or source.get("productionAuthority") is not True or review.get("verdict") != "approve":
        failures.append("approved Phase A Round 10 gate drifted")
    if receipt_r08.get("candidateRevision") != "product-card-02-phase-a-r08" or receipt_r08.get("productionAuthority") is not False:
        failures.append("Round 08 feedback receipt missing or invalid")
    r08_counts = {verdict: sum(item.get("verdict") == verdict for item in receipt_r08.get("specimens", [])) for verdict in ("keep", "revise", "kill", "unreviewed")}
    if r08_counts != {"keep": 20, "revise": 13, "kill": 16, "unreviewed": 1}:
        failures.append("Round 08 verdict evidence drifted")
    if receipt.get("candidateRevision") != "product-card-02-phase-a-r09" or receipt.get("productionAuthority") is not False:
        failures.append("Round 09 feedback receipt missing or invalid")
    verdict_counts = {verdict: sum(item.get("verdict") == verdict for item in receipt.get("specimens", [])) for verdict in ("keep", "revise", "kill", "unreviewed")}
    if verdict_counts != {"keep": 14, "revise": 18, "kill": 4, "unreviewed": 0}:
        failures.append("Round 09 verdict evidence drifted")
    if receipt_r10.get("candidateRevision") != "product-card-02-phase-a-r10" or receipt_r10.get("productionAuthority") is not False:
        failures.append("Round 10 submitted feedback receipt missing or invalid")
    r10_counts = {verdict: sum(item.get("verdict") == verdict for item in receipt_r10.get("specimens", [])) for verdict in ("keep", "revise", "kill", "unreviewed")}
    if r10_counts != {"keep": 32, "revise": 0, "kill": 0, "unreviewed": 0}:
        failures.append("Round 10 unanimous approval evidence drifted")
    if review.get("decisionId") != "DEC-PRODUCT-CARD-VISUAL-ARCHITECTURE-001" or review.get("productionAuthority") is not True:
        failures.append("Phase A approval record drifted")
    programme = source.get("programme", {})
    if programme.get("phaseA", {}).get("status") != "complete" or programme.get("phaseB", {}).get("status") != "ready-to-start":
        failures.append("two-phase sequence drifted")
    if [item.get("id") for item in source.get("postures", [])] != [f"P{number}" for number in range(1, 6)]:
        failures.append("five ordered material postures required")
    expressions = source.get("expressions", [])
    if [item.get("id") for item in expressions] != EXPRESSION_IDS:
        failures.append("four ordered active card families required")
    for item in expressions:
        if not all(item.get(key) for key in ("role", "placement", "thesis", "motion", "variants", "failure")):
            failures.append("unexplained family: " + str(item.get("id")))
    declared = [variant for item in expressions for variant in item.get("variants", [])]
    if declared != SPECIMEN_IDS:
        failures.append("thirty-two ordered Round 10 specimens required")
    registry_slugs = {product["slug"] for product in registry.get("products", [])}
    if not registry_slugs.issubset(source.get("territories", {}).get("assignments", {}).keys()):
        failures.append("every registry product needs a territory assignment")
    if not source.get("agentRecommendation", {}).get("base", "").startswith("BO01"):
        failures.append("Round 10 must preserve BO01 as the contextual champion")
    allocation = source.get("coreAllocation", {})
    if allocation.get("maximumLivePerViewport") != 1 or "Deep Mineral" not in allocation.get("finish", ""):
        failures.append("Living Core allocation drifted")
    if len(source.get("reviewSurface", {}).get("sections", [])) != 8:
        failures.append("review surface must declare eight Round 10 sections")
    if source.get("editions", {}).get("active") is not False:
        failures.append("System Editions must remain inactive after the Round 09 kill")
    if len(source.get("reviewSurface", {}).get("feedbackCapture", [])) != 5:
        failures.append("review surface must preserve family, specimen and global feedback")
    ethos = BRAND / "docs" / "PRODUCT-CARD-DESIGN-ETHOS.md"
    if not ethos.is_file():
        failures.append("approved product-expression ethos is missing")
    else:
        ethos_text = ethos.read_text()
        for phrase in ("Approved invariants", "What Olli consistently rejected", "The ten-round learning trail", "Phase B inheritance"):
            if phrase not in ethos_text:
                failures.append("design ethos missing: " + phrase)

    protected = []
    for dependency in source.get("dependencies", {}).values():
        path = BRAND / dependency["path"].removeprefix("brand-kit/")
        protected.append(path)
        if not path.is_file() or sha(path) != dependency["sha256"]:
            failures.append("dependency drift: " + dependency["path"])
    before = {path: sha(path) for path in protected}
    old = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    build = subprocess.run([sys.executable, str(ROOT / "build_product_card_contract.py")], cwd=BRAND.parent, capture_output=True, text=True)
    if build.returncode:
        failures.append("build failed: " + (build.stderr or build.stdout).strip())
    new = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()}
    if old and old != new:
        failures.append("deterministic rebuild changed output")
    if before != {path: sha(path) for path in before}:
        failures.append("canonical dependency changed")

    html = (WORKBENCH / "index.html").read_text()
    javascript = (WORKBENCH / "product-card.js").read_text()
    components = (WORKBENCH / "card-components.js").read_text()
    styles = (WORKBENCH / "styles.css").read_text()
    proof = "\n".join((html, javascript, components, styles, json.dumps(source)))
    for phrase in FAMILY_NAMES + ("Name first.", "One rule across every survivor.", "Alive by default.", "Approved visual grammar"):
        if phrase not in proof:
            failures.append("review proof missing: " + phrase)
    for specimen_id in SPECIMEN_IDS:
        if specimen_id not in components or specimen_id not in json.dumps(expressions):
            failures.append("Round 10 specimen missing: " + specimen_id)
    for killed_id in KILLED_R08_IDS:
        if f'id:"{killed_id}"' in components or killed_id in declared:
            failures.append("killed Round 08 specimen returned: " + killed_id)
    for killed_id in KILLED_R09_IDS:
        if f'id:"{killed_id}"' in components or killed_id in declared:
            failures.append("killed Round 09 edition returned: " + killed_id)
    for phrase in ("IntersectionObserver", "data-auto-live", "moveCore", "forceStatic", "state.decisions", "candidateRevision", "registry/products.json", "prefers-reduced-motion", "renderer.mount", "surfaces?.delete", "count !== 32"):
        if phrase not in proof:
            failures.append("automatic interactive proof missing: " + phrase)
    for phrase in ("data-specimen-note", "data-family-note", "specimenNotes", "familyNotes", "feedback: state.specimenNotes", "sections,specimens"):
        if phrase not in proof:
            failures.append("detailed feedback capture missing: " + phrase)
    for phrase in ("border-radius: 16px", "border-radius: 20px", "border-radius: 24px", "border-radius: 32px", "#171715", "#252523", "#2e2e2e", "exact static twin", "Deep Mineral No. 5"):
        if phrase not in proof:
            failures.append("canonical visual rule missing: " + phrase)
    if "Animate focus" in proof or "data-animate-specimen" in proof:
        failures.append("Round 10 must not require an animation button")
    for forbidden in ("landing-disc", "explainer-disc", "edition-number", "type-index"):
        if forbidden in components or forbidden in html:
            failures.append("rejected visual debris returned: " + forbidden)
    for killed in ("Capsule rail", "Keyline ·", "Founder ·", "Grid ·", "Hero rail", "Explainer · direct"):
        if killed in components:
            failures.append("killed Round 08 path returned: " + killed)
    for revision_proof in ("card--all-dark", "bundle--single", "mark--large", "product-extended", "bundle--fan", "media--flush", "no-stroke", "SH03", "SG01"):
        if revision_proof not in proof:
            failures.append("Round 09 revision not implemented: " + revision_proof)
    if 'data-mount="editions"' in html or 'href="#editions"' in html or "family:\"editions\"" in components:
        failures.append("killed System Editions family returned to the active workbench")
    for text in (html, javascript, components):
        if "http://" in text or "https://" in text:
            failures.append("external URL in proof")
            break

    if failures:
        print("MEZ PRODUCT CARD 02 · PHASE A ROUND 10: FAIL")
        for failure in failures:
            print("- " + failure)
        return 1
    print("MEZ PRODUCT CARD 02 · PHASE A 1.0.0: PASS")
    print("- thirty-two unanimously approved specimens render from canonical product data across four real jobs")
    print("- all four killed editions are absent and Round 09 plus Round 10 feedback receipts are enforced")
    print("- every design shows static and automatic-motion twins with persistent structured feedback")
    print("- one live Deep Mineral core moves automatically; repeated objects and exact fallbacks remain static")
    print("- H-EXP-04A-CARD-VISUAL-DIRECTION is approved; canonical Phase B consumes this locked visual grammar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
