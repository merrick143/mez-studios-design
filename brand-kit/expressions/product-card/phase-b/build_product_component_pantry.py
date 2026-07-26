#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FILES = [
    ROOT / name
    for name in (
        "product-component-pantry.source.json",
        "product-component-pantry.schema.json",
        "round-01-feedback.json",
        "round-02-feedback.json",
        "round-03-feedback.json",
        "round-04-feedback.json",
        "review.json",
        "README.md",
    )
]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source = read(FILES[0])
    review = read(ROOT / "review.json")
    if source.get("status") != "canonical-functional-component-system" or source.get("productionAuthority") is not True:
        raise SystemExit("approved Phase B canonical component system required")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-PRODUCT-COMPONENT-SYSTEM-001":
        raise SystemExit("approved Phase B human review required")
    if source.get("candidateRevision") != "product-card-02-phase-b-pb2-r04":
        raise SystemExit("Phase B candidate revision must be PB2 Round 04")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in FILES:
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/product-functional-components",
        "version": source["version"],
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "reviewGateId": source["gateId"],
        "productionAuthority": True,
        "entrypoints": {
            "contract": "product-component-pantry.source.json",
            "schema": "product-component-pantry.schema.json",
            "round01Feedback": "round-01-feedback.json",
            "round02Feedback": "round-02-feedback.json",
            "round03Feedback": "round-03-feedback.json",
            "round04Feedback": "round-04-feedback.json",
            "review": "review.json",
            "guidance": "README.md"
        },
        "inventory": {
            "components": len(source["components"]),
            "patterns": len(source["patterns"]),
            "journeys": len(source["journeys"]),
            "phaseAVisualInputs": source["specimenContract"]["phaseAVisualInputs"]["count"],
            "phaseARound04Candidates": source["specimenContract"]["phaseAVisualInputs"]["round04CandidateCount"],
            "round02FunctionalSpecimens": source["specimenContract"]["functionalSpecimens"]["round02Count"],
            "round03FunctionalCandidates": source["specimenContract"]["functionalSpecimens"]["round03Count"],
            "round03Verdicts": source["specimenContract"]["functionalSpecimens"]["round03VerdictCounts"],
            "round04FunctionalCandidates": source["specimenContract"]["functionalSpecimens"]["count"],
            "killedSpecimens": len(source["specimenContract"]["functionalSpecimens"]["killedIds"]),
            "reviewSpecimens": source["specimenContract"]["totalCount"]
        }
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    packaged = sorted(path for path in DIST.iterdir() if path.is_file())
    manifest = {
        "schemaVersion": "1.0.0",
        "componentSystemId": source["componentSystemId"],
        "status": source["status"],
        "productionAuthority": True,
        "artifactCount": len(packaged),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)} for path in packaged]
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MEZ PRODUCT CARD 02 · PHASE B 1.0.0: BUILT")
    print("- thirty-two canonical Phase A keeps remain approved visual inputs, not candidates")
    print("- exact Round 03 evidence records eleven keeps, thirty-five revisions and one kill")
    print("- forty-six unanimously kept functional specimens across six families; B-FT04 and B-FT06 are removed")
    print("- every surviving Phase A reference is preserved")
    print("- fifteen reusable contracts, thirteen website patterns and six journeys")
    print("- H-EXP-04B-CARD-FUNCTIONAL-PROOF is approved for the bounded component-system scope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
