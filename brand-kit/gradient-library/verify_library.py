#!/usr/bin/env python3
"""Validate the complete source-PNG gradient library and isolation boundaries."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures = []
    manifest = read_json(HERE / "library-manifest.json")
    catalogue = read_json(HERE / "catalogue.json")
    palettes = read_json(HERE / "palettes.json")
    assignments = read_json(HERE / "assignments.json")
    approval = read_json(HERE / "approval.json")

    if manifest["sourceCount"] != 43:
        failures.append(f"expected 43 source IDs, found {manifest['sourceCount']}")
    if manifest["uniqueVisualCount"] != 33:
        failures.append(f"expected 33 unique source images, found {manifest['uniqueVisualCount']}")
    if len(manifest["duplicateIdGroups"]) != 10:
        failures.append("expected ten duplicate-ID groups")
    if manifest.get("activeCount") != 33 or len(manifest.get("aliases", {})) != 10:
        failures.append("duplicate policy must expose 33 active cores and ten archived aliases")
    if manifest["qualityExceptions"] != ["MZ-G01"]:
        failures.append("MZ-G01 must remain the explicit 250px quality exception")
    if len(palettes) != 43 or len(catalogue["cores"]) != 43:
        failures.append("palette and runtime catalogues must cover all 43 IDs")

    for row in manifest["sources"]:
        source = HERE / "source-masters" / row["file"]
        static = HERE / "assets" / "static" / f"{row['id'].lower()}.webp"
        if not source.is_file() or sha256(source) != row["sha256"]:
            failures.append(f"source master hash drift: {row['id']}")
        if not static.is_file():
            failures.append(f"missing static twin: {row['id']}")
        if source.is_file():
            with Image.open(source) as image:
                if list(image.size) != [row["width"], row["height"]]:
                    failures.append(f"source dimensions drift: {row['id']}")

    context = next((row for row in assignments["products"] if row["slug"] == "context-engine"), None)
    if not context or context["gradient"] is not None or context["state"] != "unassigned":
        failures.append("Context Engine must remain explicitly unassigned")
    if assignments.get("productionAuthority") is not False:
        failures.append("assignment plan must deny production authority")
    if approval.get("status") != "approved-research-system":
        failures.append("library and animation approval record is missing")
    if approval.get("scope", {}).get("sourceException", {}).get("id") != "MZ-G01":
        failures.append("MZ-G01 accepted source exception is not recorded")
    if approval.get("scope", {}).get("duplicatePolicy") != "remove duplicate IDs from active selection while preserving compatibility aliases and provenance":
        failures.append("approved duplicate-alias policy is not recorded")

    renderer = (BRAND_KIT / "source-pack" / "design-system-export" / "mz-core.js").read_text(encoding="utf-8")
    if renderer.count('getContext("webgl"') != 1:
        failures.append("renderer source must allocate one shared WebGL context")
    if "setCore(element, reference)" not in renderer:
        failures.append("renderer must support one-instance inspector core switching")

    html = (HERE / "index.html").read_text(encoding="utf-8")
    for expression in ("disc", "sphere", "card", "pill", "wings"):
        if f"expression--{expression}" not in html:
            failures.append(f"missing {expression} expression")

    if failures:
        print("COMPLETE GRADIENT LIBRARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("COMPLETE GRADIENT LIBRARY: PASS")
    print("- 43 IDs / 33 unique source PNGs / 10 alias groups")
    print("- every source hash, palette, runtime core and static twin is present")
    print("- five approved expressions use one switchable shared renderer")
    print("- assignments and local decisions remain non-canonical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
