# Mez Systems Brand Kit Workbench

This is the organised, non-canonical workspace for turning the current Mez Systems design programme into a stable standalone repository and portable release.

It has four jobs:

1. make the real animated Living Core visible;
2. preserve the protected Claude Code benchmark and expose why WebP re-extraction is invalid;
3. generate and review Context Engine candidates without editing canonical files;
4. show exactly which foundations, product expressions and release gates are stable or unresolved.

## Authority boundary

This repository is a workbench and future distribution home. It is **not yet canonical**.

The current canonical source remains the Mez Systems pack on `codex/mez-gradient-system`. The standalone `source-pack/` snapshot came from source-system checkpoint `84eb5a9`; the internal migration-first governance reconciliation is pushed through `50c3b90`. `source-manifest.json` records both roles. Candidate generation writes only to the gitignored `workspace/` directory.

The existing Claude Code work at `/play-orb/` is preserved untouched as the protected visual benchmark.

The complete source-PNG library and every approved expression live at `/brand-kit/gradient-library/`. Its generator preserves all 43 supplied IDs, flags duplicate visual sources and keeps product assignment decisions separate from palette extraction.

`DEC-MIGRATION-SEQUENCE-001` makes canonical cutover the primary programme goal. Before cutover, the internal control plane must approve the five-product roster, stable product IDs, product-gradient assignments and a genuine Context Engine source, then validate a versioned migration snapshot and rollback path. Foundations, the product-expression suite, golden homepage, consumer proof and the production Figma library are post-cutover work in this repository.

## Run locally

Use a Python environment with Pillow and NumPy:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r brand-kit/source-pack/living-core/requirements.txt
.venv/bin/python brand-kit/server.py --port 8914
```

Open `http://127.0.0.1:8914/brand-kit/`.

The static interface works on Vercel. Candidate upload and decision persistence are local-only because they deliberately write to a non-canonical workspace.

## Folder map

```text
brand-kit/
├── index.html                    the workbench
├── styles.css                    workbench presentation
├── app.js                        live cores, navigation and candidate review
├── server.py                     local candidate API and static server
├── source-manifest.json          provenance and conflict record
├── docs/
│   ├── MIGRATION-PLAN.md         safest route to the standalone repository
│   └── SOURCE-MAP.md             canonical, benchmark, snapshot and generated boundaries
├── source-pack/                  imported snapshot, never hand-edited here
│   ├── products.json
│   ├── gradients-systemized.json
│   ├── palettes-claude-original.json
│   ├── claude-catalogue.json       generated comparison-only catalogue
│   ├── design-system-export/
│   └── living-core/
├── candidates/README.md          candidate contract
├── gradient-library/             43-ID source library, generator and expression board
├── releases/README.md            portable release gates
├── scripts/
│   ├── build_claude_catalogue.py reproducible benchmark adapter
│   └── verify_workbench.py       deterministic boundary validation
└── workspace/                    gitignored uploads, plates and decisions
```

## Do not do these things

- Do not hand-edit imported snapshot files.
- Do not call Context Engine assigned until a genuine source candidate is selected.
- Do not overwrite the Claude Code play-orb while the palette conflict is unresolved.
- Do not publish a portable release with the old Inter-only typography claim after `DEC-TYPE-001`.
- Do not promote this repository to canonical before the migration exit gates pass.
