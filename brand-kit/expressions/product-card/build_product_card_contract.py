#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FILES = [ROOT / name for name in ("product-card.source.json", "product-card.schema.json", "README.md", "review.json")]


def read(path: Path):
    return json.loads(path.read_text())


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source, review = read(FILES[0]), read(FILES[3])
    if source.get("status") != "visual-research-candidate" or source.get("productionAuthority") is not False or review.get("verdict") != "pending":
        raise SystemExit("pending candidate required")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in FILES:
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion": "1.0.0",
        "name": "@mez-systems/expression-product-card",
        "version": "0.4.0",
        "status": "visual-research-candidate",
        "candidateRevision": "product-card-02-phase-a-r02",
        "reviewGateId": "H-EXP-04A-CARD-VISUAL-DIRECTION",
        "programmePhase": "A-visual-architecture",
        "phaseBStatus": "held-until-visual-lock",
        "productionReadyForScope": False,
        "productionAuthority": False,
        "entrypoints": {"contract": "product-card.source.json", "schema": "product-card.schema.json", "review": "review.json", "guidance": "README.md"},
        "runtimeDependencies": source["dependencies"],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n")
    packaged = sorted(path for path in DIST.iterdir() if path.is_file())
    manifest = {
        "schemaVersion": "1.0.0",
        "expressionId": source["expressionId"],
        "status": "visual-research-candidate",
        "productionAuthority": False,
        "artifactCount": len(packaged),
        "artifacts": [{"path": path.name, "bytes": path.stat().st_size, "sha256": sha(path)} for path in packaged],
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("MEZ PRODUCT CARD 02 · PHASE A: BUILT")
    print("- one portrait website-card architecture with four bounded treatments")
    print("- family shelf, bundle offer and complete Phase B website-component scope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
