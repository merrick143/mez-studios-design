# Start here: Mez Systems design system

Status: canonical control plane active on `main`; foundation, disc, sphere and Wings/mark 1.0.0 canonical; `product-card-02` Phase A round 02 visual architecture ready for critique

## What this repository is

`brand-kit/` is the governed home for the Mez Systems identity, foundations, product expressions, channel systems, machine contracts, releases, and human/LLM operating guidance.

It is intentionally broader than a visual brand guide. The finished system must let a human or LLM create excellent websites, ads, email, social, video, presentations, documents, product surfaces, and future formats while preserving one unmistakable identity.

## Current truth

- The canonical five-product roster and MZ-G13/G12/G06/G15/G20 assignments are approved.
- The complete source-gradient library, source authority, shared Living Core renderer, static twins, and Deep Mineral finish are approved.
- The migration identity release is `0.1.0-alpha.1`.
- The recovery branch has been integrated into `main`; new work starts from normal feature branches based on `main`.
- Typography, colour, space-layout, and geometry-controls are canonical portable foundations. `control-lock-01` is approved through `DEC-GEOMETRY-CONTROLS-FOUNDATION-001`, including eight named radii, three border widths, bounded depth, seven variants, eight complete state contracts, fields, choice controls, dark inversion and mobile hierarchy.
- The four canonical packages are assembled byte-for-byte as foundation release `1.0.0`, with one ordered CSS entrypoint, local fonts and licences, deterministic integrity, isolated proof and explicit migration boundaries. `DEC-FOUNDATION-RELEASE-001` records its bounded authority.
- Canonical disc expression `1.0.0` is approved through `H-EXP-01-DISC-PROOF` and `DEC-DISC-EXPRESSION-001`. The informed approval record states the circle, Wings, 48px marked minimum, static/live allocation and fallbacks that were accepted.
- Canonical sphere expression `1.0.0` is approved through `H-EXP-02-SPHERE-PROOF` and `DEC-SPHERE-EXPRESSION-001`. It adds only approved renderer depth plus focal scale/crop rules to the canonical disc.
- Canonical Wings and mark expression `1.0.0` is approved through `H-EXP-03-WINGS-MARK-PROOF` and `DEC-WINGS-MARK-EXPRESSION-001`.
- `product-card-01` was rejected as a generic under-designed chassis. The first `product-card-02` pass went prematurely into discovery, pricing and checkout functions. Phase A round 01 then overcorrected into ten isolated art-card treatments and was rejected on 22 July 2026. Round 02 holds one narrow portrait website-card architecture steady and compares four credible contextual treatments: Editorial Portrait, Full Field Portrait, System Index and Product Pack. It also makes the family-shelf versus bundle-offer distinction, surface contrast and the complete Phase B website-component scope explicit. Phase A remains non-authoritative at `H-EXP-04A-CARD-VISUAL-DIRECTION`; Phase B is held until the visual lock.

See [Current state](docs/CURRENT-STATE.md) for the exact programme boundary.

## Reading order

1. [Shared agent guide](AGENT-GUIDE.md).
2. [Current state](docs/CURRENT-STATE.md).
3. [Execution roadmap](docs/ROADMAP.md).
4. [Approved decisions](governance/decisions.json).
5. [Full audit and end-to-end roadmap](docs/END-TO-END-ROADMAP.md) when planning a phase.
6. [Research index](docs/RESEARCH-INDEX.md) when making a design decision.
7. [Source map](docs/SOURCE-MAP.md) before changing authority or generated data.

## Run locally

Create the pinned Python environment once:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r brand-kit/source-pack/living-core/requirements.txt
```

Run the local workbench:

```bash
.venv/bin/python brand-kit/server.py --port 8914
```

Open `http://127.0.0.1:8914/brand-kit/`.

## Choose work from the roadmap

Do not restart the original audit or rebuild the gradient engine. Continue from the first incomplete task in [ROADMAP.md](docs/ROADMAP.md), unless Olli explicitly changes priority.

The active programme task is `TASK-EXP-04-PRODUCT-CARD`. Review the `product-card-02` round 02 Visual Architecture proof at `brand-kit/workbench/expressions/product-card/`; decide the base treatment and bounded special modes at `H-EXP-04A-CARD-VISUAL-DIRECTION`. Do not start Phase B website components or proceed to trading cards, channels or homepage work until the visual gate is decided.
