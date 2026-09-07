#!/usr/bin/env python3
"""Non-destructive intake scanner and verifier for product screenshots."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
BRAND_KIT = ROOT.parents[1]
INBOX = ROOT / "_INBOX-DROP-HERE"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
PAGE_TYPES = {
    "system-home", "dashboard", "database-board", "database-gallery",
    "database-table", "document", "workflow", "settings", "other",
}
PLATFORMS = {"notion", "web", "desktop-app", "mobile-app", "other"}
NOTION_WIDTHS = {"full-width", "centred", "not-applicable", "unknown"}
CHROME_STATES = {"browser-and-app", "app-only", "none", "unknown"}
PRIVACY_STATES = {"internal", "redaction-required", "public-safe-candidate", "approved-public"}
CAPTURE_STATES = {"raw", "curated", "redacted", "approved"}
ASSET_CLASSES = {"native-capture", "supplied-composition"}
CURATION_TIERS = {"hero", "supporting", "archive", "hold"}
RATIOS = {"1:1", "4:5", "9:16", "16:9", "4:3", "3:4", "free"}
USE_CASES = {"ad-static", "website", "carousel", "presentation", "other"}
VIEW_TREATMENTS = {"native", "near-native", "device-mockup"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def within_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def probe_video(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        raise RuntimeError("ffprobe is required to inventory video assets")
    result = subprocess.run(
        [
            ffprobe,
            "-v", "error",
            "-show_entries", "format=duration:stream=width,height,codec_name",
            "-of", "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    metadata = json.loads(result.stdout)
    stream = next(item for item in metadata["streams"] if "width" in item and "height" in item)
    return {
        "width": stream["width"],
        "height": stream["height"],
        "format": "MP4" if path.suffix.lower() == ".mp4" else path.suffix[1:].upper(),
        "codec": stream.get("codec_name"),
        "durationSeconds": round(float(metadata["format"]["duration"]), 3),
    }


def scan_inbox() -> int:
    inventory: list[dict[str, Any]] = []
    for path in sorted(INBOX.rglob("*")):
        if not path.is_file() or path.name == "README.md" or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                details = probe_video(path)
            else:
                with Image.open(path) as image:
                    width, height = image.size
                    details = {
                        "width": width,
                        "height": height,
                        "format": image.format,
                        "mode": image.mode,
                    }
        except Exception as error:  # pragma: no cover - surfaced in CLI output
            inventory.append({
                "relativePath": path.relative_to(ROOT).as_posix(),
                "error": str(error),
            })
            continue
        inventory.append({
            "relativePath": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            **details,
        })
    print(json.dumps({"inbox": "_INBOX-DROP-HERE", "count": len(inventory), "files": inventory}, indent=2))
    return 0 if all("error" not in item for item in inventory) else 1


def require_enum(errors: list[str], value: Any, allowed: set[str], label: str) -> None:
    if value not in allowed:
        errors.append(f"{label}: expected one of {sorted(allowed)}, got {value!r}")


def verify_capture(capture: Any, manifest_path: Path, seen_ids: set[str], errors: list[str]) -> None:
    prefix = manifest_path.relative_to(ROOT).as_posix()
    if not isinstance(capture, dict):
        errors.append(f"{prefix}: capture must be an object")
        return
    capture_id = capture.get("id")
    label = f"{prefix}:{capture_id or '<missing-id>'}"
    required = {
        "id", "assetClass", "curationTier", "sourceFile", "sha256", "width", "height", "platform", "pageType",
        "notionWidth", "chrome", "privacy", "status", "visibleSensitiveData",
        "description", "proofRole", "alt", "cropRecommendations",
    }
    missing = sorted(required - capture.keys())
    if missing:
        errors.append(f"{label}: missing fields {missing}")
        return
    if not isinstance(capture_id, str) or not capture_id:
        errors.append(f"{label}: id must be a non-empty string")
    elif capture_id in seen_ids:
        errors.append(f"{label}: duplicate capture id")
    else:
        seen_ids.add(capture_id)

    require_enum(errors, capture["assetClass"], ASSET_CLASSES, f"{label}.assetClass")
    require_enum(errors, capture["curationTier"], CURATION_TIERS, f"{label}.curationTier")
    require_enum(errors, capture["platform"], PLATFORMS, f"{label}.platform")
    require_enum(errors, capture["pageType"], PAGE_TYPES, f"{label}.pageType")
    require_enum(errors, capture["notionWidth"], NOTION_WIDTHS, f"{label}.notionWidth")
    require_enum(errors, capture["chrome"], CHROME_STATES, f"{label}.chrome")
    require_enum(errors, capture["privacy"], PRIVACY_STATES, f"{label}.privacy")
    require_enum(errors, capture["status"], CAPTURE_STATES, f"{label}.status")

    source_file = capture["sourceFile"]
    if not isinstance(source_file, str):
        errors.append(f"{label}.sourceFile: expected string")
        return
    source_path = ROOT / source_file
    if not within_root(source_path):
        errors.append(f"{label}.sourceFile: path escapes the library")
        return
    if not source_path.is_file():
        errors.append(f"{label}.sourceFile: missing {source_file}")
        return

    if sha256(source_path) != capture["sha256"]:
        errors.append(f"{label}.sha256: does not match original bytes")
    try:
        with Image.open(source_path) as image:
            actual_width, actual_height = image.size
    except Exception as error:
        errors.append(f"{label}.sourceFile: unreadable image ({error})")
        return
    if (capture["width"], capture["height"]) != (actual_width, actual_height):
        errors.append(
            f"{label}: dimensions are {capture['width']}x{capture['height']}, "
            f"file is {actual_width}x{actual_height}"
        )

    crops = capture["cropRecommendations"]
    if not isinstance(crops, list):
        errors.append(f"{label}.cropRecommendations: expected array")
        return
    crop_ids: set[str] = set()
    for index, crop in enumerate(crops):
        crop_label = f"{label}.cropRecommendations[{index}]"
        if not isinstance(crop, dict):
            errors.append(f"{crop_label}: expected object")
            continue
        crop_id = crop.get("id")
        if not isinstance(crop_id, str) or not crop_id:
            errors.append(f"{crop_label}.id: expected non-empty string")
        elif crop_id in crop_ids:
            errors.append(f"{crop_label}.id: duplicate {crop_id}")
        else:
            crop_ids.add(crop_id)
        require_enum(errors, crop.get("aspectRatio"), RATIOS, f"{crop_label}.aspectRatio")
        require_enum(errors, crop.get("useCase"), USE_CASES, f"{crop_label}.useCase")
        require_enum(errors, crop.get("viewTreatment"), VIEW_TREATMENTS, f"{crop_label}.viewTreatment")
        geometry = crop.get("crop")
        if not isinstance(geometry, dict) or not all(key in geometry for key in ("x", "y", "width", "height")):
            errors.append(f"{crop_label}.crop: expected x, y, width and height")
        else:
            values = [geometry[key] for key in ("x", "y", "width", "height")]
            if not all(isinstance(value, int) for value in values):
                errors.append(f"{crop_label}.crop: all values must be integers")
            elif geometry["x"] < 0 or geometry["y"] < 0 or geometry["width"] < 1 or geometry["height"] < 1:
                errors.append(f"{crop_label}.crop: invalid geometry")
            elif geometry["x"] + geometry["width"] > actual_width or geometry["y"] + geometry["height"] > actual_height:
                errors.append(f"{crop_label}.crop: extends beyond original")
        focal = crop.get("focalPoint")
        if not isinstance(focal, dict) or not all(key in focal for key in ("x", "y")):
            errors.append(f"{crop_label}.focalPoint: expected x and y")
        elif not all(isinstance(focal[key], (int, float)) and 0 <= focal[key] <= 1 for key in ("x", "y")):
            errors.append(f"{crop_label}.focalPoint: values must be between 0 and 1")


def verify() -> int:
    errors: list[str] = []
    try:
        library = load_json(ROOT / "library.json")
        registry = load_json(BRAND_KIT / "registry" / "products.json")
        schema = load_json(ROOT / "schema" / "product-screenshot-manifest.schema.json")
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"[FAIL] {error}")
        return 1
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def validate_schema(manifest: dict[str, Any], relative_path: str) -> None:
        for validation_error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
            field = ".".join(str(part) for part in validation_error.path)
            location = f"{relative_path}:{field}" if field else relative_path
            errors.append(f"{location}: {validation_error.message}")

    if library.get("productionAuthority") is not False:
        errors.append("library.json: productionAuthority must be false")
    canonical = {product["slug"]: product for product in registry.get("products", [])}
    listed = {product.get("slug"): product for product in library.get("products", []) if isinstance(product, dict)}
    if set(listed) != set(canonical):
        errors.append(f"library.json: product slugs must exactly match canonical registry {sorted(canonical)}")

    seen_ids: set[str] = set()
    for slug, product in canonical.items():
        entry = listed.get(slug, {})
        manifest_relative = entry.get("manifest", f"products/{slug}/manifest.json")
        manifest_path = ROOT / manifest_relative
        try:
            manifest = load_json(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            continue
        validate_schema(manifest, manifest_relative)
        expected = {
            "productId": product["productId"],
            "productSlug": slug,
            "publicName": product["publicName"],
            "productionAuthority": False,
        }
        for key, value in expected.items():
            if manifest.get(key) != value:
                errors.append(f"{manifest_relative}: {key} must be {value!r}")
        captures = manifest.get("captures")
        if not isinstance(captures, list):
            errors.append(f"{manifest_relative}: captures must be an array")
            continue
        for capture in captures:
            verify_capture(capture, manifest_path, seen_ids, errors)

    shared_relative = library.get("sharedManifest")
    shared_path = ROOT / str(shared_relative)
    try:
        shared = load_json(shared_path)
        validate_schema(shared, str(shared_relative))
        if shared.get("productId") is not None or shared.get("productionAuthority") is not False:
            errors.append(f"{shared_relative}: shared manifest must have null productId and productionAuthority false")
        captures = shared.get("captures")
        if not isinstance(captures, list):
            errors.append(f"{shared_relative}: captures must be an array")
        else:
            for capture in captures:
                verify_capture(capture, shared_path, seen_ids, errors)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(str(error))

    reference_count = 0
    for collection in library.get("referenceCollections", []):
        if not isinstance(collection, dict):
            errors.append("library.json: every reference collection must be an object")
            continue
        manifest_relative = collection.get("manifest")
        if not isinstance(manifest_relative, str):
            errors.append("library.json: reference collection manifest must be a string")
            continue
        try:
            reference_manifest = load_json(ROOT / manifest_relative)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
            continue
        if reference_manifest.get("productionAuthority") is not False:
            errors.append(f"{manifest_relative}: productionAuthority must be false")
        if reference_manifest.get("usageBoundary") != "reference-only":
            errors.append(f"{manifest_relative}: usageBoundary must be reference-only")
        assets = reference_manifest.get("assets")
        if not isinstance(assets, list):
            errors.append(f"{manifest_relative}: assets must be an array")
            continue
        for asset in assets:
            if not isinstance(asset, dict):
                errors.append(f"{manifest_relative}: every asset must be an object")
                continue
            reference_count += 1
            source_file = asset.get("sourceFile")
            expected_hash = asset.get("sha256")
            if not isinstance(source_file, str) or not isinstance(expected_hash, str):
                errors.append(f"{manifest_relative}: every asset needs sourceFile and sha256")
                continue
            source_path = ROOT / source_file
            if not within_root(source_path):
                errors.append(f"{manifest_relative}:{source_file}: path escapes the library")
            elif not source_path.is_file():
                errors.append(f"{manifest_relative}:{source_file}: missing file")
            elif sha256(source_path) != expected_hash:
                errors.append(f"{manifest_relative}:{source_file}: SHA-256 mismatch")

    if errors:
        print("[FAIL] Product screenshot library")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        f"[PASS] Product screenshot library: {len(canonical)} products, "
        f"{len(seen_ids)} catalogued captures, {reference_count} reference assets"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--verify", action="store_true", help="verify manifests and catalogued files")
    action.add_argument("--scan-inbox", action="store_true", help="print a read-only inventory of inbox images and videos")
    args = parser.parse_args()
    return scan_inbox() if args.scan_inbox else verify()


if __name__ == "__main__":
    sys.exit(main())
