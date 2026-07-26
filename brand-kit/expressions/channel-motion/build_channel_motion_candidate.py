#!/usr/bin/env python3
"""Build the deterministic canonical EXP-07 website-motion package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "channel-motion.source.json"
SCHEMA = ROOT / "channel-motion.schema.json"
README = ROOT / "README.md"
REVIEW = ROOT / "review.json"
FEEDBACK = [ROOT / f"round-{number:02d}-feedback.json" for number in (1, 2, 3)]
DIST = ROOT / "dist"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        raise SystemExit("website-motion build requires canonical status and true bounded authority")
    if review.get("verdict") != "approve-with-deferral" or review.get("productionAuthority") is not True:
        raise SystemExit("website-motion build requires the approved human review")
    if review.get("decisionId") not in source.get("decisionIds", []):
        raise SystemExit("approved website-motion decision is missing from the source contract")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW, *FEEDBACK):
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/website-motion",
        "version": source["version"],
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "reviewGateId": source["candidateGateId"],
        "decisionId": review["decisionId"],
        "productionReadyForScope": True,
        "productionAuthority": True,
        "entrypoints": {
            "contract": "channel-motion.source.json",
            "schema": "channel-motion.schema.json",
            "guidance": "README.md",
            "review": "review.json",
            "round01Feedback": "round-01-feedback.json",
            "round02Feedback": "round-02-feedback.json",
            "round03Feedback": "round-03-feedback.json"
        },
        "deferredTaskId": "TASK-CMP-01-GLOBAL-NAVIGATION",
        "note": "Canonical seven-specimen website-motion grammar. The menu component remains separate and deferred."
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    paths = sorted(path for path in DIST.iterdir() if path.is_file() and path.name != "manifest.json")
    manifest = {
        "schemaVersion": "1.0.0",
        "expressionId": source["expressionId"],
        "version": source["version"],
        "status": source["status"],
        "decisionId": review["decisionId"],
        "productionAuthority": True,
        "artifactCount": len(paths),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)} for path in paths]
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MEZ WEBSITE MOTION 1.0.0: BUILT")
    print("- 3 motion laws and 4 component behaviours approved")
    print("- MOT-W02 deferred to TASK-CMP-01-GLOBAL-NAVIGATION")
    print("- H-EXP-07-CHANNEL-MOTION-PROOF closed by DEC-WEBSITE-MOTION-SYSTEM-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
