#!/usr/bin/env python3
"""Validate the Living Core depth-and-light calibration plate."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parents[2]


def main() -> int:
    failures = []
    profiles = json.loads((HERE / "profiles.json").read_text(encoding="utf-8"))
    rows = profiles.get("profiles", [])
    if profiles.get("productionAuthority") is not False or profiles.get("sourcePaletteChanged") is not False:
        failures.append("calibration must remain non-authoritative and palette-neutral")
    if len(rows) != 6 or len({row["id"] for row in rows}) != 6:
        failures.append("calibration must define six unique finish profiles")
    current = next((row for row in rows if row["id"] == "current"), None)
    expected_current = {"opacity": 1, "exposure": 1, "saturation": 1, "contrast": 1, "lift": 0, "shadeStrength": 0.62, "bloomStrength": 1, "grainStrength": 1}
    if not current or current["values"] != expected_current:
        failures.append("current control profile must preserve the approved renderer defaults")

    app = (HERE / "app.js").read_text(encoding="utf-8")
    html = (HERE / "index.html").read_text(encoding="utf-8")
    renderer = (BRAND_KIT / "source-pack" / "design-system-export" / "mz-core.js").read_text(encoding="utf-8")
    for core_id in ("MZ-G06", "MZ-G13", "MZ-G48"):
        if core_id not in app:
            failures.append(f"missing representative core: {core_id}")
    for expression in ("Disc", "Sphere", "Card", "Pill", "Wings"):
        if expression not in html:
            failures.append(f"missing expression control: {expression}")
    if 'data-radius="1"' not in app:
        failures.append("pill must use a full-radius, full-bleed mask")
    for method in ("setProfile(element, profileName)", "setShape(element, shape, radius)"):
        if method not in renderer:
            failures.append(f"renderer missing calibration method: {method}")
    for uniform in ("uExposure", "uSaturation", "uContrast", "uLift", "uShadeStrength", "uBloomStrength", "uGrainStrength", "uOpacity"):
        if uniform not in renderer:
            failures.append(f"renderer missing finish uniform: {uniform}")
    if renderer.count('getContext("webgl"') != 1:
        failures.append("renderer source must retain one shared WebGL context")

    approval = json.loads((BRAND_KIT / "gradient-library" / "approval.json").read_text(encoding="utf-8"))
    if approval.get("scope", {}).get("finishCalibration") != "open; depth and lightness profile selection pending":
        failures.append("approval scope must keep finish calibration open")

    if failures:
        print("DEPTH & LIGHT CALIBRATION: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("DEPTH & LIGHT CALIBRATION: PASS")
    print("- six finish profiles preserve the source palettes")
    print("- MZ-G06, MZ-G13 and MZ-G48 cover every approved expression")
    print("- current defaults, full-bleed pill and shared renderer are intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
