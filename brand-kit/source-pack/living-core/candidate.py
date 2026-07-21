#!/usr/bin/env python3
"""Create a non-authoritative Living Core candidate from one square image."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from PIL import Image

from build import K, SAMPLE, SEED, canonical_core, extract


HERE = Path(__file__).resolve().parent
PACK_ROOT = HERE.parent
RUNTIME = PACK_ROOT / "design-system-export" / "mz-core.js"
WINGS = PACK_ROOT / "design-system-export" / "assets" / "wings.svg"
TEMPLATE = HERE / "candidate-template.html"
ID_PATTERN = re.compile(r"^MZ-G\d{2,3}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract one research-only Living Core candidate without mutating Mez authority."
    )
    parser.add_argument("--source", required=True, type=Path, help="Square PNG, JPEG or WebP source")
    parser.add_argument("--id", required=True, dest="candidate_id", help="Provisional ID such as MZ-G54")
    parser.add_argument("--product", required=True, help="Candidate product name")
    parser.add_argument("--output", required=True, type=Path, help="New empty output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()

    if not source.is_file():
        raise SystemExit(f"Source image not found: {source}")
    if not ID_PATTERN.fullmatch(args.candidate_id):
        raise SystemExit("Candidate ID must match MZ-G## or MZ-G###")
    if output.exists():
        raise SystemExit(f"Output already exists. Choose a new directory: {output}")
    for required in (RUNTIME, WINGS, TEMPLATE):
        if not required.is_file():
            raise SystemExit(f"Required Living Core file missing: {required}")

    with Image.open(source) as image:
        width, height = image.size
        if width != height:
            raise SystemExit(f"Source must be square, received {width}x{height}")
        if width < 512:
            raise SystemExit(f"Source must be at least 512px, received {width}px")

    entry = extract(source)
    static_relative = "assets/static-twin.webp"
    core = {
        "id": args.candidate_id,
        "product": args.product,
        "state": "research-only",
        "file": static_relative,
        **canonical_core(entry, static_relative),
    }
    record = {
        "schemaVersion": "1.0.0",
        "candidateId": args.candidate_id,
        "product": args.product,
        "status": "research-only",
        "productionAuthority": False,
        "sourceExpressionApproved": False,
        "source": {
            "filename": source.name,
            "sha256": sha256(source),
            "width": width,
            "height": height,
        },
        "extraction": {
            "method": "k-means++",
            "clusters": K,
            "sample": SAMPLE,
            "seed": SEED,
            "colourSpace": "sRGB extraction, linear-space shader mixing",
        },
        "cores": {"candidate": core},
        "promotionGate": {
            "required": [
                "human visual approval of static and living comparison",
                "recorded product-to-gradient assignment decision",
                "canonical products.json and gradients.json update",
                "portable release rebuild and validation",
            ],
            "mutatesCanonicalAuthority": False,
        },
    }

    output.mkdir(parents=True)
    assets = output / "assets"
    assets.mkdir()
    with Image.open(source) as image:
        resized = image.convert("RGB").resize((1600, 1600), Image.Resampling.LANCZOS)
        resized.save(assets / "static-twin.webp", "WEBP", quality=92, method=6)

    (output / "candidate.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    preview = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{PRODUCT}}", args.product)
        .replace("{{ID}}", args.candidate_id)
        .replace("{{CORE_JSON}}", json.dumps(core, indent=2))
    )
    (output / "preview.html").write_text(preview, encoding="utf-8")
    shutil.copy2(RUNTIME, output / "mz-core.js")
    shutil.copy2(WINGS, output / "wings.svg")

    print(f"Created research-only candidate: {output}")
    print(f"Open preview.html through a local HTTP server and review before promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
