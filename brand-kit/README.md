# Mez Systems Brand Kit Workbench

This is the canonical Mez Systems design-system control plane. `authority/authority.json` is `canonical-active` under `CUTOVER-2026-07-21-01`.

It has four jobs:

1. make the real animated Living Core visible;
2. preserve the protected Claude Code benchmark and expose why WebP re-extraction is invalid;
3. generate and review future product candidates without editing canonical files;
4. show exactly which foundations, product expressions and release gates are stable or unresolved.

## Authority boundary

This repository is the rank-one canonical authority and distribution home.

The previous Mez Systems pack on `codex/mez-gradient-system` is now a pinned archive and consumer reference through transition commit `6ac911e`, with rollback checkpoint `822aa91`. The immutable `source-pack/` snapshot remains imported evidence rather than active data. `source-manifest.json` records both roles. Candidate generation writes only to the gitignored `workspace/` directory.

The existing Claude Code work at `/play-orb/` is preserved untouched as the protected visual benchmark.

The complete source-PNG library and every approved expression live at `/brand-kit/gradient-library/`. Its generator preserves all 43 supplied IDs, flags duplicate visual sources and keeps product assignment decisions separate from palette extraction.

`DEC-MIGRATION-SEQUENCE-001` is complete. The identity kernel, schemas, clean-clone proof, rollback path and two-phase authority handshake passed. Foundations, the product-expression suite, golden homepage, consumer proof and the production Figma library are the governed next work in this repository.

The pre-cutover human gate is complete at [`product-architecture/`](product-architecture/). It records the literal five-product family, durable product IDs and approved MZ-G13/G12/G06/G15/G20 assignments under the Deep Mineral finish. There are no historical public-name aliases in the active architecture. `releases/0.1.0-alpha.1/` packages that identity kernel for clean-clone validation; it cannot transfer authority by itself.

## Run locally

Use a Python environment with Pillow and NumPy:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r brand-kit/source-pack/living-core/requirements.txt
.venv/bin/python brand-kit/server.py --port 8914
```

Open `http://127.0.0.1:8914/brand-kit/`.

The static interface works on Vercel. Candidate upload and decision persistence are local-only because candidates deliberately remain outside canonical registries until a recorded approval promotes them.

## Folder map

```text
brand-kit/
├── START-HERE.md                canonical human and LLM entrypoint
├── AGENT-GUIDE.md               shared tool-neutral operating contract
├── index.html                    the workbench
├── styles.css                    workbench presentation
├── app.js                        live cores, navigation and candidate review
├── server.py                     local candidate API and static server
├── source-manifest.json          provenance and conflict record
├── authority/                    two-phase cutover, rollback and dated evidence
├── governance/                   immutable decisions plus current evidence paths
├── registry/                     generated products, gradients and assets
├── schemas/                      stable machine-readable contracts
├── docs/
│   ├── CURRENT-STATE.md          exact completed-versus-open boundary
│   ├── ROADMAP.md                active execution sequence
│   ├── END-TO-END-ROADMAP.md     complete audit and detailed programme
│   ├── HANDOFF.md                fresh-session handoff
│   ├── MIGRATION-PLAN.md         migration history and close checklist
│   └── SOURCE-MAP.md             canonical, benchmark, snapshot and generated boundaries
├── research/                     transferred evidence and calibration records
├── history/                      frozen previous-pack knowledge snapshot
├── llm/                          task, context, receipt and evaluation contracts
├── skills/                       canonical repository-owned agent skills
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
│   ├── build_knowledge_manifest.py frozen history manifest builder
│   ├── verify_portability.py     docs, evidence and shared-skill validator
│   ├── verify_llm_contracts.py   model-neutral contract validator
│   ├── verify_authority.py       authority handshake and artifact validator
│   ├── verify_release.py         self-contained release validator source
│   └── verify_workbench.py       deterministic boundary validation
└── workspace/                    gitignored uploads, plates and decisions
```

## Do not do these things

- Do not hand-edit imported snapshot files.
- Do not change an approved product assignment without a new recorded governance decision.
- Do not treat the product-architecture review board as the registry. Canonical products live in `registry/products.json` and the active release.
- Do not overwrite the protected Claude Code play-orb benchmark.
- Do not publish a portable release with the old Inter-only typography claim after `DEC-TYPE-001`.
- Do not edit the authority manifest without a new recorded cutover, suspension or rollback decision.
