#!/usr/bin/env python3
"""Verify canonical EXP-08 stress proof and immutable inheritance."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "expression-stress.source.json"
SCHEMA = ROOT / "expression-stress.schema.json"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "expressions" / "stress-proof"
EXPECTED_COUNTS = {"reflow":3,"content":3,"fallback":3,"accessibility":2,"recovery":2,"invariants":1}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    source, review = read_json(SOURCE), read_json(REVIEW)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")
    scenarios = source.get("scenarios", [])
    ids = [item.get("id") for item in scenarios]
    if len(ids) != 14 or len(set(ids)) != 14:
        failures.append("stress proof must contain exactly 14 unique scenarios")
    if dict(Counter(item.get("suite") for item in scenarios)) != EXPECTED_COUNTS:
        failures.append("suite distribution drifted from 3/3/3/2/2/1")
    if sum(item.get("count", 0) for item in source.get("suites", [])) != 14:
        failures.append("suite counts do not total 14")
    if source.get("productionAuthority") is not True or source.get("status") != "canonical" or source.get("version") != "1.0.0":
        failures.append("stress proof must be canonical 1.0.0 with bounded authority")
    if review.get("productionAuthority") is not True or review.get("verdict") != "approve" or review.get("decisionId") != "DEC-EXPRESSION-STRESS-CERTIFICATION-001":
        failures.append("human review does not close the EXP-08 gate")
    if 320 not in source.get("coverage", {}).get("viewports", []) or 240 not in source.get("coverage", {}).get("containers", []) or source.get("coverage", {}).get("textZoom") != [100,200,400]:
        failures.append("required receiver and text-zoom coverage is incomplete")
    for dependency in source.get("dependencies", {}).values():
        path = BRAND_KIT / dependency["path"].removeprefix("brand-kit/")
        if not path.is_file() or sha256(path) != dependency["sha256"]:
            failures.append(f"immutable dependency drift: {dependency['path']}")
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    script = (WORKBENCH / "stress-proof.js").read_text(encoding="utf-8")
    css = (WORKBENCH / "styles.css").read_text(encoding="utf-8")
    for phrase in ("EXPRESSION STRESS PROOF / CANONICAL 1.0.0", "14 REPRESENTATIVE SCENARIOS", "H-EXP-08-EXPRESSION-STRESS-PROOF", "DEC-EXPRESSION-STRESS-CERTIFICATION-001", "Implementation defects only"):
        if phrase not in html:
            failures.append(f"workbench missing canonical boundary: {phrase}")
    mounted = set(re.findall(r'id:\s*"(ST-[RTFASI]\d{2})"', script))
    if mounted != set(ids):
        failures.append("workbench scenario IDs drifted from the source contract")
    for phrase in ("mountLivingCores", "prefers-reduced-motion", "data-core-host", "aria-live", "productionAuthority:true", "maximum one live"):
        if phrase not in script:
            failures.append(f"workbench controller missing stress contract: {phrase}")
    for phrase in ("forced-colors", "prefers-reduced-motion", "@container", "focus-visible", "--font-scale"):
        if phrase not in css:
            failures.append(f"workbench styles missing adversarial contract: {phrase}")
    node = subprocess.run(["node", "--check", str(WORKBENCH / "stress-proof.js")], text=True, capture_output=True, check=False)
    if node.returncode:
        failures.append(f"workbench JavaScript syntax: {node.stderr.strip()}")
    before = {path.relative_to(DIST).as_posix():path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    built = subprocess.run([sys.executable, str(ROOT / "build_expression_stress_candidate.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if built.returncode:
        failures.append(f"deterministic build failed: {built.stderr.strip() or built.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix():path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed canonical output")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if package.get("productionAuthority") is not True or manifest.get("productionAuthority") is not True or package.get("scenarioCount") != 14:
        failures.append("canonical package authority or scenario count drifted")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    if failures:
        print("MEZ EXPRESSION STRESS PROOF 1.0.0: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ EXPRESSION STRESS PROOF 1.0.0: PASS")
    print("- 14 scenarios across 6 adversarial suites")
    print("- canonical expression dependencies remain immutable")
    print("- H-EXP-08-EXPRESSION-STRESS-PROOF is closed by DEC-EXPRESSION-STRESS-CERTIFICATION-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
