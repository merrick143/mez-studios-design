# Source map

## Current ownership

| Layer | Location | Role | May own decisions? |
| --- | --- | --- | --- |
| Canonical working pack | `mez-design-system-worktree/departments/cmo/brand-library/brands/mez-systems` | Current decisions, product data, rules, generator and release source | Yes, until migration closes |
| Claude visual benchmark | `/play-orb/` in this repository | Original animated implementation and palette extraction from source PNGs | No; protected comparison evidence |
| Workbench snapshot | `/brand-kit/source-pack/` | Pinned files imported from the canonical branch | No |
| Candidate workspace | `/brand-kit/workspace/` | Uploaded images, generated plates and select/edit/reject records | No |
| Portable releases | `/brand-kit/releases/` | Future immutable distributions after all release gates pass | Only as a named release mirror |
| Figma | recorded Mez Systems file and gradient library | Human authoring and exact source-gradient reference | No independent token authority |

## Resolved extraction authority

The Claude Code `palettes.json` and the systemised canonical `palettes.json` are not identical.

- Claude extracted from the original source PNG library.
- The systemised rebuild extracted from compressed WebP static twins.
- The renderer remains animated in both systems.
- The difference is colour-anchor data, spatial centroids and cluster shares.

The source-PNG extraction is authoritative. The WebP re-extraction remains only as historical evidence of an invalid derivation path. Never extract new palette data from a WebP, screenshot or rendered Living Core.

The complete 43-ID research library now lives under `brand-kit/gradient-library/`. Its `source-masters/` PNGs, source hashes, duplicate-ID groups, extraction cache, catalogue and static twins are generated and validated together. Product assignments remain separately governed.

## Stable imports

- Canonical Wings SVG.
- Current dependency-free shared WebGL renderer.
- Four exact WebP static twins.
- Current product roster and assignment states.
- Deterministic candidate generator and extraction constants.

## Unresolved imports

- Geist display font asset is not present locally.
- Current portable release still describes Inter-only typography and therefore predates `DEC-TYPE-001`.
- Public homepage roster and canonical four-product roster still conflict.
- Context Engine has no source gradient or assignment.
- Aurora, Prism and Forge core assignments remain candidates.
