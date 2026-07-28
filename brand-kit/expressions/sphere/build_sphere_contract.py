#!/usr/bin/env python3
"""Build the portable canonical metadata package for the Mez sphere."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sphere.source.json"
SCHEMA = ROOT / "sphere.schema.json"
README = ROOT / "README.md"
REVIEW = ROOT / "review.json"
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
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True:
        raise SystemExit("sphere build requires canonical 1.0.0")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-SPHERE-EXPRESSION-001" or review.get("productionAuthority") is not True:
        raise SystemExit("sphere build requires the approved human gate")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW):
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/expression-sphere",
        "version": source["version"],
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "reviewGateId": source["candidateGateId"],
        "productionReadyForScope": True,
        "productionAuthority": True,
        "entrypoints": {"contract": "sphere.source.json", "schema": "sphere.schema.json", "review": "review.json", "guidance": "README.md"},
        "runtimeDependencies": source["dependencies"],
        "note": "Canonical metadata contract only. The disc, gradient, static twin, Wings, renderer, finish and foundations remain external immutable dependencies."
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    paths = sorted(path for path in DIST.iterdir() if path.is_file() and path.name != "manifest.json")
    manifest = {
        "schemaVersion": "1.0.0",
        "expressionId": source["expressionId"],
        "status": source["status"],
        "productionAuthority": True,
        "artifactCount": len(paths),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)} for path in paths]
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MEZ SPHERE CONTRACT: BUILT")
    print("- sphere-contract-01 is canonical 1.0.0")
    print("- one focal runtime sphere; exact colour fallback removes depth")
    print("- bounded production authority is backed by H-EXP-02-SPHERE-PROOF")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
