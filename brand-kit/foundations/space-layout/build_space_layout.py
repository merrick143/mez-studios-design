#!/usr/bin/env python3
"""Generate the portable canonical Mez space and layout package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "space-layout.source.json"
SCHEMA = ROOT / "space-layout.schema.json"
README = ROOT / "README.md"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_css(source: dict) -> str:
    lines = ["/* Generated from space-layout.source.json. Do not hand-edit. */", ":root {"]
    for name, value in source["space"].items():
        lines.append(f"  --mz-space-{name}: {value}px;")
    for name, value in source["contentWidths"].items():
        lines.append(f"  --mz-content-{name}: {value}px;")
    compact = source["responsiveProfiles"]["compact"]
    lines.extend([
        f"  --mz-grid-columns: {compact['gridColumns']};",
        f"  --mz-page-gutter: {compact['pageGutter']}px;",
        f"  --mz-grid-gap: {compact['gridGap']}px;",
        f"  --mz-section-compact: {compact['sectionCompact']}px;",
        f"  --mz-section-default: {compact['sectionDefault']}px;",
        f"  --mz-section-spacious: {compact['sectionSpacious']}px;",
        f"  --mz-hero-top: {compact['heroTop']}px;",
        "}",
    ])
    for profile_name in ("medium", "expanded", "wide"):
        profile = source["responsiveProfiles"][profile_name]
        lines.extend([
            f"@media (min-width: {profile['minWidth']}px) {{",
            "  :root {",
            f"    --mz-grid-columns: {profile['gridColumns']};",
            f"    --mz-page-gutter: {profile['pageGutter']}px;",
            f"    --mz-grid-gap: {profile['gridGap']}px;",
            f"    --mz-section-compact: {profile['sectionCompact']}px;",
            f"    --mz-section-default: {profile['sectionDefault']}px;",
            f"    --mz-section-spacious: {profile['sectionSpacious']}px;",
            f"    --mz-hero-top: {profile['heroTop']}px;",
            "  }",
            "}",
        ])
    for name, density in source["densityModes"].items():
        lines.extend([
            f'[data-mz-density="{name}"] {{',
            f"  --mz-density-gap: {density['componentGap']}px;",
            f"  --mz-density-padding: {density['componentPadding']}px;",
            f"  --mz-density-row-min: {density['rowMinHeight']}px;",
            f"  --mz-density-evidence-columns: {density['evidenceColumns']};",
            "}",
        ])
    return "\n".join(lines) + "\n"


def build_tokens(source: dict) -> dict:
    return {
        "$schema": "https://design.mez.systems/schemas/space-layout-tokens-1.0.0.json",
        "generatedFrom": SOURCE.name,
        "status": source["status"],
        "space": {name: {"$type": "dimension", "$value": {"value": value, "unit": "px"}} for name, value in source["space"].items()},
        "contentWidth": {name: {"$type": "dimension", "$value": {"value": value, "unit": "px"}} for name, value in source["contentWidths"].items()},
        "breakpoint": {name: {"$type": "dimension", "$value": {"value": value, "unit": "px"}} for name, value in source["breakpoints"].items()},
        "responsiveProfile": source["responsiveProfiles"],
        "density": source["densityModes"],
    }


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or review.get("verdict") != "approve":
        raise SystemExit("canonical source and approved review are required for package generation")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW):
        shutil.copy2(path, DIST / path.name)
    (DIST / "tokens.css").write_text(build_css(source), encoding="utf-8")
    (DIST / "tokens.json").write_text(json.dumps(build_tokens(source), indent=2) + "\n", encoding="utf-8")
    (DIST / "responsive-contracts.json").write_text(json.dumps({
        "schemaVersion": "1.0.0",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "contentRoles": source["contentRoles"],
        "relationships": source["relationships"],
        "policies": source["policies"],
        "testViewports": source["testViewports"],
    }, indent=2) + "\n", encoding="utf-8")
    package = {
        "schemaVersion": "1.0.0",
        "packageId": "mz.systems.package.space-layout",
        "version": "1.0.0",
        "scope": "space-layout-responsive-foundation",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "decisionIds": source["decisionIds"],
        "reviewGateId": review["gateId"],
        "candidateRevision": source["candidateRevision"],
        "productionReadyForScope": True,
        "entrypoints": {"css": "tokens.css", "tokens": "tokens.json", "responsiveContracts": "responsive-contracts.json", "source": SOURCE.name, "review": REVIEW.name},
        "notes": ["Canonical for the bounded space, layout and responsive scope approved through H-FND-03-SPATIAL-PROOF.", "Typography, colour, geometry, product-expression and release data are not included."],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    artifacts = []
    for path in sorted(item for item in DIST.rglob("*") if item.is_file() and item.name != "manifest.json"):
        artifacts.append({"path": path.relative_to(DIST).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    (DIST / "manifest.json").write_text(json.dumps({
        "schemaVersion": "1.0.0",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "portableRoot": ".",
        "productionReadyForScope": True,
        "artifactCount": len(artifacts),
        "artifacts": artifacts,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"MEZ SPACE + LAYOUT BUILD: {source['status']}")
    print(f"- {len(source['space'])} spacing steps / {len(source['responsiveProfiles'])} profiles / {len(source['densityModes'])} density modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
