# Mez Systems colour and surfaces foundation

Status: canonical; approved through `H-FND-02-SURFACE-PROOF`

This package turns the established light-monochrome direction and approved contained-dark control behaviour into the canonical semantic system recorded by `DEC-COLOUR-FOUNDATION-001`. `#F8F8F8` is the default canvas, `#2E2E2E` is the Wings charcoal, and Mez Systems gains no separate corporate hue. Functional colour appears only where meaning requires it: links, selection, focus, success, warning, danger and information.

## Authority and boundaries

- `colour.source.json` owns primitives, mode aliases, contrast pairs and channel policies.
- `colour.schema.json` defines the source contract.
- `build_colour.py` generates the portable canonical package under `dist/`.
- `verify_colour.py` validates schema parity, contrast, portability, deterministic output and the human proof.
- `review.json` is the immutable human approval record for `final-lock-02`.
- `brand-kit/workbench/foundations/colour/` is the canonical regression and approval-record fixture, not a second token source.
- Product gradients remain governed by `brand-kit/gradient-library/` and are not copied, sampled or modified here.

The canonical foundation preserves the historical `#F8F8F8` page, `#F6F5F4` recessed surface, white card and near-black ink logic. Routine feedback stays on neutral surfaces with hue limited to the leading rule, icon and status text; tinted surfaces are reserved for critical emphasis. Dark is an opt-in contained room, not a universal theme. Email, document and print are explicit mappings rather than hidden overrides.

## Build and verify

```bash
python3 brand-kit/foundations/colour/build_colour.py
python3 brand-kit/foundations/colour/verify_colour.py
```

Do not hand-edit `dist/`. Future visible changes require a new bounded decision; this approval does not grant permission to change Living Core palettes, product assignments, typography, controls or the active migration release.
