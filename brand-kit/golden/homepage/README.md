# Mez Systems golden homepage

Status: Round 05 motion-legibility review candidate active

Task: `TASK-GOLD-01-GOLDEN-HOMEPAGE`

Human gate: `H-GOLD-01-HOMEPAGE-PROOF`

## Current authority

- `homepage-copy.md` is the canonical homepage content approved through `DEC-GOLDEN-HOMEPAGE-COPY-001`.
- `homepage-copy.source.json` and `homepage-copy.schema.json` make that content lock machine-addressable.
- `HOMEPAGE-COMPOSITION-PLAN.md` is the detailed human implementation plan.
- `homepage-plan.source.json` and `homepage-plan.schema.json` define the same section, motion, responsive, evidence and consumer boundaries for agents and validators.

`homepage.source.json` now records the Round 05 visual candidate. It is not approved and carries no production authority. `round-01-feedback.json` preserves the complete first review; `round-02-hero-feedback.json` preserves the QC04 and five-animation redirect; `round-03-hero-feedback.json` records the radical card simplification; `round-04-hero-feedback.json` records that the live material did not read as animated; and `hero-motion.review.json` records the five-live-core hero exception. Nothing in this folder is a golden output until Olli closes `H-GOLD-01-HOMEPAGE-PROOF`.

## Repository boundary

This folder belongs to the canonical design-system repository. The actual Mez Systems technical repository remains a separate future consumer. GOLD-01 produces a portable, versioned homepage contract and no-build proof here before any consumer integration is named.

The design-system source may not import live files from the technical repository. The eventual consumer supplies routes, analytics, live availability and approved evidence through declared interfaces and pins an exact released version.

## Validate the plan

```bash
.venv/bin/python brand-kit/golden/homepage/verify_homepage_plan.py
```

## Review Round 05

Open:

```text
http://127.0.0.1:8914/brand-kit/workbench/golden/homepage/
```

The page includes a separate review drawer for section-level keep, revise or kill feedback without placing workbench controls inside the public composition.

Validate the visual candidate:

```bash
.venv/bin/python brand-kit/golden/homepage/verify_homepage_round05.py
```

## What changed in Round 05

- The hero keeps the approved layered five-product fan.
- Every object keeps the approved vertical full-field card chassis while removing the mini landing-page interface.
- All five canonical Living Core gradients run with clearly legible continuous flow while the hero is active.
- The hero’s broad card fields use a bounded `3.2` rest rate and `4` hover rate; only the Living Core material moves.
- Each card contains only bottom-left Wings, the public product name and extended system name.
- Card descriptions and card-level actions are absent.
- Live and exact-static cards retain the same dark outline, geometry and identity placement.
- Leaving the hero restores the ordinary single-page-core allocation.
- Opening Global Navigation unmounts all page cores before its five spheres run.
- Reduced motion, explicit static mode and renderer failure preserve five exact static twins.
- The Round 01 footer is preserved unchanged.

Operating evidence and testimonial consent remain governed intake work. They are not silently promoted by this visual revision.
