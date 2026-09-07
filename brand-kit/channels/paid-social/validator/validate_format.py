#!/usr/bin/env python3
"""Validate the approved price-anchored product-proof format pack."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
REPO = PACK.parents[2]
GOLDEN = PACK / "examples" / "golden"
REQUIRED_JSON = [
    "manifest.json", "content-model.schema.json", "tokens/price-anchored-product-proof.tokens.json",
    "assets/asset-map.json", "templates/copy-matrix.json", "templates/figma-template.json",
    "components/anatomy.json", "examples/golden/index.json", "examples/anti/index.json",
    "export-settings.json", "approval.json", "checksums.json",
]

def load(relative: str) -> dict:
    with (PACK / relative).open(encoding="utf-8") as handle:
        return json.load(handle)

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n" or signature[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", signature[16:24])

def validate_craft() -> list[str]:
    failures: list[str] = []
    for relative in REQUIRED_JSON:
        path = PACK / relative
        if not path.exists():
            failures.append(f"missing {relative}")
            continue
        try:
            load(relative)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON {relative}: {exc}")
    if failures:
        return failures
    manifest = load("manifest.json")
    approval = load("approval.json")
    golden = load("examples/golden/index.json")
    anti = load("examples/anti/index.json")
    tokens = load("tokens/price-anchored-product-proof.tokens.json")
    figma = load("templates/figma-template.json")
    if manifest.get("certificationStatus") != "uncertified": failures.append("paid-social channel must remain uncertified")
    if manifest.get("productionAuthority") is not False: failures.append("pack must not claim production authority")
    if manifest.get("format", {}).get("status") != "CRAFT_APPROVED": failures.append("format status must be CRAFT_APPROVED")
    if approval.get("outcomeStatus") != "CRAFT_APPROVED" or approval.get("productionAuthority") is not False: failures.append("approval boundary drifted")
    if tokens.get("headline", {}).get("authoringFamily") != "Geist" or tokens.get("headline", {}).get("weight") != 500: failures.append("headline must remain Geist Medium")
    if figma.get("approvedSectionId") != "1407:936" or figma.get("canvas") != {"width": 1080, "height": 1350}: failures.append("approved Figma route or canvas drifted")
    if len(golden.get("examples", [])) != 5: failures.append("golden set must contain five approved R07 frames")
    if len(anti.get("examples", [])) < 3: failures.append("at least three anti-examples are required")
    for example in golden.get("examples", []):
        path = GOLDEN / example["file"]
        if not path.exists():
            failures.append(f"missing golden PNG {path.name}")
            continue
        try:
            size = png_size(path)
            if size != (1080, 1350): failures.append(f"wrong dimensions for {path.name}: {size}")
        except (OSError, ValueError) as exc:
            failures.append(str(exc))
        if sha256(path) != example.get("sha256"): failures.append(f"hash drift for {path.name}")
    contact = GOLDEN / golden.get("contactSheet", {}).get("file", "")
    if not contact.exists() or sha256(contact) != golden.get("contactSheet", {}).get("sha256"): failures.append("contact-sheet hash missing or drifted")
    skill = REPO / "brand-kit" / "skills" / "build-price-anchored-product-static" / "SKILL.md"
    if not skill.exists(): failures.append("execution skill is missing")
    checksum_index = load("checksums.json")
    for artifact in checksum_index.get("artifacts", []):
        path = PACK / artifact["path"]
        if not path.exists():
            failures.append(f"checksum target missing: {artifact['path']}")
        elif sha256(path) != artifact.get("sha256"):
            failures.append(f"checksum drift: {artifact['path']}")
    return failures

def validate_publish() -> list[str]:
    failures = validate_craft()
    approval = load("approval.json")
    if approval.get("publicUseApproval", {}).get("status") != "approved":
        failures.extend([
            "publish blocker: current product price and destination require campaign preflight",
            "publish blocker: current category-cost evidence and comparison wording require campaign preflight",
            "publish blocker: selected screenshot derivative requires approved-public status",
        ])
    return failures

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("craft", "publish"), default="craft")
    args = parser.parse_args()
    failures = validate_craft() if args.mode == "craft" else validate_publish()
    if failures:
        print(f"FAIL paid-social price-proof ({args.mode})")
        for failure in failures: print(f"- {failure}")
        return 2 if args.mode == "publish" else 1
    print(f"PASS paid-social price-proof ({args.mode})")
    print("- five 1080x1350 golden PNGs and contact sheet verified")
    print("- Geist Medium, Figma source and authority boundary verified")
    print("- three anti-examples and execution skill verified")
    return 0

if __name__ == "__main__": sys.exit(main())
