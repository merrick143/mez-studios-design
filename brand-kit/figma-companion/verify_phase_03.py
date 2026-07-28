#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT / "figma-companion/phase-03-identity-expressions.json").read_text())
state = json.loads((ROOT / "figma-companion/build-state.json").read_text())

assert record["taskId"] == "TASK-FIG-01-FIGMA-COMPANION"
assert record["status"] == "complete"
assert record["fileKey"] == state["file"]["fileKey"] == "QxZT3FJ8BDXOZfBQDt0qPW"
assert record["authority"] == {
    "figmaRole": "companion-mirror",
    "historicalFileMutated": False,
    "frozenReleaseMutated": False,
    "runtimeAssetsRemainRepositoryOwned": True,
}
assert len(record["pages"]) == 6
assert all(page["visualInspection"] == "pass" for page in record["pages"])
assert record["liveAudit"] == {
    "method": "Figma Plugin API whole-file traversal plus rendered screenshot inspection of all six Phase 3 pages",
    "pages": 10,
    "nodes": 1030,
    "components": 29,
    "componentSets": 6,
    "instances": 29,
    "textNodes": 469,
    "missingFontTextNodes": 0,
    "phase3TaggedNodes": 70,
    "temporaryUploadNodes": 0,
}
assert set(record["componentSets"]) == {
    "Product Material",
    "Wings & Mark",
    "Disc",
    "Sphere · Colour Fallback",
    "Product Card Grammar",
    "Trading Card",
}
assert record["componentSets"] == state["entities"]["components"]
assert record["assetTruth"]["temporaryUploadNodesRemaining"] == 0
assert "exact colour fallback" in record["runtimeBoundaries"][0]
assert "phase3-live-audit" in state["completedSteps"]
assert state["phase"] in {"phase4", "final-review", "complete"}

print("PASS: Figma companion Phase 3 identity and expression receipt is internally consistent")
