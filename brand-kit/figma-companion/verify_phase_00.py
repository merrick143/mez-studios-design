#!/usr/bin/env python3
"""Verify the Figma Phase 0 discovery and consumer-last sequence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


discovery = load(HERE / "phase-00-discovery.json")
approval = load(HERE / "phase-00-approval.json")
sequence = load(BRAND_KIT / "docs/consumer-transition-sequence.json")
priority = load(BRAND_KIT / "docs/product-ui-priority-sequence.json")
status = load(BRAND_KIT / "data/status.json")
fig_task = load(BRAND_KIT / "llm/tasks/TASK-FIG-01-FIGMA-COMPANION.json")
port_task = load(BRAND_KIT / "llm/tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json")
manifest_path = BRAND_KIT / "releases/production-01/1.0.0-rc.1/manifest.json"

expect(discovery["mutationCount"] == 0, "Phase 0 must remain read-only")
historical = discovery["historicalFigma"]
for key in ("localVariableCollections", "localVariables", "localTextStyles", "localEffectStyles", "localPaintStyles", "components", "componentSets"):
    expect(historical[key] == 0, f"historical Figma inventory drifted for {key}")
expect(historical["treatment"] == "retain-as-research-only", "historical Figma must remain research-only")
expect(discovery["canonicalInventory"]["phaseBComponents"] == 15, "Phase B component count mismatch")
expect(len(discovery["canonicalInventory"]["expressionFamilies"]) == 5, "expression-family count mismatch")
expect(len(discovery["canonicalInventory"]["standaloneComponents"]) == 3, "standalone component count mismatch")
expect(approval["gateId"] == "H-FIG-01-FIGMA-COMPANION-SCOPE", "Phase 0 approval gate mismatch")
expect(approval["status"] == "approved" and approval["approvedBy"] == "Olli", "Phase 0 must have Olli's approval")
expect(fig_task["status"] in {"in-progress", "complete"}, "FIG-01 must progress from the approved Phase 0 scope")
expect(status["nextTask"] == "TASK-PORT-04-NAMED-CONSUMER-PROOF", "current status must advance to the final Product UI priority-sequence task")

ordered = [item["taskId"] for item in sequence["orderedWork"]]
expect(ordered == [
    "TASK-FIG-01-FIGMA-COMPANION",
    "TASK-CHAN-01-FIRST-RELEASE-CHANNEL-SYSTEMS",
    "TASK-CERT-01-SYSTEM-CERTIFICATION",
    "TASK-PORT-04-NAMED-CONSUMER-PROOF",
], "consumer-last programme sequence mismatch")
expect(priority["activeSequence"] == [
    "TASK-UI-01-PRODUCT-UI-DATA-VISUALISATION",
    "TASK-CERT-01-SYSTEM-CERTIFICATION",
    "TASK-PORT-04-NAMED-CONSUMER-PROOF",
], "later Product UI priority sequence mismatch")
expect(port_task["dependencies"][:3] == [
    "TASK-FIG-01-FIGMA-COMPANION",
    "TASK-UI-01-PRODUCT-UI-DATA-VISUALISATION",
    "TASK-CERT-01-SYSTEM-CERTIFICATION",
], "PORT-04 must apply the current Figma, Product UI and certification dependencies")

manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
expect(manifest_hash == sequence["frozenMilestone"]["manifestSha256"], "approved rc.1 manifest bytes changed")
expect(sequence["authority"]["productionAuthority"] is False, "sequence must not claim production authority")

print("FIGMA PHASE 0: PASS")
print("- historical Figma file remains read-only research evidence")
print("- canonical source inventory and proposed mirror scope are recorded")
print("- rc.1 remains byte-identical and PORT-04 is sequenced last")
print("- later SEQ-PRODUCT-UI-FIRST-001 changes current priority without rewriting the original consumer-last record")
print("- H-FIG-01-FIGMA-COMPANION-SCOPE remains the valid scope approval for the completed FIG-01 build")
