#!/usr/bin/env python3
"""Generate the portable canonical Mez geometry and controls package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "geometry-controls.source.json"
SCHEMA = ROOT / "geometry-controls.schema.json"
README = ROOT / "README.md"
REVIEW = ROOT / "review.json"
DIST = ROOT / "dist"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_tokens_css(source: dict) -> str:
    lines = ["/* Generated from geometry-controls.source.json. Do not hand-edit. */", ":root {"]
    for name, value in source["radii"].items():
        lines.append(f"  --mz-radius-{name}: {value}px;")
    for name, value in source["borders"].items():
        lines.append(f"  --mz-border-width-{name}: {value}px;")
    for name, value in source["depth"].items():
        lines.append(f"  --mz-depth-{name.replace('H', '-h').lower()}: {value};")
    motion = source["motion"]
    lines.extend([
        f"  --mz-motion-fast: {motion['durationFast']}ms;",
        f"  --mz-motion-default: {motion['durationDefault']}ms;",
        f"  --mz-motion-control-ease: {motion['easeControl']};",
        f"  --mz-control-hover-lift: {motion['hoverLift']}px;",
        f"  --mz-control-icon-travel: {motion['iconTravel']}px;",
        f"  --mz-focus-width: {source['focus']['width']}px;",
        f"  --mz-focus-offset: {source['focus']['offset']}px;",
    ])
    for name, scale in source["controlScale"].items():
        lines.extend([
            f"  --mz-control-{name}-height: {scale['height']}px;",
            f"  --mz-control-{name}-padding-inline: {scale['paddingInline']}px;",
        ])
    icon = source["iconControl"]
    lines.extend([
        f"  --mz-icon-control-size: {icon['defaultSize']}px;",
        f"  --mz-icon-control-compact-size: {icon['compactSize']}px;",
        f"  --mz-control-icon-size: {icon['iconSize']}px;",
        f"  --mz-control-icon-gap: {icon['iconGap']}px;",
    ])
    fields = source["fields"]
    for name, value in fields.items():
        css_name = "".join(("-" + char.lower()) if char.isupper() else char for char in name)
        lines.append(f"  --mz-field-{css_name}: {value}px;")
    lines.append("}")
    return "\n".join(lines) + "\n"


def build_controls_css() -> str:
    return """/* Generated Mez control primitives. Load canonical typography, colour, space-layout, then tokens.css first. */
.mz-control {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--mz-control-icon-gap);
  min-height: var(--mz-control-default-height);
  padding-inline: var(--mz-control-default-padding-inline);
  border: var(--mz-border-width-hairline) solid transparent;
  border-radius: var(--mz-radius-control);
  font: var(--mz-type-ui-control-weight) var(--mz-type-ui-control-size)/var(--mz-type-ui-control-leading) var(--mz-font-body);
  letter-spacing: var(--mz-type-ui-control-tracking);
  text-decoration: none;
  cursor: pointer;
  transform: translateY(0);
  transition: transform var(--mz-motion-default) var(--mz-motion-control-ease), box-shadow var(--mz-motion-default) var(--mz-motion-control-ease), background-color var(--mz-motion-fast) linear, border-color var(--mz-motion-fast) linear, color var(--mz-motion-fast) linear;
}
.mz-control[data-variant="primary"] { color: var(--mz-action-primary-foreground); background: var(--mz-action-primary-background); box-shadow: var(--mz-depth-inset-highlight); }
.mz-control[data-variant="secondary"] { color: var(--mz-action-secondary-foreground); background: var(--mz-action-secondary-background); border-color: var(--mz-action-secondary-border); }
.mz-control[data-variant="tertiary"] { min-height: 36px; padding-inline: 2px; color: var(--mz-text-primary); background: transparent; border-radius: var(--mz-radius-fine); }
.mz-control[data-variant="destructive"] { color: var(--mz-colour-neutral-0); background: var(--mz-feedback-danger-text); }
[data-mz-mode="dark"] .mz-control[data-variant="primary"], .mz-control[data-variant="inverse-primary"] { color: var(--mz-colour-neutral-950); background: var(--mz-colour-neutral-0); }
[data-mz-mode="dark"] .mz-control[data-variant="secondary"], .mz-control[data-variant="inverse-secondary"] { color: var(--mz-text-inverse); background: transparent; border-color: var(--mz-border-inverse); }
[data-mz-mode="dark"] .mz-control[data-variant="tertiary"], .mz-control[data-variant="inverse-tertiary"] { color: var(--mz-text-inverse); background: transparent; }
.mz-control[data-size="compact"] { min-height: var(--mz-control-compact-height); padding-inline: var(--mz-control-compact-padding-inline); font-size: 13px; }
.mz-control[data-size="prominent"] { min-height: var(--mz-control-prominent-height); padding-inline: var(--mz-control-prominent-padding-inline); }
.mz-control[data-full] { width: 100%; }
.mz-control svg { width: var(--mz-control-icon-size); height: var(--mz-control-icon-size); flex: none; transition: transform var(--mz-motion-default) var(--mz-motion-control-ease); }
.mz-control:focus-visible, .mz-field:focus-visible, .mz-choice input:focus-visible + span, .mz-switch input:focus-visible + span { outline: var(--mz-focus-width) solid var(--mz-focus-ring); outline-offset: var(--mz-focus-offset); }
.mz-control:active { transform: translateY(0); box-shadow: none; }
.mz-control:disabled, .mz-control[aria-disabled="true"] { color: var(--mz-disabled-text); background: var(--mz-disabled-surface); border-color: var(--mz-disabled-border); cursor: not-allowed; box-shadow: none; transform: none; }
.mz-control[data-loading="true"] { pointer-events: none; }
.mz-control[data-loading="true"] .mz-control__label { visibility: hidden; }
.mz-control__spinner { position: absolute; display: none; width: 18px; height: 18px; border: 2px solid currentColor; border-right-color: transparent; border-radius: var(--mz-radius-full); animation: mz-spin 720ms linear infinite; }
.mz-control[data-loading="true"] .mz-control__spinner { display: block; }
.mz-icon-control { width: var(--mz-icon-control-size); min-width: var(--mz-icon-control-size); padding: 0; }
.mz-icon-control[data-size="compact"] { width: var(--mz-icon-control-compact-size); min-width: var(--mz-icon-control-compact-size); }

.mz-field-group { display: grid; gap: var(--mz-field-label-gap); }
.mz-field-label { color: var(--mz-text-primary); font: var(--mz-type-ui-label-weight) var(--mz-type-ui-label-size)/var(--mz-type-ui-label-leading) var(--mz-font-body); letter-spacing: var(--mz-type-ui-label-tracking); text-transform: uppercase; }
.mz-field { width: 100%; min-height: var(--mz-field-height); padding: 0 var(--mz-field-padding-inline); border: var(--mz-border-width-hairline) solid var(--mz-border-strong); border-radius: var(--mz-radius-control); color: var(--mz-text-primary); background: var(--mz-surface-base); font: var(--mz-type-body-default-weight) var(--mz-type-body-default-size)/var(--mz-type-body-default-leading) var(--mz-font-body); }
textarea.mz-field { min-height: var(--mz-field-textarea-min-height); padding-block: 12px; resize: vertical; }
.mz-field:hover:not(:disabled) { border-color: var(--mz-text-primary); }
.mz-field:disabled { color: var(--mz-disabled-text); background: var(--mz-disabled-surface); border-color: var(--mz-disabled-border); }
.mz-field[aria-invalid="true"] { border-width: var(--mz-border-width-emphasis); border-color: var(--mz-feedback-danger-border); }
.mz-field-message { display: flex; gap: var(--mz-field-message-gap); color: var(--mz-text-muted); font: var(--mz-type-caption-weight) var(--mz-type-caption-size)/var(--mz-type-caption-leading) var(--mz-font-body); }
.mz-field-message[data-state="error"] { color: var(--mz-feedback-danger-text); }

.mz-choice, .mz-switch { position: relative; display: inline-flex; align-items: center; min-height: 48px; gap: 12px; cursor: pointer; }
.mz-choice input, .mz-switch input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.mz-choice__mark { display: grid; width: var(--mz-field-choice-size); height: var(--mz-field-choice-size); place-items: center; border: var(--mz-border-width-hairline) solid var(--mz-border-strong); border-radius: var(--mz-radius-fine); background: var(--mz-surface-base); }
.mz-choice input[type="radio"] + .mz-choice__mark { border-radius: var(--mz-radius-full); }
.mz-choice input:checked + .mz-choice__mark { border-color: var(--mz-action-primary-background); color: var(--mz-action-primary-foreground); background: var(--mz-action-primary-background); }
.mz-choice input:checked + .mz-choice__mark::after { width: 8px; height: 8px; border-radius: inherit; background: currentColor; content: ""; }
.mz-switch__track { position: relative; width: var(--mz-field-switch-width); height: var(--mz-field-switch-height); border: var(--mz-border-width-hairline) solid var(--mz-border-strong); border-radius: var(--mz-radius-full); background: var(--mz-surface-recessed); transition: background var(--mz-motion-fast) linear; }
.mz-switch__track::after { position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: var(--mz-radius-full); background: var(--mz-text-muted); content: ""; transition: transform var(--mz-motion-default) var(--mz-motion-control-ease); }
.mz-switch input:checked + .mz-switch__track { background: var(--mz-action-primary-background); }
.mz-switch input:checked + .mz-switch__track::after { background: var(--mz-action-primary-foreground); transform: translateX(20px); }

@media (hover: hover) {
  .mz-control:not(:disabled):not([aria-disabled="true"]):not([data-variant="tertiary"]):not([data-variant="inverse-tertiary"]):hover { transform: translateY(var(--mz-control-hover-lift)); box-shadow: var(--mz-depth-contact), var(--mz-depth-inset-highlight); }
  .mz-control:hover svg[data-directional] { transform: translateX(var(--mz-control-icon-travel)); }
  .mz-control[data-variant="tertiary"]:hover, .mz-control[data-variant="inverse-tertiary"]:hover { text-decoration: underline; text-underline-offset: 4px; }
}
@media (prefers-reduced-motion: reduce) {
  .mz-control, .mz-control svg, .mz-switch__track::after { transition-duration: .001ms; transform: none !important; }
  .mz-control__spinner { animation-duration: 1.4s; }
}
@media (forced-colors: active) {
  .mz-control, .mz-field, .mz-choice__mark, .mz-switch__track { forced-color-adjust: auto; }
}
@keyframes mz-spin { to { transform: rotate(360deg); } }
"""


def build_tokens(source: dict) -> dict:
    return {
        "$schema": "https://design.mez.systems/schemas/geometry-controls-tokens-1.0.0.json",
        "generatedFrom": SOURCE.name,
        "status": source["status"],
        "radius": {name: {"$type": "dimension", "$value": {"value": value, "unit": "px"}} for name, value in source["radii"].items()},
        "borderWidth": {name: {"$type": "dimension", "$value": {"value": value, "unit": "px"}} for name, value in source["borders"].items()},
        "shadow": {name: {"$type": "shadow", "$value": value} for name, value in source["depth"].items()},
        "controlScale": source["controlScale"],
        "iconControl": source["iconControl"],
        "fields": source["fields"],
        "focus": source["focus"],
        "motion": source["motion"],
    }


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or review.get("verdict") != "approve":
        raise SystemExit("canonical source and approved review are required for package generation")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW):
        shutil.copy2(path, DIST / path.name)
    (DIST / "tokens.css").write_text(build_tokens_css(source), encoding="utf-8")
    (DIST / "controls.css").write_text(build_controls_css(), encoding="utf-8")
    (DIST / "tokens.json").write_text(json.dumps(build_tokens(source), indent=2) + "\n", encoding="utf-8")
    (DIST / "control-contracts.json").write_text(json.dumps({
        "schemaVersion": "1.0.0",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "variants": source["variants"],
        "stateContracts": source["stateContracts"],
        "policies": source["policies"],
        "testViewports": source["testViewports"],
    }, indent=2) + "\n", encoding="utf-8")
    package = {
        "schemaVersion": "1.0.0",
        "packageId": "mz.systems.package.geometry-controls",
        "version": "1.0.0",
        "scope": "geometry-border-depth-controls-foundation",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "decisionIds": source["decisionIds"],
        "reviewGateId": review["gateId"],
        "candidateRevision": source["candidateRevision"],
        "productionReadyForScope": True,
        "entrypoints": {"tokensCss": "tokens.css", "controlsCss": "controls.css", "tokens": "tokens.json", "contracts": "control-contracts.json", "source": SOURCE.name, "review": REVIEW.name},
        "dependencies": {"typography": "mz.systems.package.typography@1.0.0", "colour": "mz.systems.package.colour@1.0.0", "spaceLayout": "mz.systems.package.space-layout@1.0.0"},
        "notes": ["Canonical for the bounded geometry, depth and controls scope approved through H-FND-04-CONTROL-PROOF.", "Product expressions, homepage, consumers, Figma and release data are not included."],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    artifacts = []
    for path in sorted(item for item in DIST.rglob("*") if item.is_file() and item.name != "manifest.json"):
        artifacts.append({"path": path.relative_to(DIST).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    (DIST / "manifest.json").write_text(json.dumps({
        "schemaVersion": "1.0.0", "foundationId": source["foundationId"], "status": source["status"],
        "portableRoot": ".", "productionReadyForScope": True, "artifactCount": len(artifacts), "artifacts": artifacts,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"MEZ GEOMETRY + CONTROLS BUILD: {source['status']}")
    print(f"- {len(source['radii'])} radii / {len(source['variants'])} variants / {len(source['stateContracts'])} state contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
