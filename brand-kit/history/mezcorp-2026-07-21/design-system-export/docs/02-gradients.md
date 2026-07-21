# 02 · Gradients

Gradients are the colour system for **products only**. Each product owns exactly one library gradient, called its **core**. The core is expressed through a small set of treatments (disc, Gradient-M, trading, sphere, living core), never as a bare rectangle in UI.

## Naming convention

- Every library gradient has a stable ID: **`MZ-G01`** through **`MZ-G53`**.
- Each maps to a Figma **imageHash** (the value below). Reference gradients by `MZ-G##` in specs; the full hash lives here and in [`../gradients.json`](../gradients.json).
- Source of the raw library: frame `312:57` ("MZ Gradient Library · raw") on the Playground page (`0:1`), 53 swatches laid out as an 8-wide grid. `MZ-G01`–`MZ-G20` have confirmed imageHashes (catalogued below); `MZ-G21`–`MZ-G53` exist in the raw frame with hashes not yet catalogued, export before use.
- To apply a gradient in the Plugin API: set an `IMAGE` fill with `scaleMode: 'FILL'` and the imageHash on an ellipse (sphere/disc), a flattened wings vector (Gradient-M), or a card rectangle (trading).

## The four cores

| Product | Function | Core | imageHash |
|---------|----------|------|-----------|
| **AI OS** | AI Operating System | `MZ-G13` | `4ea105843cbc5fe3450b70aa0f3c3bcc9b487408` |
| **Aurora** | Auto Ads System | `MZ-G20` | `76df089a7f3d0fe9f9fc44349a71401ed214c4d9` |
| **Prism** | Analytics Pack | `MZ-G06` | `34e197fd0fc94cdc231d66446fa6c3f2b1e48fad` |
| **Forge** | Claude Code OS | `MZ-G15` | `876be3cf1c6da154d9a532d2b5a865199b29c939` |

These are strong current picks, not finally signed off. Cores can be reselected from the full library below by `MZ-G##`; every treatment updates with the new core automatically.

## The full library

| ID | imageHash | Core? |
|----|-----------|-------|
| MZ-G01 | `1844468e23a3a7b6d4a73de83e46e8d893e40fa5` | |
| MZ-G02 | `9326690c06692a31c0ba2882c5fa62b247527b55` | |
| MZ-G03 | `eeffea4352c19e8de036f78bbd639f59af03c10f` | |
| MZ-G04 | `3d490437a315f274c4a497ce1262e021572f7193` | |
| MZ-G05 | `1d90b07e94d412ca0a2f1e24c95293b0bad5d86b` | |
| MZ-G06 | `34e197fd0fc94cdc231d66446fa6c3f2b1e48fad` | **Prism** |
| MZ-G07 | `73063ea6aa0b0961c59a3f621e28f0092be63fb7` | |
| MZ-G08 | `441431b343fed8e5cda120025604375c2e1b8326` | |
| MZ-G09 | `636d364c52854b8eb395f063c2bc043f5687f4e1` | |
| MZ-G10 | `a0c2b5f5fbdbcb2d995491f345cddacf835fe7ed` | |
| MZ-G11 | `26cae1755ca7f413a6b9ff0755163c0fa062f771` | |
| MZ-G12 | `e0a2c42dcfc3f9a6d82b11123174699dac886c23` | |
| MZ-G13 | `4ea105843cbc5fe3450b70aa0f3c3bcc9b487408` | **AI OS** |
| MZ-G14 | `2ced4b6f181f5f15bb615ae5f21b89cd404b2f21` | |
| MZ-G15 | `876be3cf1c6da154d9a532d2b5a865199b29c939` | **Forge** |
| MZ-G16 | `0b9fac29925166f40e8fb35b0265b4d6606df583` | |
| MZ-G17 | `95f307a89df5fceaa959cd62b279e54bedb0db0b` | |
| MZ-G18 | `aa4e18ed06cf737df5d506d960cb53670d28f7f4` | |
| MZ-G19 | `7568125fa03e1e3927ad578f9fc38ff3f2c4cd4b` | |
| MZ-G20 | `76df089a7f3d0fe9f9fc44349a71401ed214c4d9` | **Aurora** |

`MZ-G21`–`MZ-G53` exist in the raw frame, hashes uncatalogued; export before use.

Live in Figma: raw library frame `312:57` on the Playground page (`0:1`); curated catalogue board `155:2`.

## Treatments

A core is always shown through one of these, depending on context:

| Treatment | What it is | Where it is used |
|-----------|-----------|-------------------|
| **Disc** | Flat gradient circle, hard edge, white wings at 50% of Ø | THE standard product treatment: cards, heroes, nav chips, favicons |
| **Gradient-M** | The wings flattened into one vector, filled with the gradient (a window into the gradient). | Marks, app icons, compact lockups. |
| **Trading** | Full-bleed gradient card, white 16% inner hairline, white wings (~32% width), product name in white Semi Bold under the wings. No sphere. | Stacks, decks, bundles, collectible contexts. |
| **Sphere** | Gradient ellipse, inner-shadow depth, white wings knocked out. | Identity boards only. Never a product card, see Disc. |
| **Living core** | The core reconstructed from four parametric colour anchors and rendered as continuous shader motion. It is an approximation of the source swatch, not a pixel-exact reproduction. | Internal identity surfaces first. Hero, product-card disc and runtime app-icon use require the limits in [20-living-core.md](20-living-core.md). Static WebP remains the exact-colour fallback. |

Glow was retired 2026-07-17. Never add halos, blurs or diffuse spreads behind a core.

## Rules

1. One gradient per product. That gradient is its core, for life (until formally reselected).
2. Gradients belong to products only, never the holdco, never a page background.
3. Always show a gradient through a treatment. Never a bare rectangle in UI.
4. Reselect a core by `MZ-G##`; treatments update automatically.
5. Reference gradients by `MZ-G##` in specs; the full hash lives in this file and `gradients.json`.
6. The living core is the sole sanctioned animated-gradient treatment. It never changes the product assignment, and Figma plus the static WebP remain the reference when exact colour matching is required.
