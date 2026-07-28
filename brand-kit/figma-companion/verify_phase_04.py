#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / "figma-companion/phase-04-functional-components.json").read_text())
gate = json.loads((ROOT / "figma-companion/phase-04-gate-b.json").read_text())
state = json.loads((ROOT / "figma-companion/build-state.json").read_text())
task = json.loads((ROOT / "llm/tasks/TASK-FIG-01-FIGMA-COMPANION.json").read_text())
channel_task = json.loads((ROOT / "llm/tasks/TASK-CHAN-01-FIRST-RELEASE-CHANNEL-SYSTEMS.json").read_text())
ui_task = json.loads((ROOT / "llm/tasks/TASK-UI-01-PRODUCT-UI-DATA-VISUALISATION.json").read_text())
cert_task = json.loads((ROOT / "llm/tasks/TASK-CERT-01-SYSTEM-CERTIFICATION.json").read_text())
priority = json.loads((ROOT / "docs/product-ui-priority-sequence.json").read_text())
fixture = json.loads((ROOT / "components/testimonial-marquee/fixtures/ai-os-testimonials.json").read_text())
approval = json.loads((ROOT / "figma-companion/approval.json").read_text())
status = json.loads((ROOT / "data/status.json").read_text())

expected_variants = {
    "ProductDiscoveryCard": 7,
    "ProductFeatureCard": 6,
    "ProductProofCard": 7,
    "ProductFeatureBento": 4,
    "ProductPricingCard": 8,
    "ProductPlanComparison": 4,
    "ProductCheckoutSummary": 6,
    "ProductBundleOffer": 6,
    "ProductBundleBuilder": 5,
    "ProductUpsellRow": 5,
    "ProductMobileStickySummary": 5,
    "ProductFamilyMatrix": 5,
    "ProductMenuItem": 5,
    "ProductFooterCTA": 5,
    "ProductPurchaseConfirmation": 5,
    "Global Navigation": 14,
    "Halftone Portrait": 4,
    "Testimonial Marquee": 4,
}

assert record["taskId"] == task["taskId"] == "TASK-FIG-01-FIGMA-COMPANION"
assert record["status"] == "complete"
assert record["fileKey"] == state["file"]["fileKey"] == "QxZT3FJ8BDXOZfBQDt0qPW"
assert record["authority"]["figmaRole"] == "companion-mirror"
assert record["authority"]["productionAuthority"] is False
assert record["authority"]["historicalFileMutated"] is False
assert record["authority"]["frozenReleaseMutated"] is False
assert {name: item["variants"] for name, item in record["componentSets"].items()} == expected_variants
assert record["componentSummary"] == {
    "componentSets": 18,
    "variants": 105,
    "canonicalPhaseBContracts": 15,
    "runtimeStaticTwinContracts": 3,
    "allExpectedVariantCountsPass": True,
    "allSetsExposeComponentProperties": True,
}
assert sum(expected_variants.values()) == 105
assert record["detachAudit"]["setsTested"] == record["detachAudit"]["passed"] == 18
assert record["detachAudit"]["failed"] == 0
assert record["liveAudit"]["missingFontTextNodes"] == 0
assert record["liveAudit"]["temporaryUploadNodes"] == 0

kayvon = next(item for item in fixture["testimonials"] if item["id"] == "kayvon-jafarzadeh")
assert record["contentTruth"] == {
    "sampleRecordId": kayvon["id"],
    "name": kayvon["name"],
    "username": kayvon["handle"],
    "followers": kayvon["social"]["followers"],
    "verified": kayvon["social"]["verified"],
    "quote": kayvon["quote"],
    "method": "Exact values read from the approved repository fixture; the earlier placeholder identity, quote and follower count were removed before review.",
}
assert "static twin" in record["runtimeStaticTwins"]["Testimonial Marquee"]["boundary"]
assert "execute in repository code" in record["runtimeStaticTwins"]["Global Navigation"]["boundary"]
assert gate["verdict"] == "gate-b"
assert gate["productionAuthority"] is False
assert gate["score"]["weighted"] >= 64
assert gate["score"]["verdict"] == "pass"
assert all(test["result"] == "pass" for test in gate["tests"].values())
assert gate["readyForOlliReview"] is True
assert state["phase"] == "complete"
assert state["step"] == "H-FIG-02-closed"
assert state["pendingValidations"] == []
assert state["entities"]["functionalComponents"] == record["componentSets"]
assert task["status"] == "complete"
assert task["humanGate"]["gateId"] == record["next"] == "H-FIG-02-FIGMA-COMPANION-APPROVAL"
assert approval["taskId"] == task["taskId"]
assert approval["gateId"] == record["next"]
assert approval["verdict"] == "approved" and approval["approvedBy"] == "Olli"
assert approval["fileKey"] == record["fileKey"]
assert approval["productionAuthority"] is False
assert approval["canonicalAuthority"] is False
assert approval["nextTask"] == channel_task["taskId"]
assert channel_task["status"] == "blocked"
assert priority["activeSequence"][0] == ui_task["taskId"]
assert cert_task["status"] == "complete"
assert status["nextTask"] == priority["activeSequence"][2] == "TASK-PORT-04-NAMED-CONSUMER-PROOF"
assert ui_task["status"] == "complete"

print("PASS: Figma companion Phase 4 evidence and H-FIG-02 approval are internally consistent")
