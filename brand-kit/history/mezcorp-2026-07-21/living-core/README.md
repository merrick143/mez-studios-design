# Living Core system

This directory contains the authoritative build sources for the Mez Systems Living Core. It turns
one exact square gradient image into deterministic parametric colour data, then renders that data
through one shared WebGL engine across discs, spheres, cards, Wings and pills.

## Authority

- `../products.json` owns the product roster, public names and core assignments.
- `../gradients.json` owns the static twins and parametric anchor data.
- `../brand-system/20-living-core.md` owns use, motion and fallback law.
- `../design-system-export/mz-core.js` is the dependency-free runtime.

`palettes.json` is a reproducible extraction cache. It is never product or brand authority.

## Environment

The generator has two build-time dependencies. Install the pinned versions into an isolated
environment rather than the system Python:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The exported runtime has no Python or third-party JavaScript dependency.

## Rebuild assigned cores

From this directory:

```bash
.venv/bin/python build.py
```

The build reads the assigned WebP twins from `../canvas/assets/`, extracts five clusters with
the fixed seed `7`, writes four anchors plus shade and bloom back to `../gradients.json`, and
generates:

- `../canvas/core.html`
- `../canvas/core-compare.html`
- `../canvas/core-orbs/<MZ-G##>.html`

Use `.venv/bin/python build.py --keep-palettes` only after intentionally hand-tuning the cache. The
script still synchronises the resulting values into canonical `gradients.json`.

## Create a new candidate

Candidate ingestion never edits `products.json`, canonical `gradients.json`, or the portable release.
It creates a reviewable folder with the exact static twin, extracted parameter data, shared renderer,
Wings and a multi-expression preview:

```bash
.venv/bin/python candidate.py \
  --source "/path/to/context-engine-source.png" \
  --id MZ-G54 \
  --product "Context Engine" \
  --output "/path/to/context-engine-candidate"
```

Serve the output folder over HTTP and open `preview.html`. Promotion requires a completed human
review, a recorded product assignment decision, canonical contract updates, and a rebuilt portable
release. The candidate command deliberately performs none of those mutations.

## Validate

Run the standard-library validator from this directory:

```bash
python3 validate.py
```

Then rebuild with the pinned environment. A correct rebuild creates zero Git diff.

## Hand-edited versus generated

Hand-edit:

- `build.py`
- `candidate.py`
- `candidate-template.html`
- `candidate.schema.json`
- `validate.py`
- `requirements.txt`
- `orb-template.html`
- `expressions-template.html`
- `palettes.json`, only for an intentional palette correction

Generated files are overwritten without warning. Do not hand-edit anything under
`../canvas/core*`.

Pillow and NumPy are build-time dependencies only. Consumers need the exported JSON,
`mz-core.js`, the exact WebP static twins and the wings asset.
