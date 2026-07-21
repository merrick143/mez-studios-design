#!/usr/bin/env python3
"""Build the deterministic Mez Systems migration identity kernel."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
REPO = BRAND_KIT.parent
VERSION = "0.1.0-alpha.1"
CUTOVER_ID = "CUTOVER-2026-07-21-01"
RELEASE = BRAND_KIT / "releases" / VERSION
REGISTRY = BRAND_KIT / "registry"
AUTHORITY = BRAND_KIT / "authority"
SCHEMAS = BRAND_KIT / "schemas"
GRADIENTS = BRAND_KIT / "gradient-library"
ARCHITECTURE = BRAND_KIT / "product-architecture" / "manifest.json"
DECISIONS = BRAND_KIT / "governance" / "decisions.json"
WINGS = BRAND_KIT / "source-pack" / "design-system-export" / "assets" / "wings.svg"
RENDERER = BRAND_KIT / "source-pack" / "design-system-export" / "mz-core.js"
RELEASE_VERIFIER = HERE / "verify_release.py"
INTERNAL_ROLLBACK_COMMIT = "822aa91"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Mez Systems migration snapshot")
    parser.add_argument("--authority-state", choices=("prepared", "canonical-active"), default="prepared")
    parser.add_argument("--internal-transition-commit", help="Required when activating canonical authority")
    return parser.parse_args()


def canonical_products(authority_state: str) -> dict:
    source = read_json(ARCHITECTURE)
    products = []
    for row in source["products"]:
        products.append(
            {
                "productId": row["productId"],
                "slug": row["slug"],
                "publicName": row["publicName"],
                "function": row["function"],
                "availability": row["availability"],
                "summary": row["summary"],
                "gradientId": row["gradientId"],
                "identityState": "locked",
            }
        )
    return {
        "schemaVersion": "1.0.0",
        "registryId": "mz.systems.registry.products",
        "authorityState": authority_state,
        "productionAuthority": authority_state == "canonical-active",
        "decision": "DEC-PRODUCT-ARCHITECTURE-001",
        "namingPolicy": "literal-product-names-only",
        "products": products,
    }


def canonical_gradients(authority_state: str) -> dict:
    manifest = read_json(GRADIENTS / "library-manifest.json")
    catalogue = read_json(GRADIENTS / "catalogue.json")
    finish = read_json(GRADIENTS / "calibration" / "depth-light-01" / "decision.json")
    aliases = manifest["aliases"]
    records = []
    for source in manifest["sources"]:
        core_id = source["id"]
        core = catalogue["cores"][core_id.lower()]
        static_path = GRADIENTS / "assets" / "static" / f"{core_id.lower()}.webp"
        records.append(
            {
                "id": core_id,
                "state": "compatibility-alias" if core_id in aliases else "active",
                "aliasOf": aliases.get(core_id),
                "source": {
                    "path": f"gradient-library/source-masters/{source['file']}",
                    "sha256": source["sha256"],
                    "width": source["width"],
                    "height": source["height"],
                    "quality": "approved-exception" if core_id in manifest["qualityExceptions"] else "pass",
                },
                "staticTwin": {
                    "path": f"gradient-library/assets/static/{static_path.name}",
                    "sha256": sha256(static_path),
                    "role": "exact-source-derived-static-fallback",
                },
                "runtime": {
                    "anchors": core["anchors"],
                    "shade": core["shade"],
                    "bloom": core["bloom"],
                    "bloomAnchor": core.get("bloomAnchor"),
                },
                "approximation": True,
            }
        )
    return {
        "schemaVersion": "1.0.0",
        "registryId": "mz.systems.registry.gradients",
        "authorityState": authority_state,
        "productionAuthority": authority_state == "canonical-active",
        "decisions": ["DEC-GRADIENT-LIBRARY-001", "DEC-LIVING-CORE-FINISH-001"],
        "sourceAuthority": "exact PNG masters",
        "sourceCount": manifest["sourceCount"],
        "uniqueVisualCount": manifest["uniqueVisualCount"],
        "activeCount": manifest["activeCount"],
        "aliases": aliases,
        "qualityExceptions": manifest["qualityExceptions"],
        "extraction": catalogue["livingCoreExtraction"],
        "finish": {"id": finish["profileId"], "name": finish["profileName"], "values": finish["values"]},
        "gradients": records,
    }


def canonical_assets(authority_state: str, gradients: dict) -> dict:
    assets = [
        {
            "assetId": "mz.systems.asset.wings.canonical",
            "kind": "wings",
            "path": "source-pack/design-system-export/assets/wings.svg",
            "sha256": sha256(WINGS),
            "authorityRole": "canonical-mark",
        },
        {
            "assetId": "mz.systems.asset.runtime.living-core",
            "kind": "runtime",
            "path": "source-pack/design-system-export/mz-core.js",
            "sha256": sha256(RENDERER),
            "authorityRole": "runtime-expression",
        },
    ]
    for row in gradients["gradients"]:
        suffix = row["id"].lower()
        assets.extend(
            [
                {
                    "assetId": f"mz.systems.asset.gradient-source.{suffix}",
                    "kind": "gradient-source",
                    "path": row["source"]["path"],
                    "sha256": row["source"]["sha256"],
                    "authorityRole": "colour-authority",
                },
                {
                    "assetId": f"mz.systems.asset.gradient-static.{suffix}",
                    "kind": "gradient-static",
                    "path": row["staticTwin"]["path"],
                    "sha256": row["staticTwin"]["sha256"],
                    "authorityRole": "static-fallback",
                },
            ]
        )
    return {
        "schemaVersion": "1.0.0",
        "registryId": "mz.systems.registry.assets",
        "authorityState": authority_state,
        "productionAuthority": authority_state == "canonical-active",
        "assets": assets,
    }


def release_path_data(value, authority_state: str):
    copied = json.loads(json.dumps(value))
    copied["authorityState"] = authority_state
    copied["productionAuthority"] = authority_state == "canonical-active"
    if "gradients" in copied:
        for row in copied["gradients"]:
            row["source"]["path"] = f"assets/source/{Path(row['source']['path']).name}"
            row["staticTwin"]["path"] = f"assets/static/{Path(row['staticTwin']['path']).name}"
    if "assets" in copied:
        for row in copied["assets"]:
            name = Path(row["path"]).name
            if row["kind"] == "wings":
                row["path"] = "assets/wings.svg"
            elif row["kind"] == "runtime":
                row["path"] = "runtime/mz-core.js"
            elif row["kind"] == "gradient-source":
                row["path"] = f"assets/source/{name}"
            else:
                row["path"] = f"assets/static/{name}"
    return copied


def build_release(authority_state: str, products: dict, gradients: dict, assets: dict) -> None:
    if RELEASE.exists():
        shutil.rmtree(RELEASE)
    for directory in ("data", "runtime", "assets/source", "assets/static", "schemas"):
        (RELEASE / directory).mkdir(parents=True, exist_ok=True)

    write_json(RELEASE / "data/products.json", release_path_data(products, authority_state))
    write_json(RELEASE / "data/gradients.json", release_path_data(gradients, authority_state))
    write_json(RELEASE / "data/assets.json", release_path_data(assets, authority_state))
    copy_file(DECISIONS, RELEASE / "data/decisions.json")
    copy_file(RENDERER, RELEASE / "runtime/mz-core.js")
    write_json(RELEASE / "runtime/palettes.json", read_json(GRADIENTS / "palettes.json"))
    copy_file(WINGS, RELEASE / "assets/wings.svg")
    for source in sorted((GRADIENTS / "source-masters").glob("MZ-G*.png")):
        copy_file(source, RELEASE / "assets/source" / source.name)
    for static in sorted((GRADIENTS / "assets/static").glob("mz-g*.webp")):
        copy_file(static, RELEASE / "assets/static" / static.name)
    for schema in sorted(SCHEMAS.glob("*.schema.json")):
        copy_file(schema, RELEASE / "schemas" / schema.name)
    copy_file(RELEASE_VERIFIER, RELEASE / "verify.py")

    decisions = [row["id"] for row in read_json(DECISIONS)["decisions"]]
    release_manifest = {
        "schemaVersion": "1.0.0",
        "releaseId": "mz.systems.release.0-1-0-alpha-1",
        "version": VERSION,
        "stage": "migration-snapshot",
        "cutoverId": CUTOVER_ID,
        "authorityState": authority_state,
        "canonicalSnapshot": authority_state == "canonical-active",
        "productionReady": False,
        "decisions": decisions,
        "contents": {
            "products": "data/products.json",
            "gradients": "data/gradients.json",
            "assets": "data/assets.json",
            "decisions": "data/decisions.json",
            "renderer": "runtime/mz-core.js",
            "palettes": "runtime/palettes.json",
            "wings": "assets/wings.svg",
            "artifactManifest": "artifact-manifest.json",
            "verifier": "verify.py",
        },
    }
    write_json(RELEASE / "release.json", release_manifest)
    write_text(
        RELEASE / "README.md",
        "# Mez Systems 0.1.0-alpha.1\n\n"
        "This is the canonical-migration identity snapshot, not the foundation-complete production release. "
        "It contains the literal five-product registry, complete source-backed gradient library, exact static twins, "
        "canonical Wings, shared Living Core renderer, approved decision ledger and schemas.\n\n"
        "Run `python3 verify.py` from this directory. The verifier uses only the Python standard library.\n",
    )

    artifact_rows = []
    for path in sorted(RELEASE.rglob("*")):
        if path.is_file() and path.name != "artifact-manifest.json":
            artifact_rows.append(
                {
                    "path": str(path.relative_to(RELEASE)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    write_json(
        RELEASE / "artifact-manifest.json",
        {
            "schemaVersion": "1.0.0",
            "release": VERSION,
            "cutoverId": CUTOVER_ID,
            "authorityState": authority_state,
            "artifactCount": len(artifact_rows),
            "artifacts": artifact_rows,
        },
    )


def build_authority(authority_state: str, internal_transition_commit: str | None) -> None:
    active = authority_state == "canonical-active"
    if active and not internal_transition_commit:
        raise SystemExit("--internal-transition-commit is required for canonical activation")
    manifest = {
        "schemaVersion": "1.0.0",
        "cutoverId": CUTOVER_ID,
        "status": authority_state,
        "rank": 1 if active else None,
        "repository": "merrick143/mez-studios-design",
        "branch": "codex/brand-kit-workbench",
        "path": "brand-kit",
        "productionAuthority": active,
        "activeRelease": VERSION,
        "previousAuthority": {
            "repository": "merrick143/mezcorp-claudecode",
            "branch": "codex/mez-gradient-system",
            "path": "departments/cmo/brand-library/brands/mez-systems",
            "rollbackCommit": INTERNAL_ROLLBACK_COMMIT,
            "transitionCommit": internal_transition_commit,
            "stateAfterActivation": "pinned-archive-and-consumer-reference",
        },
        "activationConditions": [
            f"release {VERSION} validates from a clean clone",
            f"internal rollback commit {INTERNAL_ROLLBACK_COMMIT} remains reachable",
            "the internal transfer record carries the same cutover ID",
            "all target authority and artifact validators pass",
        ],
        "rollback": {
            "record": "authority/rollback.json",
            "procedure": "Restore rank-one authority to the pinned internal rollback commit and mark this target authority suspended through a new recorded decision.",
        },
    }
    write_json(AUTHORITY / "authority.json", manifest)
    write_json(
        AUTHORITY / "rollback.json",
        {
            "schemaVersion": "1.0.0",
            "cutoverId": CUTOVER_ID,
            "status": "ready",
            "trigger": "Target corruption, unrecoverable validator failure or explicit executive rollback decision.",
            "restore": {
                "repository": "merrick143/mezcorp-claudecode",
                "branch": "codex/mez-gradient-system",
                "commit": INTERNAL_ROLLBACK_COMMIT,
                "path": "departments/cmo/brand-library/brands/mez-systems",
            },
            "steps": [
                "Suspend writes to the standalone brand kit.",
                "Record the rollback decision and reason in both repositories.",
                f"Restore the internal pack from commit {INTERNAL_ROLLBACK_COMMIT} without using the dirty everyday checkout.",
                "Run the internal authority, Phase 1 and migration validators.",
                "Point consumers back to the restored internal authority until a new cutover passes.",
            ],
            "dataLossBoundary": "Work created only after cutover must be exported before rollback or it will remain target-only backlog.",
        },
    )
    write_text(
        AUTHORITY / "CUTOVER.md",
        "# Mez Systems canonical cutover\n\n"
        f"Cutover ID: `{CUTOVER_ID}`  \n"
        f"Active migration snapshot: `{VERSION}`  \n"
        f"Authority state: `{authority_state}`\n\n"
        "The activation is a two-phase handshake. The internal pack remains rank-one until its transfer record "
        "and this authority manifest share the cutover ID and this manifest is `canonical-active`. After activation, "
        "all new design-system work happens in `brand-kit/`; the old internal pack is a pinned archive and consumer reference.\n",
    )


def build_dated_manifest(authority_state: str) -> None:
    paths = [
        AUTHORITY / "authority.json",
        AUTHORITY / "rollback.json",
        REGISTRY / "products.json",
        REGISTRY / "gradients.json",
        REGISTRY / "assets.json",
        DECISIONS,
        *sorted(SCHEMAS.glob("*.schema.json")),
        RELEASE / "release.json",
        RELEASE / "artifact-manifest.json",
    ]
    clean_clone_proof = AUTHORITY / "clean-clone-proof.json"
    if clean_clone_proof.is_file():
        paths.append(clean_clone_proof)
    rows = [
        {"path": str(path.relative_to(BRAND_KIT)), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in paths
    ]
    write_json(
        AUTHORITY / "artifact-manifest-2026-07-21.json",
        {
            "schemaVersion": "1.0.0",
            "manifestId": "MEZ-MIGRATION-ARTIFACTS-2026-07-21",
            "cutoverId": CUTOVER_ID,
            "authorityState": authority_state,
            "historicalManifestPolicy": "The 19 July Phase 0 artifact manifest remains untouched historical evidence.",
            "artifactCount": len(rows),
            "artifacts": rows,
        },
    )


def main() -> int:
    args = parse_args()
    products = canonical_products(args.authority_state)
    gradients = canonical_gradients(args.authority_state)
    assets = canonical_assets(args.authority_state, gradients)
    write_json(REGISTRY / "products.json", products)
    write_json(REGISTRY / "gradients.json", gradients)
    write_json(REGISTRY / "assets.json", assets)
    build_release(args.authority_state, products, gradients, assets)
    build_authority(args.authority_state, args.internal_transition_commit)
    build_dated_manifest(args.authority_state)
    print(f"Built {VERSION} in {args.authority_state} state")
    print(f"Products: {len(products['products'])}; gradients: {len(gradients['gradients'])}; assets: {len(assets['assets'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
