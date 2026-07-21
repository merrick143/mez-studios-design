# AGENTS.md: building for Mez Systems

You are building UI for **Mez Systems**. Read `DESIGN_SYSTEM.md` in full before writing any styling. Use the tokens in `tokens/tokens.css` / `tokens/tailwind.tokens.cjs`; do not hardcode values that exist as tokens.

## Non-negotiables

1. **Surfaces are one V1 system (not five):** page `#F8F8F8` → recessed panel `#F6F5F4` → card `#FFFFFF` → dark UI / buttons / bundles `#0D0D0D`. Never pure white for the page.
2. **Text is `#0D0D0D`** (primary) / `#2E2E2E` (body). Muted via `--mz-text-muted`, never a lighter weight or a new grey.
3. **The only colour is the product gradient**, and it goes on **products only**, never a page/section background, the holdco, or a bundle container. No coloured text, no coloured UI.
4. **Radius** from the component scale `--mz-r-*`: chip 8 · tile 14 · card 20 · panel 28 · pill 999. **Spacing** from `--mz-s-*`: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64.
5. **Components:** primary CTA = dark `#0D0D0D` pill "Get the AI OS" (no price); product pill = white pill + gradient disc glyph + name; product card = white, radius 20, hairline, soft shadow, disc; trading card = full-bleed gradient nameplate (no paper, no sphere); bundle = dark `#0D0D0D` container (never a gradient). Sphere is reserved for identity boards, never a pill or card.
6. **Type is Inter.** H1 and H2 are **Bold 700**. H3 and buttons are **Semi Bold 600**. Use the tracking and leading in `typography.md`; never use Extra Bold or default Inter metrics.
7. **Serif (Instrument Serif) is a garnish**: one accent phrase, never body/UI. **Mono (IBM Plex Mono)** for code and technical labels only.
8. **One gradient per product** (from `gradients.json`), always through a treatment (disc / gradient-M / trading / sphere). Product cards use the **disc**. Glow is retired. If a design shows a halo behind a core, it is stale; build the flat disc.
9. **Radius encodes tier** (brand-tier, a separate namespace from the component scale): product = pill, holdco = medium, parent = nearly square.
10. **The CTA label never carries a price** ("Get the AI OS"). Ads default price-free. Pricing and checkout surfaces always show the price: $99 one-time (per-surface judgement, see `docs/09-governance.md`).
11. **Australian English. No em dashes** in copy.
12. **Light-only.** No `prefers-color-scheme`, no dark mode, no theme toggle. Dark is a section treatment, not a theme (`docs/12-states-and-forms.md`).
13. **Sentence case everywhere**, including headings and buttons ("Get the AI OS", not "Get The AI OS") (`docs/17-voice-and-copy.md`).
14. **Functional colour only in forms and feedback.** `--mz-error` `#B42318` and `--mz-success` `#15803D` are the sole colour exception besides the product gradient, never a heading, background or brand accent (`docs/12-states-and-forms.md`).
15. **Product screenshots stay in full colour** inside the doc-18 window frame (radius 14, 36px `#F6F5F4` title bar, three mono dots, on white or recessed, never dark). Never greyscale a screenshot; it is the one exception to the monochrome rule (`docs/18-imagery-and-og.md`).
16. **Motion is one duration, one easing, hover only, with one named exception:** 200ms on `cubic-bezier(.2,.7,.2,1)` (`--mz-duration` / `--mz-ease`). No scroll-reveal, no parallax and no moving gradient fills. A product core may move continuously only when rendered by `mz-core.js` as the living-core treatment under `docs/20-living-core.md`. Reduced motion and renderer failure must use its static WebP twin.
17. **Run the checklist before you present.** `docs/19-review-checklist.md` is the definition of done: ten baseline checks plus four living-core checks when that treatment is present. Clear every fail, then present. A build that fails a check is off-system.

## When unsure

Stop before inventing brand intent. Follow the included tokens, `DESIGN_SYSTEM.md`, and the
release manifest. Figma is a milestone mirror, so it may help explain an approved composition
but never overrides the included contracts. If a component is undefined, compose it only from
existing primitives and flag the gap with the affected rule and consumer.
