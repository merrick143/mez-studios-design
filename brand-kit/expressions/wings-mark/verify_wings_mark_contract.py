#!/usr/bin/env python3
"""Verify the Wings and mark review candidate."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parent
BRAND=ROOT.parents[1]
DIST=ROOT/"dist"
WORK=BRAND/"workbench"/"expressions"/"wings-mark"
def read(path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    failures=[]; source=read(ROOT/"wings-mark.source.json"); review=read(ROOT/"review.json")
    try: jsonschema.Draft202012Validator(read(ROOT/"wings-mark.schema.json")).validate(source)
    except jsonschema.ValidationError as error: failures.append("schema: "+error.message)
    if source.get("status")!="canonical" or source.get("version")!="1.0.0" or source.get("productionAuthority") is not True: failures.append("canonical authority drifted")
    if review.get("verdict")!="approve" or review.get("decisionId")!="DEC-WINGS-MARK-EXPRESSION-001" or review.get("productionAuthority") is not True: failures.append("approved human gate drifted")
    geometry=source.get("geometry",{})
    wings=BRAND/geometry.get("assetPath","missing").removeprefix("brand-kit/")
    if not wings.is_file() or sha(wings)!=geometry.get("sha256") or geometry.get("pathCount")!=2 or geometry.get("redraw")!="forbidden": failures.append("canonical Wings geometry drifted")
    roles={role["id"]:role for role in source.get("roles",[])}
    if set(roles)!={"holdco-lockup","standalone","product-core","gradient-mask"}: failures.append("mark roles are incomplete")
    colour=source.get("colour",{})
    if colour.get("lightSurface")!="#2E2E2E" or colour.get("darkSurface")!="#FFFFFF" or colour.get("newCorporateHue") is not False: failures.append("canonical monochrome colour boundary drifted")
    if source.get("spaceAndScale",{}).get("minimumStandaloneHeightPx")!=24 or source.get("spaceAndScale",{}).get("minimumLockupMarkHeightPx")!=28: failures.append("minimum sizes drifted")
    protected=[]
    for dep in source.get("dependencies",{}).values():
        path=BRAND/dep["path"].removeprefix("brand-kit/"); protected.append(path)
        if not path.is_file() or sha(path)!=dep["sha256"]: failures.append("dependency drift: "+dep["path"])
    before={p:sha(p) for p in protected+[wings] if p.is_file()}
    old={p.relative_to(DIST).as_posix():p.read_bytes() for p in DIST.rglob("*") if p.is_file()} if DIST.is_dir() else {}
    result=subprocess.run([sys.executable,str(ROOT/"build_wings_mark_contract.py")],cwd=BRAND.parent,text=True,capture_output=True)
    if result.returncode: failures.append("build failed: "+(result.stderr or result.stdout).strip())
    new={p.relative_to(DIST).as_posix():p.read_bytes() for p in DIST.rglob("*") if p.is_file()}
    if old and old!=new: failures.append("deterministic rebuild changed output")
    if before!={p:sha(p) for p in before}: failures.append("canonical dependency changed")
    html=(WORK/"index.html").read_text(encoding="utf-8") if (WORK/"index.html").is_file() else ""
    for phrase in ("One canonical mark hierarchy", "One geometry", "Holdco lockup", "PRODUCT-CORE MARK", "Gradient Wings", "24 px", "H-EXP-03-WINGS-MARK-PROOF"):
        if phrase not in html: failures.append("human proof missing: "+phrase)
    if html.count("data-mz-core")!=1 or 'data-shape="wings"' not in html: failures.append("proof must contain exactly one gradient Wings runtime")
    if "http://" in html or "https://" in html: failures.append("proof contains external URL")
    script=(WORK/"wings-mark.js").read_text(encoding="utf-8") if (WORK/"wings-mark.js").is_file() else ""
    for phrase in ("forceStatic","disableWebGL","mountLivingCores","prefers-reduced-motion"):
        if phrase not in script: failures.append("runtime control missing: "+phrase)
    if failures:
        print("MEZ WINGS MARK CONTRACT: FAIL")
        for failure in failures: print("- "+failure)
        return 1
    print("MEZ WINGS MARK CONTRACT: PASS")
    print("- exact two-path Wings, four roles and monochrome ordinary marks validate")
    print("- one rare gradient-mask runtime retains an exact static fallback")
    print("- canonical 1.0.0 authority is backed by H-EXP-03-WINGS-MARK-PROOF")
    return 0
if __name__ == "__main__": raise SystemExit(main())
