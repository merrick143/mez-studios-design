#!/usr/bin/env python3
"""Generate the portable canonical Mez colour and surfaces package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "colour.source.json"
SCHEMA = ROOT / "colour.schema.json"
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


def relative_luminance(hex_value: str) -> float:
    values = [int(hex_value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    light, dark = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def resolved_modes(source: dict) -> dict:
    primitives = source["primitives"]
    return {
        mode_name: {
            "purpose": mode["purpose"],
            "roles": {role: primitives[reference] for role, reference in mode["roles"].items()},
            "references": mode["roles"],
        }
        for mode_name, mode in source["modes"].items()
    }


def build_css(source: dict, modes: dict) -> str:
    blocks = ["/* Generated from colour.source.json. Do not hand-edit. */"]
    primitive_lines = [":root {"]
    for name, value in source["primitives"].items():
        primitive_lines.append(f"  --mz-colour-{name.replace('.', '-')}: {value};")
    primitive_lines.append("}")
    blocks.append("\n".join(primitive_lines))

    for mode_name, mode in modes.items():
        selectors = ":root, [data-mz-mode=\"light\"]" if mode_name == "light" else f'[data-mz-mode="{mode_name}"]'
        lines = [f"{selectors} {{"]
        for role, value in mode["roles"].items():
            lines.append(f"  --mz-{role.replace('.', '-')}: {value};")
        lines.extend(["  color: var(--mz-text-primary);", "  background-color: var(--mz-canvas);", "  color-scheme: light;" if mode_name != "dark" else "  color-scheme: dark;", "}"])
        blocks.append("\n".join(lines))

    blocks.append(
        "@media print {\n"
        "  :root, [data-mz-mode] {\n"
        + "\n".join(f"    --mz-{role.replace('.', '-')}: {value};" for role, value in modes["print"]["roles"].items())
        + "\n    color-scheme: light;\n  }\n}"
    )
    blocks.append(
        "@media (forced-colors: active) {\n"
        "  :root, [data-mz-mode] {\n"
        "    --mz-canvas: Canvas;\n    --mz-surface-base: Canvas;\n    --mz-surface-raised: Canvas;\n"
        "    --mz-surface-recessed: Canvas;\n    --mz-surface-inverse: CanvasText;\n"
        "    --mz-text-primary: CanvasText;\n    --mz-text-secondary: CanvasText;\n    --mz-text-muted: CanvasText;\n"
        "    --mz-text-inverse: Canvas;\n    --mz-text-link: LinkText;\n"
        "    --mz-border-default: ButtonBorder;\n    --mz-border-strong: ButtonText;\n"
        "    --mz-action-primary-background: ButtonText;\n    --mz-action-primary-foreground: ButtonFace;\n"
        "    --mz-action-secondary-background: ButtonFace;\n    --mz-action-secondary-foreground: ButtonText;\n"
        "    --mz-action-secondary-border: ButtonBorder;\n    --mz-focus-ring: Highlight;\n"
        "    --mz-selection-background: Highlight;\n    --mz-selection-foreground: HighlightText;\n"
        "  }\n}"
    )
    return "\n\n".join(blocks) + "\n"


def build_tokens(source: dict, modes: dict) -> dict:
    return {
        "$schema": "https://design.mez.systems/schemas/colour-tokens-1.0.0.json",
        "generatedFrom": "colour.source.json",
        "status": source["status"],
        "primitive": {name: {"$type": "color", "$value": value} for name, value in source["primitives"].items()},
        "mode": {
            mode_name: {
                role: {"$type": "color", "$value": value, "$extensions": {"mez": {"reference": mode["references"][role]}}}
                for role, value in mode["roles"].items()
            }
            for mode_name, mode in modes.items()
        },
    }


def build_contrast_report(source: dict, modes: dict) -> dict:
    checks = []
    for mode_name, mode in modes.items():
        for pair in source["contrastPairs"]:
            foreground = mode["roles"][pair["foreground"]]
            background = mode["roles"][pair["background"]]
            ratio = contrast_ratio(foreground, background)
            checks.append({
                "id": f"{mode_name}:{pair['id']}",
                "mode": mode_name,
                "foregroundRole": pair["foreground"],
                "foreground": foreground,
                "backgroundRole": pair["background"],
                "background": background,
                "ratio": round(ratio, 2),
                "minimum": pair["minimum"],
                "status": "pass" if ratio >= pair["minimum"] else "fail",
            })
    return {
        "schemaVersion": "1.0.0",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "checkCount": len(checks),
        "failureCount": sum(check["status"] == "fail" for check in checks),
        "checks": checks,
    }


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or review.get("verdict") != "approve":
        raise SystemExit("canonical source and approved review are required for package generation")
    if review.get("decisionId") not in source.get("decisionIds", []):
        raise SystemExit("approved colour decision is not applied to the source")
    modes = resolved_modes(source)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    for path in (SOURCE, SCHEMA, README, REVIEW):
        shutil.copy2(path, DIST / path.name)

    (DIST / "tokens.css").write_text(build_css(source, modes), encoding="utf-8")
    (DIST / "tokens.json").write_text(json.dumps(build_tokens(source, modes), indent=2) + "\n", encoding="utf-8")
    (DIST / "channels.json").write_text(json.dumps({
        "schemaVersion": "1.0.0", "foundationId": source["foundationId"], "status": source["status"],
        "modes": modes, "policies": source["policies"]
    }, indent=2) + "\n", encoding="utf-8")
    report = build_contrast_report(source, modes)
    (DIST / "contrast-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    package = {
        "schemaVersion": "1.0.0", "packageId": "mz.systems.package.colour", "version": "1.0.0",
        "scope": "colour-and-surfaces-foundation", "foundationId": source["foundationId"], "status": source["status"],
        "decisionIds": source["decisionIds"], "reviewGateId": review["gateId"], "candidateRevision": source["candidateRevision"], "productionReadyForScope": True,
        "entrypoints": {"css": "tokens.css", "tokens": "tokens.json", "channels": "channels.json", "contrast": "contrast-report.json", "source": "colour.source.json", "review": "review.json"},
        "notes": ["Canonical for the colour-and-surfaces foundation scope through DEC-COLOUR-FOUNDATION-001.", "No gradient or Living Core data is included."],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

    artifacts = []
    for path in sorted(item for item in DIST.rglob("*") if item.is_file() and item.name != "manifest.json"):
        artifacts.append({"path": path.relative_to(DIST).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "schemaVersion": "1.0.0", "foundationId": source["foundationId"], "status": source["status"],
        "portableRoot": ".", "productionReadyForScope": True, "artifactCount": len(artifacts), "artifacts": artifacts,
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"MEZ COLOUR BUILD: {source['status']}")
    print(f"- {len(source['primitives'])} primitives / {len(modes)} modes / {report['checkCount']} contrast checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
