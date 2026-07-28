# Handoff · Golden Homepage, GH-S05

Paste this whole file as your opening prompt.

---

You are picking up the Mez Systems Golden Homepage. Repo `merrick143/mez-studios-design`,
branch `codex/brand-kit-foundations-expressions`, currently at `1600316`. Working tree is clean
except one stray untracked `bento-1.png` at the repo root, which nobody has claimed. Leave it.

## Read first

`brand-kit/AGENT-GUIDE.md` is the operating contract and is imported by `CLAUDE.md`, so it applies
to you. Follow its required-reading order. Beyond that, before you generate or judge any visual,
read `brand-kit/design-authority/` — it exists because the verifiers can prove a build is correct
and cannot prove it is good, and a mediocre build passes every one of them.

Then read `brand-kit/golden/homepage/round-21-feedback.json`. It records the section that was just
locked, everything rejected on the way, and the defects found.

## Where the page stands

| Section | State |
|---|---|
| GH-S01 Hero | keep. R17, five-card arc |
| GH-S02 The problem | **rebuilt R19** — the staircase |
| GH-S03 The principle | **rebuilt R20** — concentric orbit, product family cycling at the centre |
| GH-S04 Built on ourselves first | **rebuilt R21** — the sequence. Just landed |
| **GH-S05 Operating proof** | **open. This is your task** |
| GH-S06 Available now: AI OS | open, still R17 |
| GH-S07 The ecosystem | open, still R17 |
| GH-S08 / S09 / S10 | keep |

GH-S04 as locked: a horizontal workflow sequence. Four small charcoal dots and one 44px material
disc on a single hairline, stage name and description beneath each. Horizontal on purpose, because
GH-S02 owns the vertical staircase and repeating that shape two sections later fails the repetition
test. Only the thing that ships carries material, so the section spends exactly one colour event.

## Your task: GH-S05

The section is at `brand-kit/workbench/golden/homepage/index.html`, `data-review-id="GH-S05"`.

It currently renders three charcoal cards reading **"Evidence pending"**. That is deliberate, not
laziness. The section's stated job is *"Three carefully redacted screens from the live Mez Studios
system"*, and fabricating a plausible-looking UI there would be inventing evidence, which the
contract forbids. It will look unfinished until it is resolved one of two ways:

1. **Olli supplies real screens**, even heavily redacted. Then build the section around them.
2. **Olli confirms he cannot yet.** Then redesign the section so it does not depend on screenshots
   at all: prove the claim with something that actually exists rather than three boxes waiting for
   an image.

**Ask him which before designing anything.** Do not resolve this by inventing a UI, a mock
dashboard, a fake chart, or a "representative" screen.

## Non-obvious things about this codebase that will cost you hours

These were all learned the hard way in the last session. They are not written in the renderer's
docs.

**`mount()` writes `position: relative` inline onto its host.** If you mount onto an element you
styled `position: absolute; inset: 0`, the inline style wins, the element collapses to zero size,
and you get a black box with a canvas in it that draws nothing. Every DOM measurement still passes.
Stack layers with CSS grid (`grid-area: 1 / 1`) instead. This is MOT-03 and it bit twice.

**The renderer shares one framebuffer capped at 2048 device pixels, with DPR clamped to 2.** Any
material surface wider than **1024 CSS pixels** is drawn from source that ran out, and the overflow
arrives as a stretched band with a hard vertical seam near the right edge. Keep material surfaces
under that, or skip the live mount and keep the static twin.

**`renderer.surfaces` is a Map, so more than one surface can share the one WebGL context.** That is
how a blend between two *live* gradients is possible: mount the incoming one behind the outgoing
one, cross-fade opacity, then release the outgoing. GH-S03 rides a static twin across a `setCore`
call instead, which is correct when a swap must be *hidden*, but it puts a still frame in the middle
of the transition and reads as a freeze. GH-S04 does it the live-to-live way. Copy GH-S04's
approach, in `homepage.js`, search `advanceSequence`.

**Check that colour tokens actually resolve on the page you are editing.** The homepage stylesheet
defines `--page-line` and `--page-line-soft` but *not* `--page-line-strong`. A rule written against
the missing token renders fully transparent while every geometric assertion passes. Round 21's
verifier now checks this specifically.

**Replacing a section's CSS block can delete a neighbour's rules.** It has happened twice: once
taking out the split-card family, once taking out GH-S03's closing thesis. Before deleting a CSS
range, grep every class in it against the markup to confirm which section actually uses it.

## The rule that matters most

**Look at the render before judging anything, including your own work.** Screenshot it. Two defects
last session — a fully invisible connector line and a collapsed core that drew nothing — passed
every DOM measurement and were obvious in the first screenshot. Reporting "all checks pass" about a
surface you have not looked at is a failure of the contract, not a shortcut.

Related: render into a browser Olli can actually see. If you have a visible browser pane, use it.

## Running it

```bash
python3 -m http.server 8914
# http://localhost:8914/brand-kit/workbench/golden/homepage/
```

`?static` and `?no-webgl` force the reduced-motion path on every section.

## Validation

```bash
python3 brand-kit/scripts/verify_portability.py
python3 brand-kit/scripts/verify_llm_contracts.py
python3 brand-kit/scripts/verify_workbench.py
python3 brand-kit/gradient-library/verify_library.py
python3 brand-kit/product-architecture/verify_architecture.py
python3 brand-kit/scripts/verify_authority.py
python3 brand-kit/scripts/verify_release.py --release brand-kit/releases/0.1.0-alpha.1
python3 brand-kit/components/global-navigation/verify_global_navigation_contract.py
python3 brand-kit/components/product-feature-bento/verify_product_feature_bento_contract.py
python3 brand-kit/golden/homepage/verify_homepage_round19.py
python3 brand-kit/golden/homepage/verify_homepage_round20.py
python3 brand-kit/golden/homepage/verify_homepage_round21.py
```

All twelve pass at `1600316`. Round verifiers are per-round and go stale by design; when a round's
premise genuinely expires, retire that specific check with a comment rather than deleting the file
or weakening the rest. Write `verify_homepage_round22.py` for your round, and negative-test it by
breaking the page each way it claims to catch. A verifier that has never failed has never been
tested.

**Mechanical green is not design green.** After the verifiers, run the `design-critique` skill on the
rendered section before showing Olli.

## Also available, built last session

- `brand-kit/design-authority/` — anti-slop canon with cited defect IDs, craft, Gate B, feedback
  discipline
- `brand-kit/references/` — three studies from screenshots Olli supplied, climbing the abstraction
  ladder so influence becomes a principle rather than a copy
- `brand-kit/assets/third-party-marks/` — 58 real brand mark sets with a registry recording aspect
  and form, so a wordmark cannot be dropped into a ring of symbols. Never invent or draw a mark
- `brand-kit/components/product-feature-bento/` — `PC2-B-C04`, candidate status. A real bento layout
  contract that enforces one colour event. Built and then **not** adopted for GH-S04, because Olli
  decided a bento was the wrong way to present that content. Still valid for anything that genuinely
  is a mosaic. It is a candidate: its build script refuses to cut a release without a human decision
  in `governance/decisions.json`, and that refusal is correct

## Working with Olli

He specifies taste by screenshot and by reaction, not by spec. When a surface is rejected, the
complaint is almost always about the composition family or the craft standard, not the quantity of
stuff in it — adding or removing elements while keeping the same family is the trap that burned four
rounds on GH-S02. A genuine restart changes the family.

Ideate in plain sentences before building when a surface has been rejected before. He responds well
to a numbered set of distinct directions and will pick by number.
