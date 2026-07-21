#!/usr/bin/env python3
"""Generate the self-contained canonical Mez typography package."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "typography.source.json"
SCHEMA = ROOT / "typography.schema.json"
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


def slug(value: str) -> str:
    return value.replace(".", "-")


def size_css(size: int | float | dict) -> str:
    if isinstance(size, dict):
        return f"clamp({size['minPx']}px, {size['preferredVw']}vw, {size['maxPx']}px)"
    return f"{size}px"


def feature_css(features: list[str]) -> str:
    return ", ".join(f'"{feature}" 1' for feature in features) or "normal"


def font_face(family: dict, file: dict) -> str:
    style = file.get("style", "normal")
    weight = file.get("weight", 400)
    return "\n".join(
        [
            "@font-face {",
            f'  font-family: "{family["cssFamily"]}";',
            f'  src: url("./{file["path"]}") format("woff2");',
            f"  font-style: {style};",
            f"  font-weight: {weight};",
            "  font-display: swap;",
            "}",
        ]
    )


def build_css(source: dict) -> str:
    faces: list[str] = []
    for family in source["families"].values():
        for file in family["web"]:
            faces.append(font_face(family, file))

    root_tokens = [
        ":root {",
        '  --mz-font-display: "Mez Geist", "Mez Inter", Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
        '  --mz-font-body: "Mez Inter", Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
        '  --mz-font-editorial: "Mez Instrument Serif", Georgia, "Times New Roman", serif;',
        '  --mz-font-technical: "Mez IBM Plex Mono", ui-monospace, "SFMono-Regular", Consolas, "Liberation Mono", monospace;',
    ]
    for role_name, role in source["roles"].items():
        name = slug(role_name)
        root_tokens.extend(
            [
                f"  --mz-type-{name}-size: {size_css(role['size'])};",
                f"  --mz-type-{name}-weight: {role['weight']};",
                f"  --mz-type-{name}-leading: {role['lineHeight']};",
                f"  --mz-type-{name}-tracking: {role['trackingEm']}em;",
            ]
        )
    root_tokens.append("}")

    utilities: list[str] = []
    for role_name, role in source["roles"].items():
        name = slug(role_name)
        family = source["families"][role["family"]]
        declarations = [
            f'  font-family: "{family["cssFamily"]}", {family["fallback"]};',
            f"  font-size: var(--mz-type-{name}-size);",
            f"  font-style: {role.get('style', 'normal')};",
            f"  font-weight: var(--mz-type-{name}-weight);",
            f"  line-height: var(--mz-type-{name}-leading);",
            f"  letter-spacing: var(--mz-type-{name}-tracking);",
            f"  font-feature-settings: {feature_css(role['features'])};",
            "  text-wrap: pretty;",
        ]
        if role["case"] == "uppercase":
            declarations.append("  text-transform: uppercase;")
        if "maxWidth" in role:
            declarations.append(f"  max-inline-size: {role['maxWidth']};")
        utilities.append("\n".join([f".mz-type-{name} {{", *declarations, "}"]))

    return "\n\n".join(
        [
            "/* Generated from typography.source.json. Do not hand-edit. */",
            *faces,
            "\n".join(root_tokens),
            *utilities,
            ".mz-type-truncate {\n  min-inline-size: 0;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n}",
            ".mz-type-numeric {\n  font-variant-numeric: tabular-nums slashed-zero;\n}",
        ]
    ) + "\n"


def build_tokens(source: dict) -> dict:
    roles: dict[str, dict] = {}
    for name, role in source["roles"].items():
        roles[name] = {
            "$type": "typography",
            "$value": {
                "fontFamily": source["families"][role["family"]]["cssFamily"],
                "fontSize": size_css(role["size"]),
                "fontWeight": role["weight"],
                "letterSpacing": f"{role['trackingEm']}em",
                "lineHeight": role["lineHeight"],
            },
            "$extensions": {
                "mez": {
                    "decisionIds": source["decisionIds"],
                    "status": source["status"],
                    "usage": role.get("usage", ""),
                    "features": role["features"],
                    "case": role["case"],
                    "maxWidth": role.get("maxWidth"),
                }
            },
        }
    return {
        "$schema": "https://design.mez.systems/schemas/typography-tokens-1.0.0.json",
        "generatedFrom": "typography.source.json",
        "status": source["status"],
        "fontFamily": {
            key: {"$type": "fontFamily", "$value": value["cssFamily"]}
            for key, value in source["families"].items()
        },
        "typography": roles,
    }


def main() -> int:
    source = read_json(SOURCE)
    review = read_json(REVIEW)
    if source.get("status") != "canonical" or review.get("verdict") != "approve":
        raise SystemExit("canonical source and approved review are required for package generation")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, DIST / SOURCE.name)
    shutil.copy2(SCHEMA, DIST / SCHEMA.name)
    shutil.copy2(REVIEW, DIST / REVIEW.name)
    for family in source["families"].values():
        paths = [family["licencePath"], *(item["path"] for item in family["web"] + family["authoring"])]
        for relative in paths:
            destination = DIST / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
    css_path = DIST / "tokens.css"
    json_path = DIST / "tokens.json"
    css_path.write_text(build_css(source), encoding="utf-8")
    json_path.write_text(json.dumps(build_tokens(source), indent=2) + "\n", encoding="utf-8")

    package = {
        "schemaVersion": "1.0.0",
        "packageId": "mz.systems.package.typography",
        "version": "1.0.0",
        "scope": "typography-foundation",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "decisionIds": source["decisionIds"],
        "reviewGateId": review["gateId"],
        "productionReadyForScope": True,
        "entrypoints": {"css": "tokens.css", "tokens": "tokens.json", "source": "typography.source.json"},
        "notes": ["This is a portable typography slice, not the foundation-complete design-system release."],
    }
    (DIST / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

    artifacts = []
    tracked = sorted(path for path in DIST.rglob("*") if path.is_file() and path.name != "manifest.json")
    for path in tracked:
        artifacts.append(
            {
                "path": path.relative_to(DIST).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "schemaVersion": "1.0.0",
        "foundationId": source["foundationId"],
        "status": source["status"],
        "decisionIds": source["decisionIds"],
        "portableRoot": ".",
        "productionReadyForScope": True,
        "generated": ["tokens.css", "tokens.json", "package.json"],
        "artifactCount": len(artifacts),
        "artifacts": artifacts,
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"MEZ TYPOGRAPHY BUILD: {source['status']}")
    print(f"- {len(source['families'])} families / {len(source['roles'])} roles / {len(artifacts)} portable artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
