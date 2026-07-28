#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / "figma-companion/phase-01-foundations.json").read_text())
state = json.loads((ROOT / "figma-companion/build-state.json").read_text())
task = json.loads((ROOT / "llm/tasks/TASK-FIG-01-FIGMA-COMPANION.json").read_text())

assert record["taskId"] == task["taskId"] == "TASK-FIG-01-FIGMA-COMPANION"
assert record["status"] == "complete"
assert record["file"]["fileKey"] == state["file"]["fileKey"] == "QxZT3FJ8BDXOZfBQDt0qPW"
assert record["authority"]["figmaRole"] == "companion-mirror"
assert record["authority"]["figmaCreatesIndependentAuthority"] is False
assert record["authority"]["historicalFileMutated"] is False
assert record["authority"]["frozenReleaseMutated"] is False

audit = record["liveAudit"]
assert audit == {
    "method": "Figma Plugin API inspection after construction",
    "collections": 8,
    "variables": 255,
    "semanticAliasValues": 215,
    "brokenAliases": 0,
    "missingWebCodeSyntax": 0,
    "implicitAllScopes": 0,
    "textStyles": 15,
    "effectStyles": 5,
}
assert sum(collection["variables"] for collection in record["collections"]) == audit["variables"]
assert len(record["collections"]) == audit["collections"]
assert len(record["styles"]["text"]) == audit["textStyles"]
assert len(record["styles"]["effect"]) == audit["effectStyles"]
assert state["entities"]["variables"]["brokenAliases"] == 0
assert state["entities"]["variables"]["missingWebCodeSyntax"] == 0
assert state["entities"]["variables"]["implicitAllScopes"] == 0
assert "phase1-live-audit" in state["completedSteps"]
assert task["status"] in {"in-progress", "complete"}

print("PASS: Figma companion Phase 1 foundations receipt is internally consistent")
