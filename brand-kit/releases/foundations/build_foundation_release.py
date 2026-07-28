#!/usr/bin/env python3
"""Build the portable Mez Systems foundation release without changing source packages."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
SOURCE = ROOT / "release.source.json"
SCHEMA = ROOT / "release.schema.json"
README = ROOT / "README.md"
MIGRATION = ROOT / "MIGRATION.md"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source_package(declared: dict, source_dist: Path) -> dict:
    package_path = source_dist / "package.json"
    manifest_path = source_dist / "manifest.json"
    if not package_path.is_file() or not manifest_path.is_file():
        raise SystemExit(f"missing canonical package metadata: {declared['key']}")
    if sha256(package_path) != declared["packageSha256"] or sha256(manifest_path) != declared["manifestSha256"]:
        raise SystemExit(f"declared source hash drift: {declared['key']}")
    package = read_json(package_path)
    review_path = source_dist / "review.json"
    if not review_path.is_file():
        raise SystemExit(f"missing approval record: {declared['key']}")
    review = read_json(review_path)
    required = {
        "packageId": declared["packageId"],
        "foundationId": declared["foundationId"],
        "version": declared["version"],
        "status": "canonical",
        "reviewGateId": declared["reviewGateId"],
        "productionReadyForScope": True,
    }
    for key, expected in required.items():
        if package.get(key) != expected:
            raise SystemExit(f"canonical package contract drift: {declared['key']} {key}")
    if review.get("gateId") != declared["reviewGateId"] or review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        raise SystemExit(f"source package is not backed by its approved gate: {declared['key']}")
    return package


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        raise SystemExit("canonical foundation release source and production authority are required")
    if review.get("gateId") != source.get("candidateGateId") or review.get("verdict") != "approve" or review.get("productionAuthority") is not True:
        raise SystemExit("canonical foundation release must be backed by its approved human gate")
    if review.get("decisionId") != "DEC-FOUNDATION-RELEASE-001" or review.get("resultingStatus") != "canonical":
        raise SystemExit("foundation release approval decision is missing or incomplete")

    source_hashes: dict[str, dict[str, str]] = {}
    packages: dict[str, dict] = {}
    for declared in source["packages"]:
        source_dist = BRAND_KIT / "foundations" / declared["key"] / "dist"
        packages[declared["key"]] = validate_source_package(declared, source_dist)
        source_hashes[declared["key"]] = {
            "packageSha256": sha256(source_dist / "package.json"),
            "manifestSha256": sha256(source_dist / "manifest.json"),
        }

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "packages").mkdir(parents=True)
    for declared in source["packages"]:
        source_dist = BRAND_KIT / "foundations" / declared["key"] / "dist"
        shutil.copytree(source_dist, DIST / "packages" / declared["key"])
    for path in (SOURCE, SCHEMA, README, MIGRATION, REVIEW):
        shutil.copy2(path, DIST / path.name)

    imports = "\n".join(f'@import url("{path}");' for path in source["loadOrder"])
    (DIST / "index.css").write_text(
        "/* Generated from release.source.json. Copy the complete release directory. */\n" + imports + "\n",
        encoding="utf-8",
    )
    write_json(DIST / "load-order.json", {
        "schemaVersion": "1.0.0",
        "releaseId": source["releaseId"],
        "entrypoint": "index.css",
        "order": source["loadOrder"],
        "reason": "Typography defines fonts and type roles; colour defines semantic channels; space-layout defines responsive geometry; geometry tokens define shape and motion; controls consume every preceding layer.",
    })
    licences = []
    for path in sorted((DIST / "packages").rglob("OFL.txt")):
        licences.append({
            "path": path.relative_to(DIST).as_posix(),
            "sha256": sha256(path),
            "license": "SIL Open Font License 1.1",
        })
    write_json(DIST / "licences.json", {
        "schemaVersion": "1.0.0",
        "releaseId": source["releaseId"],
        "licences": licences,
        "note": "Licence texts remain beside their font files; this inventory does not replace them.",
    })
    write_json(DIST / "package.json", {
        "schemaVersion": "1.0.0",
        "packageId": "mz.systems.package.foundation-release",
        "releaseId": source["releaseId"],
        "version": source["version"],
        "scope": "typography-colour-space-layout-geometry-controls",
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "reviewGateId": source["candidateGateId"],
        "productionReadyForScope": True,
        "productionAuthority": True,
        "decisionIds": source["decisionIds"],
        "entrypoints": {
            "css": "index.css",
            "loadOrder": "load-order.json",
            "licences": "licences.json",
            "source": SOURCE.name,
            "review": REVIEW.name,
            "migration": MIGRATION.name,
        },
        "packages": [
            {
                "key": declared["key"],
                "path": f"packages/{declared['key']}",
                "packageId": declared["packageId"],
                "version": declared["version"],
                "reviewGateId": declared["reviewGateId"],
                **source_hashes[declared["key"]],
            }
            for declared in source["packages"]
        ],
        "notes": [
            "The four nested packages are byte-for-byte copies of their canonical 1.0.0 distributions.",
            "The assembled release is canonical and production-authorised for its bounded foundation scope through H-FND-05-FOUNDATION-RELEASE.",
        ],
    })

    artifacts = []
    for path in sorted(item for item in DIST.rglob("*") if item.is_file() and item.name != "manifest.json"):
        artifacts.append({
            "path": path.relative_to(DIST).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    write_json(DIST / "manifest.json", {
        "schemaVersion": "1.0.0",
        "releaseId": source["releaseId"],
        "version": source["version"],
        "status": source["status"],
        "candidateRevision": source["candidateRevision"],
        "portableRoot": ".",
        "productionReadyForScope": True,
        "productionAuthority": True,
        "sourcePackageCount": len(source["packages"]),
        "artifactCount": len(artifacts),
        "artifacts": artifacts,
    })
    print("MEZ FOUNDATION RELEASE BUILD: canonical")
    print(f"- {len(source['packages'])} canonical packages copied without mutation")
    print(f"- {len(licences)} font licence records / {len(artifacts)} release artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
