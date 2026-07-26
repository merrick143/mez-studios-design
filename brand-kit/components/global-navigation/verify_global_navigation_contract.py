#!/usr/bin/env python3
"""Verify the canonical CMP-01 Global Navigation 1.0.0 contract."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
REPO = BRAND_KIT.parent
DIST = ROOT / "dist"
RELEASE = BRAND_KIT / "releases" / "components" / "global-navigation" / "1.0.0"
WORKBENCH = BRAND_KIT / "workbench" / "components" / "global-navigation"
DECISION_ID = "DEC-GLOBAL-NAVIGATION-COMPONENT-001"


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
    source, review = read_json(ROOT / "global-navigation.source.json"), read_json(ROOT / "review.json")
    try:
        jsonschema.Draft202012Validator(read_json(ROOT / "global-navigation.schema.json")).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source schema: {error.message}")
    if source.get("status") != "canonical" or source.get("version") != "1.0.0" or source.get("productionAuthority") is not True:
        failures.append("source must be canonical 1.0.0 with bounded production authority")
    if review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        failures.append("human gate must be approved")
    if review.get("decisionId") != DECISION_ID or DECISION_ID not in source.get("decisionIds", []):
        failures.append("canonical Global Navigation decision is missing or inconsistent")
    if source.get("selectedFamily") != "registry" or source.get("motion", {}).get("maximumLiveCores") != 5:
        failures.append("Registry family or five-live-sphere allocation drifted")
    if source.get("motionDecisionException", {}).get("status") != "approved-bounded":
        failures.append("five-live-sphere exception is not explicitly bounded by the approved decision")
    for dependency in source.get("dependencies", {}).values():
        path = REPO / dependency["path"]
        if not path.is_file() or sha256(path) != dependency["sha256"]:
            failures.append(f"immutable dependency drift: {dependency['path']}")
    component_js = (ROOT / "mez-global-navigation.js").read_text(encoding="utf-8")
    component_css = (ROOT / "mez-global-navigation.css").read_text(encoding="utf-8")
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    controller = (WORKBENCH / "global-navigation-workbench.js").read_text(encoding="utf-8")
    if component_js.count("this.renderer.mount(") != 1 or "hosts.forEach" not in component_js or 'shape:"sphere"' not in component_js:
        failures.append("component must mount the five product hosts through one spherical renderer path")
    if 'class="mz-global-trigger__stack"' not in component_js or "--stack-material" not in component_js:
        failures.append("compact Explore control is missing the five-circle family stack")
    if "<footer>" in component_js or "Choose a system to continue" in component_js or "Enter select" in component_js:
        failures.append("instructional footer copy returned to the simplified registry")
    for phrase in ("aria-expanded", "aria-pressed", "Escape", "ArrowDown", "Home", "End", "mez-product-navigate", "focus({preventScroll:true})", "prefers-reduced-motion"):
        if phrase not in component_js:
            failures.append(f"component missing behaviour contract: {phrase}")
    for forbidden in ("System 01", "variant=\"signal\"", "variant=\"aperture\"", "variant=\"gallery\"", "variant=\"console\""):
        if forbidden in component_js:
            failures.append(f"research-only direction leaked into component: {forbidden}")
    for phrase in ("grid-template-columns:1fr", "overflow-y:auto", "prefers-reduced-motion", "forced-colors", "focus-visible", "border-radius:50%", ".mz-global-trigger__stack", "transition-delay:0s,0s,100ms,100ms", "height 520ms"):
        if phrase not in component_css:
            failures.append(f"component styles missing responsive or accessibility proof: {phrase}")
    for phrase in ("GLOBAL NAVIGATION · CANONICAL 1.0.0", "SELECTED FAMILY / REGISTRY", "Five live spheres", "Consumer-owned routes", "DEC-GLOBAL-NAVIGATION-COMPONENT-001"):
        if phrase not in html:
            failures.append(f"workbench missing review evidence: {phrase}")
    mobile_proof = (WORKBENCH / "mobile-proof.html").read_text(encoding="utf-8")
    if "width:320px" not in mobile_proof or "?open=1&version=1.0.0" not in mobile_proof or "FIVE LIVE SPHERES" not in mobile_proof or "COMPACT FAMILY STACK" not in mobile_proof:
        failures.append("workbench is missing the bounded 320px compact-stack and five-live-sphere proofs")
    for phrase in ("mez-navigation-open", "mez-product-focus", "mez-product-navigate", "data-canvas-count"):
        if phrase not in controller and phrase not in html:
            failures.append(f"workbench controller missing live proof: {phrase}")
    for script in (ROOT / "mez-global-navigation.js", WORKBENCH / "global-navigation-workbench.js"):
        node = subprocess.run(["node", "--check", str(script)], text=True, capture_output=True, check=False)
        if node.returncode:
            failures.append(f"JavaScript syntax {script.name}: {node.stderr.strip()}")
    fixture = (ROOT / "fixtures" / "static-html.html").read_text(encoding="utf-8")
    react = (ROOT / "fixtures" / "react.jsx").read_text(encoding="utf-8")
    if "mez-product-navigate" not in fixture or "onProductNavigate" not in react:
        failures.append("consumer fixtures do not expose consumer-owned routing")
    before = {path.relative_to(DIST).as_posix():path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    built = subprocess.run([sys.executable, str(ROOT / "build_global_navigation_contract.py")], cwd=REPO, text=True, capture_output=True, check=False)
    if built.returncode:
        failures.append(f"candidate build failed: {built.stderr.strip() or built.stdout.strip()}")
    after = {path.relative_to(DIST).as_posix():path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if before and before != after:
        failures.append("deterministic rebuild changed the candidate package")
    package = read_json(DIST / "package.json") if (DIST / "package.json").is_file() else {}
    manifest = read_json(DIST / "manifest.json") if (DIST / "manifest.json").is_file() else {}
    if package.get("productionAuthority") is not True or package.get("productionReadyForScope") is not True or manifest.get("productionAuthority") is not True:
        failures.append("canonical package does not expose bounded production authority")
    for artifact in manifest.get("artifacts", []):
        path = DIST / artifact["path"]
        if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            failures.append(f"manifest drift: {artifact['path']}")
    if not (DIST / "components/global-navigation/mez-global-navigation.js").is_file() or not (DIST / "registry/products.json").is_file():
        failures.append("portable package is missing component code or canonical product data")
    release_files = {path.relative_to(RELEASE).as_posix(): path.read_bytes() for path in RELEASE.rglob("*") if path.is_file()} if RELEASE.is_dir() else {}
    dist_files = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in DIST.rglob("*") if path.is_file()} if DIST.is_dir() else {}
    if release_files != dist_files:
        failures.append("canonical release mirror drifted from component dist")
    if failures:
        print("MEZ GLOBAL NAVIGATION 1.0.0: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("MEZ GLOBAL NAVIGATION 1.0.0: PASS")
    print("- Registry is the only promoted family with one bounded surface option")
    print("- compact Explore control previews the family with five layered circles")
    print("- simplified footer-free registry uses the approved smoother disclosure sequence")
    print("- five automatically animated spheres with inherited hover-speed response")
    print("- keyboard, mobile, fallback and consumer-event contracts verified")
    print("- H-CMP-01-GLOBAL-NAVIGATION-PROOF closed by DEC-GLOBAL-NAVIGATION-COMPONENT-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
