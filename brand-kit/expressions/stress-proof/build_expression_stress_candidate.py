#!/usr/bin/env python3
"""Build the deterministic canonical EXP-08 package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FILES = [ROOT / name for name in ("expression-stress.source.json", "expression-stress.schema.json", "review.json", "README.md")]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = json.loads(FILES[0].read_text(encoding="utf-8"))
    review = json.loads(FILES[2].read_text(encoding="utf-8"))
    if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        raise SystemExit("EXP-08 build requires canonical bounded authority")
    if review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        raise SystemExit("EXP-08 build requires the approved human review")
    if review.get("decisionId") not in source.get("decisionIds", []):
        raise SystemExit("EXP-08 decision is missing from the source contract")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in FILES:
        shutil.copy2(path, DIST / path.name)
    package = {
        "schemaVersion":"1.0.0",
        "name":"@mez-systems/expression-stress-proof",
        "version":source["version"],
        "status":source["status"],
        "candidateRevision":source["candidateRevision"],
        "reviewGateId":source["gateId"],
        "scenarioCount":len(source["scenarios"]),
        "suiteCount":len(source["suites"]),
        "decisionId":review["decisionId"],
        "productionAuthority":True,
        "entrypoints":{"contract":"expression-stress.source.json","schema":"expression-stress.schema.json","review":"review.json","guidance":"README.md"}
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    paths = sorted(path for path in DIST.iterdir() if path.is_file() and path.name != "manifest.json")
    manifest = {"schemaVersion":"1.0.0","proofId":source["proofId"],"version":source["version"],"status":source["status"],"decisionId":review["decisionId"],"productionAuthority":True,"artifactCount":len(paths),"artifacts":[{"path":path.name,"bytes":path.stat().st_size,"sha256":sha256(path)} for path in paths]}
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MEZ EXPRESSION STRESS PROOF 1.0.0: BUILT")
    print("- 6 suites / 14 representative scenarios")
    print("- H-EXP-08-EXPRESSION-STRESS-PROOF closed by DEC-EXPRESSION-STRESS-CERTIFICATION-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
