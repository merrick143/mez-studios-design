# Complete gradient library

This directory turns the Mez source-gradient folder into a deterministic Living Core catalogue.

The research system is approved at 33 active visual cores. The ten higher duplicate IDs are removed from active selection and retained as compatibility aliases with full provenance. `MZ-G01` is an accepted source exception.

## Authority chain

1. `source-masters/*.png` — source colour and extraction authority.
2. `library-manifest.json` — identity, hashes, dimensions, aliases and gaps.
3. `palettes.json` — deterministic five-cluster extraction cache.
4. `catalogue.json` — portable four-anchor Living Core data.
5. `assets/static/*.webp` — derived runtime fallback and distribution preview.
6. `assignments.json` — non-canonical product assignment plan.
7. `brand-kit/workspace/library-decisions/` — local select/edit/reject records.

Never extract palette data from WebP, screenshots or rendered Living Cores.

## Rebuild

Use the pinned NumPy and Pillow environment declared in `../source-pack/living-core/requirements.txt`.

```bash
python brand-kit/gradient-library/build_library.py
python brand-kit/gradient-library/build_library.py --verify
```

To import a new authoritative source folder byte-for-byte:

```bash
python brand-kit/gradient-library/build_library.py \
  --source /absolute/path/to/sources \
  --import-sources
```

The generator does not change product assignments, canonical registries or review decisions.

Depth and lightness finish profiles are reviewed separately at `calibration/depth-light-01/`; they cannot change palette data.

For fallback QA, append `?static=1` to force static twins or `?no-webgl=1` to simulate WebGL unavailability.
