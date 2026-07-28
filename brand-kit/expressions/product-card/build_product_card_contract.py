#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FILES = [ROOT / name for name in ("product-card.source.json", "product-card.schema.json", "README.md", "review.json", "round-05-feedback.json", "round-06-feedback.json", "round-07-feedback.json", "round-08-feedback.json", "round-09-feedback.json", "round-10-feedback.json")]


def read(path: Path):
    return json.loads(path.read_text())


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source, review = read(FILES[0]), read(FILES[3])
    if source.get("status") != "canonical-visual-grammar" or source.get("productionAuthority") is not True or review.get("verdict") != "approve":
        raise SystemExit("approved Phase A visual grammar required")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in FILES:
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/expression-product-card",
        "version": "1.0.0",
        "status": "canonical-visual-grammar",
        "candidateRevision": "product-card-02-phase-a-r10",
        "reviewGateId": "H-EXP-04A-CARD-VISUAL-DIRECTION",
        "programmePhase": "A-visual-architecture",
        "phaseBStatus": "ready-to-start",
        "productionReadyForScope": True,
        "productionAuthority": True,
        "entrypoints": {"contract": "product-card.source.json", "schema": "product-card.schema.json", "review": "review.json", "guidance": "README.md"},
        "runtimeDependencies": source["dependencies"],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n")
    packaged = sorted(path for path in DIST.iterdir() if path.is_file())
    manifest = {
        "schemaVersion": "1.0.0",
        "expressionId": source["expressionId"],
        "status": "canonical-visual-grammar",
        "productionAuthority": True,
        "artifactCount": len(packaged),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)} for path in packaged],
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("MEZ PRODUCT CARD 02 · PHASE A 1.0.0: BUILT")
    print("- thirty-two approved specimens across four real product jobs")
    print("- round 05 through 10 human feedback preserved; canonical Phase B now consumes this locked visual grammar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
