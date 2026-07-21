#!/usr/bin/env python3
"""Build a portable, read-only catalogue from Claude's original palette cache.

The output exists only for visual comparison inside the migration workbench.
It does not promote the Claude dataset or mutate the canonical systemized pack.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
SOURCE_PACK = BRAND_KIT / "source-pack"
BUILD_PATH = SOURCE_PACK / "living-core" / "build.py"
PALETTES_PATH = SOURCE_PACK / "palettes-claude-original.json"
OUTPUT_PATH = SOURCE_PACK / "claude-catalogue.json"

PRODUCTS = {
    "MZ-G13": ("aios", "AI OS", "locked", "mz-g13.webp"),
    "MZ-G20": ("aurora", "Aurora", "candidate", "mz-g20.webp"),
    "MZ-G06": ("prism", "Prism", "candidate", "mz-g06.webp"),
    "MZ-G15": ("forge", "Forge", "candidate", "mz-g15.webp"),
}


def load_builder():
    spec = importlib.util.spec_from_file_location("living_core_build", BUILD_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {BUILD_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    builder = load_builder()
    palettes = json.loads(PALETTES_PATH.read_text(encoding="utf-8"))
    cores = {}
    for core_id, (slug, product, state, static_twin) in PRODUCTS.items():
        core = {
            "product": product,
            "id": core_id,
            "state": state,
            "file": static_twin,
            "sourceMethod": "Claude source-PNG extraction cache",
        }
        core.update(builder.canonical_core(palettes[core_id], static_twin))
        cores[slug] = core

    output = {
        "schemaVersion": "1.0.0",
        "scope": "comparison-only",
        "productionAuthority": False,
        "source": "palettes-claude-original.json",
        "cores": cores,
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(BRAND_KIT.parent)}")


if __name__ == "__main__":
    main()
