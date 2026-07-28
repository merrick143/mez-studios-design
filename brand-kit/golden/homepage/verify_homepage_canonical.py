#!/usr/bin/env python3
"""Verify the bounded canonical promotion of Golden Homepage 1.0.0."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "homepage.source.json"
SCHEMA = ROOT / "homepage.schema.json"
REVIEW = ROOT / "review.json"
APPROVAL = ROOT / "round-29-approval.json"
ROADMAP = BRAND_KIT / "docs" / "ROADMAP.md"
CURRENT_STATE = BRAND_KIT / "docs" / "CURRENT-STATE.md"


def validate(source: dict, review: dict, approval: dict, roadmap: str, current_state: str) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, code: str, message: str) -> None:
        if not condition:
            failures.append(f"{code}: {message}")

    require(source.get("version") == "1.0.0", "SOURCE", "homepage version is not 1.0.0")
    require(source.get("status") == "canonical", "SOURCE", "homepage status is not canonical")
    require(source.get("productionAuthority") is False, "BOUNDARY", "unreleased homepage must not claim consumer production authority")
    require(source.get("decisionId") == "DEC-GOLDEN-HOMEPAGE-001", "SOURCE", "canonical decision ID is missing")
    require(source.get("humanGate", {}).get("status") == "approved", "GATE", "homepage human gate is not approved")
    require(len(source.get("approval", {}).get("releaseBlockers", [])) >= 3, "BOUNDARY", "release blockers are not explicit")

    require(review.get("verdict") == "approved", "REVIEW", "review verdict is not approved")
    require(review.get("resultingStatus") == "canonical", "REVIEW", "review does not produce canonical status")
    require(review.get("decisionId") == "DEC-GOLDEN-HOMEPAGE-001", "REVIEW", "review decision ID is missing")
    require(review.get("productionAuthority") is False, "BOUNDARY", "review overstates production authority")

    require(approval.get("verdict") == "approved", "APPROVAL", "human approval record is not approved")
    require(approval.get("approvedBy") == "Olli", "APPROVAL", "human approver is not Olli")
    require(approval.get("decisionId") == "DEC-GOLDEN-HOMEPAGE-001", "APPROVAL", "approval decision ID is missing")
    require(approval.get("nextTask") == "TASK-PORT-01-RELEASE-BOUNDARY", "NEXT", "approval does not route to the release-boundary task")

    require("TASK-PORT-01-RELEASE-BOUNDARY" in roadmap and "complete" in roadmap, "NEXT", "roadmap does not preserve the completed release-boundary task")
    require("TASK-PORT-02-HOMEPAGE-DEPENDENCY-GATES" in roadmap and "TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY" in roadmap, "NEXT", "roadmap does not preserve PORT-02 and route to PORT-03")
    require("TASK-PORT-02-HOMEPAGE-DEPENDENCY-GATES" in current_state and "TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY" in current_state, "NEXT", "current state does not preserve PORT-02 and route to PORT-03")
    require("H-GOLD-01-HOMEPAGE-PROOF` is closed" in roadmap, "GATE", "roadmap does not close the homepage gate")

    return failures


def load() -> tuple[dict, dict, dict, str, str]:
    return (
        json.loads(SOURCE.read_text(encoding="utf-8")),
        json.loads(REVIEW.read_text(encoding="utf-8")),
        json.loads(APPROVAL.read_text(encoding="utf-8")),
        ROADMAP.read_text(encoding="utf-8"),
        CURRENT_STATE.read_text(encoding="utf-8"),
    )


def self_test(data: tuple[dict, dict, dict, str, str]) -> int:
    source, review, approval, roadmap, current_state = data
    old_source = copy.deepcopy(source)
    old_source["productionAuthority"] = True
    failures = validate(old_source, review, approval, roadmap, current_state)
    if not any(item.startswith("BOUNDARY:") for item in failures):
        print("GOLDEN HOMEPAGE CANONICAL SELF-TEST: FAIL")
        print("- production-authority overclaim mutation was not caught")
        return 1
    print("GOLDEN HOMEPAGE CANONICAL SELF-TEST: PASS")
    print("- production-authority overclaim fails in memory")
    return 0


def main() -> int:
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE CANONICAL: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("GOLDEN HOMEPAGE CANONICAL: PASS")
    print("- H-GOLD-01-HOMEPAGE-PROOF closed by DEC-GOLDEN-HOMEPAGE-001")
    print("- Golden Homepage 1.0.0 is canonical as a design reference and remains unreleased")
    print("- the approval routes historically to completed PORT-01; current state and roadmap now route to PORT-04 consumer registration and proof")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
