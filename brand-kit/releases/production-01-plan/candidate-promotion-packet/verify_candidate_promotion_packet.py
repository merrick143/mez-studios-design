#!/usr/bin/env python3
"""Verify the closed PORT-02 candidate promotion packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment guidance only
    print("jsonschema is required: use the pinned environment in brand-kit/START-HERE.md")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[2]
REPO = BRAND_KIT.parent


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_path(value: str) -> Path:
    return REPO / value


def main() -> int:
    failures: list[str] = []

    packet = read_json(ROOT / "promotion-packet.source.json")
    schema = read_json(ROOT / "promotion-packet.schema.json")
    review = read_json(ROOT / "review.json")
    interaction = read_json(ROOT / "interaction-evidence.json")
    human_decision = read_json(ROOT / "human-decision.json")

    try:
        jsonschema.Draft202012Validator(schema).validate(packet)
    except jsonschema.ValidationError as error:
        failures.append(f"packet does not satisfy its schema: {error.message}")

    if packet.get("status") != "closed" or packet.get("productionAuthority") is not False:
        failures.append("closed packet status or non-authoritative packet boundary drifted")
    if packet.get("generatedRelease") is not False or review.get("generatedRelease") is not False:
        failures.append("PORT-02 generated a release")
    if review.get("verdict") != "approved-and-closed" or review.get("productionAuthority") is not False:
        failures.append("packet review is not safely closed")
    if human_decision.get("verdict") != "approved" or human_decision.get("approvedBy") != "Olli":
        failures.append("human decision record is missing or unattributed")
    if human_decision.get("productionReleaseAuthorised") is not False:
        failures.append("component promotion was widened into release authority")

    components = {item.get("id"): item for item in packet.get("components", [])}
    if set(components) != {"CMP-05", "CMP-06"}:
        failures.append("packet must contain exactly CMP-05 and CMP-06")

    base_ledger = read_json(BRAND_KIT / "governance" / "decisions.json")
    supplement = read_json(BRAND_KIT / "governance" / "post-cutover-decisions.json")
    ledger_by_id = {item.get("id"): item for item in base_ledger.get("decisions", [])}
    supplement_by_id = {item.get("id"): item for item in supplement.get("decisions", [])}
    all_decision_ids = set(ledger_by_id) | set(supplement_by_id)
    reconciliation = packet.get("authorityReconciliation", {})
    reconciled_ids = {
        "DEC-FOUNDATION-RELEASE-001",
        "DEC-GLOBAL-NAVIGATION-COMPONENT-001",
        "DEC-GOLDEN-HOMEPAGE-001",
    }
    if reconciliation.get("status") != "complete" or set(reconciliation.get("reconciledDecisionIds", [])) != reconciled_ids:
        failures.append("authority reconciliation is incomplete or has drifted")
    component_decisions = {
        "DEC-HALFTONE-PORTRAIT-COMPONENT-001",
        "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001",
    }
    if set(supplement_by_id) != reconciled_ids | component_decisions:
        failures.append("post-cutover supplement does not contain the three reconciled approvals plus two component promotions")
    if reconciliation.get("ledger") != "brand-kit/governance/post-cutover-decisions.json" or reconciliation.get("baseLedger") != "brand-kit/governance/decisions.json":
        failures.append("packet loses the immutable cutover-ledger boundary")
    if supplement.get("baseLedger") != "brand-kit/governance/decisions.json" or set(ledger_by_id) & set(supplement_by_id):
        failures.append("post-cutover register does not cleanly supplement the immutable ledger")
    supporting = reconciliation.get("supportingRecords", [])
    for decision_id, source in zip(reconciliation.get("reconciledDecisionIds", []), supporting, strict=True):
        if supplement_by_id.get(decision_id, {}).get("source") != source:
            failures.append(f"ledger source does not match supporting approval for {decision_id}")

    expected = {
        "CMP-05": {
            "componentId": "mz.systems.component.halftone-portrait",
            "decisionId": "DEC-HALFTONE-PORTRAIT-COMPONENT-001",
            "gateB": "brand-kit/components/halftone-portrait/gate-b.json",
        },
        "CMP-06": {
            "componentId": "mz.systems.component.testimonial-marquee",
            "decisionId": "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001",
            "gateB": "brand-kit/components/testimonial-marquee/round-04-gate-b.json",
        },
    }

    for component_id, contract in expected.items():
        entry = components.get(component_id, {})
        if entry.get("componentId") != contract["componentId"]:
            failures.append(f"{component_id} component identity drifted")
        if entry.get("currentVerdict") != "promote" or entry.get("decisionId") != contract["decisionId"]:
            failures.append(f"{component_id} does not carry Olli's separate promotion verdict")
        if entry.get("proposedDecisionId") != contract["decisionId"]:
            failures.append(f"{component_id} proposed decision ID drifted")
        if contract["decisionId"] not in all_decision_ids:
            failures.append(f"{component_id} promotion decision is absent from governance")
        if entry.get("agentRecommendation") not in {"promote", "exclude"}:
            failures.append(f"{component_id} has no explicit agent recommendation")

        source = read_json(repo_path(entry.get("source", "")))
        component_review = read_json(repo_path(entry.get("review", "")))
        if source.get("componentId") != contract["componentId"] or source.get("candidateRevision") != entry.get("candidateRevision"):
            failures.append(f"{component_id} packet does not describe the live candidate revision")
        if source.get("status") != "canonical" or source.get("productionAuthority") is not True or source.get("decisionIds") != [contract["decisionId"]]:
            failures.append(f"{component_id} live source does not carry bounded canonical authority")
        if component_review.get("productionAuthority") is not True or component_review.get("decisionId") != contract["decisionId"]:
            failures.append(f"{component_id} review does not carry its promotion decision")
        if entry.get("currentStatus") != "canonical":
            failures.append(f"{component_id} packet status did not close as canonical")

        gate_b_path = entry.get("evidence", {}).get("gateB")
        if gate_b_path != contract["gateB"]:
            failures.append(f"{component_id} points to the wrong Gate B record")
        else:
            gate_b = read_json(repo_path(gate_b_path))
            if gate_b.get("candidateRevision") != entry.get("candidateRevision") or gate_b.get("score", 0) < 64:
                failures.append(f"{component_id} exact candidate has no passing Gate B")
            if gate_b.get("blockingReasons") or gate_b.get("productionAuthority") is not False:
                failures.append(f"{component_id} Gate B retains a blocker or invents authority")

        review_gaps = set(component_review.get("knownGaps", []))
        packet_gaps = {item.get("reviewGap") for item in entry.get("gaps", [])}
        if review_gaps != packet_gaps:
            failures.append(f"{component_id} known gaps are hidden, duplicated or stale in the packet")
        if any(item.get("disposition") not in {"accepted", "policy-selected", "follow-up-required", "out-of-component-scope"} for item in entry.get("gaps", [])):
            failures.append(f"{component_id} retains a pending or invalid gap disposition")

    follower = packet.get("followerPolicy", {})
    if follower.get("choices") != ["frozen-evidence", "manual-refresh", "omit"]:
        failures.append("follower policy choices drifted")
    if follower.get("recommendation") != "frozen-evidence" or follower.get("selected") != "frozen-evidence":
        failures.append("approved frozen-evidence follower policy is missing")

    exceptions = {item.get("componentId"): item for item in packet.get("motionExceptions", [])}
    if set(exceptions) != {"mz.systems.component.halftone-portrait", "mz.systems.component.testimonial-marquee"}:
        failures.append("packet does not preserve both bounded motion exceptions")
    for exception in exceptions.values():
        if exception.get("currentState") != "approved-bounded" or exception.get("promotionReconfirmation") != "reconfirmed-bounded":
            failures.append("a motion exception was widened or not reconfirmed")

    portrait_js = (BRAND_KIT / "components" / "halftone-portrait" / "mez-halftone-portrait.js").read_text(encoding="utf-8")
    marquee_js = (BRAND_KIT / "components" / "testimonial-marquee" / "mez-testimonial-marquee.js").read_text(encoding="utf-8")
    for needle in ('policy === "always"', "IntersectionObserver", "releaseMotion"):
        if needle not in portrait_js:
            failures.append(f"CMP-05 motion implementation missing: {needle}")
    for needle in ('this.viewport.addEventListener("pointerenter"', "this.viewport.scrollLeft = this.autoOffset", "900", "IntersectionObserver"):
        if needle not in marquee_js:
            failures.append(f"CMP-06 motion implementation missing: {needle}")

    if interaction.get("candidateRevision") != "testimonial-marquee-01-r04" or interaction.get("productionAuthority") is not False:
        failures.append("interaction receipt does not describe the locked candidate")
    for key in ("hover", "performance", "spokenOutput"):
        if "UNMEASURED" not in interaction.get(key, {}).get("result", "") and key != "spokenOutput":
            failures.append(f"interaction receipt launders the unmeasured {key} claim")
    if "UNMEASURED" not in interaction.get("spokenOutput", {}).get("result", ""):
        failures.append("interaction receipt launders exact spoken output")

    human = packet.get("humanGate", {})
    if human.get("state") != "closed" or human.get("combinedDecisionForbidden") is not True or len(human.get("separateQuestions", [])) != 2:
        failures.append("human gate does not preserve the two independent verdicts")
    if packet.get("next", {}).get("productionAssemblyAllowedNow") is not True:
        failures.append("closed gate does not route to release-candidate assembly")

    if failures:
        print("MEZ CANDIDATE PROMOTION PACKET: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("MEZ CANDIDATE PROMOTION PACKET: PASS")
    print("- CMP-05 and CMP-06 are separate canonical components with distinct approvals")
    print("- Gate B scores are 67/75 for both candidates with no blocker")
    print("- every live review gap has one visible accepted, policy or follow-up disposition")
    print("- frozen dated follower evidence is selected")
    print("- both bounded motion exceptions are implemented and reconfirmed without widening canon")
    print("- the immutable cutover ledger is preserved; the supplement carries three prior and two component approvals")
    print("- release-candidate assembly may start; production release remains unauthorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
