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


def read(path: Path):
    return json.loads(path.read_text())


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    failures = []
    source = read(ROOT / "product-card.source.json")
    review = read(ROOT / "review.json")
    try:
        jsonschema.Draft202012Validator(read(ROOT / "product-card.schema.json")).validate(source)
    except jsonschema.ValidationError as error:
        failures.append("schema: " + error.message)

    if source.get("candidateRevision") != "product-card-02-phase-a-r02" or source.get("productionAuthority") is not False or review.get("verdict") != "pending":
        failures.append("Phase A candidate gate drifted")
    programme = source.get("programme", {})
    if programme.get("phaseA", {}).get("status") != "active" or programme.get("phaseB", {}).get("status") != "held-until-visual-lock":
        failures.append("two-phase sequence drifted")
    treatments = source.get("visualTreatments", [])
    if [item.get("id") for item in treatments] != [f"C{number:02}" for number in range(1, 5)]:
        failures.append("four ordered website-card treatments required")
    if source.get("agentRecommendation", {}).get("base") != "C01 Editorial Portrait":
        failures.append("agent recommendation drifted")
    if {item.get("id") for item in source.get("groupingComponents", [])} != {"G01", "G02"}:
        failures.append("family shelf and bundle offer components required")
    architecture = source.get("cardArchitecture", {})
    if architecture.get("widthRange") != [320, 360] or "2:3" not in architecture.get("ratio", ""):
        failures.append("portrait architecture drifted")
    phase_b = source.get("phaseBScope", {})
    if len(phase_b.get("websiteComponents", [])) < 7 or "pricing" not in phase_b.get("websiteFlows", []) or "checkout" not in phase_b.get("websiteFlows", []):
        failures.append("Phase B website component scope incomplete")
    if source.get("coreAllocation", {}).get("maximumLivePerViewport") != 1:
        failures.append("Living Core allocation drifted")

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

    html = (WORKBENCH / "index.html").read_text() if (WORKBENCH / "index.html").is_file() else ""
    javascript = (WORKBENCH / "product-card.js").read_text() if (WORKBENCH / "product-card.js").is_file() else ""
    required_phrases = (
        "These are website cards", "One architecture", "Four treatments",
        "Editorial Portrait", "Full Field Portrait", "System Index", "Product Pack",
        "family shelf", "Bundle offer", "Discovery card", "Pricing card", "Checkout card",
        "Responsive system", "Interaction states", "#171715", "#252523",
        "H-EXP-04A-CARD-VISUAL-DIRECTION",
    )
    for phrase in required_phrases:
        if phrase not in html:
            failures.append("human proof missing: " + phrase)
    if html.count("data-direction-id=") != 4:
        failures.append("proof must contain exactly four treatment candidates")
    if html.count("data-mz-core") != 1:
        failures.append("proof must contain exactly one interactive Living Core mount")
    if "data-shape=\"rect\"" not in html:
        failures.append("interactive Core must prove non-disc rounded-rectangle expression")
    for phrase in ("mountLivingCores", "forceStatic", "selectedBaseTreatment", "contrastRule", "phaseBStatus"):
        if phrase not in javascript:
            failures.append("interactive review missing: " + phrase)
    if "http://" in html or "https://" in html:
        failures.append("external URL in proof")

    if failures:
        print("MEZ PRODUCT CARD 02 · PHASE A: FAIL")
        for failure in failures:
            print("- " + failure)
        return 1
    print("MEZ PRODUCT CARD 02 · PHASE A: PASS")
    print("- one portrait website-card architecture with four contextual treatments")
    print("- family shelf, bundle offer, surface allocation and Phase B website components are explicit")
    print("- H-EXP-04A-CARD-VISUAL-DIRECTION remains pending; Phase B is held")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
