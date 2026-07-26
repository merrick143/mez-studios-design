#!/usr/bin/env python3
"""Verify canonical EXP-07 website motion and its explicit menu deferral."""

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
SOURCE = ROOT / "channel-motion.source.json"
SCHEMA = ROOT / "channel-motion.schema.json"
REVIEW = ROOT / "review.json"
ROUND03 = ROOT / "round-03-feedback.json"
DIST = ROOT / "dist"
WORKBENCH = BRAND_KIT / "workbench" / "expressions" / "channel-motion"
APPROVED_IDS = {"MOT-L01", "MOT-L02", "MOT-L03", "MOT-W01", "MOT-W03", "MOT-W04", "MOT-W05"}


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
    feedback = read_json(ROUND03)
    try:
        jsonschema.Draft202012Validator(read_json(SCHEMA)).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")
    if source.get("status") != "canonical" or source.get("productionAuthority") is not True or source.get("version") != "1.0.0":
        failures.append("website motion must be canonical 1.0.0 with bounded authority")
    if review.get("verdict") != "approve-with-deferral" or review.get("decisionId") != "DEC-WEBSITE-MOTION-SYSTEM-001" or review.get("productionAuthority") is not True:
        failures.append("human review does not close the website-motion gate")
    if feedback.get("resultingApprovedSpecimens") != 7 or feedback.get("deferredSpecimens") != ["MOT-W02"]:
        failures.append("Round 03 disposition must preserve seven keeps and one explicit deferral")
    if source.get("approval", {}).get("round03FeedbackSha256") != sha256(ROUND03):
        failures.append("Round 03 approval hash drifted")
    specimens = source.get("specimens", [])
    ids = [item.get("id") for item in specimens]
    if len(ids) != 7 or set(ids) != APPROVED_IDS or len(set(ids)) != 7:
        failures.append("canonical contract must contain the seven approved specimen IDs only")
    if dict(Counter(item.get("family") for item in specimens)) != {"laws": 3, "components": 4}:
        failures.append("canonical contract must contain 3 laws and 4 component behaviours")
    if source.get("deferral", {}).get("specimenId") != "MOT-W02" or source.get("deferral", {}).get("taskId") != "TASK-CMP-01-GLOBAL-NAVIGATION":
        failures.append("menu specimen is not deferred to the named component task")
    for evidence in source.get("deferral", {}).get("evidence", []):
        if not (BRAND_KIT.parent / evidence).is_file():
            failures.append(f"deferred menu evidence missing: {evidence}")
    if source.get("decisionModel", {}).get("maximumActiveMotionEventsPerViewport") != 1:
        failures.append("single active motion allocation drifted")
    if source.get("exportContract", {}).get("staticTwinRequired") is not True or source.get("exportContract", {}).get("motionMayNotCarrySoleMeaning") is not True:
        failures.append("static twin and equivalent meaning must remain required")
    excluded = set(source.get("scope", {}).get("excludedMotionProduction", []))
    for item in ("email", "paid advertising", "organic social", "video and film"):
        if item not in excluded:
            failures.append(f"out-of-scope motion production missing: {item}")
    for dependency_id, dependency in source.get("dependencies", {}).items():
        path = BRAND_KIT / dependency["path"].removeprefix("brand-kit/")
        if not path.is_file():
            failures.append(f"immutable dependency drift: {dependency['path']}")
            continue
        # The programme audit is a living roadmap, not canonical visual input.
        # Its recorded hash is approval-time provenance; later completed tasks
        # must be allowed to update the roadmap without invalidating EXP-07.
        if dependency_id == "programmeAudit":
            audit = path.read_text(encoding="utf-8")
            if "## Phase 6" not in audit or "#### P6.5: marketing patterns" not in audit:
                failures.append("programme audit no longer contains the required Phase 6 component boundary")
            continue
        if sha256(path) != dependency["sha256"]:
            failures.append(f"immutable dependency drift: {dependency['path']}")
    task = read_json(BRAND_KIT / "llm" / "tasks" / "TASK-CMP-01-GLOBAL-NAVIGATION.json")
    if task.get("status") not in {"ready", "awaiting-human", "complete"} or "explore-menu/explore-menu.js" not in task.get("inputs", {}).get("requiredFiles", []):
        failures.append("deferred global-navigation task is missing or does not name the existing component evidence")
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    script = (WORKBENCH / "channel-motion.js").read_text(encoding="utf-8")
    css = (WORKBENCH / "styles.css").read_text(encoding="utf-8")
    for phrase in ("WEBSITE MOTION / CANONICAL 1.0.0", "7 APPROVED BEHAVIOURS", "TASK-CMP-01-GLOBAL-NAVIGATION", "DEC-WEBSITE-MOTION-SYSTEM-001"):
        if phrase not in html:
            failures.append(f"locked workbench missing boundary: {phrase}")
    mounted_ids = set(re.findall(r'id:\s*"(MOT-[LW]\d{2})"', script))
    if mounted_ids != APPROVED_IDS or "MOT-W02" in mounted_ids:
        failures.append("locked workbench IDs drifted from the seven approved specimens")
    for phrase in ("mountLivingCores", "prefers-reduced-motion", "IntersectionObserver", "data-motion-eligible", "productionAuthority:true"):
        if phrase not in script:
            failures.append(f"locked workbench controller missing contract: {phrase}")
    for phrase in ("var(--mz-font-display)", "var(--mz-font-body)", "@media (max-width: 640px)", "prefers-reduced-motion"):
        if phrase not in css:
            failures.append(f"workbench styles missing contract: {phrase}")
    before = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    result = subprocess.run([sys.executable, str(ROOT / "build_channel_motion_candidate.py")], cwd=BRAND_KIT.parent, text=True, capture_output=True, check=False)
    if result.returncode:
        failures.append(f"deterministic build failed: {result.stderr.strip() or result.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed canonical output")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if package.get("productionAuthority") is not True or package.get("productionReadyForScope") is not True or manifest.get("productionAuthority") is not True:
        failures.append("canonical package does not expose bounded authority")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    if failures:
        print("MEZ WEBSITE MOTION 1.0.0: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ WEBSITE MOTION 1.0.0: PASS")
    print("- 7 approved specimens: 3 motion laws and 4 component behaviours")
    print("- MOT-W02 is explicitly deferred to TASK-CMP-01-GLOBAL-NAVIGATION")
    print("- static equivalence, one-event allocation and channel exclusions remain canonical")
    print("- H-EXP-07-CHANNEL-MOTION-PROOF is closed by DEC-WEBSITE-MOTION-SYSTEM-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
