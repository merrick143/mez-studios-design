#!/usr/bin/env python3
"""Verify GOLD-01 Round 23: real, governed operating proof.

Round 23 resolves GH-S05's evidence-intake gate with four screenshots supplied
by Olli. The section uses a three-stage sticky-proof composition: command,
context (two surfaces) and application. The verifier forbids a regression to
placeholder UI, fabricated metrics or an ungoverned public-proof claim.

Run with --self-test to mutate each owned contract in memory. No worktree files
are changed by the self-test.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
REPO = BRAND_KIT.parent
WORKBENCH = BRAND_KIT / "workbench" / "golden" / "homepage"
HTML = WORKBENCH / "index.html"
CSS = WORKBENCH / "styles.css"
JS = WORKBENCH / "homepage.js"
SOURCE = ROOT / "homepage.source.json"
REVIEW = ROOT / "review.json"
FEEDBACK = ROOT / "round-23-feedback.json"
PROVENANCE = WORKBENCH / "assets" / "operating-proof" / "provenance.json"
REFERENCE = BRAND_KIT / "references" / "mez-notion-operating-proof" / "design-language.md"
REFERENCE_REGISTRY = BRAND_KIT / "references" / "REGISTRY.md"

EXPECTED_ASSETS = {
    "command.png": "97f576860ab1151ef1379ed1bfcf7e44ccd7da5c7376e773f3091eb6326c6f59",
    "backend.png": "6e34b55413ed333ab7230227e705a6bb4642f0b5e61ef6bb47fbf76467f14e73",
    "docs.png": "069b7d76fe274801c6e3208b8f28c2277536854b872b050c0d01272a8b4e70d8",
    "ad-system.png": "af217f1949122469004055050389da7a10169a267dc2de057cd4fde2ef2937e8",
}
EXPECTED_STAGES = ("command", "context", "application")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(
    html: str,
    css: str,
    javascript: str,
    source: dict,
    review: dict,
    feedback: dict,
    provenance: dict,
    reference: str,
    reference_registry: str,
) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    # Candidate identity and non-production authority.
    for label, value in (
        ("source", source.get("candidateRevision")),
        ("review", review.get("candidateRevision")),
        ("provenance", provenance.get("candidateRevision")),
    ):
        if value not in {"golden-homepage-01-r23", "golden-homepage-01-r24"}:
            fail("META", f"{label} does not identify R23 or its direct successor R24")
    if feedback.get("candidateRevision") != "golden-homepage-01-r23":
        fail("META", "Round 23 feedback no longer identifies its own candidate")
    if source.get("version") not in {"0.23.0-candidate", "0.24.0-candidate"}:
        fail("META", "homepage.source.json version is outside the R23 to R24 lineage")
    if not any(label in html for label in ("Round 23", "Round 24")) or not any(
        revision in javascript for revision in ("golden-homepage-01-r23", "golden-homepage-01-r24")
    ):
        fail("META", "workbench title or review export predates Round 23")
    if feedback.get("productionAuthority") is not False or provenance.get("productionAuthority") is not False:
        fail("META", "feedback and evidence provenance must remain non-production")

    # GH-S05 must remain bounded between its locked neighbours.
    s04_start = html.find('data-review-id="GH-S04"')
    s05_start = html.find('data-review-id="GH-S05"')
    s06_start = html.find('data-review-id="GH-S06"')
    if min(s04_start, s05_start, s06_start) < 0 or not s04_start < s05_start < s06_start:
        fail("BOUNDARY", "GH-S05 must remain between GH-S04 and GH-S06")
        s05 = ""
    else:
        s05 = html[s05_start:s06_start]

    # Real evidence, three claims and four supplied surfaces.
    if 'class="shell op-layout"' not in s05 or 'class="op-reel"' not in s05:
        fail("COMPOSITION", "GH-S05 is missing the sticky-proof layout and evidence reel")
    stages = re.findall(r'data-proof-stage="([^"]+)"', s05)
    if tuple(stages) != EXPECTED_STAGES:
        fail("COMPOSITION", f"expected command, context, application stages; found {stages}")
    if s05.count('<figure class="op-record') != 3:
        fail("COMPOSITION", "GH-S05 must carry exactly three proof records")
    asset_refs = re.findall(r'src="\./assets/operating-proof/([^"]+\.png)"', s05)
    if set(asset_refs) != set(EXPECTED_ASSETS) or len(asset_refs) != 4:
        fail("TRUTH", f"GH-S05 must use the four supplied evidence assets exactly once; found {asset_refs}")
    if s05.count("loading=\"lazy\"") != 4:
        fail("MEDIA", "all four below-fold proof images must lazy-load")
    if "Evidence pending" in s05 or "op-screen__bars" in s05 or "op-screen__status" in s05:
        fail("PLACEHOLDER", "retired evidence placeholders returned")

    # Screenshot copy stays inside what the pixels prove.
    for phrase in ("Command surface", "Context layer", "System in use"):
        if phrase not in s05:
            fail("COPY", f"evidence title missing: {phrase}")
    if re.search(r"\b(?:revenue|profit|conversion|faster|percent|%|\$[0-9])\b", s05, re.I):
        fail("TRUTH", "GH-S05 contains an unsupported performance or financial claim")
    alt_values = re.findall(r'<img\s+[^>]*alt="([^"]*)"', s05, re.S)
    if len(alt_values) != 4 or any(not value or value.lower() in {"image", "screenshot"} for value in alt_values):
        fail("ALT", "each evidence image needs specific, non-generic alt text")

    # The public-redaction gate is visible and machine-readable.
    if provenance.get("publicRedactionStatus") != "pending":
        fail("REDACTION", "provenance must keep public redaction pending")
    proof = source.get("proof", {})
    if proof.get("operatingRecords") != 3 or proof.get("operatingSurfaces") != 4:
        fail("SOURCE", "source contract must record three stages and four real surfaces")
    if proof.get("operatingStatus") != "evidence-supplied-redaction-pending":
        fail("SOURCE", "source contract does not record the supplied-evidence state")

    # Every asset must remain byte-identical to the supplied evidence.
    provenance_assets = {item.get("file"): item.get("sha256") for item in provenance.get("assets", [])}
    if provenance_assets != EXPECTED_ASSETS:
        fail("ASSET", "provenance hashes do not match the supplied screenshot set")
    for filename, expected_hash in EXPECTED_ASSETS.items():
        path = PROVENANCE.parent / filename
        if not path.exists():
            fail("ASSET", f"missing supplied evidence asset: {filename}")
        elif sha256(path) != expected_hash:
            fail("ASSET", f"evidence asset changed without a provenance update: {filename}")

    # Sticky-proof composition and plain-frame material discipline.
    op_start = max(
        css.find("/* -------------------------------------- GH-S05 · operating proof (R23) */"),
        css.find("/* -------------------------------------- GH-S05 · operating proof (R24) */"),
    )
    op_end = css.find("/* ------------------------------------------------------ GH-S05 · AI OS */")
    op_css = css[op_start:op_end] if op_start >= 0 and op_end > op_start else ""
    if not op_css or "grid-template-columns: minmax(240px, .72fr) minmax(0, 1.58fr)" not in op_css:
        fail("COMPOSITION", "desktop GH-S05 is not the selected two-register sticky proof")
    op_head = re.search(r"\.op-head \{(.*?)\}", op_css, re.S)
    if not op_head or "position: sticky" not in op_head.group(1):
        fail("COMPOSITION", "the proof thesis must remain pinned while evidence accumulates")
    if "@media (max-width: 900px)" not in op_css or "position: static" not in op_css:
        fail("RESPONSIVE", "sticky proof must release into document flow on compact layouts")
    for banned, pattern in (
        ("box-shadow", r"box-shadow\s*:"),
        ("perspective", r"perspective\s*:"),
        ("rotateX", r"rotateX\s*\("),
        ("rotateY", r"rotateY\s*\("),
        ("backdrop-filter", r"backdrop-filter\s*:"),
    ):
        if re.search(pattern, op_css, re.I):
            fail("CANON", f"real proof frame uses banned treatment: {banned}")
    screen_rule = re.search(r"\.op-screen \{(.*?)\}", op_css, re.S)
    if not screen_rule or "solid var(--mz-border-default)" not in screen_rule.group(1):
        fail("CANON", "proof images need one plain hairline frame")

    # Reference abstraction landed before the section and names what not to copy.
    if "**Composition family:** Sticky proof." not in reference or "## 5 · What not to take" not in reference:
        fail("REFERENCE", "operating-proof reference study is incomplete")
    if "mez-notion-operating-proof" not in reference_registry:
        fail("REFERENCE", "operating-proof reference study is not registered")

    # Scoped portability.
    if "http://" in html or "http://" in css:
        fail("PORTABILITY", "http:// is forbidden in workbench artifacts")
    if "/Users/" in html or "/Users/" in css:
        fail("PORTABILITY", "workbench markup must not depend on local absolute paths")

    return failures


def load() -> tuple[str, str, str, dict, dict, dict, dict, str, str]:
    return (
        HTML.read_text(encoding="utf-8"),
        CSS.read_text(encoding="utf-8"),
        JS.read_text(encoding="utf-8"),
        json.loads(SOURCE.read_text(encoding="utf-8")),
        json.loads(REVIEW.read_text(encoding="utf-8")),
        json.loads(FEEDBACK.read_text(encoding="utf-8")),
        json.loads(PROVENANCE.read_text(encoding="utf-8")),
        REFERENCE.read_text(encoding="utf-8"),
        REFERENCE_REGISTRY.read_text(encoding="utf-8"),
    )


def self_test(data: tuple[str, str, str, dict, dict, dict, dict, str, str]) -> int:
    html, css, javascript, source, review, feedback, provenance, reference, registry = data
    bad_provenance = copy.deepcopy(provenance)
    bad_provenance["assets"][0]["sha256"] = "0" * 64
    bad_redaction = copy.deepcopy(provenance)
    bad_redaction["publicRedactionStatus"] = "approved"
    cases = (
        ("META", html.replace("Round 23", "Round 22").replace("Round 24", "Round 22"), css, provenance),
        ("COMPOSITION", html, css.replace("position: sticky;", "position: static;", 1), provenance),
        ("PLACEHOLDER", html.replace("Command surface", "Evidence pending", 1), css, provenance),
        ("REDACTION", html, css, bad_redaction),
        ("ALT", html.replace('alt="Mez Studios Command page showing quick links, active task views and the current content queue."', 'alt="screenshot"', 1), css, provenance),
        ("ASSET", html, css, bad_provenance),
    )
    misses: list[str] = []
    for expected, mutated_html, mutated_css, mutated_provenance in cases:
        failures = validate(
            mutated_html, mutated_css, javascript, source, review, feedback,
            mutated_provenance, reference, registry,
        )
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 23 SELF-TEST: FAIL")
        for code in misses:
            print(f"  - mutation was not caught: {code}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 23 SELF-TEST: PASS")
    print("- identity, composition, placeholder, redaction, alt and provenance regressions all fail in memory")
    return 0


def main() -> int:
    required = (HTML, CSS, JS, SOURCE, REVIEW, FEEDBACK, PROVENANCE, REFERENCE, REFERENCE_REGISTRY)
    missing = [path for path in required if not path.exists()]
    if missing:
        print("GOLDEN HOMEPAGE ROUND 23: FAIL")
        for path in missing:
            print(f"  - missing artifact: {path.relative_to(REPO)}")
        return 1

    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)

    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 23: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("GOLDEN HOMEPAGE ROUND 23: PASS")
    print("- GH-S05 uses three sticky-proof stages and four byte-verified screenshots supplied by Olli")
    print("- placeholder UI is gone and public redaction remains explicitly pending")
    print("- the proof claims stay inside what the supplied pixels show")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
