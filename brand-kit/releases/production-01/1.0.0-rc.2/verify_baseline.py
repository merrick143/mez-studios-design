#!/usr/bin/env python3
"""Dependency-free verifier for the isolated Mez web design-system package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:  # pragma: no cover - diagnostic path
        fail(f"invalid JSON {path.relative_to(ROOT)}: {error}")
        return {}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_local(source: Path, raw: str, label: str) -> None:
    if "${" in raw or "{{" in raw:
        return
    value = raw.split("?", 1)[0].split("#", 1)[0]
    if not value or value.startswith(("#", "data:", "mailto:", "tel:")):
        return
    parsed = urlparse(value)
    if parsed.scheme or value.startswith("//"):
        fail(f"network/external reference in {label}: {raw}")
        return
    target = (source.parent / value).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        fail(f"reference leaves package in {label}: {raw}")
        return
    if not target.exists():
        fail(f"unresolved reference in {label}: {raw}")


manifest_path = ROOT / "manifest.json"
package_path = ROOT / "package.json"
manifest = read_json(manifest_path)
package = read_json(package_path)

if package.get("name") != "@mez-systems/design-system-web":
    fail("package name is not @mez-systems/design-system-web")
if package.get("version") != "1.0.0-rc.2":
    fail("package version is not 1.0.0-rc.2")
if package.get("status") != "candidate" or package.get("productionAuthority") is not False:
    fail("package must remain a non-authoritative candidate")
if manifest.get("name") != package.get("name") or manifest.get("version") != package.get("version"):
    fail("manifest/package identity mismatch")

artifacts = manifest.get("artifacts", [])
listed = set()
canonical_rows = []
for artifact in artifacts:
    relative = artifact.get("path", "")
    if not relative or relative in listed:
        fail(f"empty or duplicate manifest path: {relative!r}")
        continue
    listed.add(relative)
    path = ROOT / relative
    if not path.is_file():
        fail(f"manifest artifact missing: {relative}")
        continue
    if path.is_symlink():
        fail(f"symlink is not allowed: {relative}")
    actual_size = path.stat().st_size
    actual_hash = sha256(path)
    if artifact.get("bytes") != actual_size:
        fail(f"size mismatch: {relative}")
    if artifact.get("sha256") != actual_hash:
        fail(f"hash mismatch: {relative}")
    canonical_rows.append({"path": relative, "bytes": actual_size, "sha256": actual_hash})

canonical_rows.sort(key=lambda item: item["path"])
content_hash = hashlib.sha256(
    json.dumps(canonical_rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()
if manifest.get("contentSha256") != content_hash:
    fail("manifest contentSha256 mismatch")
if manifest.get("artifactCount") != len(canonical_rows):
    fail("manifest artifactCount mismatch")

actual = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file() and path != manifest_path and "__pycache__" not in path.parts
}
if actual != listed:
    for missing in sorted(actual - listed):
        fail(f"unmanifested file: {missing}")
    for extra in sorted(listed - actual):
        fail(f"manifest lists absent file: {extra}")

required = [
    "styles/index.css",
    "runtime/index.js",
    "runtime/version.js",
    "components/index.js",
    "golden/homepage/index.html",
    "authority/decision-snapshot.json",
    "examples/testimonial-snapshot/BOUNDARY.json",
    "guidance/CONSUMER-BOUNDARY.md",
    "licences/third-party-marks.json",
]
for relative in required:
    if not (ROOT / relative).is_file():
        fail(f"required package entry missing: {relative}")

runtime_files = list((ROOT / "runtime").rglob("*.js"))
runtime_files += list((ROOT / "components").rglob("*.js"))
runtime_files += list((ROOT / "components").rglob("*.css"))
runtime_files += list((ROOT / "golden").rglob("*.js"))
runtime_files += list((ROOT / "golden").rglob("*.html"))
runtime_files += list((ROOT / "golden").rglob("*.css"))
runtime_files += list((ROOT / "styles").rglob("*.css"))
runtime_files += list((ROOT / "foundations").rglob("*.css"))
for path in runtime_files:
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(ROOT).as_posix()
    if re.search(r"https?://|/Users/|brand-kit/", text):
        fail(f"runtime contains network or canonical-checkout dependency: {label}")
    for raw in re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", text):
        resolve_local(path, raw, label)
    for raw in re.findall(r"@import\s+(?:url\()?\s*[\"']([^\"']+)[\"']", text):
        resolve_local(path, raw, label)
    for raw in re.findall(r"url\(\s*[\"']?([^\"')]+)", text):
        if not raw.startswith("var("):
            resolve_local(path, raw, label)
    if path.suffix == ".js":
        for raw in re.findall(r"(?:from\s+|import\s*)[\"']([^\"']+)[\"']", text):
            resolve_local(path, raw, label)
        for raw in re.findall(r"new URL\([\"']([^\"']+)[\"'],\s*import\.meta\.url\)", text):
            if "${" not in raw:
                resolve_local(path, raw, label)

proof = read_json(ROOT / "golden/homepage/assets/operating-proof/payload.json")
if proof.get("status") != "redacted-approved" or proof.get("publicReleaseEligible") is not True:
    fail("operating proof is not exact-byte approved")
if proof.get("sourceProvenance", {}).get("originalPathsIncluded") is not False:
    fail("operating proof exposes original paths")
for record in proof.get("records", []):
    asset = ROOT / "golden/homepage" / record.get("redactedAsset", "")
    if not asset.is_file() or sha256(asset) != record.get("redactedSha256"):
        fail(f"operating-proof derivative mismatch: {record.get('id')}")

boundary = read_json(ROOT / "examples/testimonial-snapshot/BOUNDARY.json")
if boundary.get("productionAuthority") is not False or boundary.get("snapshotDate") != "2026-07-28":
    fail("testimonial example boundary is absent or not dated")
fixture_path = ROOT / "examples/testimonial-snapshot/ai-os-testimonials.json"
fixture = read_json(fixture_path)
testimonials = fixture.get("testimonials", [])
if len(testimonials) != 7 or any(item.get("id") == "daniel-leung" for item in testimonials):
    fail("testimonial snapshot must contain the approved seven records and no Daniel record")
for item in testimonials:
    for raw in (item.get("portrait", {}).get("src"), item.get("social", {}).get("profileImage")):
        if not raw:
            fail(f"testimonial media reference missing: {item.get('id')}")
        else:
            resolve_local(fixture_path, raw, f"testimonial {item.get('id')}")

homepage = (ROOT / "golden/homepage/index.html").read_text(encoding="utf-8")
for token in ("<main", "<footer", "Skip to content", "data-package-diagnostic", "mez-testimonial-marquee"):
    if token not in homepage:
        fail(f"homepage semantic/diagnostic token missing: {token}")
if "review-drawer" in homepage or "review-trigger" in homepage:
    fail("workbench review controls entered the packaged homepage")

decision_snapshot = read_json(ROOT / "authority/decision-snapshot.json")
expected_decisions = {
    "DEC-FOUNDATION-RELEASE-001",
    "DEC-GLOBAL-NAVIGATION-COMPONENT-001",
    "DEC-GOLDEN-HOMEPAGE-001",
    "DEC-HALFTONE-PORTRAIT-COMPONENT-001",
    "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001",
}
if set(decision_snapshot.get("decisionIds", [])) != expected_decisions:
    fail("authority decision snapshot is incomplete")

marquee_js = (ROOT / "components/testimonial-marquee/mez-testimonial-marquee.js").read_text(encoding="utf-8")
portrait_js = (ROOT / "components/halftone-portrait/mez-halftone-portrait.js").read_text(encoding="utf-8")
motion_tokens = [
    'matchMedia("(prefers-reduced-motion: reduce)")',
    "const AUTO_SPEED_PX_PER_SECOND = 24",
    "const INTERACTION_PAUSE_MS = 900",
    'data-copy="primary"',
    'data-copy="clone"',
    'motion-policy="always"',
    "document.visibilityState",
    "requestAnimationFrame",
]
for token in motion_tokens:
    if token not in marquee_js:
        fail(f"CMP-06 motion implementation token missing: {token}")
portrait_tokens = [
    'matchMedia("(prefers-reduced-motion: reduce)")',
    'target.policy === "always"',
    "entry.isIntersecting",
    "video?.pause()",
    "source unavailable",
]
for token in portrait_tokens:
    if token not in portrait_js:
        fail(f"CMP-05 fallback/motion implementation token missing: {token}")

if FAILURES:
    print("MEZ PRODUCTION RELEASE CANDIDATE: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    raise SystemExit(1)

print("MEZ PRODUCTION RELEASE CANDIDATE: PASS")
print(f"- {package['name']} {package['version']} ({manifest['contentSha256'][:12]})")
print(f"- {len(canonical_rows)} artifacts verified")
print("- all runtime design references are package-local")
print("- redacted proof and dated testimonial boundaries verified")
