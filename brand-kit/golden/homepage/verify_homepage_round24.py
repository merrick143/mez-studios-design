#!/usr/bin/env python3
"""Verify GOLD-01 Round 24: simplified and consistent operating proof.

Round 24 keeps the real R23 evidence but removes duplicated explanation. The
right column is titles and visuals only, and the two Context surfaces share one
size and treatment. The public redaction status remains in provenance rather
than customer-facing copy, exactly as Olli requested.
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
FEEDBACK = ROOT / "round-24-feedback.json"
PROVENANCE = WORKBENCH / "assets" / "operating-proof" / "provenance.json"

EXPECTED_ASSETS = {
    "command.png": "97f576860ab1151ef1379ed1bfcf7e44ccd7da5c7376e773f3091eb6326c6f59",
    "backend.png": "6e34b55413ed333ab7230227e705a6bb4642f0b5e61ef6bb47fbf76467f14e73",
    "docs.png": "069b7d76fe274801c6e3208b8f28c2277536854b872b050c0d01272a8b4e70d8",
    "ad-system.png": "af217f1949122469004055050389da7a10169a267dc2de057cd4fde2ef2937e8",
}
REMOVED_UI = (
    "op-index",
    "op-governance",
    "op-record__head",
    "op-record__number",
    "op-record__mech",
    "op-close",
    "op-screen--secondary",
)


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
) -> list[str]:
    failures: list[str] = []

    def fail(code: str, message: str) -> None:
        failures.append(f"{code}: {message}")

    for label, value in (("source", source.get("candidateRevision")), ("review", review.get("candidateRevision"))):
        if value not in {"golden-homepage-01-r24", "golden-homepage-01-r25"}:
            fail("META", f"{label} does not identify R24 or its direct successor R25")
    for label, value in (("feedback", feedback.get("candidateRevision")), ("provenance", provenance.get("candidateRevision"))):
        if value != "golden-homepage-01-r24":
            fail("META", f"{label} no longer identifies the locked R24 proof candidate")
    if source.get("version") not in {"0.24.0-candidate", "0.25.0-candidate"}:
        fail("META", "source version is outside the R24 to R25 lineage")
    if not any(label in html for label in ("Round 24", "Round 25")) or not any(
        revision in javascript for revision in ("golden-homepage-01-r24", "golden-homepage-01-r25")
    ):
        fail("META", "workbench title or review export predates Round 24")
    if feedback.get("productionAuthority") is not False or provenance.get("productionAuthority") is not False:
        fail("META", "feedback and evidence provenance must remain non-production")

    s04_start = html.find('data-review-id="GH-S04"')
    s05_start = html.find('data-review-id="GH-S05"')
    s06_start = html.find('data-review-id="GH-S06"')
    if min(s04_start, s05_start, s06_start) < 0 or not s04_start < s05_start < s06_start:
        fail("BOUNDARY", "GH-S05 must remain between GH-S04 and GH-S06")
        s05 = ""
    else:
        s05 = html[s05_start:s06_start]

    for retired in REMOVED_UI:
        if retired in s05 or f".{retired}" in css:
            fail("SIMPLICITY", f"retired R23 text or asymmetric treatment remains: {retired}")
    if "Internal working-state text visible" in s05 or "Production redaction pending" in s05:
        fail("SIMPLICITY", "the visible redaction notice Olli removed has returned")

    stages = re.findall(r'data-proof-stage="([^"]+)"', s05)
    if stages != ["command", "context", "application"]:
        fail("COMPOSITION", f"expected command, context, application; found {stages}")
    if s05.count('<figure class="op-record') != 3:
        fail("COMPOSITION", "right column must contain exactly three evidence figures")
    titles = re.findall(r'<figcaption class="op-record__title"><h3>([^<]+)</h3></figcaption>', s05)
    if titles != ["Command surface", "Context layer", "System in use"]:
        fail("SIMPLICITY", f"right column must contain the three titles only; found {titles}")

    reel_start = s05.find('<div class="op-reel">')
    right_column = s05[reel_start:] if reel_start >= 0 else ""
    if "<p" in right_column:
        fail("SIMPLICITY", "right evidence column contains explanatory text below its titles")

    context_start = s05.find('data-proof-stage="context"')
    application_start = s05.find('data-proof-stage="application"')
    context = s05[context_start:application_start] if 0 <= context_start < application_start else ""
    if context.count('class="op-screen"') != 2:
        fail("CONSISTENCY", "Context must contain exactly two identically treated op-screen frames")
    if context.count("width=\"1920\"") != 2 or context.count("height=\"1045\"") != 2:
        fail("CONSISTENCY", "Context source images must retain their matching native dimensions")

    asset_refs = re.findall(r'src="\./assets/operating-proof/([^"]+\.png)"', s05)
    if set(asset_refs) != set(EXPECTED_ASSETS) or len(asset_refs) != 4:
        fail("TRUTH", f"GH-S05 must use the four supplied assets exactly once; found {asset_refs}")
    if s05.count('loading="lazy"') != 4:
        fail("MEDIA", "all four below-fold proof images must lazy-load")
    alt_values = re.findall(r'<img\s+[^>]*alt="([^"]*)"', s05, re.S)
    if len(alt_values) != 4 or any(not value or value.lower() in {"image", "screenshot"} for value in alt_values):
        fail("ALT", "each evidence image needs specific, non-generic alt text")

    proof = source.get("proof", {})
    if proof.get("operatingPresentation") != "sticky-proof-title-only-equal-context-pair":
        fail("SOURCE", "source does not record the simplified title-only treatment")
    if proof.get("operatingRecords") != 3 or proof.get("operatingSurfaces") != 4:
        fail("SOURCE", "source must record three titles and four real surfaces")
    if proof.get("operatingStatus") != "evidence-supplied-redaction-pending":
        fail("GOVERNANCE", "internal evidence status was incorrectly promoted")
    if provenance.get("publicRedactionStatus") != "pending":
        fail("GOVERNANCE", "removing visible copy must not approve public redaction")

    provenance_assets = {item.get("file"): item.get("sha256") for item in provenance.get("assets", [])}
    if provenance_assets != EXPECTED_ASSETS:
        fail("ASSET", "provenance hashes do not match the supplied screenshot set")
    for filename, expected_hash in EXPECTED_ASSETS.items():
        path = PROVENANCE.parent / filename
        if not path.exists() or sha256(path) != expected_hash:
            fail("ASSET", f"missing or changed evidence asset: {filename}")

    op_start = css.find("/* -------------------------------------- GH-S05 · operating proof (R24) */")
    op_end = css.find("/* ------------------------------------------------------ GH-S05 · AI OS */")
    op_css = css[op_start:op_end] if op_start >= 0 and op_end > op_start else ""
    if "grid-template-columns: minmax(240px, .72fr) minmax(0, 1.58fr)" not in op_css:
        fail("COMPOSITION", "desktop sticky-proof registers changed")
    if "position: sticky" not in op_css or "position: static" not in op_css:
        fail("RESPONSIVE", "thesis must pin on desktop and return to flow below 900px")
    context_rule = re.search(r"\.op-context-pair \{(.*?)\}", op_css, re.S)
    if not context_rule or "display: grid" not in context_rule.group(1):
        fail("CONSISTENCY", "Context pair must share one full-width grid track")
    if re.search(r"\.op-context-pair[^}]*grid-template-columns", op_css, re.S):
        fail("CONSISTENCY", "Context screenshots must stack at the same width, not split into unequal columns")

    for banned, pattern in (
        ("box-shadow", r"box-shadow\s*:"),
        ("perspective", r"perspective\s*:"),
        ("backdrop-filter", r"backdrop-filter\s*:"),
    ):
        if re.search(pattern, op_css, re.I):
            fail("CANON", f"proof frame uses banned treatment: {banned}")
    if "http://" in html or "http://" in css or "/Users/" in html or "/Users/" in css:
        fail("PORTABILITY", "workbench HTML or CSS contains a non-portable path")

    return failures


def load() -> tuple[str, str, str, dict, dict, dict, dict]:
    return (
        HTML.read_text(encoding="utf-8"),
        CSS.read_text(encoding="utf-8"),
        JS.read_text(encoding="utf-8"),
        json.loads(SOURCE.read_text(encoding="utf-8")),
        json.loads(REVIEW.read_text(encoding="utf-8")),
        json.loads(FEEDBACK.read_text(encoding="utf-8")),
        json.loads(PROVENANCE.read_text(encoding="utf-8")),
    )


def self_test(data: tuple[str, str, str, dict, dict, dict, dict]) -> int:
    html, css, javascript, source, review, feedback, provenance = data
    bad_hash = copy.deepcopy(provenance)
    bad_hash["assets"][0]["sha256"] = "0" * 64
    bad_status = copy.deepcopy(provenance)
    bad_status["publicRedactionStatus"] = "approved"
    cases = (
        ("META", html.replace("Round 25", "Round 22"), css, provenance),
        (
            "SIMPLICITY",
            html.replace(
                '<figcaption class="op-record__title"><h3>Command surface</h3></figcaption>',
                '<figcaption class="op-record__title"><h3>Command surface</h3></figcaption><p>Extra explanation</p>',
                1,
            ),
            css,
            provenance,
        ),
        ("CONSISTENCY", html.replace('<div class="op-screen">\n                  <img\n                    src="./assets/operating-proof/docs.png"', '<div class="op-screen op-screen--secondary">\n                  <img\n                    src="./assets/operating-proof/docs.png"', 1), css, provenance),
        (
            "SIMPLICITY",
            html.replace(
                "</header>\n\n          <div class=\"op-reel\">",
                "<p>Production redaction pending.</p></header>\n\n          <div class=\"op-reel\">",
                1,
            ),
            css,
            provenance,
        ),
        ("GOVERNANCE", html, css, bad_status),
        ("ASSET", html, css, bad_hash),
    )
    misses: list[str] = []
    for expected, mutated_html, mutated_css, mutated_provenance in cases:
        failures = validate(mutated_html, mutated_css, javascript, source, review, feedback, mutated_provenance)
        if not any(item.startswith(f"{expected}:") for item in failures):
            misses.append(expected)
    if misses:
        print("GOLDEN HOMEPAGE ROUND 24 SELF-TEST: FAIL")
        for code in misses:
            print(f"  - mutation was not caught: {code}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 24 SELF-TEST: PASS")
    print("- metadata, simplicity, consistency, governance and asset regressions all fail in memory")
    return 0


def main() -> int:
    required = (HTML, CSS, JS, SOURCE, REVIEW, FEEDBACK, PROVENANCE)
    missing = [path for path in required if not path.exists()]
    if missing:
        print("GOLDEN HOMEPAGE ROUND 24: FAIL")
        for path in missing:
            print(f"  - missing artifact: {path.relative_to(REPO)}")
        return 1
    data = load()
    if "--self-test" in sys.argv:
        return self_test(data)
    failures = validate(*data)
    if failures:
        print("GOLDEN HOMEPAGE ROUND 24: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("GOLDEN HOMEPAGE ROUND 24: PASS")
    print("- the right evidence column contains only three titles and four real visuals")
    print("- both Context screenshots share one full-width treatment")
    print("- visible governance copy is removed while internal provenance stays pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
