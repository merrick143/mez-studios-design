# Mez Systems: Design Pack

A portable, self-contained design system for **Mez Systems**. Copy this whole folder into another repo and an AI agent (or a human) can build on-brand from it.

## Structure

```
design-system-export/
├── README.md              # this file
├── DESIGN_SYSTEM.md       # the single AI-readable master, read first
├── AGENTS.md              # rules for an AI agent working in the target repo
├── typography.md          # the locked type system (Inter, Notion-tuned)
├── gradients.json         # release catalogue: four assigned cores + source/export hashes
├── mz-core.js             # dependency-free living-core WebGL renderer
├── products.json          # canonical product names, status, price and core assignments
├── colours.json           # canonical monochrome palette
├── fonts.json             # canonical family and role metadata
├── tokens/
│   ├── tokens.css         # CSS custom properties + type utilities
│   ├── tokens.json        # the same tokens as JSON
│   └── tailwind.tokens.cjs# Tailwind theme.extend snippet
├── docs/                  # complete numbered brand book, 00 through 20
├── contracts/             # authority, roster, colour and font contracts
├── licences/              # font licensing and acquisition notes
├── scripts/               # deterministic release build and clean-copy validator
└── assets/
    ├── wings.svg          # backwards-compatible mark path
    ├── fonts/             # vendored production fonts
    ├── gradients/         # exact 1600px assigned product cores
    ├── icons/             # SVG sources plus favicon and app-icon matrices
    ├── og/                # 1200 by 630 social-share assets
    └── email/             # SVG and high-resolution raster lockup
```

## How to import

**Any project:** copy this folder in, `@import "./tokens/tokens.css";`, and read `DESIGN_SYSTEM.md`.

**Next.js / Tailwind (Mez stack):**
1. Copy `tokens/tokens.css` into `app/` and import it in the root layout.
2. Merge `tokens/tailwind.tokens.cjs` into `tailwind.config` `theme.extend`.
3. Point your agent at `AGENTS.md` + `DESIGN_SYSTEM.md`.

**Fonts:** Inter (default), Instrument Serif (serif accent), IBM Plex Mono (mono). See
`licences/FONTS.md` for licences, source links, weights, and the rule for vendoring files.

**Gradients:** the four assigned cores ship in `assets/gradients/` as exact 1600px WebP exports.
`tokens/tokens.css` points at those files. `gradients.json` also carries the approved parametric
anchors used by `mz-core.js`. The living result is an approximation; the WebP is always its exact
static twin and is mandatory for reduced motion and renderer fallback.

## Locked decisions (2026-07-10)

- **Colour:** `#F8F8F8` bg · `#F6F5F4` grey · `#FFFFFF` cards · `#0D0D0D` / `#2E2E2E` text. Gradient is the only colour.
- **Type:** Inter, **Bold headings** with negative tracking + tight leading (Notion feel). Instrument Serif for accents, IBM Plex Mono for code.

## Source of truth

- **This distribution:** consume the included release manifest, tokens, guidance, and assets together.
- **This release:** `contracts/authority-model.json` defines precedence and reference states.
- **Optional provenance:** the internal pack and Figma mirror may explain history, but neither is required to use this release.

If this portable copy contains two conflicting rules, stop and report both file paths plus the
release ID from `export-manifest.json`. Do not invent a tie-break or repair a mirror independently.

## Validate a copied release

Run `python3 scripts/validate_release.py` from any copied release. It uses only Python's standard
library and verifies the complete file set, every checksum, internal links, required assets, and
the absence of private source paths in the entrypoints.
