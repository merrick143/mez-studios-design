#!/usr/bin/env python3
"""Validate Brand Kit Workbench boundaries and imported Living Core files."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
REPO = BRAND_KIT.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    required = [
        REPO / "index.html",
        BRAND_KIT / "README.md",
        BRAND_KIT / "index.html",
        BRAND_KIT / "styles.css",
        BRAND_KIT / "app.js",
        BRAND_KIT / "server.py",
        BRAND_KIT / "source-manifest.json",
        BRAND_KIT / "docs/MIGRATION-PLAN.md",
        BRAND_KIT / "docs/SOURCE-MAP.md",
        BRAND_KIT / "source-pack/products.json",
        BRAND_KIT / "source-pack/gradients-systemized.json",
        BRAND_KIT / "source-pack/palettes-claude-original.json",
        BRAND_KIT / "source-pack/claude-catalogue.json",
        BRAND_KIT / "source-pack/living-core/palettes.json",
        BRAND_KIT / "source-pack/living-core/build.py",
        BRAND_KIT / "source-pack/living-core/candidate.py",
        BRAND_KIT / "source-pack/living-core/candidate-template.html",
        BRAND_KIT / "source-pack/living-core/requirements.txt",
        BRAND_KIT / "scripts/build_claude_catalogue.py",
        BRAND_KIT / "source-pack/design-system-export/gradients.json",
        BRAND_KIT / "source-pack/design-system-export/mz-core.js",
        BRAND_KIT / "source-pack/design-system-export/assets/wings.svg",
        BRAND_KIT / "gradient-library/index.html",
        BRAND_KIT / "gradient-library/app.js",
        BRAND_KIT / "gradient-library/styles.css",
        BRAND_KIT / "gradient-library/build_library.py",
        BRAND_KIT / "gradient-library/verify_library.py",
        BRAND_KIT / "gradient-library/library-manifest.json",
        BRAND_KIT / "gradient-library/catalogue.json",
        BRAND_KIT / "gradient-library/palettes.json",
        BRAND_KIT / "gradient-library/assignments.json",
        BRAND_KIT / "gradient-library/approval.json",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/index.html",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/app.js",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/styles.css",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/profiles.json",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/decision.json",
        BRAND_KIT / "gradient-library/calibration/depth-light-01/verify_calibration.py",
        BRAND_KIT / "product-architecture/index.html",
        BRAND_KIT / "product-architecture/styles.css",
        BRAND_KIT / "product-architecture/app.js",
        BRAND_KIT / "product-architecture/manifest.json",
        BRAND_KIT / "product-architecture/verify_architecture.py",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty workbench file: {path.relative_to(REPO)}")

    manifest = json.loads((BRAND_KIT / "source-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("workbenchStatus") != "non-canonical-migration-proof":
        failures.append("workbench must remain explicitly non-canonical")
    if manifest.get("productionAuthority") is not False:
        failures.append("workbench must deny production authority")
    if len(manifest.get("knownConflicts", [])) != 4:
        failures.append("source manifest must expose all four known conflicts")

    claude_path = BRAND_KIT / "source-pack/palettes-claude-original.json"
    system_path = BRAND_KIT / "source-pack/living-core/palettes.json"
    if sha256(claude_path) != manifest["claudeBenchmark"]["paletteSha256"]:
        failures.append("Claude benchmark palette hash drift")
    claude_catalogue = BRAND_KIT / "source-pack/claude-catalogue.json"
    if sha256(claude_catalogue) != manifest["claudeBenchmark"]["comparisonCatalogueSha256"]:
        failures.append("Claude comparison catalogue hash drift")
    if sha256(system_path) != manifest["systemizedSnapshot"]["paletteSha256"]:
        failures.append("systemized palette hash drift")
    renderer = BRAND_KIT / "source-pack/design-system-export/mz-core.js"
    if sha256(renderer) != manifest["systemizedSnapshot"]["rendererSha256"]:
        failures.append("Living Core renderer hash drift")
    renderer_text = renderer.read_text(encoding="utf-8")
    if renderer_text.count('getContext("webgl"') != 1:
        failures.append("renderer must allocate exactly one WebGL context")

    catalogue = json.loads((BRAND_KIT / "source-pack/design-system-export/gradients.json").read_text(encoding="utf-8"))
    core_ids = {core["id"] for core in catalogue.get("cores", {}).values()}
    if core_ids != {"MZ-G06", "MZ-G13", "MZ-G15", "MZ-G20"}:
        failures.append(f"unexpected imported core set: {sorted(core_ids)}")
    for core_id in core_ids:
        asset = BRAND_KIT / "source-pack/design-system-export/assets/gradients" / f"{core_id.lower()}.webp"
        if not asset.is_file():
            failures.append(f"missing exact static twin: {core_id}")

    html = (BRAND_KIT / "index.html").read_text(encoding="utf-8")
    if html.count("data-mz-core=") != 1:
        failures.append("workbench must expose one systemized comparison core")
    if html.count("data-claude-core=") != 1:
        failures.append("workbench must expose one Claude source-PNG comparison core")
    if html.count('class="static-family-core"') != 5:
        failures.append("approved five-product family must use five exact static cores")
    for phrase in ("AI OS", "Context Engine", "AI Ads System", "Claude Code OS", "Organic Content OS", "MZ-G12"):
        if phrase not in html:
            failures.append(f"approved family missing: {phrase}")
    for phrase in ("Claude original", "Historical systemisation error", "Exact authority", "Non-canonical workbench"):
        if phrase not in html:
            failures.append(f"workbench missing clarity label: {phrase}")

    gitignore = (REPO / ".gitignore").read_text(encoding="utf-8")
    if "brand-kit/workspace/*" not in gitignore:
        failures.append("candidate workspace must be ignored by Git")

    if failures:
        print("BRAND KIT WORKBENCH: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("BRAND KIT WORKBENCH: PASS")
    print("- canonical, Claude benchmark, snapshot and generated layers are explicit")
    print("- approved five-product family uses exact static twins")
    print("- future candidate generation remains isolated from approved assignments")
    print("- palette and renderer snapshot hashes match the recorded provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
