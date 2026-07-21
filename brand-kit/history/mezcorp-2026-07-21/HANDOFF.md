# Mez Systems design system: end-to-end handoff

Written 2026-07-19. This is the operator manual for an LLM asked to update, improve or rework the Mez Systems design system. It maps every surface, what is truth vs mirror, how to change things safely, and the traps that have already bitten previous sessions. Read this fully before touching anything.

## Current programme state

Phase 1 safety and portability repair is complete. Phase 2 passed H1, completed the five-source deep cycle and TR-4 synthesis, invalidated the first TR-5 instrument, and completed the replacement source-level taste review. The three-route build, four homepage foundation studies and coherent homepage synthesis are all invalid as directions. An authority reset was recorded on 20 July 2026.

The active research index is `research/phase-2/README.md`. Olli selected Notion, Linear, Stripe, ElevenLabs, and Ramp for deep study. The invalid 12-pair pilot remains quarantined in `research/phase-2/calibration/invalid-pilot/`. The valid source-level record is preserved in Taste Reverse and synthesised in `research/phase-2/REFERENCE-TASTE-SYNTHESIS.md`. The invalid TR-6 record and postmortem are preserved in `research/phase-2/directions/invalid-round/`.

The current programme decision is `governance/MIGRATION-FIRST-GATE.md`. The failed synthesis and review remain preserved in `research/phase-2/homepage-studio/invalid-synthesis-01.html` and `invalid-synthesis-01-review.json`. Visual truth passed unanimously. `DEC-MOTION-002` promoted the Living Core as one narrow product-only rule. `DEC-TYPE-001` approves tuned Inter for primary UI and body, Geist for display, contextual-only Instrument Serif, restricted IBM Plex Mono, and mobile revision around the split. `DEC-CONTROL-001` approves the 12px moderate control radius, solid/outline/text hierarchy, one-pixel lift, 48px default, selective directional icons, inverted dark-section hierarchy and mobile full-width primary. `DEC-FAMILY-001` approves the homepage five, aligned catalogue, gradient-and-copy territories, static cores in repeated contexts, equal family weight, AI OS first with bundles later, and a vertical mobile catalogue with sticky purchase summary. The family plate's visual execution is not approved. `DEC-HERO-001` approves Hero 03's overall direction, centred hierarchy, five-card composition, animation use and product-family read; mobile needs revision.

The complete source-gradient library, Living Core animation and cross-shape expression family are approved through `DEC-GRADIENT-LIBRARY-001`. Deep Mineral is selected through `DEC-LIVING-CORE-FINISH-001`. `DEC-PRODUCT-ARCHITECTURE-001` locks the literal five-product identity kernel. `CUTOVER-2026-07-21-01` is complete: target activation `19f1570` and clean-clone proof `6b1f0c4` make `merrick143/mez-studios-design/brand-kit` rank-one canonical authority. This pack is now a pinned archive, rollback source and consumer reference.

The approved literal five-product roster supersedes the older alternate-name roster for migration. The old internal registry remains frozen evidence until the approved identity kernel is generated atomically into the versioned target snapshot.

Taste Reverse is operationally usable through its sanitised findings export, but it is not yet an immutable Git-pinned dependency. Its first repository commit and tag remain pending confirmation of whether historical screenshots and overlays belong in the initial history.

## 1. What Mez Systems is

Mez Systems is the digital-products brand inside Mez Studios Pty Ltd (Oliver "Olli" Merrick, Australian solo founder). The approved migration roster is:

| Product | Function | Core | Status |
|---|---|---|---|
| AI OS | AI Operating System | MZ-G13 | LIVE at mez.systems, USD $99 one-time. Migration assignment approved. |
| Context Engine | Business context system | MZ-G12 | Coming soon. Migration assignment approved. |
| AI Ads System | Advertising operating system | MZ-G06 | Coming soon. Migration assignment approved. |
| Claude Code OS | Software-work operating system | MZ-G15 | Coming soon. Migration assignment approved. |
| Organic Content OS | Organic content operating system | MZ-G20 | Coming soon. Migration assignment approved. |

The product name is exactly "AI OS" with a space. Banned spellings: "AIOS" and the retired codename "Atlas". Do not introduce alternate product names or a second public naming layer.

The approved direction is a monochrome chassis where product gradients appear only on product elements. The Living Core may animate through the approved disc, sphere, rounded-rectangle and Wings masks while structural Wings and UI remain static. Exact PNG/WebP sources remain colour authority. Geist owns display titles, tuned Inter owns body and UI, Instrument Serif is contextual-only, and IBM Plex Mono is restricted to code, provenance and technical metadata. Implementation of the full foundation token system remains post-cutover work.

## 2. The five surfaces and what wins

There are five places the system exists. Their authority is defined in
`governance/authority-model.json`; approved decisions and canonical data outrank every mirror.

1. **THE PACK (current truth until cutover):** `departments/cmo/brand-library/brands/mez-systems/` on `codex/mez-gradient-system` at the frozen or latest approved checkpoint. Written docs and machine-readable data remain authoritative until the migration gate passes.
2. **THE CANVAS (live render of truth):** `canvas/` inside the pack. Plain HTML pages that import the pack's tokens.css directly. Zero build step. This is where design work is REVIEWED and ITERATED now. Olli has explicitly moved day-to-day design work here, away from Figma and away from the website repo.
3. **THE TARGET WORKBENCH (recovery, not yet truth):** `merrick143/mez-studios-design/brand-kit`, branch `codex/brand-kit-workbench`. It becomes canonical only through the atomic cutover in `governance/MIGRATION-FIRST-GATE.md`.
4. **THE FIGMA (milestone mirror):** file `HU0GVaDhatjWrKCiSg3wlU`. Visual reference only. The production library waits until cutover and foundation/component approval.
5. **THE WEBSITE REPO (consumer):** `~/Desktop/mez-studios/landing-pages/apps/ceos-notion-landingpage`. The live mez.systems codebase. It consumes a released pack. See section 6 for its delicate state.

Precedence when anything disagrees: approved decisions > canonical data > `START-HERE.md` and numbered docs > portable export > certified references > Figma mirror > consumers. Newer content does not silently override an approved decision; it must carry the required gate and changelog evidence.

## 3. The pack, file by file

Root: `departments/cmo/brand-library/brands/mez-systems/`

- `START-HERE.md`: the entry point. Reading order, precedence, the 15 hard rules (law) vs creative latitude, and the lock-states table (LOCKED / CANDIDATE / DEFAULT / OPEN). Read first, always.
- `products.json`: the frozen internal roster baseline. `DEC-PRODUCT-ARCHITECTURE-001` now outranks it, but the file remains unchanged as migration evidence until the approved five-product registry is generated atomically in the target snapshot.
- `gradients.json`: the MZ-G## gradient catalogue. Raw master library is Figma frame 312:57 (53 swatches, MZ-G01 to G53). G01 to G20 have confirmed Figma image hashes; G21 to G53 are uncatalogued. Files are named `mz-g##.webp`.
- `manifest.json`, `colours.json`, `fonts.json`: brand-library metadata.
- `brand-system/` (the written brand book, numbered reading order):
  - 00 architecture, 01 colour, 02 gradients, 03 typography, 04 the mark (wings geometry + SVG recipe), 05 product system (disc law, card anatomy), 06 trading cards and stacks (full-bleed gradient card: radius 7.5% of width, glass MEZ SYSTEMS chip top-left at 8% inset, wings 32% of width + name in the bottom third), 07 UI components (pills, buttons, radius-is-hierarchy), 08 figma map (every board's node ID), 09 governance (decisions register + dated changelog; every change gets a changelog line), 10 product template (a product owns only 4 things: gradient, name, copy, screens; everything else is inherited)
  - The web layer (added 2026-07-17/18): 11 layout and grid (container 1160, gutters 24/32, breakpoints 600/920/1200, section rhythm 72/120, spacing extensions 96/120/160), 12 states and forms (button/input states, focus rings, functional colours error #B42318 success #15803D, dark-surface text tokens, LOCKED light-only declaration), 13 sections (ten specced sections with copy-slot character limits), 14 page archetypes (ordered section lists per page type; the product template varies only copy/screens/core), 15 commerce (checkout, success, delivery email; GST by buyer location, AU sees "Includes 10% GST (AU)"), 16 motion (200ms, 280ms for accordions/sheets, cubic-bezier(.2,.7,.2,1), hover-only, no scroll-reveal, reduced-motion respected), 17 voice and copy (sentence case, semantic CTA actions, banned hype words, approved default copy), 18 imagery and OG (screenshots stay IN COLOUR inside a window frame: radius 14, #F6F5F4 title bar, three dots; OG 1200x630 spec; favicon system), 19 review checklist (the self-review an LLM runs before presenting any build; testable yes/no items)
  - Every doc ends with a machine-readable JSON block carrying its numeric values. Docs marked DEFAULT hold working values Olli has not signed off; docs/values marked LOCKED are law.
- `design-system-export/` (the portable pack, copied into consuming projects):
  - `DESIGN_SYSTEM.md` (single-file condensed master), `AGENTS.md` (the rule sheet for coding agents), `README.md`, `typography.md`, `gradients.json` (a marked copy of the root file; header key `_copy_of`; never hand-edit), `assets/wings.svg`
  - `tokens/tokens.css` + `tokens.json` + `tailwind.tokens.cjs`: THE tokens. All three files must always carry identical values. tokens.css is what the canvas imports; the .cjs is what Tailwind projects consume.
- `canvas/` (the live showroom): `index.html` hub, `tokens.html` (token board rendered from the CSS vars), `components.html` (every component, every state), `sections.html` (the section library), `pages/` (home, product-aurora, checkout, email archetypes), `canvas.css` (component classes; imports ../design-system-export/tokens/tokens.css; NEVER hardcodes a value a token holds), `canvas.js` (nav sheet only), `SNIPPETS.md` (markup patterns; use these exact patterns), `README.md`. To view: serve the PACK ROOT, not canvas/, or the token import 404s: `python3 -m http.server 8905 --directory departments/cmo/brand-library/brands/mez-systems` then open `http://localhost:8905/canvas/index.html`. file:// double-click also works.
- `trading-cards-fut-study/`: FUT card design-language teardown (rarity = finish escalation). Reference.
- `aios-website/index.html`: an OLD demo, banner-marked SUPERSEDED. Never copy values or copy text from it.
- `_archive/old-product-ladder/`: retired six-product PNGs. Ignore. (Note: `_archive/` is gitignored repo-wide by convention; it exists on disk only.)
- `HANDOFF.md`: this file.

## 4. The laws that keep getting violated (do not repeat these)

1. "AI OS" with a space. Never AIOS, never Atlas. Lowercase `aios` is fine as a slug/key only.
2. Flat disc. No glow, no halos, no blurred ellipses behind orbs, ever. The sphere exists on identity boards only.
3. Gradient only on product elements. Never on a page or section background. Chrome is monochrome.
4. NEVER use em dashes or double hyphens anywhere: docs, code comments, commit messages, Figma text, UI copy. Use full stops, commas, colons, or the interpunct (·) for label separators. Australian English. Sentence case everywhere, including headings and buttons.
5. Price: $99 one-time, lifetime access. Never subscription framing ("/mo", "billed annually"). Price display is per-surface judgement: ads default price-free, pricing/checkout surfaces always show it.
6. Tokens only. Never invent a grey, shadow, radius, duration or spacing value. If a needed value does not exist, add it to ALL THREE token files and document it, with a governance changelog line.
7. The radius set is closed: chip 8, tile 14, card 20, panel 28, pill 999.
8. Light-only site. No prefers-color-scheme handling. Dark (#0D0D0D) is a section treatment, not a theme.
9. Product screenshots stay in colour (they are evidence, not chrome) inside the doc-18 window frame.
10. Deletion on this machine: `rm` is blocked by a hook. Use `trash`, and never bundle a delete with other steps.

## 5. The Figma (mirror), and its traps

File `HU0GVaDhatjWrKCiSg3wlU`. Pages:
- "Mez Systems: Brand System" (page 149:30). Sections left to right: 00 Start here `447:2`, then `153:34` (01 colour), `165:62` (02 type), `170:34` (03 product), `172:28` (04 stacks), `176:47` (05 gradient in context), `175:60` (06 UI), `177:47` (07 governance), `266:116` (08 surfaces), `286:2` (09 sizing, LOCKED board), `463:2` (10 layout), `474:2` (11 sections), `469:2` (12 states and forms), `484:2` (13 pages), `486:2` (14 commerce). The wide frame `149:31` is the backbone: reference archive only, it LOSES conflicts with numbered sections.
- "Mez Systems · Products" (page 304:2): TEMPLATE `311:2`, AI OS built out `306:2` (identity 306:3, hero 308:2, card+bundle 308:16, trading+stack 309:2, gradient-in-context 309:41, UI 310:2), slots Aurora `311:31`, Prism `311:46`, Forge `311:61`.
- "Playground for ideas - branding" (page 0:1): raw gradient grid `312:57` (MZ-G01 top-left = 312:23, sequential; G13=312:35, G15=312:37, G20=312:42). Drafts and Type-Tests pages contain deliberate design history including old glow explorations; leave them.

Figma MCP traps (server prefix `mcp__d334d903-...`): `use_figma` returns NO values ever; `get_metadata` with no nodeId shows a stale page list; `figma.loadAllPagesAsync` is unsupported (use `figma.root.children.find` + `setCurrentPageAsync`); text edits require loading every font in the node first (`getStyledTextSegments(['fontName'])` then `loadFontAsync` each); screenshot before and after every change, section-level nodes only (wide renders kill the connection); auto-layout pills need sizing AUTO set before cornerRadius 999; image fills use `{type:'IMAGE', scaleMode:'FILL', imageHash}` with the hashes from products.json.

Update policy: Figma is updated AFTER a change locks in the pack, as a mirror pass. When you change a board, update `brand-system/08-figma-map.md` and add a `09-governance.md` changelog line.

## 6. The website repo (consumer), handle with care

`~/Desktop/mez-studios/landing-pages/apps/ceos-notion-landingpage`. Vite 6 + React 19 + TS + Tailwind 3.4 + vite-react-ssg, Vercel, LIVE Stripe checkout at mez.systems.

Observed state (2026-07-19 Phase 0 baseline):
- The current checkout is on branch `codex/mez-systems-design-system` at commit `cc4f3abc145fc7bdd96e67ab1eb06d038923a997`, with untracked local files. This is evidence, not a release claim.
- The prior handoff's `feat/mez-design-system` branch and `/home` integration claim could not be verified in the current checkout. Do not assume the old branch, base commit, sync state or deployment state remains true. Re-run repository, remote and deployment checks before any consumer work.
- DO-NOT-TOUCH: `src/pages/Checkout*.tsx`, `components/checkout/`, pricing wiring, analytics, routing, the `/ai-os` page. These carry live revenue.
- The claimed paths `docs/mez-design-system/`, `src/pages/Home.tsx`, `components/home/`, `src/styles/mez-tokens.css` and `public/gradients/manifest.json` are absent in the current checkout. Treat the consumer as `candidate` and migration-required until those contracts are installed and certified.
- The Canvas remains the local reference fixture. It is not a certified golden until the Phase 1 breakpoint, accessibility and deterministic review gates pass.

## 7. What is NOT settled (Olli's open decisions)

DEFAULT (working values, he may overrule): nav links "Products · Pricing"; functional form colours; legacy product one-liners and home hero copy in doc 17; section rhythm numbers; h2 fluid clamp capped at 2.5rem; email pay-control and refund wording in doc 15.
OPEN: the master holdco mark; nav IA final. The five-product roster, stable IDs and Living Core assignments are approved migration inputs through `DEC-PRODUCT-ARCHITECTURE-001`.
GATE ITEMS on /home he has not reviewed: the Ethos + Thesis sections break the locked 7-section home archetype; a success-green chip used decoratively in Ethos; small shared-token deltas that touch the /ai-os footer; the OG image uses a disc where doc 18 wants the trading-card fan; planned product cards carry no CTA.
He has also said, generally, that there is a lot he does not like. Treat every DEFAULT as up for challenge; treat every LOCKED rule as law unless he explicitly reopens it.

## 8. How to make a change (the loop)

Migration is the active programme boundary. Do not start broad foundation, component, homepage or Figma-library work in this pack. The product architecture gate is closed. Until cutover, restrict changes to migration evidence, schemas, validators, the final frozen snapshot and rollback proof.

1. Read `START-HERE.md`, then the doc that owns the value.
2. Change the DOC and the TOKENS first (all three token files, identical values). Never change a mirror first.
3. Render it: refresh the canvas (it imports tokens.css live; component/section markup lives in canvas.css + the html pages). The canvas is the review surface; iterate here with Olli.
4. When Olli approves: add a dated `09-governance.md` changelog line (colons, no dashes); update `design-system-export/DESIGN_SYSTEM.md` and `AGENTS.md` if the change touches their condensed content; keep the export `gradients.json` identical to root if gradients changed.
5. Re-copy the export + START-HERE + products.json into the website repo's `docs/mez-design-system/`.
6. Mirror to Figma (section 5 policy) when the milestone warrants it.
7. Before presenting ANY build, run `brand-system/19-review-checklist.md` on it.
8. Commit style: small scoped commits, message prefix `mez-systems:`, no em dashes, co-author line if you are a Claude agent.

## 9. Fast orientation for a fresh session

```
cd /Users/olivermerrick/mezcorp_claude_code/departments/cmo/brand-library/brands/mez-systems
cat START-HERE.md products.json
python3 -m http.server 8905 --directory . &
open http://localhost:8905/canvas/index.html
```
Look at the canvas first. It is the fastest way to see what the system actually is, and the fastest way to see what Olli means when he says he does not like something.
