# Mez Studios · Design

A public workbench for design experiments. Everything here is live and
interactive, built with no framework, no build step and no dependencies at
runtime.

**Live: https://mez-studios-design.vercel.app**

## Work

### Play Orb · expression system (`/play-orb/`)

A domain-warped mesh gradient rendered in WebGL, expressed across a full
treatment library: gradient-filled mark, flat disc, shaded sphere, squircle,
trading card, stacks, bundles and edition finishes.

Fifty-three live surfaces on one page, all drawn by a single offscreen WebGL
context that blits into each surface's own 2D canvas.

- `/play-orb/` the expression system
- `/play-orb/compare.html` gradient comparison board
- `/play-orb/orbs/<ID>.html` a single standalone orb

**How it works.** Each source gradient is clustered with k-means. The darkest
cluster becomes the sphere shading; the remaining four become mesh anchors
that drift on mismatched Lissajous orbits and are blended by Gaussian falloff
at a domain-warped coordinate. Every anchor keeps its spatial position and its
share of the source, so a colour that lived in the top-right of the gradient
still lives in the top-right of the orb, and an accent stays an accent.

Colour is mixed in linear space. Mixing in raw sRGB goes grey through the
middle, which is what makes most gradients look cheap.

**Rebuild:**

```bash
cd play-orb
python3 build.py --keep-palettes
```

`--keep-palettes` reuses `palettes.json`, which is committed. Regenerating
palettes from scratch needs the source gradient PNGs, which are not in this
repo. Only the two `*-template.html` files are edited by hand; everything else
in `play-orb/` is generated output.

Requires `pillow` and `numpy`. No API keys, no network.

## Running locally

There is no build step. Serve the folder over HTTP:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`. A plain `file://` open mostly works, but
some browsers block the iframe previews over `file://`.

## Notes

- Not tested on Windows or Android. Developed against Chromium and Safari on
  macOS with Metal-backed ANGLE.
- The `prefers-reduced-motion` and WebGL-fallback paths are implemented but
  have not been triggered in testing.

---

Built with [Claude Code](https://claude.com/claude-code).
