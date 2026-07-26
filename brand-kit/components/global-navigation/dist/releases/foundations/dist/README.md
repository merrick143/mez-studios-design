# Mez Systems foundation release

This directory builds the four approved Mez Systems foundation packages into one portable canonical release. It introduces no new foundation values.

## Build and verify

```sh
python3 brand-kit/releases/foundations/build_foundation_release.py
python3 brand-kit/releases/foundations/verify_foundation_release.py
```

The generated `dist/` directory is the complete copy boundary. Consumers should copy the whole directory and load `index.css`; do not cherry-pick font or package files.

## Runtime order

`index.css` preserves the only supported CSS order:

1. typography tokens and local fonts
2. colour and semantic surfaces
3. space, layout and responsive profiles
4. geometry and motion tokens
5. control primitives

The component packages retain their approved 1.0.0 identities and bounded authority. The assembled `1.0.0` release is canonical for its foundation scope through `H-FND-05-FOUNDATION-RELEASE` and `DEC-FOUNDATION-RELEASE-001`.

See `MIGRATION.md` for the boundary between this release and the immutable migration identity release.
