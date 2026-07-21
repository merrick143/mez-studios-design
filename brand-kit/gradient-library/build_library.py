#!/usr/bin/env python3
"""Build the complete Mez Systems source-PNG gradient library.

The source PNG is authority. Palette JSON, WebP static twins and the browser
catalogue are derived outputs. Product assignments and human decisions are not
written by this generator.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, __version__ as pillow_version


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
DEFAULT_DOWNLOADS = Path.home() / "Downloads" / "all-gradients"
SOURCES = HERE / "source-masters"
STATIC = HERE / "assets" / "static"
PALETTES = HERE / "palettes.json"
CATALOGUE = HERE / "catalogue.json"
MANIFEST = HERE / "library-manifest.json"
BUILDER_PATH = BRAND_KIT / "source-pack" / "living-core" / "build.py"
ID_PATTERN = re.compile(r"^MZ-G(\d{2,3})\.png$")
MIN_SOURCE_SIZE = 512


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def load_builder():
    spec = importlib.util.spec_from_file_location("mez_living_core_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {BUILDER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build all Mez source-PNG Living Cores")
    parser.add_argument("--source", type=Path, help="Directory containing MZ-G##.png masters")
    parser.add_argument(
        "--import-sources",
        action="store_true",
        help="Copy source PNGs byte-for-byte into source-masters before building",
    )
    parser.add_argument("--verify", action="store_true", help="Rebuild and fail if tracked outputs drift")
    return parser.parse_args()


def source_files(directory: Path) -> list[tuple[str, Path]]:
    rows = []
    for path in directory.glob("MZ-G*.png"):
        match = ID_PATTERN.fullmatch(path.name)
        if match:
            rows.append((f"MZ-G{int(match.group(1)):02d}", path))
    return sorted(rows, key=lambda row: int(row[0].split("G")[1]))


def snapshot_outputs() -> dict[str, str]:
    paths = [PALETTES, CATALOGUE, MANIFEST, *sorted(STATIC.glob("*.webp"))]
    return {str(path.relative_to(HERE)): sha256(path) for path in paths if path.is_file()}


def main() -> int:
    args = parse_args()
    origin = args.source.expanduser().resolve() if args.source else SOURCES
    if not origin.is_dir() and not args.source:
        origin = DEFAULT_DOWNLOADS
    if not origin.is_dir():
        raise SystemExit(f"Gradient source directory not found: {origin}")

    rows = source_files(origin)
    if not rows:
        raise SystemExit(f"No MZ-G##.png sources found in {origin}")

    if args.import_sources:
        SOURCES.mkdir(parents=True, exist_ok=True)
        for _, source in rows:
            shutil.copy2(source, SOURCES / source.name)
        origin = SOURCES
        rows = source_files(origin)

    before = snapshot_outputs() if args.verify else {}
    builder = load_builder()
    STATIC.mkdir(parents=True, exist_ok=True)

    ids = [core_id for core_id, _ in rows]
    numeric_ids = [int(core_id.split("G")[1]) for core_id in ids]
    missing_ids = [f"MZ-G{value:02d}" for value in range(1, max(numeric_ids) + 1) if value not in numeric_ids]
    raw_palettes = {}
    cores = {}
    sources = []
    hashes: defaultdict[str, list[str]] = defaultdict(list)

    for core_id, source in rows:
        source_hash = sha256(source)
        hashes[source_hash].append(core_id)
        with Image.open(source) as image:
            width, height = image.size
            mode = image.mode
            if width != height:
                raise SystemExit(f"Source is not square: {source.name} ({width}x{height})")
            static_file = f"{core_id.lower()}.webp"
            output = STATIC / static_file
            image.convert("RGB").save(output, "WEBP", quality=92, method=6)

        entry = builder.extract(source)
        raw_palettes[core_id] = entry
        core = builder.canonical_core(entry, static_file)
        cores[core_id.lower()] = {
            "id": core_id,
            "state": "library",
            "product": None,
            "file": static_file,
            "sourceMaster": f"source-masters/{source.name}",
            "sourceSha256": source_hash,
            "sourceWidth": width,
            "sourceHeight": height,
            "sourceQuality": "pass" if min(width, height) >= MIN_SOURCE_SIZE else "below-minimum",
            **core,
        }
        sources.append(
            {
                "id": core_id,
                "file": source.name,
                "sha256": source_hash,
                "width": width,
                "height": height,
                "mode": mode,
                "quality": "pass" if min(width, height) >= MIN_SOURCE_SIZE else "below-minimum",
            }
        )

    duplicate_groups = [group for group in hashes.values() if len(group) > 1]
    aliases = {}
    for group in duplicate_groups:
        ordered = sorted(group, key=lambda value: int(value.split("G")[1]))
        canonical = ordered[0]
        for alias in ordered[1:]:
            aliases[alias] = canonical
            cores[alias.lower()]["aliasOf"] = canonical
    active_ids = [core_id for core_id in ids if core_id not in aliases]
    unique_count = len(hashes)
    source_set_payload = "\n".join(f"{row['file']}:{row['sha256']}" for row in sources).encode()
    source_set_hash = hashlib.sha256(source_set_payload).hexdigest()

    catalogue = {
        "schemaVersion": "1.0.0",
        "scope": "complete-source-png-library",
        "productionAuthority": False,
        "sourceAuthority": "source-masters/*.png",
        "staticAssetContract": {
            "format": "WebP",
            "quality": 92,
            "role": "runtime fallback and distribution preview; never palette authority",
            "path": "assets/static/{file}",
        },
        "livingCoreExtraction": {
            "method": "k-means++",
            "clusters": builder.K,
            "sample": builder.SAMPLE,
            "seed": builder.SEED,
            "colourSpace": "sRGB extraction, linear-space shader mixing",
            "numpy": np.__version__,
            "pillow": pillow_version,
        },
        "cores": cores,
    }
    manifest = {
        "schemaVersion": "1.0.0",
        "productionAuthority": False,
        "sourceRole": "research library pending canonical transfer",
        "sourceSetSha256": source_set_hash,
        "sourceCount": len(sources),
        "uniqueVisualCount": unique_count,
        "activeCount": len(active_ids),
        "ids": ids,
        "activeIds": active_ids,
        "aliases": aliases,
        "missingIdsWithinRange": missing_ids,
        "duplicateIdGroups": duplicate_groups,
        "qualityExceptions": [row["id"] for row in sources if row["quality"] != "pass"],
        "sources": sources,
    }

    write_json(PALETTES, raw_palettes)
    write_json(CATALOGUE, catalogue)
    write_json(MANIFEST, manifest)

    if args.verify:
        after = snapshot_outputs()
        if before != after:
            changed = sorted(set(before) | set(after))
            drift = [name for name in changed if before.get(name) != after.get(name)]
            raise SystemExit("Deterministic rebuild drift: " + ", ".join(drift))

    print(f"Built {len(ids)} IDs from {unique_count} unique PNG masters")
    print(f"Duplicate groups: {len(duplicate_groups)}; missing IDs: {len(missing_ids)}")
    print(f"Quality exceptions: {', '.join(manifest['qualityExceptions']) or 'none'}")
    print(f"Source set SHA-256: {source_set_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
