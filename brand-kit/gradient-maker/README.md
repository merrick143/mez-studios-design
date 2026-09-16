# Gradient maker

Compose colours or upload an original image, preview the result through the shared Living Core renderer, then save, compare, review and export private drafts.

## Open on the web

Use **https://design.mez.studio/brand-kit/gradient-maker/**. The homepage, Brand Kit console and gradient library link to it. No account or local server is needed.

- Compose a 1024px source from the existing colour recipes, or upload an original square PNG/JPEG, 512–1024px and up to 3 MB.
- **Random palette** draws five independent RGB colours and a new composition seed on every click. It does not cycle through presets. **Remix** keeps those colours and changes the flow; **Reset palette** restores the current starting recipe. Saved packages retain the generated recipe.
- The stateless generation function processes the recipe or image using the same pinned Python extractor. It does not persist uploads, drafts or review notes on the server.
- Saved drafts and original uploads live in IndexedDB in this browser, on this website. Another person, browser, device or origin cannot see that collection. Clearing site data removes it; export ZIP packages as backups.
- Saves are immutable versions with random `DRAFT-…` labels, not canonical MZ-G allocations. Reviews and comparison stay private. A saved preview URL works only in the browser that owns the draft.
- Export includes the source PNG, lossless WebP twin, recipe or original upload, metadata, copied renderer/Wings, standalone preview, file hashes and any private review history. Serve the extracted folder over local HTTP to use its animated preview.

Public generation is bounded to a 4.3 MB JSON body and 1024px images, with two concurrent jobs per function instance. Source PNG and binary WebP responses are separate to stay below the host's payload ceiling. Oversized or malformed uploads, cross-origin requests and public save/review API requests are rejected. A busy instance returns a retryable error. The frontend debounces public generation while retaining the last completed preview.

This publishes an authoring tool, not a new identity decision. Private drafts never enter the approved library automatically.

## Open locally

From the repository root, use the pinned environment described in `brand-kit/START-HERE.md`:

```bash
.venv/bin/python brand-kit/server.py --port 8915
```

Open <http://127.0.0.1:8915/brand-kit/gradient-maker/>. Any free port works. An already-running server needs a restart to load new Python routes; use a separate port when another task owns the existing preview. The local server keeps its existing file-based workflow. The public site uses the stateless Vercel function and private browser storage instead.

## Create and refine locally

1. **Compose colours:** choose a research starter, edit its five colours, then select a colour number to set its position and strength. Softness controls blending; flow controls the coordinate warp. Remix advances the seed while retaining the palette. Equal recipe + generator version + runtime produces equal source pixels. PNG compression can differ between operating systems even when the decoded pixels and extracted core match.
2. **Upload image:** choose a square original PNG/JPEG, 512–4096px and at most 12 MB. The original bytes are retained; EXIF orientation is applied to the normalised RGB PNG and transparency is flattened onto white. WebP fallbacks are deliberately not accepted as palette sources.
3. **Inspect:** switch between sphere, disc, card, pill and Wings, with or without the static Wings overlay, on light or dark surfaces. There is one live core, using the existing Deep Mineral finish. Compare source opens the source PNG beside a captured animation frame. The animation is a parametric approximation, not an exact reproduction of the image.
4. **Save candidate:** name it and save an immutable local version. IDs are provisional, allocated above the highest known library/candidate ID under a cross-process lock. Retrying the same request does not duplicate a save. Loading and saving an earlier candidate creates a new version with a parent reference.
5. **Compare and review:** select two saved source twins to compare. Record Shortlist, Needs changes or Reject, with notes. Reviews are append-only history plus a current review record. A preference does not approve identity or promote a gradient.
6. **Export package:** download the source, recipe or original upload, lossless static twin, extracted core, copied shared renderer and Wings, standalone preview and SHA-256 manifest. Serve the extracted folder over local HTTP to animate its preview. No external assets or services are required by the portable preview. It uses system fonts for portability.

Uploaded versions reload their retained normalised source PNG. The earlier version keeps its untouched original upload. Closing or reloading the maker discards unsaved edits. Public drafts persist in the current browser; local-server candidates persist in the local workspace.

## Authority and reproducibility

```text
editable mesh recipe                  original PNG/JPEG
        ↓ mesh-source-1                      ↓ normalise, retain original
        └───────────────── source.png ────────┘
                              ↓ unchanged deterministic extractor
                     1 shade + 4 spatial anchors
                              ↓ unchanged shared renderer
                       Deep Mineral Living Core
```

Authored hexes are inputs to a **source image**, not direct replacements for extracted anchors. The PNG remains the colour authority. `mesh-source-1` blends weighted Gaussian fields in linear-light RGB with a deterministic seeded sine warp. Existing k-means++ extraction remains k=5, seed=7, sample=160. The static WebP is encoded losslessly from the same RGB image, so its decoded pixels equal the source PNG exactly. Animated output preserves the established approximation contract.

The four starting palettes are new research recipes, not approved library gradients or product assignments. Canonical masters, renderer, extraction code, registries and releases are not regenerated by maker operations.

Saved output is gitignored at `brand-kit/workspace/gradient-maker/draft-<uuid>/`. `candidate.json` records origin hashes, extraction constants, environment versions, parent version and `productionAuthority: false`. `manifest.json` covers immutable package files; later review files are separately timestamped and included in exports. Copy or export candidates before moving to a different computer: the workspace is not synced by Git.

No maker endpoint promotes a candidate. A separate human library-import decision is needed before copying a source into `source-masters/` and rebuilding derived assets. Product assignment and release distribution need their own decisions when applicable. Allocation of an MZ-G number here is provisional and does not reserve it in the canonical library; reconcile IDs again at import.

## Agent and command-line use

Claude Code and Codex use the same repository skill: `brand-kit/skills/codex-made-it/SKILL.md`. The discovery name is historical, not a restriction on which agent can operate it.

```bash
.venv/bin/python brand-kit/gradient-maker/cli.py \
  --recipe /absolute/path/to/recipe.json \
  --name "Mineral exploration"

.venv/bin/python brand-kit/gradient-maker/cli.py \
  --source /absolute/path/to/original.png \
  --name "Uploaded exploration"
```

Use `--parent draft-<uuid>` to record lineage. Use `--request-id <uuid>` to safely retry one logical save. Recipe files are available in compose candidate exports. The original `source-pack/living-core/candidate.py` and legacy workbench remain available for older workflows; the maker is the source-preserving route for new work.

## Public deployment and checks

`api/gradient-maker.py` exposes `GET /api/gradient-maker?action=status`, `POST …?action=preview` and `POST …?action=static`. Only generation is hosted. The root requirements file mirrors the canonical NumPy/Pillow pins, with a test preventing drift; `.python-version` selects Python 3.12. No database credentials or public workspace are needed.

```bash
.venv/bin/python brand-kit/gradient-maker/test_public.py
.venv/bin/python brand-kit/gradient-maker/serve_public.py --port 8916
```

Open `http://127.0.0.1:8916/brand-kit/gradient-maker/?public` to exercise the production storage and API path locally. This QA server only serves static files and the stateless function. `test_public.py` covers source/core parity, exact twins, bounded payloads, origin and route isolation, overload recovery and portable ZIP compatibility.

## Local API and checks

All endpoints live under `/api/gradient-maker/`: GET `status`, `candidates`, `export?slug=…`; POST `preview`, `save`, `review`. POSTs use JSON, local Host validation and same-origin checks. The server binds to loopback. Preview generation has a bounded worker semaphore, input limits and actionable validation errors. The renderer honours the operating system's reduced-motion setting and falls back to the exact static twin when WebGL is unavailable.

```bash
.venv/bin/python brand-kit/gradient-maker/test_engine.py
node --check brand-kit/gradient-maker/maker.js
```

Backend tests use temporary directories, including malformed/flat uploads, deterministic pixels, lossless static twins, immutable/idempotent saves, concurrent IDs, lineage, review history, export hashes and canonical-file preservation. Run all seven checks from `brand-kit/AGENT-GUIDE.md` after changes.

Browser verification URLs: `?static` forces static; `?no-webgl` exercises WebGL unavailability; `?qa` exposes actual draw-call counts as `#live-core[data-draw-calls]` for observation. `?qa-reduced` simulates a reduced-motion media query for the renderer in this page only; it does not change the OS preference. `?qa-strip` removes the live material and greyscales the page for the distinctiveness check. These switches do not alter canonical assets or system settings.

## Work receipt

Task: `TASK-GRAD-MAKER-01`, a bounded user-requested extension of the gradient candidate workflow. Direction authorised in this side conversation: both editable palettes and original-image upload. No canonical identity decision or release is implied. Scope: this folder, maker routes in `server.py`, entry link in the gradient library and shared skill guidance. See `round-01-feedback.json` for validation and visual review evidence.

Public extension: `TASK-GRAD-MAKER-02-PUBLIC`. The user authorised public generation with private browser drafts and downloads on 16 September 2026. This does not authorise library promotion or product assignment. See `round-02-feedback.json` for the implementation receipt.
