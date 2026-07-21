#!/usr/bin/env python3
"""Build the portable canonical metadata package for the Mez product disc."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "disc.source.json"
SCHEMA = ROOT / "disc.schema.json"
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
        raise SystemExit("canonical disc 1.0.0 with bounded production authority is required")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-DISC-EXPRESSION-001" or review.get("productionAuthority") is not True:
        raise SystemExit("canonical disc build requires the approved human gate")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW):
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/expression-disc",
        "version": source["version"],
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "reviewGateId": source["candidateGateId"],
        "productionReadyForScope": True,
        "productionAuthority": True,
        "entrypoints": {"contract": "disc.source.json", "schema": "disc.schema.json", "review": "review.json", "guidance": "README.md"},
        "runtimeDependencies": source["dependencies"],
        "note": "Metadata contract only. Canonical gradients, static twins, Wings, renderer and foundations remain external immutable dependencies."
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    artifact_paths = sorted(path for path in DIST.iterdir() if path.is_file() and path.name != "manifest.json")
    manifest = {
        "schemaVersion": "1.0.0",
        "expressionId": source["expressionId"],
        "status": source["status"],
        "productionAuthority": True,
        "artifactCount": len(artifact_paths),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)} for path in artifact_paths]
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MEZ DISC CONTRACT: BUILT")
    print(f"- {source['candidateRevision']} is canonical 1.0.0")
    print(f"- {len(source['products'])} canonical product assignments referenced without copying")
    print("- bounded production authority is backed by H-EXP-01-DISC-PROOF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
