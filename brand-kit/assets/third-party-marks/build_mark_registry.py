#!/usr/bin/env python3
"""Build the third-party mark registry from the copied brand folders.

Deterministic. Reads brand-kit/assets/third-party-marks/marks/<slug>/ and writes
registry.json beside it. Never hand-edit registry.json: change a mark folder and
re-run this script.

Usage:
    python3 brand-kit/assets/third-party-marks/build_mark_registry.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKS = ROOT / "marks"
OUT = ROOT / "registry.json"

# Variant roles, in the order an agent should prefer them for a greyscale
# monochrome surface. "mark" is the freestanding symbol with no enclosing shape.
SVG_ROLES = {
    "mark.svg": "mark",
    "mark-light.svg": "mark-light",
    "mark-dark.svg": "mark-dark",
    "wordmark.svg": "wordmark",
    "logo.svg": "logo",
}


VIEWBOX = re.compile(r'viewBox\s*=\s*["\']([\d.\-\s]+)["\']')
DIMENSION = re.compile(r'\b(width|height)\s*=\s*["\']([\d.]+)')


def measure(svg_path: Path) -> dict | None:
    """Aspect ratio and form of a mark.

    Not every file named mark.svg is a freestanding symbol: some vendors ship a
    horizontal wordmark under the same name. A wordmark dropped into a row of
    symbols wrecks the row, so the form is recorded here and callers filter on
    it rather than eyeballing 40 files.
    """
    try:
        head = svg_path.read_text(errors="replace")[:2000]
    except OSError:
        return None

    width = height = None
    box = VIEWBOX.search(head)
    if box:
        parts = box.group(1).split()
        if len(parts) == 4:
            try:
                width, height = float(parts[2]), float(parts[3])
            except ValueError:
                width = height = None
    if not width or not height:
        dims = dict(DIMENSION.findall(head))
        try:
            width, height = float(dims["width"]), float(dims["height"])
        except (KeyError, ValueError):
            return None

    if not height:
        return None
    ratio = round(width / height, 2)
    # A symbol is roughly square. Past ~1.8:1 it is reading as a lockup.
    form = "symbol" if 0.55 <= ratio <= 1.8 else "wordmark"
    return {"aspect": ratio, "form": form}


def collect(slug_dir: Path) -> dict:
    logos = slug_dir / "logos"
    entry: dict = {"slug": slug_dir.name, "svg": {}, "raster": {}, "appIcon": None}

    manifest_path = slug_dir / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
        except json.JSONDecodeError:
            manifest = {}
        entry["name"] = manifest.get("name", slug_dir.name)
        entry["domain"] = manifest.get("domain")
        primary = (manifest.get("colours") or {}).get("primary")
        entry["brandColour"] = primary
    else:
        entry["name"] = slug_dir.name

    if not logos.is_dir():
        return entry

    for svg in sorted(logos.glob("*.svg")):
        role = SVG_ROLES.get(svg.name, svg.stem)
        entry["svg"][role] = str(svg.relative_to(ROOT))
        if role == "mark":
            shape = measure(svg)
            if shape:
                entry.update(shape)

    app_icon = logos / "app-icon.png"
    if app_icon.exists():
        entry["appIcon"] = str(app_icon.relative_to(ROOT))

    raster_dir = logos / "raster"
    if raster_dir.is_dir():
        for png in sorted(raster_dir.glob("*.png")):
            # mark-512.png -> role "mark", size 512
            stem = png.stem
            if "-" in stem:
                role, _, size = stem.rpartition("-")
            else:
                role, size = stem, ""
            entry["raster"].setdefault(role, {})[size] = str(png.relative_to(ROOT))

    return entry


def main() -> int:
    if not MARKS.is_dir():
        raise SystemExit(f"missing marks directory: {MARKS}")

    brands = [collect(d) for d in sorted(MARKS.iterdir()) if d.is_dir()]

    registry = {
        "schemaVersion": "1.0.0",
        "generatedBy": "brand-kit/assets/third-party-marks/build_mark_registry.py",
        "status": "reference",
        "productionAuthority": False,
        "note": (
            "Third-party marks are other companies' property, held here as reference "
            "assets so Mez surfaces never invent or fake a logo. They are not Mez brand "
            "data and they never enter brand-kit/registry/."
        ),
        "count": len(brands),
        "brands": brands,
    }

    OUT.write_text(json.dumps(registry, indent=2) + "\n")
    with_mark = sum(1 for b in brands if "mark" in b["svg"])
    print(f"wrote {OUT.relative_to(ROOT.parents[2])}")
    print(f"  brands: {len(brands)}  with freestanding mark.svg: {with_mark}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
