#!/usr/bin/env python3
"""Assemble @mez-systems/design-system-web 1.0.0-rc.1 deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

PLAN_DIR = Path(__file__).resolve().parent
BRAND_KIT = PLAN_DIR.parent.parent
DEFAULT_OUTPUT = BRAND_KIT / "releases/production-01/1.0.0-rc.1"
PACKAGE_NAME = "@mez-systems/design-system-web"
VERSION = "1.0.0-rc.1"
CUTOVER_LEDGER_SHA256 = "9e6efb323924416e7225714f6901a50e1662285ffdb559c2bad6dcc2bc84d587"
DECISIONS = [
    "DEC-FOUNDATION-RELEASE-001",
    "DEC-GLOBAL-NAVIGATION-COMPONENT-001",
    "DEC-GOLDEN-HOMEPAGE-001",
    "DEC-HALFTONE-PORTRAIT-COMPONENT-001",
    "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001",
]
MARKS = [
    "chatgpt", "claude", "gemini", "grok", "mistral", "perplexity",
    "stripe", "notion", "shopify", "figma", "github", "gmail",
    "supabase", "vercel", "n8n", "clickup",
]


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


def copy_tree(source: Path, target: Path) -> None:
    shutil.copytree(source, target, dirs_exist_ok=True, copy_function=shutil.copyfile)


def validate_inputs() -> dict:
    ledger = BRAND_KIT / "governance/decisions.json"
    if sha256(ledger) != CUTOVER_LEDGER_SHA256:
        raise SystemExit("Refusing assembly: immutable cutover ledger hash changed")

    supplement = read_json(BRAND_KIT / "governance/post-cutover-decisions.json")
    records = {item["id"]: item for item in supplement.get("decisions", [])}
    missing = [item for item in DECISIONS if records.get(item, {}).get("status") != "approved"]
    if missing:
        raise SystemExit(f"Refusing assembly: approved decision records missing: {missing}")

    approval_files = [
        BRAND_KIT / "releases/foundations/review.json",
        BRAND_KIT / "components/global-navigation/review.json",
        BRAND_KIT / "golden/homepage/round-29-approval.json",
        BRAND_KIT / "components/halftone-portrait/approval.json",
        BRAND_KIT / "components/testimonial-marquee/approval.json",
    ]
    if not all(path.is_file() for path in approval_files):
        raise SystemExit("Refusing assembly: a bounded approval record is absent")

    promotion = read_json(PLAN_DIR / "candidate-promotion-packet/human-decision.json")
    if promotion.get("verdict") != "approved" or promotion.get("releaseCandidateAssemblyMayStart") is not True:
        raise SystemExit("Refusing assembly: PORT-02 promotion gate is not closed")

    proof_path = PLAN_DIR / "operating-proof-review/payload.json"
    proof = read_json(proof_path)
    if proof.get("status") != "redacted-approved" or proof.get("publicReleaseEligible") is not True:
        raise SystemExit("Refusing assembly: operating-proof derivatives are not exact-byte approved")
    review = proof.get("review") or {}
    if review.get("reviewedBy") != "Olli" or review.get("exactDerivativeBytesInspected") is not True or review.get("verdict") != "approve":
        raise SystemExit("Refusing assembly: operating-proof approval record is incomplete")
    proof_root = PLAN_DIR / "operating-proof-review"
    for record in proof.get("records", []):
        path = proof_root / record["redactedAsset"]
        if not path.is_file() or sha256(path) != record["redactedSha256"]:
            raise SystemExit(f"Refusing assembly: approved derivative hash mismatch for {record['id']}")
    return {"supplement": supplement, "promotion": promotion, "proof": proof}


def copy_component(source: Path, target: Path, names: list[str]) -> None:
    for name in names:
        path = source / name
        if path.is_file():
            copy_file(path, target / name)


def build(output: Path) -> dict:
    inputs = validate_inputs()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    # Canonical foundation distribution, byte-for-byte under one package root.
    copy_tree(BRAND_KIT / "releases/foundations/dist", output / "foundations")

    # Authority snapshot and bounded approval receipts.
    copy_tree(BRAND_KIT / "authority", output / "authority/cutover")
    copy_file(BRAND_KIT / "governance/decisions.json", output / "authority/decisions.cutover.json")
    copy_file(BRAND_KIT / "governance/post-cutover-decisions.json", output / "authority/decisions.post-cutover.json")
    approvals = {
        "foundations": BRAND_KIT / "releases/foundations/review.json",
        "global-navigation": BRAND_KIT / "components/global-navigation/review.json",
        "golden-homepage": BRAND_KIT / "golden/homepage/round-29-approval.json",
        "halftone-portrait": BRAND_KIT / "components/halftone-portrait/approval.json",
        "testimonial-marquee": BRAND_KIT / "components/testimonial-marquee/approval.json",
        "port-02": PLAN_DIR / "candidate-promotion-packet/human-decision.json",
        "operating-proof": PLAN_DIR / "operating-proof-review/payload.json",
    }
    for name, source in approvals.items():
        copy_file(source, output / f"authority/approvals/{name}.json")
    write_json(output / "authority/decision-snapshot.json", {
        "schemaVersion": "1.0.0",
        "status": "candidate-authority-snapshot",
        "productionAuthority": False,
        "cutoverLedgerSha256": CUTOVER_LEDGER_SHA256,
        "decisionIds": DECISIONS,
        "rule": "This immutable candidate snapshot preserves bounded approvals; it does not create production release authority.",
    })

    # Identity inputs and static fallbacks.
    copy_file(BRAND_KIT / "registry/products.json", output / "identity/products.json")
    copy_file(BRAND_KIT / "schemas/product.schema.json", output / "identity/product.schema.json")
    for name in ("catalogue.json", "palettes.json", "library-manifest.json", "assignments.json"):
        copy_file(BRAND_KIT / f"gradient-library/{name}", output / f"identity/{name}")
    copy_tree(BRAND_KIT / "gradient-library/assets/static", output / "identity/gradients")
    copy_file(BRAND_KIT / "source-pack/design-system-export/gradients.json", output / "identity/runtime-gradients.json")
    copy_file(BRAND_KIT / "source-pack/design-system-export/assets/wings.svg", output / "identity/wings.svg")

    core = (BRAND_KIT / "source-pack/design-system-export/mz-core.js").read_text(encoding="utf-8")
    core = core.replace('new URL("./gradients.json", import.meta.url)', 'new URL("../identity/runtime-gradients.json", import.meta.url)')
    core = core.replace('new URL("./assets/gradients/", import.meta.url)', 'new URL("../identity/gradients/", import.meta.url)')
    core = core.replace('new URL("./assets/wings.svg", import.meta.url)', 'new URL("../identity/wings.svg", import.meta.url)')
    write_text(output / "runtime/mz-core.js", core)
    write_text(output / "runtime/index.js", '''export * from "./mz-core.js";
export * from "./version.js";

export const MANIFEST_URL = new URL("../manifest.json", import.meta.url);
export async function getPackageManifest() {
  const response = await fetch(MANIFEST_URL);
  if (!response.ok) throw new Error("Mez package manifest unavailable");
  return response.json();
}
''')

    # Canonical components in their independently approved scopes.
    nav_release = BRAND_KIT / "releases/components/global-navigation/1.0.0"
    nav_target = output / "components/global-navigation"
    copy_tree(nav_release / "components/global-navigation", nav_target)
    for name in ("README.md", "global-navigation.schema.json", "global-navigation.source.json", "review.json"):
        copy_file(nav_release / name, nav_target / name)
    nav_js_path = nav_target / "mez-global-navigation.js"
    nav_js = nav_js_path.read_text(encoding="utf-8")
    nav_js = nav_js.replace('../../source-pack/design-system-export/mz-core.js', '../../runtime/mz-core.js')
    nav_js = nav_js.replace('../../registry/products.json', '../../identity/products.json')
    nav_js = nav_js.replace('../../gradient-library/catalogue.json', '../../identity/catalogue.json')
    nav_js = nav_js.replace('../../gradient-library/assets/static/', '../../identity/gradients/')
    nav_js = nav_js.replace('../../source-pack/design-system-export/assets/wings.svg', '../../identity/wings.svg')
    write_text(nav_js_path, nav_js)

    portrait_source = BRAND_KIT / "components/halftone-portrait"
    portrait_names = [
        "README.md", "approval.json", "gate-b.json", "responsive-evidence.json",
        "halftone-portrait.schema.json", "halftone-portrait.source.json", "review.json",
        "mez-halftone-portrait.css", "mez-halftone-portrait.js",
    ]
    copy_component(portrait_source, output / "components/halftone-portrait", portrait_names)
    copy_tree(portrait_source / "fixtures", output / "components/halftone-portrait/fixtures")

    marquee_source = BRAND_KIT / "components/testimonial-marquee"
    marquee_names = [
        "README.md", "approval.json", "gate-b.json", "testimonial-marquee.schema.json",
        "testimonial-marquee.source.json", "review.json", "mez-testimonial-marquee.css",
        "mez-testimonial-marquee.js",
    ]
    copy_component(marquee_source, output / "components/testimonial-marquee", marquee_names)
    copy_file(marquee_source / "fixtures/react.jsx", output / "components/testimonial-marquee/fixtures/react.jsx")
    write_text(output / "components/index.js", '''export * from "./global-navigation/mez-global-navigation.js";
export * from "./halftone-portrait/mez-halftone-portrait.js";
export * from "./testimonial-marquee/mez-testimonial-marquee.js";
''')
    write_text(output / "styles/index.css", '''@import url("../foundations/index.css");
@import url("../components/global-navigation/mez-global-navigation.css");
@import url("../components/testimonial-marquee/mez-testimonial-marquee.css");
''')

    # Approved expression distributions and their bounded contracts.
    for expression in ("disc", "sphere", "wings-mark", "product-card", "trading-card", "channel-motion", "stress-proof"):
        copy_tree(BRAND_KIT / f"expressions/{expression}/dist", output / f"expressions/{expression}")

    # Dated consumer-owned testimonial example. This is test/demo content, not component truth.
    snapshot = output / "examples/testimonial-snapshot"
    copy_file(marquee_source / "fixtures/ai-os-testimonials.json", snapshot / "ai-os-testimonials.json")
    copy_tree(marquee_source / "fixtures/media", snapshot / "media")
    write_json(snapshot / "BOUNDARY.json", {
        "schemaVersion": "1.0.0",
        "snapshotId": "mez.systems.example.ai-os-testimonials.2026-07-28",
        "snapshotDate": "2026-07-28",
        "status": "dated-example",
        "productionAuthority": False,
        "recordCount": 7,
        "danielIncluded": False,
        "followerValuesLive": False,
        "networkRefresh": False,
        "consentEvidence": "Olli confirmation dated 2026-07-27; see media/PROVENANCE.md.",
        "consumerRule": "A named consumer owns wording, freshness, deployment consent operations and replacement media.",
    })
    missing = read_json(snapshot / "ai-os-testimonials.json")
    missing["fixtureId"] = "ai-os-video-testimonials-missing-media-proof"
    missing["testimonials"][0]["portrait"]["src"] = "./media/intentionally-missing.mp4"
    write_json(output / "examples/missing-media/missing-testimonials.json", missing)
    write_text(output / "examples/missing-media/index.html", '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Missing media proof</title><link rel="stylesheet" href="../../styles/index.css"></head>
<body><main><h1>Missing media proof</h1><mez-testimonial-marquee src="./missing-testimonials.json" label="Testimonials with one unavailable portrait" presentation="social-caption"></mez-testimonial-marquee></main>
<script type="module" src="../../components/index.js"></script></body></html>
''')
    copy_tree(snapshot / "media", output / "examples/missing-media/media")

    # Sixteen reference marks used by the approved homepage composition.
    mark_registry = read_json(BRAND_KIT / "assets/third-party-marks/registry.json")
    brand_records = {record["slug"]: record for record in mark_registry.get("brands", [])}
    notice_records = []
    for slug in MARKS:
        source = BRAND_KIT / f"assets/third-party-marks/marks/{slug}/logos/mark.svg"
        target = output / f"assets/third-party-marks/marks/{slug}/logos/mark.svg"
        copy_file(source, target)
        record = brand_records.get(slug, {})
        notice_records.append({
            "slug": slug,
            "name": record.get("name", slug),
            "domain": record.get("domain"),
            "asset": f"assets/third-party-marks/marks/{slug}/logos/mark.svg",
            "sha256": sha256(target),
        })
    write_json(output / "licences/third-party-marks.json", {
        "schemaVersion": "1.0.0",
        "status": "reference-assets-consumer-review-required",
        "productionAuthority": False,
        "ownedByMez": False,
        "count": len(notice_records),
        "notice": "Marks identify third-party systems in the Golden Homepage example. Their inclusion is not endorsement, ownership or Mez identity authority; named-consumer legal/attribution confirmation remains required before deployment.",
        "marks": notice_records,
    })
    copy_file(BRAND_KIT / "releases/foundations/dist/licences.json", output / "licences/foundations.json")

    # Release-safe Golden Homepage implementation. Workbench review controls and raw proof are excluded.
    homepage_source = BRAND_KIT / "workbench/golden/homepage"
    html = (homepage_source / "index.html").read_text(encoding="utf-8")
    html = html.replace("Round 28 mobile refinement for the first Mez Systems golden homepage.", "Isolated Mez Systems Golden Homepage release candidate.")
    html = html.replace("Mez Systems — Golden Homepage · Round 28", "Mez Systems — Golden Homepage · 1.0.0-rc.1")
    html = html.replace('../../../releases/foundations/dist/index.css', '../../foundations/index.css')
    html = html.replace('../../../components/', '../../components/')
    html = html.replace('../../../source-pack/design-system-export/assets/wings.svg', '../../identity/wings.svg')
    html = html.replace('../../../gradient-library/assets/static/', '../../identity/gradients/')
    html = html.replace('../../components/testimonial-marquee/fixtures/ai-os-testimonials.json', '../../examples/testimonial-snapshot/ai-os-testimonials.json')
    html = html.replace('<p><a href="https://mez.systems/ai-os">Read the source testimonials.</a></p>', '<p>Testimonial content is supplied by the consumer.</p>')
    html = html.replace('./assets/operating-proof/command.png', './assets/operating-proof/redacted/command.png')
    html = html.replace('./assets/operating-proof/backend.png', './assets/operating-proof/redacted/backend.png')
    html = html.replace('./assets/operating-proof/docs.png', './assets/operating-proof/redacted/docs.png')
    html = html.replace('./assets/operating-proof/ad-system.png', './assets/operating-proof/redacted/ad-system.png')
    html = re.sub(r'\n\s*<button class="review-trigger".*?</aside>\n', '\n', html, flags=re.S)
    html = html.replace(
        '<p class="footer-boundary">Routes are supplied by the production consumer.</p>',
        '<p class="footer-boundary">Routes are supplied by the production consumer. <span data-package-diagnostic aria-label="Design-system package version">@mez-systems/design-system-web 1.0.0-rc.1 · manifest loading</span></p>'
    )
    write_text(output / "golden/homepage/index.html", html)

    css = (homepage_source / "styles.css").read_text(encoding="utf-8")
    css = css.replace('../../../gradient-library/assets/static/', '../../identity/gradients/')
    css = re.sub(r'\n/\* -------------------------------------------------------- review tools \*/.*?(?=/\* ------------------------------------------------------ reduced motion \*/)', '\n', css, flags=re.S)
    css = css.replace('body.review-open {\n  overflow: hidden;\n}\n', '')
    css = re.sub(r'\n\.review-target\[data-current-review\].*?\n}\n', '\n', css, flags=re.S)
    css += '''\n/* PORT-03 Gate B query-only material strip. Normal presentation is unchanged. */
html[data-strip="true"] [data-gradient-id],
html[data-strip="true"] [data-hero-material],
html[data-strip="true"] [data-eco-live],
html[data-strip="true"] .hero-card__material {
  background-image: none !important;
  background: var(--page-charcoal) !important;
}
'''
    write_text(output / "golden/homepage/styles.css", css)

    js = (homepage_source / "homepage.js").read_text(encoding="utf-8")
    js = js.replace('../../../components/global-navigation/mez-global-navigation.js?v=1.0.0', '../../components/global-navigation/mez-global-navigation.js')
    js = js.replace('../../../components/testimonial-marquee/mez-testimonial-marquee.js?v=1.0.0', '../../components/testimonial-marquee/mez-testimonial-marquee.js')
    js = js.replace('../../../source-pack/design-system-export/mz-core.js', '../../runtime/mz-core.js')
    js = js.replace('../../../registry/products.json', '../../identity/products.json')
    js = js.replace('../../../gradient-library/catalogue.json', '../../identity/catalogue.json')
    js = js.replace('../../../gradient-library/assets/static/', '../../identity/gradients/')
    js = js.replace('../../../source-pack/design-system-export/assets/wings.svg', '../../identity/wings.svg')
    js = js.replace('../../../assets/third-party-marks/', '../../assets/third-party-marks/')
    js = re.sub(
        r'/\* Section-level keep/revise/kill review tooling\. \*/.*?(?=/\* ============================================================ GH-S03 · principle)',
        '',
        js,
        flags=re.S,
    )
    js += '''\n\n/* Package diagnostic: candidate identity is visible without claiming release authority. */
fetch(new URL("../../manifest.json", import.meta.url))
  .then(response => response.json())
  .then(manifest => {
    const node = document.querySelector("[data-package-diagnostic]");
    if (node) node.textContent = `${manifest.name} ${manifest.version} · ${manifest.contentSha256.slice(0, 12)}`;
  })
  .catch(() => {
    const node = document.querySelector("[data-package-diagnostic]");
    if (node) node.textContent = "@mez-systems/design-system-web 1.0.0-rc.1 · manifest unavailable";
  });
'''
    write_text(output / "golden/homepage/homepage.js", js)
    proof_target = output / "golden/homepage/assets/operating-proof"
    copy_tree(PLAN_DIR / "operating-proof-review/assets/operating-proof/redacted", proof_target / "redacted")
    copy_file(PLAN_DIR / "operating-proof-review/payload.json", proof_target / "payload.json")

    # Golden contract, schemas, source validators, design guidance and packaged skill sources.
    golden_names = [
        "HOMEPAGE-COMPOSITION-PLAN.md", "homepage.schema.json", "homepage.source.json", "review.json",
        "round-28-gate-b.json", "round-29-approval.json",
    ]
    copy_component(BRAND_KIT / "golden/homepage", output / "golden/homepage/contract", golden_names)
    copy_tree(BRAND_KIT / "design-authority", output / "guidance/design-authority")
    copy_tree(BRAND_KIT / "skills", output / "skills")
    copy_tree(BRAND_KIT / "schemas", output / "schemas")
    copy_file(PLAN_DIR / "release-plan.source.json", output / "guidance/release-plan.source.json")
    copy_file(PLAN_DIR / "operating-proof-payload.schema.json", output / "schemas/operating-proof-payload.schema.json")
    copy_file(PLAN_DIR / "verify_production_release_candidate.py", output / "verify.py")
    write_text(output / "validators/verify_production_release_candidate.py", '''#!/usr/bin/env python3
import runpy
from pathlib import Path

runpy.run_path(Path(__file__).resolve().parents[1] / "verify.py", run_name="__main__")
''')
    write_json(output / "validators/claims.json", {
        "schemaVersion": "1.0.0",
        "validator": "verify_production_release_candidate.py",
        "scope": [
            "integrity manifest and deterministic content root",
            "package-local runtime imports and assets",
            "bounded authority decisions and candidate status",
            "approved operating-proof derivatives",
            "dated testimonial example boundary",
            "CMP-05 and CMP-06 motion/fallback implementation claims",
        ],
        "sourceContractValidators": "Executed in the canonical repository by the repository validation receipt; not copied because their paths intentionally target the control-plane checkout.",
    })

    write_text(output / "guidance/CONSUMER-BOUNDARY.md", '''# Consumer boundary

This is an isolated candidate package, not a deployed website and not production release authority.

The package owns approved design tokens, local fonts, identity assets, Living Core runtime, approved component machinery, Golden Homepage composition, responsive behaviour, accessibility/fallback contracts, schemas and validators.

A named consumer owns routes, analytics, SEO, deployment, live availability, testimonial wording and freshness, continuing likeness-consent operations, third-party-mark legal review, application behaviour, commerce, authentication and payments. The dated testimonial snapshot under `examples/` is evidence and demonstration content, not live product truth.
''')
    write_text(output / "README.md", '''# @mez-systems/design-system-web 1.0.0-rc.1

Deterministic, self-contained candidate package assembled by `TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY`.

Status: candidate. Production authority: false. Publishing, deployment and consumer integration are not authorised by these bytes.

Run `python3 -B verify.py`, then serve the package root and open `golden/homepage/`. See `guidance/CONSUMER-BOUNDARY.md` before integration.
''')
    write_json(output / "package.json", {
        "schemaVersion": "1.0.0",
        "name": PACKAGE_NAME,
        "version": VERSION,
        "type": "module",
        "status": "candidate",
        "productionAuthority": False,
        "publishConfig": {"access": "restricted"},
        "exports": {
            ".": "./runtime/index.js",
            "./styles": "./styles/index.css",
            "./components": "./components/index.js",
            "./homepage": "./golden/homepage/index.html",
            "./manifest": "./manifest.json",
        },
        "scripts": {"verify": "python3 -B verify.py"},
    })

    # Manifest all included bytes except the manifest itself (the standard non-circular root).
    write_text(output / "runtime/version.js", f'''export const PACKAGE_NAME = "{PACKAGE_NAME}";
export const PACKAGE_VERSION = "{VERSION}";
export const PACKAGE_STATUS = "candidate";
export const PRODUCTION_AUTHORITY = false;
''')
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
        "taskId": "TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY",
        "gateId": "H-PORT-03-PRODUCTION-RELEASE-CANDIDATE",
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
        print("MEZ PRODUCTION RELEASE INPUTS: PASS")
        return
    manifest = build(args.output.resolve())
    print("MEZ PRODUCTION RELEASE CANDIDATE: BUILT")
    print(f"- output: {args.output.resolve()}")
    print(f"- artifacts: {manifest['artifactCount']}")
    print(f"- contentSha256: {manifest['contentSha256']}")


if __name__ == "__main__":
    main()
