# Mez Systems Brand Kit Workbench

This is the organised control-plane workspace for turning the current Mez Systems design programme into a stable standalone repository and portable release. It remains non-canonical while `authority/authority.json` is `prepared`.

It has four jobs:

1. make the real animated Living Core visible;
2. preserve the protected Claude Code benchmark and expose why WebP re-extraction is invalid;
3. generate and review future product candidates without editing canonical files;
4. show exactly which foundations, product expressions and release gates are stable or unresolved.

## Authority boundary

This repository is a workbench and future distribution home. It is **not yet canonical**.

The current canonical source remains the Mez Systems pack on `codex/mez-gradient-system` until the two-phase authority handshake activates. The standalone `source-pack/` snapshot came from source-system checkpoint `84eb5a9`; newer governance evidence is imported separately. `source-manifest.json` records both roles. Candidate generation writes only to the gitignored `workspace/` directory.

The existing Claude Code work at `/play-orb/` is preserved untouched as the protected visual benchmark.

The complete source-PNG library and every approved expression live at `/brand-kit/gradient-library/`. Its generator preserves all 43 supplied IDs, flags duplicate visual sources and keeps product assignment decisions separate from palette extraction.

`DEC-MIGRATION-SEQUENCE-001` makes canonical cutover the primary programme goal. Before cutover, the internal control plane must approve the five-product roster, stable product IDs, product-gradient assignments and a genuine Context Engine source, then validate a versioned migration snapshot and rollback path. Foundations, the product-expression suite, golden homepage, consumer proof and the production Figma library are post-cutover work in this repository.

The pre-cutover human gate is complete at [`product-architecture/`](product-architecture/). It records the literal five-product family, durable product IDs and approved MZ-G13/G12/G06/G15/G20 assignments under the Deep Mineral finish. There are no historical public-name aliases in the active architecture. `releases/0.1.0-alpha.1/` packages that identity kernel for clean-clone validation; it cannot transfer authority by itself.

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
├── authority/                    two-phase cutover, rollback and dated evidence
├── governance/                   imported approved decision ledger
├── registry/                     generated products, gradients and assets
├── schemas/                      stable machine-readable contracts
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
├── releases/0.1.0-alpha.1/       self-contained migration identity snapshot
├── scripts/
│   ├── build_claude_catalogue.py reproducible benchmark adapter
│   ├── build_migration_release.py deterministic snapshot and registry builder
│   ├── verify_authority.py       authority handshake and artifact validator
│   ├── verify_release.py         self-contained release validator source
│   └── verify_workbench.py       deterministic boundary validation
└── workspace/                    gitignored uploads, plates and decisions
```

## Do not do these things

- Do not hand-edit imported snapshot files.
- Do not change an approved product assignment without a new recorded governance decision.
- Do not treat the product-architecture board as a canonical registry. Its exported decision becomes input to the atomic internal migration update.
- Do not overwrite the Claude Code play-orb while the palette conflict is unresolved.
- Do not publish a portable release with the old Inter-only typography claim after `DEC-TYPE-001`.
- Do not set the authority manifest to `canonical-active` before clean-clone proof and the matching internal transfer record exist.
