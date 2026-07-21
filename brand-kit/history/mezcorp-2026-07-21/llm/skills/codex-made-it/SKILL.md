---
name: codex-made-it
description: Build, validate, or extend the Mez Systems Living Core gradient system. Use when an agent needs to ingest an MZ-G source gradient, generate deterministic parametric core data, render animated disc, sphere, rounded-rectangle, pill, card, or Wings expressions, create a research-only product-gradient candidate, or decide between exact static and animated output.
---

# Codex Made It

Operate the canonical Mez Systems Living Core: one parametric shader, four masks, many product cores.

## Authority

1. In the Mez Systems pack, read `governance/decision-register.json`, `gradients.json`, `products.json`, and `brand-system/20-living-core.md` before changing data or behaviour.
2. Treat the exact source gradient and static WebP twin as colour authority. The parametric core is an animated approximation, not a pixel-exact replacement.
3. Preserve `productionAuthority: false` for research candidates. Never assign a candidate to a product or edit canonical registries without a recorded human promotion decision.
4. Use the canonical Wings asset. Do not redraw, approximate, recolour, tile, or place it on an inset white tile.

## Choose the workflow

### Rebuild assigned cores

Use this only when validating or regenerating already assigned products:

```bash
python3 living-core/build.py
python3 living-core/validate.py
```

The canonical builder reads `products.json` and `gradients.json`. It uses pinned dependencies from `living-core/requirements.txt`. A clean deterministic rebuild of unchanged source assets must produce no Git diff.

### Create a new candidate

Use the isolated candidate builder for a new product gradient:

```bash
python3 living-core/candidate.py \
  --source "/absolute/path/to/source.png" \
  --id MZ-G54 \
  --product "Context Engine" \
  --output "/absolute/path/to/new-candidate-directory"
```

The source must be square and at least 512 by 512 pixels. The output directory must not exist. The command produces candidate metadata, an exact static twin, the shared renderer, canonical Wings, and a review plate. It must not edit `products.json`, `gradients.json`, `palettes.json`, or the portable export.

## Ingestion contract

- Downsample the source to 160 by 160.
- Run seeded k-means++ with `k=5` and seed `7`.
- Use the darkest cluster as the shading colour.
- Use the other four clusters as anchors.
- Preserve each anchor's spatial centroid and relative source weight.
- Mix colour in linear space, not raw sRGB.
- Keep the exact static twin beside every parametric core.
- Pin NumPy and Pillow versions. Do not claim determinism using an unpinned environment.

## Renderer contract

- Use one shared offscreen WebGL context for all live surfaces.
- Render each shape at the viewport origin, then blit to that surface's cheap 2D canvas.
- Keep a 2x DPR ceiling.
- Skip offscreen surfaces and pause when the document is hidden.
- Use the same core data, shading and motion for all masks.
- Allowed masks: disc, sphere, rounded rectangle, Wings.
- Keep Wings, labels, borders, chips, controls and layout static above the field.
- Hover may accelerate the fluid field to 1.85x. Never scale or move the core or Wings.
- Reduced motion, WebGL failure, shader failure, missing data, or runtime failure must show the exact static twin.
- Do not use the gradient as a page background, section background, text fill, ambient blob, or decorative glow.

## Expression selection

- Disc: canonical compact product mark and default card object.
- Sphere: hero or identity treatment for one focal product.
- Rounded rectangle: core field inside a trading card or compact pill.
- Gradient Wings: identity or motion study only; ordinary product marks use white Wings inside the core.
- Website hero: at most one animated core after consumer approval.
- Repeated cards, catalogues, bundles, upsells and dense UI: static by default.
- Email, still ads, social stills, OG, documents, print, PDF, packaged icons and reduced motion: exact static twin only.
- Video: one focal Living Core may animate; structure and end frame stay static.

Read [references/product-disc-contract.md](references/product-disc-contract.md) for the full expression and verification contract.

## Verification

1. Run the Living Core validator.
2. Confirm a full canonical rebuild produces no diff.
3. Open the candidate or reference plate in a browser.
4. Verify all masks are visible, animated surfaces share one WebGL context, and the console is clean.
5. Verify desktop and mobile overflow.
6. Trigger reduced motion and confirm the exact static twin renders.
7. Confirm the candidate did not mutate canonical files.
8. Report the source path, candidate or assigned ID, output path, authority state, and checks completed.

Do not promote a visually plausible approximation without comparing it to the exact source.
