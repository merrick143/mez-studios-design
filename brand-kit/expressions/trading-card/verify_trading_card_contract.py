#!/usr/bin/env python3
"""Verify the canonical EXP-05 Trading Card 1.0.0 contract."""

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
SOURCE = ROOT / "trading-card.source.json"
SCHEMA = ROOT / "trading-card.schema.json"
REVIEW = ROOT / "review.json"
ROUND_02 = ROOT / "round-02-feedback.json"
ROUND_03 = ROOT / "round-03-feedback.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "expressions" / "trading-card"
DECISION_ID = "DEC-TRADING-CARD-EXPRESSION-001"


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
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    round_three = read_json(ROUND_03)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")
    if source.get("version") != "1.0.0" or source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        failures.append("Trading Card source must be canonical 1.0.0 with production authority for its bounded scope")
    if DECISION_ID not in source.get("decisionIds", []):
        failures.append("canonical Trading Card decision is missing from source")
    if review.get("gateId") != source.get("candidateGateId") or review.get("candidateRevision") != source.get("candidateRevision"):
        failures.append("review gate or candidate revision drifted from source")
    if review.get("verdict") != "approve" or review.get("decisionId") != DECISION_ID or review.get("resultingStatus") != "canonical" or review.get("productionAuthority") is not True:
        failures.append("human review does not provide canonical Trading Card approval")
    if review.get("specimenVerdicts") != {"keep": 23, "revise": 0, "kill": 0}:
        failures.append("review must preserve the unanimous 23-keep verdict")
    approved = source.get("approval", {})
    if approved.get("round03FeedbackSha256") != sha256(ROUND_03) or approved.get("decisionId") != DECISION_ID or approved.get("approvedSpecimens") != 23:
        failures.append("Round 03 approval receipt is missing or drifted")
    receipt_specimens = round_three.get("specimens", [])
    if len(receipt_specimens) != 23 or {item.get("verdict") for item in receipt_specimens} != {"keep"}:
        failures.append("Round 03 receipt must contain exactly 23 unanimous keeps")
    specimens = source.get("specimens", [])
    ids = [item.get("id") for item in specimens]
    receipt_ids = [item.get("id") for item in receipt_specimens]
    if len(ids) != 23 or len(set(ids)) != 23 or ids != receipt_ids:
        failures.append("canonical source and Round 03 receipt must contain the same ordered 23 specimen IDs")
    expected_counts = {"faces": 4, "backs": 4, "decks": 8, "placements": 7}
    if dict(Counter(item.get("family") for item in specimens)) != expected_counts:
        failures.append("family counts must remain 4 faces, 4 backs, 8 decks and 7 placements")
    family_counts = {item["id"]: item["count"] for item in source.get("families", [])}
    if family_counts != expected_counts:
        failures.append("declared family counts drifted from specimen scope")
    if source.get("motion", {}).get("maximumLivePerViewport") != 1:
        failures.append("single-live Living Core allocation drifted")
    lineage = source.get("roundLineage", {})
    if not ROUND_02.is_file() or lineage.get("inputSha256") != sha256(ROUND_02):
        failures.append("Round 02 review receipt missing or drifted")
    if lineage.get("disposition") != {"champions": 22, "rebuilds": 1, "removed": 2, "round03Candidates": 23}:
        failures.append("Round 02 disposition must remain 22 keep, 1 revise and 2 kill")
    removed = {"TC-F06", "TC-P04"}
    if removed & set(ids) or set(lineage.get("removedIds", [])) != removed:
        failures.append("killed Round 02 specimen directions must remain absent")
    policy = json.dumps({
        "thesis": source.get("thesis"),
        "meaning": source.get("meaning"),
        "anatomy": source.get("anatomy"),
        "motion": source.get("motion"),
        "prohibited": source.get("prohibited")
    }).lower()
    for phrase in ("not an edition", "omit the card", "public product name is largest", "no manual animate button", "multiple live cores", "fake scores"):
        if phrase not in policy:
            failures.append(f"canonical policy missing boundary: {phrase}")
    for dependency in source.get("dependencies", {}).values():
        path = BRAND_KIT / dependency["path"].removeprefix("brand-kit/")
        if not path.is_file() or sha256(path) != dependency["sha256"]:
            failures.append(f"immutable dependency drift: {dependency['path']}")
    html_path = WORKBENCH / "index.html"
    js_path = WORKBENCH / "trading-card.js"
    css_path = WORKBENCH / "styles.css"
    html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    script = js_path.read_text(encoding="utf-8") if js_path.is_file() else ""
    css = css_path.read_text(encoding="utf-8") if css_path.is_file() else ""
    for phrase in ("TRADING CARD 01 / CANONICAL 1.0.0", "23 approved specimens", "Not System Editions", "DEC-TRADING-CARD-EXPRESSION-001"):
        if phrase not in html:
            failures.append(f"workbench missing canonical boundary: {phrase}")
    mounted_ids = set(re.findall(r'id:\s*"(TC-[FBDP]\d{2})"', script))
    if mounted_ids != set(ids):
        failures.append("workbench specimen IDs drifted from the canonical contract")
    for phrase in ("mountLivingCores", "prefers-reduced-motion", "data-auto-live", "data-verdict", "productionAuthority:true"):
        if phrase not in script:
            failures.append(f"workbench controller missing contract: {phrase}")
    for phrase in ("var(--mz-font-display)", "var(--mz-font-body)", "border-radius", "@media (max-width: 640px)"):
        if phrase not in css:
            failures.append(f"workbench styles missing contract: {phrase}")
    if "http://" in html or "https://" in html or "http://" in css or "https://" in css:
        failures.append("workbench must not load external runtime assets")
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_trading_card_contract.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed generated output")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if package.get("productionAuthority") is not True or package.get("productionReadyForScope") is not True or manifest.get("productionAuthority") is not True:
        failures.append("canonical package does not expose bounded production authority")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    if failures:
        print("MEZ TRADING CARD 1.0.0: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ TRADING CARD 1.0.0: PASS")
    print("- 23 approved specimens: 4 faces, 4 backs, 8 decks and 7 placements")
    print("- Round 03 receipt is unanimous and exact; all prior killed directions remain absent")
    print("- canonical identity, Product Card grammar and one-live motion allocation remain inherited")
    print("- H-EXP-05-TRADING-CARD-PROOF is closed by DEC-TRADING-CARD-EXPRESSION-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
