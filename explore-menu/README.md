# Mez Systems Explore Menu

Status: research component. This is not a canonical `brand-kit/` expression and does not carry production authority.

The component adapts the spatial continuity of a morphing product menu into a minimal Mez Systems product navigator. Its expanded state is only the five canonical Living Core discs and their product names. It is built as a dependency-free custom element so it can run inside the current static design workbench and move into a future consumer after the product-card and website-component gates are complete.

## What it uses

- Canonical foundation release `1.0.0` for type, colour, geometry and controls.
- Canonical product names, summaries, lifecycle states and gradient assignments from `brand-kit/registry/products.json`.
- Five animated Deep Mineral Living Core discs mounted through one shared renderer.
- Exact static gradient twins for reduced motion and renderer failure.
- The canonical Wings SVG, always static.

## Run

From the repository root:

```bash
.venv/bin/python brand-kit/server.py --port 8914
```

Open `http://127.0.0.1:8914/explore-menu/`.

Append `?static=1` to force the exact static fallback or `?no-webgl=1` to simulate renderer unavailability.

## Reuse

Load the canonical foundation stylesheet and the component module, then place the custom element in the page:

```html
<link rel="stylesheet" href="/brand-kit/releases/foundations/dist/index.css">
<link rel="stylesheet" href="/explore-menu/explore-menu.css">
<mez-explore-menu selected="aios"></mez-explore-menu>
<script type="module" src="/explore-menu/explore-menu.js"></script>
```

Supported attributes:

- `selected`: a canonical product slug highlighted in the gallery. Defaults to `aios`.
- `variant`: `registry`, `signal`, `aperture`, `gallery`, or `console`.

The preview page includes a five-direction switcher and keeps only one direction mounted at a time.

1. `registry` — quiet, balanced product catalogue.
2. `signal` — typographic identity with numbered system objects.
3. `aperture` — compact closed control with a generous reveal.
4. `gallery` — canonical light canvas and collected cores.
5. `console` — technical index built from hairlines and coordinates.
