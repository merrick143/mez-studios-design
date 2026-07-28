---
name: codex-made-it
description: Build, validate, or extend the canonical Mez Systems Living Core gradient system. Use when Claude Code, Codex, or another repository agent needs to ingest an MZ-G source PNG, rebuild deterministic palette data and exact static twins, render disc, sphere, rounded-rectangle, pill, card, or Wings expressions, create a non-canonical product-gradient candidate, or decide between static and animated output.
---

# Operate the Mez Living Core

Use one source-PNG authority, one deterministic extraction contract, one shared renderer, and one recorded promotion path.

## Establish authority

From the repository root, read:

1. `brand-kit/authority/authority.json`.
2. `brand-kit/governance/decisions.json`.
3. `brand-kit/registry/products.json` and `brand-kit/registry/gradients.json`.
4. `brand-kit/gradient-library/README.md` and `brand-kit/gradient-library/assignments.json`.
5. [references/product-disc-contract.md](references/product-disc-contract.md) when choosing an expression or channel behavior.

Treat `brand-kit/gradient-library/source-masters/*.png` as colour and extraction authority. Treat generated WebP files as exact static delivery twins, never palette sources. Treat the animated core as a parametric approximation.

## Rebuild or verify the source library

Use the pinned Python environment from `brand-kit/START-HERE.md`:

```bash
.venv/bin/python brand-kit/gradient-library/build_library.py --verify
.venv/bin/python brand-kit/gradient-library/verify_library.py
```

An unchanged deterministic rebuild must create no Git diff.

To import a reviewed set of correctly named source masters:

```bash
.venv/bin/python brand-kit/gradient-library/build_library.py \
  --source "/absolute/path/to/source-directory" \
  --import-sources
```

Never import screenshots, WebP fallbacks, or rendered cores as source masters.

## Create a research candidate

Use the local workbench:

```bash
.venv/bin/python brand-kit/server.py --port 8914
```

Open `/brand-kit/`, upload a square source image of at least 512px, and create an unused `MZ-G##` or `MZ-G###` candidate. Generated files remain under the gitignored `brand-kit/workspace/candidates/` directory.

Candidate generation must not edit `registry/`, `governance/`, `gradient-library/assignments.json`, or a release. Promotion requires an explicit human select/edit/reject record followed by a separate canonical update.

## Preserve the ingestion contract

- Downsample the source to 160 by 160.
- Run seeded k-means++ with `k=5` and seed `7`.
- Use the darkest cluster as shade and the other four as moving anchors.
- Preserve anchor centroid and relative source weight.
- Mix runtime colour in linear space.
- Keep Pillow and NumPy pinned.
- Keep the exact static twin beside every core.

## Preserve the renderer contract

- Use one shared offscreen WebGL context and blit into cheap 2D canvases.
- Use one core dataset across disc, sphere, rounded rectangle, and Wings masks.
- Keep Wings, labels, controls, borders, and layout static.
- Permit hover to change field speed only; never grow or move the core.
- Cap DPR, pause hidden or offscreen work, and keep reduced-motion and runtime failure fallbacks exact.
- Use the approved Deep Mineral finish unless a bounded calibration explicitly compares profiles.
- Never use a core as page background, section background, text fill, ambient blob, or decorative glow.

## Verify and report

1. Run `verify_library.py` and the shared portability and workbench validators.
2. Confirm a rebuild creates no unintended diff.
3. Inspect source, static twin, disc, sphere, card field, pill, and Wings.
4. Verify reduced motion, WebGL failure, responsive overflow, and console state.
5. Confirm candidates did not mutate canonical files.
6. Report source path, core ID, authority state, output path, decisions applied, and checks completed.

Do not promote a visually plausible approximation without comparing it to the source PNG and exact static twin.
