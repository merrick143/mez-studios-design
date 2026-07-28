#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parent
BRAND = ROOT.parents[2]
REPO = BRAND.parent
DIST = ROOT / "dist"
WORKBENCH = BRAND / "workbench" / "expressions" / "product-card" / "phase-b"
ROUND01_RECEIPT_SHA = "858dca76ab4e3fcaabcc5a4ca3996f7ce3a4a2654681e9085220bd6d784be9b1"
ROUND02_RECEIPT_SHA = "86f8e5fd02514ec2a55d81eecfb08e91946f66ddcaa667a379b87c5d584b182f"
ROUND03_RECEIPT_SHA = "0ebc1bc12d4a41d0ec66aed163f130aa625db9615e09e24479f52fed1c7d566c"
ROUND04_RECEIPT_SHA = "2a2f7779de4f2251d837eba163be936ab9e991080acdab06c1d3f9974c6fb844"
APPROVAL_REVIEW_SHA = "ff1397a73e7193e4aa574a2e8d6f17396beee8bf4fa64c26d99d408cdfe8dae5"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    source = read(ROOT / "product-component-pantry.source.json")
    schema = read(ROOT / "product-component-pantry.schema.json")
    review = read(ROOT / "review.json")
    try:
        jsonschema.Draft202012Validator(schema).validate(source)
    except jsonschema.ValidationError as error:
        failures.append("schema: " + error.message)

    if source.get("productionAuthority") is not True or source.get("status") != "canonical-functional-component-system" or source.get("version") != "1.0.0":
        failures.append("Phase B must be canonical 1.0.0 for its bounded component-system scope")
    if source.get("gateId") != "H-EXP-04B-CARD-FUNCTIONAL-PROOF":
        failures.append("Phase B human gate drifted")
    if source.get("candidateRevision") != "product-card-02-phase-b-pb2-r04":
        failures.append("Phase B candidate revision must be product-card-02-phase-b-pb2-r04")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-PRODUCT-COMPONENT-SYSTEM-001" or review.get("productionAuthority") is not True:
        failures.append("Phase B approval record drifted")
    if review.get("resultingStatus") != "canonical-functional-component-system" or review.get("programmeStatus") != "complete":
        failures.append("Phase B approval must close the programme and record canonical status")

    inherited = source.get("inherits", {})
    for name, dependency in inherited.items():
        path = REPO / dependency["path"]
        if not path.is_file() or sha(path) != dependency["sha256"]:
            failures.append(f"pinned Phase A dependency drift: {name}")

    evidence = source.get("evidence", {})
    expected_evidence = {
        "round01Feedback": ROUND01_RECEIPT_SHA,
        "round02Feedback": ROUND02_RECEIPT_SHA,
        "round03Feedback": ROUND03_RECEIPT_SHA,
        "round04Feedback": ROUND04_RECEIPT_SHA,
        "approvalReview": APPROVAL_REVIEW_SHA,
    }
    for name, expected_sha in expected_evidence.items():
        record = evidence.get(name, {})
        path = REPO / record.get("path", "")
        if record.get("sha256") != expected_sha or not path.is_file() or sha(path) != expected_sha:
            failures.append(f"Phase B feedback evidence drift: {name}")

    expected_round02_functional = (
        [f"B-DS{index:02d}" for index in range(1, 9)]
        + [f"B-FT{index:02d}" for index in range(1, 11)]
        + [f"B-PR{index:02d}" for index in range(1, 11)]
        + [f"B-CK{index:02d}" for index in range(1, 9)]
        + [f"B-BU{index:02d}" for index in range(1, 9)]
        + [f"B-MB{index:02d}" for index in range(1, 5)]
    )
    expected_round03_functional = [item for item in expected_round02_functional if item != "B-FT04"]
    expected_round04_functional = [item for item in expected_round03_functional if item != "B-FT06"]

    round_ten = read(ROOT.parent / "round-10-feedback.json")
    approved_phase_a = [item.get("id") for item in round_ten.get("specimens", []) if item.get("verdict") == "keep"]
    if len(approved_phase_a) != 32:
        failures.append("canonical Phase A must retain exactly thirty-two approved visual inputs")

    round_one_path = ROOT / "round-01-feedback.json"
    if not round_one_path.is_file() or sha(round_one_path) != ROUND01_RECEIPT_SHA:
        failures.append("missing or mutated exact Round 01 feedback receipt")
    else:
        round_one = read(round_one_path)
        receipt_specimens = round_one.get("specimens", [])
        if round_one.get("candidateRevision") != "product-card-02-phase-b-pb1-r01" or round_one.get("verdict") != "scope-expansion":
            failures.append("Round 01 receipt identity drifted")
        if [item.get("id") for item in receipt_specimens] != expected_round02_functional:
            failures.append("Round 01 receipt must preserve all forty-eight functional specimen IDs in order")
        if any(item.get("verdict") != "unreviewed" for item in receipt_specimens):
            failures.append("Round 01 receipt must not invent functional specimen verdicts")
        next_round = round_one.get("nextRoundContract", {})
        if (
            next_round.get("candidateRevision") != "product-card-02-phase-b-pb1-r02"
            or next_round.get("phaseAApplicationCount") != 32
            or next_round.get("functionalSpecimenCount") != 48
            or next_round.get("totalSpecimenCount") != 80
            or next_round.get("defaultVerdict") != "unreviewed"
            or next_round.get("canonicalPhaseAApprovalEffect") != "none"
            or next_round.get("staticByRule") != ["FS01", "FS02"]
        ):
            failures.append("Round 01 receipt does not preserve the eighty-specimen Round 02 contract")
        if round_one.get("productionAuthority") is not False:
            failures.append("Round 01 receipt cannot grant Phase B production authority")

    receipt_lineage_round02: dict[str, list[str]] = {}
    round_two_path = ROOT / "round-02-feedback.json"
    if not round_two_path.is_file() or sha(round_two_path) != ROUND02_RECEIPT_SHA:
        failures.append("missing or mutated exact Round 02 feedback receipt")
    else:
        round_two = read(round_two_path)
        round_two_specimens = round_two.get("specimens", [])
        phase_a_receipt = [item for item in round_two_specimens if item.get("scope") == "phase-a-inheritance"]
        functional_receipt = [item for item in round_two_specimens if item.get("scope") == "functional"]
        if round_two.get("candidateRevision") != "product-card-02-phase-b-pb1-r02" or round_two.get("verdict") != "round-feedback":
            failures.append("Round 02 receipt identity drifted")
        if round_two.get("reviewScope") != {"phaseAApplications": 32, "functionalCandidates": 48, "total": 80}:
            failures.append("Round 02 receipt scope drifted")
        if [item.get("sourcePhaseAId") for item in phase_a_receipt] != approved_phase_a:
            failures.append("Round 02 receipt must preserve all thirty-two Phase A inputs in order")
        if any(item.get("canonicalPhaseAVerdict") != "keep" or item.get("verdict") != "keep" for item in phase_a_receipt):
            failures.append("Round 02 receipt must preserve canonical Phase A keep status")
        if [item.get("id") for item in functional_receipt] != expected_round02_functional:
            failures.append("Round 02 receipt functional ID order drifted")
        if [item.get("id") for item in functional_receipt if item.get("verdict") == "kill"] != ["B-FT04"]:
            failures.append("Round 02 receipt must kill only B-FT04")
        receipt_lineage_round02 = {item.get("id"): item.get("phaseARefs", []) for item in functional_receipt}
        if any(not refs or set(refs) - set(approved_phase_a) for refs in receipt_lineage_round02.values()):
            failures.append("Round 02 lineage is missing or references unknown Phase A inputs")
        if round_two.get("productionAuthority") is not False:
            failures.append("Round 02 receipt cannot grant Phase B production authority")

    receipt_lineage_round03: dict[str, list[str]] = {}
    round03_keep_ids: list[str] = []
    round03_revise_ids: list[str] = []
    round_three_path = ROOT / "round-03-feedback.json"
    if not round_three_path.is_file() or sha(round_three_path) != ROUND03_RECEIPT_SHA:
        failures.append("missing or mutated exact Round 03 feedback receipt")
    else:
        round_three = read(round_three_path)
        specimens = round_three.get("specimens", [])
        if round_three.get("candidateRevision") != "product-card-02-phase-b-pb2-r03" or round_three.get("verdict") != "round-feedback":
            failures.append("Round 03 receipt identity drifted")
        if round_three.get("reviewScope") != {"phaseAVisualInputs": 32, "functionalCandidates": 47, "totalReviewCandidates": 47}:
            failures.append("Round 03 receipt scope drifted")
        if [item.get("id") for item in specimens] != expected_round03_functional:
            failures.append("Round 03 receipt must contain the forty-seven expected functional IDs in order")
        if any(item.get("scope") != "functional" for item in specimens):
            failures.append("Round 03 receipt must contain functional candidates only")
        verdict_counts = Counter(item.get("verdict") for item in specimens)
        if verdict_counts != Counter({"keep": 11, "revise": 35, "kill": 1}):
            failures.append("Round 03 receipt must record exactly 11 keep, 35 revise and 1 kill")
        if [item.get("id") for item in specimens if item.get("verdict") == "kill"] != ["B-FT06"]:
            failures.append("Round 03 receipt must kill only B-FT06")
        round03_keep_ids = [item.get("id") for item in specimens if item.get("verdict") == "keep"]
        round03_revise_ids = [item.get("id") for item in specimens if item.get("verdict") == "revise"]
        receipt_lineage_round03 = {item.get("id"): item.get("phaseARefs", []) for item in specimens}
        for specimen_id in expected_round03_functional:
            if receipt_lineage_round03.get(specimen_id) != receipt_lineage_round02.get(specimen_id):
                failures.append(f"Round 03 receipt changed Phase A lineage for {specimen_id}")
        if round_three.get("productionAuthority") is not False:
            failures.append("Round 03 receipt cannot grant Phase B production authority")

    round_four_path = ROOT / "round-04-feedback.json"
    if not round_four_path.is_file() or sha(round_four_path) != ROUND04_RECEIPT_SHA:
        failures.append("missing or mutated exact Round 04 approval receipt")
    else:
        round_four = read(round_four_path)
        specimens = round_four.get("specimens", [])
        if round_four.get("candidateRevision") != "product-card-02-phase-b-pb2-r04" or round_four.get("verdict") != "round-feedback":
            failures.append("Round 04 receipt identity drifted")
        if round_four.get("reviewScope") != {"phaseAVisualInputs": 32, "functionalCandidates": 46, "totalReviewCandidates": 46}:
            failures.append("Round 04 receipt scope drifted")
        if [item.get("id") for item in specimens] != expected_round04_functional:
            failures.append("Round 04 receipt must preserve all forty-six survivors in order")
        if Counter(item.get("verdict") for item in specimens) != Counter({"keep": 46}):
            failures.append("Round 04 receipt must record exactly forty-six keeps")
        if any(item.get("scope") != "functional" for item in specimens):
            failures.append("Round 04 receipt must contain functional specimens only")
        for item in specimens:
            if item.get("phaseARefs") != receipt_lineage_round03.get(item.get("id")):
                failures.append(f"Round 04 receipt changed Phase A lineage for {item.get('id')}")
        interpretation = round_four.get("agentInterpretation", {})
        if interpretation.get("verdictCounts") != {"keep": 46, "revise": 0, "kill": 0, "unreviewed": 0}:
            failures.append("Round 04 approval interpretation drifted")
        if round_four.get("productionAuthority") is not False:
            failures.append("submitted Round 04 feedback cannot itself grant production authority")

    specimen_contract = source.get("specimenContract", {})
    phase_a_inputs = specimen_contract.get("phaseAVisualInputs", {})
    functional_contract = specimen_contract.get("functionalSpecimens", {})
    if specimen_contract.get("totalCount") != 46 or specimen_contract.get("totalCount") != functional_contract.get("count"):
        failures.append("Round 04 must count exactly forty-six functional candidates only")
    if phase_a_inputs.get("count") != 32 or phase_a_inputs.get("sourceIds") != approved_phase_a:
        failures.append("Phase A visual inputs must exactly preserve all Round 10 keeps in order")
    if phase_a_inputs.get("role") != "approved-visual-inputs" or phase_a_inputs.get("round04CandidateCount") != 0:
        failures.append("the thirty-two Phase A keeps must be visual inputs with zero Round 04 candidates")
    if phase_a_inputs.get("staticByRule") != ["FS01", "FS02"]:
        failures.append("FS01 and FS02 must remain static by rule")
    authority_effect = phase_a_inputs.get("authorityEffect", "").lower()
    if not all(phrase in authority_effect for phrase in ("canonical approved phase a visual inputs", "not create separate round 04 candidates", "does not", "alter phase a approval")):
        failures.append("Phase A authority effect must separate visual inputs from Round 04 candidates")
    if functional_contract.get("round02Count") != 48 or functional_contract.get("round03Count") != 47 or functional_contract.get("count") != 46:
        failures.append("Round 04 must converge 48 Round 02 functions through 47 Round 03 candidates into 46 survivors")
    if functional_contract.get("survivorIds") != expected_round04_functional:
        failures.append("Round 04 survivor IDs must equal Round 03 functional IDs minus B-FT06")
    if functional_contract.get("killedIds") != ["B-FT04", "B-FT06"]:
        failures.append("B-FT04 and B-FT06 must be the cumulative killed functional specimens")
    if functional_contract.get("round03VerdictCounts") != {"keep": 11, "revise": 35, "kill": 1}:
        failures.append("source must preserve the exact Round 03 verdict counts")
    if functional_contract.get("round03KeepIds") != round03_keep_ids:
        failures.append("source must preserve all eleven Round 03 keep IDs in receipt order")
    if functional_contract.get("round03ReviseIds") != round03_revise_ids:
        failures.append("source must preserve all thirty-five Round 03 revise IDs in receipt order")
    expected_group_counts = {"B-DS": 8, "B-FT": 8, "B-PR": 10, "B-CK": 8, "B-BU": 8, "B-MB": 4}
    actual_group_counts = {item.get("prefix"): item.get("count") for item in functional_contract.get("groups", [])}
    if actual_group_counts != expected_group_counts:
        failures.append("Round 04 functional family counts drifted")
    treatment = functional_contract.get("round04Treatment", "").lower()
    if not all(phrase in treatment for phrase in ("round 03 keep", "round 03 revise", "remove b-ft06", "b-ft04", "no replacement")):
        failures.append("Round 04 treatment must preserve keeps, revise named work and remove both kills without replacements")
    for specimen_id in expected_round04_functional:
        refs = receipt_lineage_round03.get(specimen_id, [])
        if not refs or set(refs) - set(approved_phase_a):
            failures.append(f"Round 04 survivor {specimen_id} has invalid Phase A lineage")

    components = source.get("components", [])
    patterns = source.get("patterns", [])
    journeys = source.get("journeys", [])
    component_ids = [item.get("id") for item in components]
    pattern_ids = [item.get("id") for item in patterns]
    journey_ids = [item.get("id") for item in journeys]
    if len(components) != 15 or len(set(component_ids)) != 15:
        failures.append("exactly fifteen unique reusable component contracts required")
    if len(patterns) != 13 or len(set(pattern_ids)) != 13:
        failures.append("exactly thirteen unique website composition patterns required")
    if len(journeys) != 6 or len(set(journey_ids)) != 6:
        failures.append("exactly six unique journey fixtures required")
    for pattern in patterns:
        unknown = set(pattern.get("componentIds", [])) - set(component_ids)
        if unknown:
            failures.append(f"pattern {pattern.get('id')} references unknown components: {sorted(unknown)}")

    required_models = {"Product", "Offer", "Price", "Plan", "Bundle", "LineItem", "ProofRecord", "Checkout", "CommerceState", "MotionAllocation"}
    model_names = {item.get("name") for item in source.get("semanticModels", [])}
    if not required_models.issubset(model_names):
        failures.append("semantic commerce and proof model set is incomplete")
    required_offers = {"one-time", "subscription", "usage", "bundle", "enterprise", "trial", "waitlist", "free", "add-on"}
    if set(source.get("variantAxes", {}).get("offerTypes", [])) != required_offers:
        failures.append("offer-type axis must distinguish digital product, SaaS, enterprise, trial, waitlist, free, bundle and add-on")
    bento = next((item for item in components if item.get("name") == "ProductFeatureBento"), None)
    if not bento or "declared cell jobs" not in bento.get("anatomy", []) or "decorative filler cells" not in bento.get("prohibited", []):
        failures.append("bento contract must require typed jobs and prohibit decorative filler")

    programme = source.get("reviewProgramme", {})
    rounds = programme.get("rounds", [])
    round_r01 = next((item for item in rounds if item.get("id") == "PB1-R01"), {})
    round_r02 = next((item for item in rounds if item.get("id") == "PB1-R02"), {})
    round_r03 = next((item for item in rounds if item.get("id") == "PB2-R03"), {})
    round_r04 = next((item for item in rounds if item.get("id") == "PB2-R04"), {})
    if programme.get("currentRound") != "PB4":
        failures.append("PB4 must be the closed current programme round")
    if sum(item.get("count", 0) for item in round_r01.get("specimenGroups", [])) != 48:
        failures.append("PB1 Round 01 must preserve its forty-eight-specimen record")
    if sum(item.get("count", 0) for item in round_r02.get("specimenGroups", [])) != 80:
        failures.append("PB1 Round 02 must preserve its eighty-study evidence record")
    if round_r03.get("status") != "feedback-complete" or sum(item.get("count", 0) for item in round_r03.get("specimenGroups", [])) != 47:
        failures.append("PB2 Round 03 must be feedback-complete with forty-seven recorded candidates")
    if round_r04.get("status") != "feedback-complete-unanimous" or sum(item.get("count", 0) for item in round_r04.get("specimenGroups", [])) != 46:
        failures.append("PB2 Round 04 must preserve the forty-six unanimously kept specimens")
    if any(item.get("prefix") == "B-A-" for item in round_r04.get("specimenGroups", [])):
        failures.append("Phase A visual inputs cannot appear as Round 04 specimen candidates")
    if "championVariantByComponent" not in programme.get("feedbackCapture", []):
        failures.append("review contract must preserve a champion per component")
    if programme.get("feedbackReceipts") != [
        "brand-kit/expressions/product-card/phase-b/round-01-feedback.json",
        "brand-kit/expressions/product-card/phase-b/round-02-feedback.json",
        "brand-kit/expressions/product-card/phase-b/round-03-feedback.json",
        "brand-kit/expressions/product-card/phase-b/round-04-feedback.json",
    ]:
        failures.append("review programme must preserve the exact Round 01 through Round 04 receipts")
    round_pb3 = next((item for item in rounds if item.get("id") == "PB3"), {})
    round_pb4 = next((item for item in rounds if item.get("id") == "PB4"), {})
    if round_pb3.get("status") != "closed-with-explicit-follow-up" or round_pb4.get("status") != "complete-approved":
        failures.append("PB3 follow-up boundary and PB4 approval status must remain explicit")

    if source.get("responsive", {}).get("viewports") != [320, 375, 430, 768, 1024, 1280, 1440]:
        failures.append("canonical viewport proof set drifted")
    if source.get("responsive", {}).get("containers") != [240, 320, 480, 640, 960, 1160]:
        failures.append("container receiver proof set drifted")
    if source.get("motion", {}).get("maximumLivePerViewport") != 1:
        failures.append("only one focal live core is allowed")

    proof = json.dumps(source).lower()
    for phrase in ("illustrative", "fixture", "production stripe", "golden homepage", "synthetic sixth product", "exact static"):
        if phrase not in proof:
            failures.append("plan boundary missing: " + phrase)
    if any(key in proof for key in ("sk_live_", "sk_test_", "checkout.stripe.com", "api.stripe.com")):
        failures.append("Phase B plan contains payment-provider secrets or endpoints")

    required_workbench_names = ("index.html", "styles.css", "app.js", "functional-components.js", "phase-a-lineage.js")
    required_workbench = [WORKBENCH / name for name in required_workbench_names]
    for path in required_workbench:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append("missing Phase B workbench file: " + path.name)
    if all(path.is_file() for path in required_workbench):
        workbench_text = "\n".join(path.read_text(encoding="utf-8") for path in required_workbench)
        for phrase in ("Canonical 1.0.0", "Forty-six keeps.", "Keep", "data-family-note", "product-card-02-phase-b-pb2-r04"):
            if phrase not in workbench_text:
                failures.append("functional review proof missing: " + phrase)
        index_text = (WORKBENCH / "index.html").read_text(encoding="utf-8")
        app_text = (WORKBENCH / "app.js").read_text(encoding="utf-8")
        component_text = (WORKBENCH / "functional-components.js").read_text(encoding="utf-8")
        if "phase-a-inheritance" in index_text or "phase-a-inheritance" in app_text:
            failures.append("Round 04 cannot render the thirty-two Phase A inputs as duplicate candidates")
        if 'new Set(["B-FT04", "B-FT06"])' not in app_text:
            failures.append("Round 04 workbench must preserve the two killed IDs explicitly")
        if "functionalCandidateCount = 46" not in app_text or "phaseAVisualInputCount = 32" not in app_text:
            failures.append("Round 04 workbench scope must be 46 functional candidates and 32 visual inputs")
        if "approvalLocked = true" not in app_text or "Object.fromEntries(specimenIds.map((id) => [id, \"keep\"]))" not in app_text:
            failures.append("canonical workbench must lock all forty-six approved keep verdicts")
        if "phaseAVisualInputs: phaseAVisualInputCount" not in app_text or "totalReviewCandidates: functionalCandidateCount" not in app_text:
            failures.append("Round 04 feedback export must exclude Phase A visual inputs from candidate totals")
        active_specimen_ids = re.findall(r'\{\s*id:\s*"(B-(?:DS|FT|PR|CK|BU|MB)[0-9]{2})"\s*,\s*family:', component_text)
        if active_specimen_ids != expected_round04_functional:
            failures.append("functional component module must export the forty-six Round 04 survivors in receipt order")
        if len(active_specimen_ids) != len(set(active_specimen_ids)):
            failures.append("functional component module contains duplicate active specimen IDs")
        if "export const specimenCount = SPECS.length" not in component_text or "export const specimenIds = SPECS.map((spec) => spec.id)" not in component_text:
            failures.append("functional component module must export count and IDs from the active definitions")
        lineage_text = (WORKBENCH / "phase-a-lineage.js").read_text(encoding="utf-8")
        lineage_pairs = re.findall(r'^  "(B-(?:DS|FT|PR|CK|BU|MB)[0-9]{2})": \[([^\]]+)\],?$', lineage_text, flags=re.MULTILINE)
        lineage = {specimen_id: re.findall(r'"([A-Z]{2}[0-9]{2})"', values) for specimen_id, values in lineage_pairs}
        for specimen_id in expected_round04_functional:
            if lineage.get(specimen_id) != receipt_lineage_round03.get(specimen_id):
                failures.append(f"Round 04 survivor {specimen_id} lost Phase A lineage")
        for killed_id in ("B-FT04", "B-FT06"):
            if killed_id in lineage and lineage[killed_id] != receipt_lineage_round02.get(killed_id):
                failures.append(f"historical lineage drifted for {killed_id}")
        if specimen_contract.get("requiredWorkbenchModules") != ["phase-a-lineage.js"]:
            failures.append("Round 04 required workbench module contract drifted")
        if "canonicalPhaseAVerdict" in app_text or "B-A-${sourceId}" in app_text:
            failures.append("Round 04 feedback export still treats Phase A inputs as review candidates")
        for rejected in ("Search the pantry", "This is the map", "data-search", "data-filter"):
            if rejected in workbench_text:
                failures.append("rejected planning UI remains in functional workbench: " + rejected)
        external_urls = set(re.findall(r'https?://[^\s"\')]+', workbench_text)) - {"http://www.w3.org/2000/svg"}
        if external_urls:
            failures.append("external URL in Phase B workbench: " + ", ".join(sorted(external_urls)))

    old = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    build = subprocess.run([sys.executable, str(ROOT / "build_product_component_pantry.py")], cwd=REPO, capture_output=True, text=True)
    if build.returncode:
        failures.append("canonical build failed: " + (build.stderr or build.stdout).strip())
    new = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()}
    if old and old != new:
        failures.append("deterministic canonical rebuild changed output")
    for name, expected in (("round-03-feedback.json", ROUND03_RECEIPT_SHA), ("round-04-feedback.json", ROUND04_RECEIPT_SHA), ("review.json", APPROVAL_REVIEW_SHA)):
        packaged = DIST / name
        if not packaged.is_file() or sha(packaged) != expected:
            failures.append(f"canonical package did not preserve {name}")

    phase_a = subprocess.run([sys.executable, str(ROOT.parent / "verify_product_card_contract.py")], cwd=REPO, capture_output=True, text=True)
    if phase_a.returncode:
        failures.append("approved Phase A verification failed: " + (phase_a.stderr or phase_a.stdout).strip())

    if failures:
        print("MEZ PRODUCT CARD 02 · PHASE B 1.0.0: FAIL")
        for failure in failures:
            print("- " + failure)
        return 1
    print("MEZ PRODUCT CARD 02 · PHASE B 1.0.0: PASS")
    print("- approved Phase A inputs resolve correctly")
    print(f"- exact Round 03 receipt preserved: {ROUND03_RECEIPT_SHA}")
    print("- Round 03 records 11 keep, 35 revise and 1 kill")
    print(f"- exact Round 04 approval receipt preserved: {ROUND04_RECEIPT_SHA}")
    print("- thirty-two canonical Phase A keeps remain approved visual inputs, not candidates")
    print("- forty-six functional specimens are unanimously approved across six families; B-FT04 and B-FT06 are removed")
    print("- every surviving Phase A lineage reference is preserved")
    print("- H-EXP-04B-CARD-FUNCTIONAL-PROOF is approved through DEC-PRODUCT-COMPONENT-SYSTEM-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
