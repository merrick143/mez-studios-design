#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / "figma-companion/phase-02-documentation.json").read_text())
state = json.loads((ROOT / "figma-companion/build-state.json").read_text())

assert record["taskId"] == "TASK-FIG-01-FIGMA-COMPANION"
assert record["status"] == "complete"
assert record["fileKey"] == state["file"]["fileKey"] == "QxZT3FJ8BDXOZfBQDt0qPW"
assert record["authority"] == {
    "figmaRole": "companion-mirror",
    "historicalFileMutated": False,
    "frozenReleaseMutated": False,
}
assert [page["name"] for page in record["pages"]] == [
    "00 · Cover",
    "01 · Foundations",
    "02 · Responsive & Runtime",
    "03 · Source & Governance",
]
assert all(page["width"] == 1440 and page["visualInspection"] == "pass" for page in record["pages"])
assert record["liveAudit"] == {
    "method": "Figma Plugin API page traversal plus rendered screenshot inspection",
    "pages": 4,
    "textNodes": 409,
    "variableBoundNodes": 638,
    "missingFontTextNodes": 0,
    "components": 0,
    "instances": 0,
}
for page in record["pages"]:
    assert state["entities"]["pages"][page["name"]] == {
        "pageId": page["pageId"],
        "rootId": page["rootId"],
    }
assert len(record["visualRepairs"]) == 3
assert "phase2-live-audit" in state["completedSteps"]

print("PASS: Figma companion Phase 2 documentation receipt is internally consistent")
