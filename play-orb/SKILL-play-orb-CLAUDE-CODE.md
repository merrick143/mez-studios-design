---
name: play-orb-claude-code
built-by: Claude Code (Anthropic), Opus 4.8
description: Build animated Mez Systems "play orb" components from gradient PNGs. A fluid WebGL mesh gradient inside a perfect circle with the static wings mark at centre. Extracts palettes from MZ-G## gradient files, generates one self-contained orb per gradient, and a comparison board. No API keys, no build step, no dependencies beyond pillow and numpy.
---

# Play Orb (CLAUDE CODE BUILD)

> **Naming note:** this file is deliberately marked `CLAUDE-CODE` because Olli is
> running the same brief through more than one LLM and needs to tell the outputs
> apart at a glance. Do not rename it to something generic. If another model
> produces a competing version, it gets its own suffixed file.

Turns any Mez Systems gradient into a living, interactive orb: a domain-warped
mesh gradient that churns like fluid, wrapped in a perfect circle, with the
wings mark sitting dead centre and perfectly still.

## Trigger Phrases
- "Make an orb from MZ-G07"
- "Build play orbs for MZ-G02, MZ-G09"
- "Rebuild the gradient comparison"
- "Add [gradient] to the orb comparison"
- "Regenerate the orbs"

## Where it lives

```
departments/cmo/brand-library/components/play-orb/
├── SKILL-play-orb-CLAUDE-CODE.md   # this file
├── build.py                        # extract palettes + generate everything
├── orb-template.html               # SOURCE OF TRUTH · single standalone orb
├── expressions-template.html       # SOURCE OF TRUTH · full expression board
├── palettes.json                   # extracted data, safe to hand-edit
├── index.html                      # GENERATED gradient comparison
├── expressions.html                # GENERATED expression system  ← the main one
└── orbs/<ID>.html                  # GENERATED standalone orbs
```

**The two `*-template.html` files are the only ones to edit by hand.**
`index.html`, `expressions.html` and everything in `orbs/` are generated and
will be overwritten without warning.

## The four product cores

Set in `PRODUCTS` at the top of `build.py`. Per the Figma brand kit, locked
12 Jul 2026:

| Product | Gradient | Status |
|---|---|---|
| AI OS (AI Operating System) | MZ-G13 | **LOCKED** |
| Aurora (Auto Ads System) | MZ-G20 | candidate |
| Prism (Analytics Pack) | MZ-G06 | candidate |
| Forge (Claude Code OS) | MZ-G15 | candidate |

Swapping a candidate is a one-line edit in `PRODUCTS`, then rebuild.

## Brand rules the board encodes

Do not "fix" these; they are locked decisions, several of which reverse
earlier versions of the system.

- **Light monochrome.** The product gradient is the only colour anywhere.
  Every other surface is greyscale.
- **Disc is the standard.** Ø190, hard edge, flat gradient, **no halo**.
  Glow is RETIRED.
- **Sphere is identity only.** It is the shaded 3D treatment and must never
  become the default product mark.
- **Wings are 50% of disc diameter**, free-floating, never in a container,
  never recoloured, never below 24px.
- **Card:** #FFFFFF, radius 20, 8% ink hairline, soft drop shadow.
- **Roundness drops as the entity grows:** products are pills, the holdco is
  softened, the parent is squared.
- **Stack:** offset 50 across, 38 down, newest card on top.
- **Rarity is finish, never hue.** A product owns its gradient for life, so
  editions change surface only: matte, keyline, iridescent, foil, stripped.
- **Grid ladder:** 4 columns at 1200, 2 at 920, 1 below. Never reorder source.

## Expression board architecture

Worth understanding before editing `expressions-template.html`, because the
obvious approach does not work.

Each gradient surface is a `.gx` div holding its own cheap **2D** canvas. One
shared **offscreen WebGL** context renders a surface at its viewport origin,
then `drawImage` blits that region into the surface's own canvas.

Three constraints forced this:

1. **One WebGL context per surface fails.** Browsers cap contexts at roughly
   16 and silently kill the oldest. This board has 53 surfaces.
2. **One shared canvas positioned behind the page fails twice.** Any opaque
   ancestor paints over it (white product cards, the dark bundle panel showed
   no gradient at all), and any transformed ancestor creates a stacking
   context that traps the foreground beneath it.
3. **`gl_FragCoord` is absolute, never viewport-relative.** Surfaces are
   therefore rendered at the GL viewport origin and blitted, so the shader's
   coordinates are surface-local. Rendering each surface at its on-screen
   offset instead puts every one of them outside its own shape, which shows up
   as a completely blank board with no console error.

`.gx` carries `isolation: isolate` so each surface is its own stacking
context. Remove it and overlapping cards in the stack show each other's
wings through the transparent divs above them.

## Inputs

| Input | Type | Required | Default | Notes |
|---|---|---|---|---|
| gradient IDs | list | no | `MZ-G13 MZ-G20 MZ-G06 MZ-G15` | Must exist as `~/Downloads/all-gradients/<ID>.png` |
| `--keep-palettes` | flag | no | off | Reuse `palettes.json` instead of re-extracting. Use after hand-tuning. |

## Procedure

### 1. Confirm the source PNGs exist
```bash
ls ~/Downloads/all-gradients/
```
Gradients are named `MZ-G01.png` through `MZ-G41.png` (with gaps). If the folder
has moved, update `GRADIENT_DIR` at the top of `build.py`. Do not silently fall
back to a different folder.

### 2. Run the build
```bash
cd departments/cmo/brand-library/components/play-orb
python3 build.py MZ-G13 MZ-G20 MZ-G06 MZ-G15
```
No arguments rebuilds `DEFAULT_IDS`. The script prints each extracted palette so
the colours can be sanity-checked against the source before opening anything.

### 3. Look at it
```bash
python3 -m http.server 8733
```
- `http://localhost:8733/expressions.html` (the expression system, main board)
- `http://localhost:8733/index.html` (the raw gradient comparison)

**A plain `file://` open works too**, but serve it if anything looks wrong.
Some browsers block iframe content over `file://`, which shows as four empty
boxes on the comparison board.

### 4. Verify before declaring it done
Never hand this off on the strength of the build script exiting cleanly. Check:

- [ ] Each orb's colours plausibly match its source PNG (open both side by side)
- [ ] No orb is a flat single tone (means clustering collapsed, see Guardrails)
- [ ] Browser console is clean; a shader error shows as a **flat CSS gradient**,
      which looks deceptively fine at a glance
- [ ] Hovering scales the orb up and speeds the fluid
- [ ] The wings stay perfectly still
- [ ] On the expression board: discs inside the WHITE product cards and inside
      the DARK bundle panel are visible. Those two are the canaries for the
      occlusion class of bug, and they look plausibly fine when broken (just
      an empty card) rather than obviously broken.
- [ ] Only the TOP card of the stack shows wings and a name. If all four do,
      stacking contexts have regressed.

## How a gradient becomes an orb

1. Source PNG downsampled to 160×160.
2. **k-means (k=5, fixed seed)** over RGB. Fixed seed matters: rebuilds must
   produce identical palettes or comparisons drift between runs.
3. **Darkest cluster → `SHADE`**, which does the sphere shading.
4. **Remaining four → mesh anchors** `C0..C3`.
5. Each anchor keeps its **spatial centroid** from the source, mapped into the
   disc, so a colour that lived in the top-right of the gradient still lives in
   the top-right of the orb.
6. Each anchor keeps its **share of the source** as a weight, so an accent
   stays an accent.
7. The lightest anchor drives the bloom, tinted to itself.

At render time the four anchors drift on mismatched Lissajous orbits and are
blended by Gaussian falloff, sampled at a **domain-warped** coordinate. The
warp is what makes it churn like liquid rather than rotate.

## Tuning

**To adjust one gradient's colours:** edit `palettes.json`, then
`python3 build.py --keep-palettes`. Never edit files in `orbs/`.

**To adjust the look of every orb:** edit `orb-template.html` and rebuild. The
constants worth knowing, all in the fragment shader:

| Constant | Default | Effect |
|---|---|---|
| `K` | `7.5` | Gaussian falloff. Lower = broader, softer colour fields. |
| `S` | `1.9` | Dominance exponent. Higher = anchors hold their own colour instead of averaging to mud. |
| `rim` smoothstep | `0.58, 1.14` | Where sphere shading begins. Lower start = darker orb. |
| `rim` mix | `0.46` | Shading strength. |
| grain `fine` | `0.100` | Paper texture. Sampled in CSS pixels, not device pixels. |
| `--mark-ratio` | `0.39` | Wings size as a fraction of the disc (standalone orb). |
| `HOVER.speed` | `1.85` | Fluid acceleration on hover. |
| `uOct` LOD | `<90px → 2` | Octave count. Small surfaces cannot resolve three. |
| dpr cap | `2` | Device pixel ratio ceiling for the shared GL canvas. |

## Guardrails

- **Fixed seed is load-bearing.** Changing `SEED` in `build.py` reshuffles every
  palette. Two builds must be comparable.
- **Never hand-edit generated files.** `index.html` and `orbs/*.html` are
  overwritten every run. Changes belong in `orb-template.html`.
- **Flat gradients produce flat orbs, correctly.** If a source has fewer than
  four distinguishable colours (MZ-G16 is close), clustering pads by duplicating
  the last anchor. The orb will look subtle. That is faithful, not a bug. If more
  variety is wanted, hand-edit `palettes.json`.
- **Backticks are forbidden in shader comments.** The GLSL lives inside a JS
  template literal, so a stray backtick silently closes it and the orb falls
  back to a flat CSS gradient with no console error. This has bitten once.
- **Verify visually, always.** Every failure mode in this system is silent:
  a dead shader falls back to a flat CSS gradient, an occluded surface just
  looks like an empty card, and a coordinate-space mistake renders nothing at
  all. None of them throw.
- **`half` is a reserved word in GLSL** and will not compile. So is `sample`.
- **Do not screenshot the expression board with a full-page capture.** Surfaces
  are only drawn while on screen, so a stitched full-page image shows blanks
  below the fold. Capture per viewport.
- **Australian English, no em dashes** in anything user-facing.

## Rebuilding from scratch

If everything but this file were deleted, the orb could be rebuilt from
`orb-template.html` alone. If that is gone too, the component is:

- WebGL fragment shader on a full-viewport triangle, circle-clipped by CSS
- 3D simplex noise (Ashima/Gustavson) → 3-octave fBm → two-level domain warp
- Four Gaussian colour anchors on Lissajous orbits, blended in **linear space**
  (sRGB mixing goes grey through the middle and looks cheap)
- Noise-perturbed radial shading toward the darkest colour
- Two-layer static grain, sampled in CSS pixels, luminance-masked
- Wings mark: inline SVG, `viewBox="0 0 512 363"`, mirror-symmetric about
  x=255.5, 45px corner radius, traced from `wings.png`
- Hover 1.03 / press 0.955 on the wrapper; the mark itself never transforms

## Known limitations

- Not tested on Windows or Android; developed against Chromium and Safari on
  macOS with Metal-backed ANGLE.
- The `prefers-reduced-motion` and WebGL-fallback paths are implemented and
  reasoned through but have never actually been triggered in testing.
- `webglcontextrestored` degrades to the CSS fallback rather than rebuilding the
  shader. A GPU switch mid-session leaves a static gradient until reload.
