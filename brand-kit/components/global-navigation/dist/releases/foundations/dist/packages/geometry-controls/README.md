# Mez Systems geometry, border, depth, and controls foundation

Status: canonical through `H-FND-04-CONTROL-PROOF` and `DEC-GEOMETRY-CONTROLS-FOUNDATION-001`

This package implements the approved `DEC-CONTROL-001` quiet-pressure direction as a complete geometry and interaction contract. It keeps 12px controls, 40/48/52px scale, solid-outline-text hierarchy, one-pixel hover lift, tight contact depth, white-primary dark-surface behaviour, selective directional icons, and full-width mobile primaries while adding coherent radii, borders, focus, fields, choice controls, destructive behaviour, and adversarial states.

## Authority and boundaries

- `geometry-controls.source.json` owns radii, border widths, bounded depth, motion, focus, scales, variants, state contracts, field geometry, and policies.
- `geometry-controls.schema.json` defines the source contract.
- `review.json` records Olli's approval of `control-lock-01`.
- `build_geometry_controls.py` generates the portable canonical package under `dist/`.
- `verify_geometry_controls.py` validates source, deterministic output, canonical dependency integrity, state completeness, portability, and the human proof.
- `brand-kit/workbench/foundations/geometry-controls/` is the bounded visual and interaction review fixture.
- FND-01 typography, FND-02 colour, and FND-03 space-layout are canonical inputs. This package consumes their roles and does not copy or change their values.
- Product expressions, homepage composition, consumers, Figma, and the active migration release remain outside this task.

Flat is the ordinary surface. Hairlines carry structure. Contact depth exists only during hover, raised depth only for detached temporary surfaces, and overlay depth only for drawers or dialogs. Glow and glass are refused. Full rounding is a semantic exception for switches, short status capsules, and circular controls—not a default action style.

## Build and verify

```bash
python3 brand-kit/foundations/geometry-controls/build_geometry_controls.py
python3 brand-kit/foundations/geometry-controls/verify_geometry_controls.py
```

Do not hand-edit `dist/`. The approval grants production authority only for the bounded geometry, border, depth, focus and controls scope. It does not authorize changes to earlier foundations or later expression and page work.
