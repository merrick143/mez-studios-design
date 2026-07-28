#!/usr/bin/env python3
"""Assemble the later immutable Mez candidate without mutating frozen rc.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


CERT_DIR = Path(__file__).resolve().parent
BRAND_KIT = CERT_DIR.parent
FROZEN = BRAND_KIT / "releases/production-01/1.0.0-rc.1"
DEFAULT_OUTPUT = BRAND_KIT / "releases/production-01/1.0.0-rc.2"
PACKAGE_NAME = "@mez-systems/design-system-web"
VERSION = "1.0.0-rc.2"
FROZEN_MANIFEST_SHA256 = "c9b5074b79c3f13450b7d826e938b31deda129fc5992ac70b4bafea90e5c4df8"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_json(path: Path, value) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def validate_inputs() -> None:
    if (CERT_DIR / "approval.json").is_file():
        raise SystemExit("Refusing assembly: exact rc.2 is approved and frozen; create a new version for later changes")
    frozen_manifest = FROZEN / "manifest.json"
    if not frozen_manifest.is_file() or sha256(frozen_manifest) != FROZEN_MANIFEST_SHA256:
        raise SystemExit("Refusing assembly: frozen rc.1 manifest changed")

    ui = read_json(BRAND_KIT / "product-ui/approval.json")
    figma = read_json(BRAND_KIT / "figma-companion/approval.json")
    task = read_json(BRAND_KIT / "llm/tasks/TASK-CERT-01-SYSTEM-CERTIFICATION.json")
    source = read_json(CERT_DIR / "certification.source.json")
    if ui.get("verdict") != "approved" or ui.get("productionAuthority") is not False:
        raise SystemExit("Refusing assembly: Product UI foundation approval is absent or widened")
    if figma.get("verdict") != "approved" or figma.get("canonicalAuthority") is not False:
        raise SystemExit("Refusing assembly: Figma mirror approval is absent or widened")
    if task.get("status") not in {"in-progress", "awaiting-human"}:
        raise SystemExit("Refusing assembly: CERT-01 is not active")
    if source.get("releaseCandidate", {}).get("version") != VERSION:
        raise SystemExit("Refusing assembly: certification source does not name rc.2")
    if source.get("authorityBoundary", {}).get("deferredChannelsCertified") is not False:
        raise SystemExit("Refusing assembly: deferred channels were silently certified")


def build(output: Path) -> dict:
    validate_inputs()
    if output.resolve() == FROZEN.resolve():
        raise SystemExit("Refusing assembly: output may not be frozen rc.1")
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(FROZEN, output, copy_function=shutil.copyfile)
    (output / "manifest.json").unlink()

    # Preserve the complete rc.1 verifier as the package-local baseline, changing only its expected version.
    baseline = (output / "verify.py").read_text(encoding="utf-8").replace("1.0.0-rc.1", VERSION)
    write_text(output / "verify_baseline.py", baseline)
    copy_file(CERT_DIR / "verify_certified_release_candidate.py", output / "verify.py")

    # Add the approved non-authoritative mirrors and foundation directions.
    figma_target = output / "mirrors/figma"
    for source in sorted((BRAND_KIT / "figma-companion").glob("*")):
        if source.is_file() and source.suffix in {".json", ".md"}:
            copy_file(source, figma_target / source.name)

    ui_target = output / "product-ui"
    for name in (
        "README.md",
        "approval.json",
        "product-ui-foundation.schema.json",
        "product-ui-foundation.source.json",
        "review.json",
        "round-01-gate-b.json",
    ):
        copy_file(BRAND_KIT / f"product-ui/{name}", ui_target / f"contract/{name}")
    for name in ("product-ui.js", "styles.css"):
        copy_file(BRAND_KIT / f"workbench/product-ui/{name}", ui_target / name)
    html = (BRAND_KIT / "workbench/product-ui/index.html").read_text(encoding="utf-8")
    html = html.replace("../../releases/foundations/dist/index.css", "../foundations/index.css")
    html = html.replace("../../source-pack/design-system-export/assets/wings.svg", "../identity/wings.svg")
    html = html.replace("../../gradient-library/assets/static/", "../identity/gradients/")
    write_text(ui_target / "index.html", html)
    copy_file(
        BRAND_KIT / "workbench/product-ui/fixtures/system-proof.json",
        ui_target / "fixtures/system-proof.json",
    )

    copy_file(BRAND_KIT / "figma-companion/approval.json", output / "authority/approvals/figma-companion.json")
    copy_file(BRAND_KIT / "product-ui/approval.json", output / "authority/approvals/product-ui.json")
    snapshot = read_json(output / "authority/decision-snapshot.json")
    snapshot["humanGateSnapshots"] = [
        "H-FIG-02-FIGMA-COMPANION-APPROVAL",
        "H-UI-01-PRODUCT-UI-FOUNDATION",
    ]
    snapshot["rule"] = (
        "Canonical decision IDs remain unchanged. The Figma and Product UI approvals are bounded, "
        "non-authoritative certification inputs and do not create production authority."
    )
    write_json(output / "authority/decision-snapshot.json", snapshot)

    # Copy only certification evidence that does not depend on the candidate manifest.
    cert_target = output / "certification"
    for name in ("README.md", "certification.schema.json", "certification.source.json", "scope.json", "health-checks.json"):
        copy_file(CERT_DIR / name, cert_target / name)
    for folder in ("audits", "benchmarks"):
        source_root = CERT_DIR / folder
        for source in sorted(source_root.glob("*")):
            if source.is_file():
                copy_file(source, cert_target / folder / source.name)
    write_json(cert_target / "BUILD-BOUNDARY.json", {
        "schemaVersion": "1.0.0",
        "taskId": "TASK-CERT-01-SYSTEM-CERTIFICATION",
        "gateId": "H-CERT-01-SYSTEM-CERTIFICATION",
        "status": "candidate-awaiting-human",
        "version": VERSION,
        "frozenPredecessorManifestSha256": FROZEN_MANIFEST_SHA256,
        "productionAuthority": False,
        "publishAuthority": False,
        "deploymentAuthority": False,
        "consumerIntegrationAuthority": False,
        "rule": "The exact manifest is approved only if Olli closes H-CERT-01. Until then this is gate evidence.",
    })

    package = read_json(output / "package.json")
    package["version"] = VERSION
    package["exports"]["./product-ui"] = "./product-ui/index.html"
    package["exports"]["./certification"] = "./certification/certification.source.json"
    write_json(output / "package.json", package)

    write_text(output / "runtime/version.js", f'''export const PACKAGE_NAME = "{PACKAGE_NAME}";
export const PACKAGE_VERSION = "{VERSION}";
export const PACKAGE_STATUS = "candidate";
export const PRODUCTION_AUTHORITY = false;
''')
    readme = (output / "README.md").read_text(encoding="utf-8")
    readme = readme.replace("1.0.0-rc.1", VERSION)
    readme = readme.replace("TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY", "TASK-CERT-01-SYSTEM-CERTIFICATION")
    readme += "\nThis candidate adds the approved Figma mirror, approved non-production Product UI foundation and bounded whole-system certification evidence. It remains awaiting H-CERT-01.\n"
    write_text(output / "README.md", readme)
    boundary = (output / "guidance/CONSUMER-BOUNDARY.md").read_text(encoding="utf-8")
    boundary += "\nThe Figma companion and Product UI foundation included in rc.2 remain noncanonical and nonproduction. Deferred channel families are not certified by this package.\n"
    write_text(output / "guidance/CONSUMER-BOUNDARY.md", boundary)

    for relative in ("golden/homepage/index.html", "golden/homepage/homepage.js"):
        path = output / relative
        write_text(path, path.read_text(encoding="utf-8").replace("1.0.0-rc.1", VERSION))

    artifacts = []
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item != output / "manifest.json"):
        artifacts.append({
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    content_hash = hashlib.sha256(
        json.dumps(artifacts, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    manifest = {
        "schemaVersion": "1.0.0",
        "name": PACKAGE_NAME,
        "version": VERSION,
        "status": "candidate",
        "productionAuthority": False,
        "taskId": "TASK-CERT-01-SYSTEM-CERTIFICATION",
        "gateId": "H-CERT-01-SYSTEM-CERTIFICATION",
        "contentSha256": content_hash,
        "hashAlgorithm": "sha256(canonical-json(artifacts))",
        "manifestSelfExcluded": True,
        "artifactCount": len(artifacts),
        "artifacts": artifacts,
    }
    write_json(output / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-inputs", action="store_true")
    args = parser.parse_args()
    if args.check_inputs:
        validate_inputs()
        print("MEZ CERTIFIED RELEASE INPUTS: PASS")
        return
    manifest = build(args.output.resolve())
    print("MEZ CERTIFIED RELEASE CANDIDATE: BUILT")
    print(f"- output: {args.output.resolve()}")
    print(f"- artifacts: {manifest['artifactCount']}")
    print(f"- contentSha256: {manifest['contentSha256']}")


if __name__ == "__main__":
    main()
