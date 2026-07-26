# Design authority

The judgement layer of the Mez Systems design system: what separates work that is *compliant* from
work that is *good*.

Status: **canonical guidance**. These files do not define values. They define how values get judged.

## Why this exists

The rest of `brand-kit/` can already prove a build is correct. `verify_portability.py`,
`verify_llm_contracts.py`, `verify_workbench.py`, the gradient and architecture verifiers and the
per-round expression verifiers all answer *does this match the system*. None of them answers *is
this any good*, and a mediocre build passes every one of them.

That gap has a cost record. Product Card rounds 01 to 06 were rejected as "vibe-coded" while
passing compliance. Golden Homepage GH-S02 burned four rebuild rounds in one evening, each one
technically on-system and none of them acceptable. The corrective is a second gate that scores
craft, plus a written ban list for the defaults every language model falls into.

## The four files

| File | Answers |
|---|---|
| [`ANTI-SLOP-CANON.md`](ANTI-SLOP-CANON.md) | Is this the statistical default dressed in Mez tokens? Cited defect IDs, objectively wrong, no taste involved. |
| [`CRAFT.md`](CRAFT.md) | How do you make a composition good, not merely legal? Positive craft: hierarchy, proportion, density, materiality, motion, words. |
| [`GATE-B-DESIGN-EXCELLENCE.md`](GATE-B-DESIGN-EXCELLENCE.md) | Is this excellent? A scored eleven-dimension review with blocking failures and named tests. |
| [`FEEDBACK-DISCIPLINE.md`](FEEDBACK-DISCIPLINE.md) | How do you read Olli's feedback without correcting on the wrong axis? The round protocol. |

## Precedence

This folder sits **below** canonical data and **above** an agent's own taste.

1. `brand-kit/authority/current.json` and `brand-kit/governance/decisions.json`: approved decisions
2. `brand-kit/registry/` and `brand-kit/foundations/*/dist/tokens.css`: canonical values
3. `brand-kit/docs/PRODUCT-CARD-DESIGN-ETHOS.md` and `PHASE-B-COMPONENT-PANTRY.md`: approved visual grammar
4. **This folder**: how to judge, and what never to make
5. `brand-kit/references/`: studied outside work, ethos only, never values
6. Agent judgement

When this folder and a canonical value disagree, the value wins and the disagreement is a defect
**in this folder**. Fix it here, say what you changed, do not resolve it by picking the convenient
one. When this folder and an agent's instinct disagree, this folder wins.

## Order of operations for any visual work

1. Read the canonical grammar for the surface: `PRODUCT-CARD-DESIGN-ETHOS.md`, plus
   `PHASE-B-COMPONENT-PANTRY.md` for components.
2. Read `ANTI-SLOP-CANON.md` **before generating**, not after. It is a constraint on what you make,
   not a filter on what you made. Reading it at the end is too late and shows.
3. Read the `CRAFT.md` sections that bear on this surface.
4. Make it.
5. **Look at the rendered result.** Screenshot it. Read the image with your own vision. A judgement
   written without having looked at the render is void, and this is the single most-broken rule in
   the repository's history.
6. Sweep the canon in ID order. Fix every CRITICAL and MAJOR.
7. Run Gate B. The canon is the floor; Gate B is the bar.

## Provenance

Absorbed on 2026-07-25 from the MezCorp Design department
(`mezcorp_claude_code/departments/design/`), which held the anti-slop research, the craft library
and the Gate B mandate. The material was **reconciled, not copied**: that department's `web-house`
describes the superseded 2026-07 Mez pack (`#F8F8F8` page, `#0D0D0D` ink, Inter, static discs,
motion banned). This repository's foundations supersede it, and the living gradient cores are the
point of the system rather than a violation of it. Every rule below was rewritten against
`brand-kit/foundations/*/dist/tokens.css` and the approved expression grammar. Where the two
genuinely conflicted, the conflict is called out in the rule.

Nothing here points at that repository at runtime. This folder is self-contained on purpose: the
design system has to work for a human or a model that has only this repo.
