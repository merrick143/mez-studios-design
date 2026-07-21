# Mez Studios · Design

A public workbench for design experiments. Everything here is live and
interactive, built with no framework, no build step and no dependencies at
runtime.

**Live: https://mez-studios-design.vercel.app**

## Work

### Mez Systems Brand Kit Workbench (`/brand-kit/`)

The organised migration control plane for the Living Core, foundations,
product-expression suite and portable releases. `brand-kit/` is the canonical control plane and
its active `0.1.0-alpha.1` identity snapshot validates independently.
It preserves the original Play Orb as a protected benchmark while imported system files
remain pinned to a named canonical commit.

- `/brand-kit/` the programme and live comparison workbench
- `/brand-kit/START-HERE.md` the canonical entrypoint for humans and LLMs
- `/brand-kit/docs/CURRENT-STATE.md` the exact completed-versus-open boundary
- `/brand-kit/docs/ROADMAP.md` the active execution sequence
- `/brand-kit/docs/END-TO-END-ROADMAP.md` the complete audit and big end-to-end plan
- `/brand-kit/docs/MIGRATION-PLAN.md` the full authority-transfer plan
- `/brand-kit/authority/authority.json` the two-phase canonical authority record
- `/brand-kit/releases/0.1.0-alpha.1/` the self-contained migration snapshot
- local candidate generation through `brand-kit/server.py`

Repository skills are shared between tools from one source. Codex discovers `.agents/skills/`; Claude Code discovers `.claude/skills/`; both point to `brand-kit/skills/`.

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

To enable local candidate generation, use a Python environment with the pinned Pillow and NumPy
versions, then run `python brand-kit/server.py --port 8914` instead.

## Notes

- Not tested on Windows or Android. Developed against Chromium and Safari on
  macOS with Metal-backed ANGLE.
- The `prefers-reduced-motion` and WebGL-fallback paths are implemented but
  have not been triggered in testing.

---

Built with [Claude Code](https://claude.com/claude-code).
