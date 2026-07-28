#!/usr/bin/env python3
"""Build the portable Wings and mark review candidate."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
FILES = [ROOT / name for name in ("wings-mark.source.json", "wings-mark.schema.json", "README.md", "review.json")]
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    source, review = read(FILES[0]), read(FILES[3])
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True: raise SystemExit("canonical 1.0.0 required")
    if review.get("verdict") != "approve" or review.get("decisionId") != "DEC-WINGS-MARK-EXPRESSION-001" or review.get("productionAuthority") is not True: raise SystemExit("approved human gate required")
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in FILES: shutil.copy2(path, DIST / path.name)
    package = {"schemaVersion":"1.0.0","name":"@mez-systems/expression-wings-mark","version":"1.0.0","status":"canonical","candidateRevision":"wings-mark-01","reviewGateId":"H-EXP-03-WINGS-MARK-PROOF","productionReadyForScope":True,"productionAuthority":True,"entrypoints":{"contract":"wings-mark.source.json","schema":"wings-mark.schema.json","review":"review.json","guidance":"README.md"},"runtimeDependencies":source["dependencies"]}
    (DIST / "package.json").write_text(json.dumps(package, indent=2)+"\n", encoding="utf-8")
    paths=sorted(p for p in DIST.iterdir() if p.is_file())
    manifest={"schemaVersion":"1.0.0","expressionId":source["expressionId"],"status":"canonical","productionAuthority":True,"artifactCount":len(paths),"artifacts":[{"path":p.name,"bytes":p.stat().st_size,"sha256":sha(p)} for p in paths]}
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print("MEZ WINGS MARK CONTRACT: BUILT")
    print("- wings-mark-01 is canonical 1.0.0")
    print("- canonical Wings geometry is referenced, never copied or redrawn")
    print("- bounded authority is backed by H-EXP-03-WINGS-MARK-PROOF")
    return 0
if __name__ == "__main__": raise SystemExit(main())
