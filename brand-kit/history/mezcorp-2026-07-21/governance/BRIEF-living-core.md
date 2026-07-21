# BRIEF · The Living Core

**For:** Codex
**From:** Olli (via Claude Code)
**Date:** 2026-07-20
**Status:** Implemented working system. `DEC-MOTION-002` approved 2026-07-20. Hero 03 approved systemization 2026-07-21.

---

## 1. The decision

We built the same brief twice, through two models, and we are picking a winner.

| | Claude Code | Codex |
|---|---|---|
| Path | `brands/mez-systems/living-core/` | `prototypes/aurora-play-button/` |
| Port | 8750 | 4173 |
| Method | k-means extracts a 5-colour palette, shader **reconstructs** the gradient from 4 Gaussian anchors | Ships the source `.webp` as a texture, **animates its coordinates** |

**The Claude Code build wins and becomes the Mez Systems living core.** The Codex build gets deleted.

Why: the anchor method means a core is *data*, not an image. Four hex values and four positions in `gradients.json` fully describe it. Nothing has to ship a 200KB webp per product, a new core is a one-line edit, and every treatment (disc, sphere, trading card, wings) is the same shader on a different mask. The texture method is faithful to the artwork but locks each core to a binary asset and cannot render a core the artwork does not already exist for.

The tradeoff is honest and must be recorded: **the anchor method is an approximation.** It does not reproduce the source PNG exactly. We are accepting drift from the Figma swatch in exchange for the core becoming parametric. If a core ever needs to be pixel-exact against Figma, use the flat static webp, not the orb.

---

## 2. STOP · Read this before writing any code

**The living core is currently forbidden by our own brand law.** This is not a style note. Three documents explicitly ban exactly what this component does:

`brand-system/16-motion.md`:
> **Gradients.** The product cores never shift, pulse, rotate or drift. A gradient is a static fill.
> **The discs.** No spin, no float, no breathing. The disc is a fixed mark.
> A build with a spring, a scroll animation or a **moving gradient is off-system**.

`design-system-export/AGENTS.md` non-negotiable #16:
> No scroll-reveal, no parallax, **no moving gradients**.

`brand-system/19-review-checklist.md` is the definition of done, and it tests the locked laws.

So if you implement the orb first and amend the docs after, you will ship something the review checklist fails, and every downstream consumer reading AGENTS.md will treat it as a bug and revert it.

**Order of work is therefore fixed:**

1. File the decision (§3)
2. Amend the brand law (§6)
3. Then move the code (§5)

Do not reorder these. Do not implement first.

---

## 3. Governance first · DEC-MOTION-002

Add to `governance/decision-register.json`:

```json
{
  "id": "DEC-MOTION-002",
  "title": "The living core: sanctioned continuous motion on product cores",
  "status": "proposed",
  "reversibility": "moderate",
  "gate": "H1",
  "owner": "executive-brand-owner",
  "recommendation": "Carve a single named exception into 16-motion.md: the product core may animate continuously when rendered as a living core. Everything else in the motion law is unchanged.",
  "productionEffect": "amends-brand-law",
  "source": "governance/BRIEF-living-core.md",
  "introducedAt": "2026-07-20",
  "scope": "motion law, gradient treatments, product cores",
  "supersedes": "The 'gradients never animate' and 'discs never move' clauses of 16-motion.md, for the living-core treatment only."
}
```

`reversibility: moderate` is deliberate. Backing this out means pulling a WebGL engine out of every consumer, not deleting a CSS rule.

**The exception must be narrow.** It licenses one thing: a product core, rendered as a living core, may animate continuously. It does not license scroll-reveal, parallax, springs, animated text, moving section backgrounds, or motion on anything that is not a product core. Write it that way or it will be read as permission to animate everything.

---

## 4. What the Claude Code build actually is

### 4.1 Three files, not one

The board at `localhost:8750/index.html` is **generated output**. Editing it does nothing that survives a rebuild. The real system is:

```
build.py                      generator + palette extraction (Python, pillow + numpy)
orb-template.html             HAND-EDITED source · one standalone orb
expressions-template.html     HAND-EDITED source · the 53-surface board
palettes.json                 extracted colour data, safe to hand-tune
  ↓ python3 build.py
index.html                    GENERATED · the board
compare.html                  GENERATED · gradient comparison
orbs/<ID>.html                GENERATED · standalone orbs
```

Only the two `*-template.html` files are hand-edited. Everything else is overwritten without warning.

### 4.2 How a gradient becomes a core

`build.py`, one pass per gradient:

1. Source PNG downsampled to 160×160 (`SAMPLE = 160`).
2. **k-means, k=5, `SEED = 7`.** The seed is load-bearing. Change it and every palette reshuffles, so two builds stop being comparable. k-means++ seeding is used because random seeding regularly collapses two centres onto the same colour on a smooth gradient, silently costing an anchor.
3. **Darkest cluster → `SHADE`**, which drives the sphere shading.
4. **Remaining four → mesh anchors `C0..C3`.**
5. Each anchor keeps its **spatial centroid** from the source, mapped into the disc. A colour that lived top-right of the gradient still lives top-right of the core.
6. Each anchor keeps its **share of the source** as a weight. An accent stays an accent instead of averaging out.
7. The lightest anchor drives the bloom, tinted to itself.

At render, the four anchors drift on **mismatched Lissajous orbits** and are blended by Gaussian falloff, sampled at a **domain-warped** coordinate. The warp is what makes it churn like liquid rather than rotate.

**Colour is mixed in linear space** (`toLinear` / `toSRGB`, γ 2.2). Mixing in raw sRGB goes grey through the middle. That single detail is most of the difference between this looking expensive and looking cheap. Do not "simplify" it.

### 4.3 The rendering architecture, and why the obvious approach fails

Each gradient surface is a `.gx` div holding its own cheap **2D** canvas (`.gxc`). One shared **offscreen WebGL** context renders a surface at the viewport origin, then `drawImage` blits that region into the surface's own 2D canvas.

That sounds convoluted. Three hard constraints forced it, and you will rediscover all three if you rewrite it:

1. **One WebGL context per surface fails.** Browsers cap contexts around 16 and silently kill the oldest. This board has 53 surfaces.
2. **One shared canvas behind the page fails twice.** Any opaque ancestor paints over it (white product cards and the dark bundle panel showed no gradient at all), and any transformed ancestor creates a stacking context that traps it underneath.
3. **`gl_FragCoord` is absolute, never viewport-relative.** Surfaces must be rendered at the GL viewport origin and blitted, so shader coordinates stay surface-local. Rendering each at its on-screen offset puts every surface outside its own shape: a completely blank board, with no console error.

`.gx` carries `isolation: isolate` so each surface is its own stacking context. Remove it and overlapping cards in the stack show each other's wings through the transparent divs above.

### 4.4 The shader

`expressions-template.html:558`. Fragment shader, full-viewport triangle.

- 3D simplex noise (Ashima/Gustavson) → up to 3-octave fBm → two-level domain warp
- Four Gaussian colour anchors on Lissajous orbits, blended in linear space
- Noise-perturbed radial shading toward `SHADE`
- Two-layer static grain, sampled in **CSS pixels not device pixels**, luminance-masked
- Shape is a uniform: `0 disc · 1 sphere · 2 rect · 3 wings`. One shader, four masks. The rect carries a corner-radius uniform via `sdRoundBox`, which is how the trading card and the pill come from the same code.

Tuning constants worth knowing:

| Constant | Default | Effect |
|---|---|---|
| `K` | 7.5 | Gaussian falloff. Lower = broader, softer fields. |
| `S` | 1.9 | Dominance exponent. Higher = anchors hold their colour instead of averaging to mud. |
| `rim` smoothstep | 0.58, 1.14 | Where sphere shading begins. Lower start = darker. |
| `rim` mix | 0.46 | Shading strength. |
| grain `fine` | 0.100 | Paper texture. |
| `uOct` LOD | `<90px → 2` | Octave count. Small surfaces cannot resolve three. |
| dpr cap | 2 | Device-pixel-ratio ceiling. |
| `HOVER.speed` | 1.85 | Fluid acceleration on hover. |
| `--mark-ratio` | 0.39 | Wings size as a fraction of the disc, standalone orb. |

### 4.5 The seven sections of the board

`living-core/expressions-template.html`, all markup hand-written, populated by JS:

| # | Section | Line | Proves |
|---|---|---|---|
| 01 | The four cores | 441 | One gradient per product, for life |
| 02 | One gradient, many expressions | 451 | Disc is standard, sphere is identity only |
| 03 | Every treatment, every core | 461 | The system holds when the core changes |
| 04 | The product cards | 471 | Card #FFF, radius 20, 8% hairline, soft shadow |
| 05 | Stack + bundle | 481 | Offset 50 across, 38 down, newest on top |
| 06 | Rarity is finish, never hue | 502 | Editions change surface, never colour |
| 07 | Down to 24px, up to a hero | 513 | The mark holds at favicon scale |

Section 03 is the important one. It is the falsifiable claim: same geometry, same light, same mark, only the gradient moves. If the system is wrong, that grid is where it shows.

---

## 5. Where it lands in Mez Systems

The authority model (`governance/authority-model.json`) already dictates this. Respect the ranks.

```
brands/mez-systems/
├── governance/
│   ├── decision-register.json          + DEC-MOTION-002              [rank 1]
│   └── BRIEF-living-core.md            this file
│
├── gradients.json                      + anchors/weights/shade per core [rank 2]
│
├── brand-system/
│   ├── 20-living-core.md               NEW · the treatment's brand law [rank 3]
│   ├── 02-gradients.md                 AMEND · living core as 5th treatment
│   ├── 16-motion.md                    AMEND · the carved exception
│   └── 19-review-checklist.md          AMEND · living-core checks
│
├── design-system-export/
│   ├── mz-core.js                      NEW · portable engine, no deps  [rank 4]
│   └── AGENTS.md                       AMEND · non-negotiable #16
│
└── canvas/
    ├── core.html                       the board, as reference impl    [rank 5]
    └── assets/                         mz-g06/13/15/20.webp + wings.svg (already present)
```

### 5.1 The one architectural change you must make

`build.py:49` hardcodes its own `PRODUCTS` list, and for the public repo it deliberately genericises three of the four names to "Core 02/03/04".

**That is a rank-2 violation once it lives inside mez-systems.** `products.json` owns the product roster, names and core assignments. The component must not hold a second copy.

So: delete the hardcoded `PRODUCTS` from `build.py` and read `products.json` + `gradients.json` instead. Real names come back automatically (AI OS, Aurora, Prism, Forge). If the two disagree, `products.json` wins, every time.

Write the extracted anchor data **back into `gradients.json`** per core, so a consumer that never runs Python can still render a living core:

```json
{
  "id": "MZ-G13",
  "anchors": [{"hex": "#...", "pos": [0.31, 0.22], "weight": 0.28}, ...],
  "shade": "#...",
  "bloom": "#..."
}
```

`palettes.json` then becomes a build cache, not a source of truth.

### 5.2 Portability

`mz-core.js` in the export must be a dependency-free ES module that takes an element plus a core id and renders. The Python is a *build-time* palette extractor; it must never be a runtime dependency for a consumer. A consumer reads `gradients.json`, passes anchors to `mz-core.js`, done.

---

## 6. The brand law to write

### 6.1 New · `brand-system/20-living-core.md`

Status: DEFAULT, working values, flag deviations to Olli. Must cover:

- **What it is.** The fifth treatment. The core rendered as a live shader rather than a static fill.
- **Where it is allowed.** Hero, identity boards, the product card disc, the app icon. One per viewport as a rule of thumb: two living cores competing on one screen reads as a screensaver.
- **Where it is banned.** Never in a table, list, nav chip, or any surface repeated more than ~6 times. Never behind text. Never as a section background (gradients stay on products, doc 02 is unchanged).
- **The static fallback is the default, not the degraded case.** Every living core must have a defined static twin (the flat webp). Print, email, OG images, PDF, reduced-motion and no-WebGL all take the static twin. A surface that cannot render the static version is not allowed to render the living one.
- **Motion character.** Continuous, slow, non-looping-to-the-eye. It never pulses, never strobes, never resets visibly. Hover accelerates to 1.85×; nothing else responds to input.
- **Reduced motion.** `prefers-reduced-motion: reduce` renders the static twin. Not a slowed-down orb, the static twin.
- **The 24px floor.** Below 24px the mark is never used, living or static (doc 04 already says this, restate it).

### 6.2 Amend · `16-motion.md`

Add to *What animates*:

| What | Change | Duration |
|---|---|---|
| Living core | Continuous shader motion on a product core only. Hover 1.85×. | continuous, exempt from `--mz-duration` |

Rewrite the two banned bullets rather than deleting them, so the ban survives everywhere it still applies:

- **Gradients.** A gradient used as a fill never shifts, pulses, rotates or drifts. The sole exception is the living core (doc 20), which is a rendered treatment, not a fill.
- **The discs.** A static disc never spins, floats or breathes. A disc rendered as a living core is governed by doc 20.

Then amend the closing rule, which currently reads "a build with ... a moving gradient is off-system". It must now read: a moving gradient is off-system **unless it is a living core under doc 20**.

### 6.3 Amend · `02-gradients.md`

Add the living core to the treatment table (line ~58), alongside disc / Gradient-M / trading / sphere. State plainly that it is an **approximation of the source swatch, not a reproduction**, and that Figma remains the reference for exact colour.

### 6.4 Amend · `design-system-export/AGENTS.md`

Non-negotiable #16 currently says "no moving gradients" flatly. It must carry the exception, or every consumer agent reading it will revert living cores on sight. This is the single highest-leverage line in the whole change: it is what other build agents actually read.

### 6.5 Amend · `19-review-checklist.md`

Add checks:

- Every living core has a defined static twin, and the twin is what renders under reduced motion
- No more than one living core per viewport
- No living core behind text
- Console is clean (see §8, a dead shader fails silently and looks fine)

---

## 7. Delete the Codex build

Once DEC-MOTION-002 is approved and the move is verified:

```bash
trash ~/mezcorp_claude_code/prototypes/aurora-play-button
```

Use `trash`, never `rm`. Both builds are currently **untracked** (`?? prototypes/` and `?? departments/cmo/brand-library/components/`), so commit the Claude Code build into `mez-systems` *before* deleting anything. Right now a single `git clean` destroys both.

Two things in the Codex build are worth salvaging before it goes:

- `assets/gradients/variants.json` and the webp optimisation pipeline. Those webps are already the static twins doc 20 requires, and they are already sitting in `canvas/assets/`.
- Its offscreen/visibility pause logic, if it is cleaner than ours. Ours pauses offscreen too, but theirs was written against the same constraint independently and is worth a read.

The former `codex-made-it` skill at `~/.codex/skills/codex-made-it/` held the retired texture-coordinate approach. That instruction now conflicts with the approved Living Core and must not be used as authority. The skill is synchronised to the canonical system as part of the 2026-07-21 systemization checkpoint.

---

## 8. Definition of done

Every failure mode in this component is **silent**. None of them throw. Do not report this complete on the strength of a clean build.

- [ ] DEC-MOTION-002 is `approved` in the register, not `proposed`
- [ ] `16-motion.md`, `02-gradients.md`, `19-review-checklist.md` and `AGENTS.md` all carry the exception, and none of them contradict each other
- [ ] `build.py` reads `products.json`, holds no product list of its own, and real names render (AI OS, Aurora, Prism, Forge)
- [ ] Anchors are written into `gradients.json`; a consumer can render from JSON with no Python
- [ ] `canvas/core.html` renders all seven sections
- [ ] Discs inside the **white product cards** and inside the **dark bundle panel** are visible. These two are the canaries for the occlusion bug, and a broken one looks like a merely empty card
- [ ] Only the **top** card of the stack shows wings and a name. If all four do, stacking contexts have regressed
- [ ] Hover accelerates the fluid only; core geometry and Wings stay perfectly still
- [ ] Browser console is clean. **A shader compile error falls back to a flat CSS gradient, which looks deceptively fine at a glance**
- [ ] No core is a flat single tone (means clustering collapsed)
- [ ] Reduced motion renders the static twin, and this has actually been triggered, not just implemented
- [ ] Both builds committed before the Codex one is trashed

### Known traps

- **Backticks are forbidden in shader comments.** The GLSL sits in a JS template literal. A stray backtick silently closes it and the core falls back to a flat CSS gradient with no console error. This has bitten once already.
- **`half` and `sample` are reserved words in GLSL** and will not compile.
- **Do not screenshot the board with a full-page capture.** Surfaces only draw while on screen, so a stitched image shows blanks below the fold. Capture per viewport.
- **Fixed seed is load-bearing.** `SEED = 7`. Two builds must be comparable.
- **Flat gradients produce flat cores, correctly.** If a source has fewer than four distinguishable colours, clustering pads by duplicating the last anchor. That is faithful, not a bug. Hand-tune `gradients.json` if more variety is wanted.

---

## 9. Open questions for Olli

1. **Aurora, Prism and Forge cores are still `candidate`** in `products.json`. Only AI OS / MZ-G13 is locked. Do we ship living cores for candidates, or lock all four first?
2. **Does the living core go on the live site, or stay an internal identity surface for now?** Doc 20 §"where it is allowed" changes materially depending on the answer.
3. **The approximation tradeoff.** Confirm you accept that the living core will not exactly match the Figma swatch, and that Figma stays the colour reference.

---

*Australian English. No em dashes. Prepared by Claude Code, 2026-07-20.*
