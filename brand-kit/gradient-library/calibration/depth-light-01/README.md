# Living Core depth and light calibration

Study: `MEZ-LIVING-CORE-DEPTH-LIGHT-01`

This plate tests renderer finish without changing source PNGs, extracted anchors, anchor positions, source weights, shade colours, bloom colours or motion paths.

## Representative cores

- `MZ-G06` — wide violet, cyan and pale-value travel.
- `MZ-G13` — blue flagship with a deep indigo shade.
- `MZ-G48` — green core with a darker mineral range.

## Finish controls

| Control | Meaning | Calibration range |
| --- | --- | --- |
| `opacity` | Actual internal alpha; allows the consuming surface to show through | `0.85–1.00` |
| `exposure` | Multiplies post-mix light output | `0.95–1.15` |
| `saturation` | Colour density around computed luminance | `0.85–1.15` |
| `contrast` | Tonal separation around midpoint grey | `0.85–1.15` |
| `lift` | Raises or lowers the black floor | `-0.02–0.06` |
| `shadeStrength` | Sphere-only edge depth | `0.45–0.80` |
| `bloomStrength` | Amount of palette-derived highlight bloom | `0.80–1.50` |
| `grainStrength` | Existing fine grain and mottle intensity | `0.65–1.15` |

The `current` profile exactly reproduces the previous default values. Profiles are named calibration bundles, not new gradient palettes.

## Selected finish

`05 · Deep mineral` is the approved research-system default under `DEC-LIVING-CORE-FINISH-001`. Its values are applied by the shared runtime when no explicit comparison profile is supplied. The prior `current` treatment remains on this plate as a control.

## Expression rule

The same selected finish applies to disc, sphere, rounded card, full-bleed pill and gradient Wings. PNG authority is always shown unchanged.

Wide masks use square-normalised field coordinates while preserving aspect-aware mask geometry. This prevents card and pill ends from sampling beyond all anchors and falling toward black.

## Fallback

Static and reduced-motion fallback always use the exact static twin. Finish variables are runtime behaviour and never rewrite fallback images.

Append `?static=1` to force fallback QA or `?no-webgl=1` to simulate an unavailable WebGL context.

## Decision boundary

A saved select, edit or reject record is written first to `brand-kit/workspace/finish-decisions/`. It has no production authority and cannot alter palettes or product assignments. The approved selection is then mirrored in `decision.json`, `profiles.json` and the portable renderer contract together. Production promotion remains a separate migration gate.
