# Mez Systems space, layout, and responsive foundation

Status: canonical through `H-FND-03-SPATIAL-PROOF` and `DEC-SPACE-LAYOUT-FOUNDATION-001`

This package resolves the conflict between the historical one-container rule and later approved proofs that need different measures for reading, default page work, and wide evidence. It uses one four-pixel base rhythm, three named content widths, four responsive profiles, and three receiver-led density modes.

## Authority and boundaries

- `space-layout.source.json` owns spacing primitives, content widths, breakpoint profiles, density modes, relationship ladders, and spatial policies.
- `space-layout.schema.json` defines the source contract.
- `review.json` records Olli's approval of `spatial-lock-01`.
- `build_space_layout.py` generates the portable canonical package under `dist/`.
- `verify_space_layout.py` validates schema, rhythm, ordering, deterministic output, dependency integrity, and the human proof.
- `brand-kit/workbench/foundations/space-layout/` is the bounded responsive review and regression fixture.
- FND-01 typography and FND-02 colour are canonical inputs and are not copied or changed here.
- FND-04 retains authority over final radius, border, depth, and controls.

The candidate deliberately avoids one global container. `reading` is for focused explanation, `standard` is the default page relationship, and `wide` must be earned by dense evidence or a comparable family. Density changes adjacency and evidence concentration without changing facts or hiding required content.

## Build and verify

```bash
python3 brand-kit/foundations/space-layout/build_space_layout.py
python3 brand-kit/foundations/space-layout/verify_space_layout.py
```

Do not hand-edit `dist/`. The approval grants production authority only for the bounded spacing, layout, density and responsive scope. It does not grant permission to change typography, colour, geometry, product expressions, the homepage, Figma, consumers, or the active migration release.
