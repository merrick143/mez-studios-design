# START HERE: Mez Systems design system

Read this before anything else in this pack.

## What this is

This folder is the Mez Systems design system: the surfaces, type, colour, mark, product
treatments and page rules for the digital-products holdco inside Mez Studios. The goal is
simple. An LLM should be able to read this pack and build a full, on-brand Mez Systems
website with zero guesswork. This file is the constitution that points at the rest.

## Strategic audit and roadmap

Read `AUDIT-AND-END-TO-END-ROADMAP.md` when evaluating, repairing, or expanding this
system beyond its current website baseline. It captures the 2026-07-19 audit, the Taste
Reverse research workstream, human approval gates, the HTML/Figma operating model, and
the phased plan for product UI and every creative channel. It is a planning document and
does not override the current precedence or lock states until its tasks are implemented.

## Phase 0 programme control

Phase 0 is implemented under `governance/`, `baseline/2026-07-19/`, and `llm/`.
Read `governance/README.md` before changing, distributing, or migrating the system. The
decision register distinguishes current rules from proposed replacements, while the issue,
artifact, and consumer registers make conflicts and downstream state explicit. Proposed
decisions do not override the hard rules below until their named human gate is approved.

## Migration-first programme state

`DEC-MIGRATION-SEQUENCE-001` makes canonical cutover the primary programme goal. Read
`governance/MIGRATION-FIRST-GATE.md` and
`governance/tasks/TASK-MIGRATION-CUTOVER-01.json` before starting broad design work. The
standalone target is canonical-active under `CUTOVER-2026-07-21-01`. `0.1.0-alpha.1`, its schemas,
dated manifests, prepared clean-clone proof and activation proof pass through target commit
`6b1f0c4`. This pack is now a pinned archive, rollback source and consumer reference. Do not create
new Mez Systems rules here. Foundations, product expressions, the golden homepage and the
production Figma library continue in `merrick143/mez-studios-design/brand-kit`.

## Reference implementation

The prior handoff named `/home` in the ceos-notion-landingpage repository at commit `5a3b702`
as a pending reference build. The 2026-07-19 live baseline could not find that commit on a
branch or the claimed Mez integration paths in the current checkout. Treat `canvas/` as the
local reference fixture and the website as a migration candidate until each passes certification.
See `baseline/2026-07-19/observations.json` and `governance/consumer-register.json`.

## Precedence

When two files disagree, the higher authority wins. A newer date never overrides an approved
decision by itself.

The machine-readable authority contract is `governance/authority-model.json`.

1. `governance/decision-register.json`. Approved decisions, gates, and exceptions.
2. `products.json`, `colours.json`, `fonts.json`, and `gradients.json`. Canonical data.
3. `START-HERE.md` and numbered docs `00` to `19` in `brand-system/`. Canonical guidance.
4. `design-system-export/`. A portable mirror. It never creates an independent value or decision.
5. `canvas/` and certified consumer builds. Behavioural and visual proof against a named source version.
6. Figma (`HU0GVaDhatjWrKCiSg3wlU`). Human exploration and milestone mirror. The 2026-07-19 page listing
   exposed only the playground, but direct metadata confirmed the recorded `149:30` Mez Systems
   page and its numbered sections. Publication and variable binding are still unverified, so
   Figma cannot override the sources above. It remains a mirror until the Phase 5 library audit
   and release gate pass.
7. Product, marketing, and channel repositories. Consumers that may add local runtime behaviour,
   but never fork brand rules.

## Reading order for a website build

1. `START-HERE.md` (this file).
2. `products.json`. What you are selling and how each product is named and priced.
3. `design-system-export/tokens/tokens.css`. Pull every colour, radius, spacing, motion value from here.
4. `brand-system/11-layout-and-grid.md`. Grid, container widths, breakpoints, section rhythm.
5. `brand-system/07-ui-components.md` and `brand-system/12-states-and-forms.md`. Components, states, focus rings, forms.
6. `brand-system/16-motion.md`. One duration, one easing, hover only. States reference it.
7. `brand-system/13-sections.md`. The section catalogue.
8. `brand-system/14-page-archetypes.md`. How sections assemble into pages.
9. `brand-system/17-voice-and-copy.md`. The words that fill the slots: naming law, CTA semantics, char limits.
10. `brand-system/18-imagery-and-og.md`. Screenshots, the window frame, OG cards, favicons.
11. `brand-system/15-commerce.md`. Checkout, success and the delivery email, when building commerce.
12. `brand-system/19-review-checklist.md`. The self-review to run on the build before you present it.
13. Product docs as needed: `brand-system/05-product-system.md`, `brand-system/10-product-template.md`.

Docs `11` to `19` are complete and listed above. Run `19-review-checklist.md` against every
build before presenting it: the ten checks are the definition of done.

## The hard rules (law)

1. Monochrome system. Every surface and every piece of text is greyscale.
2. Gradient appears on product elements only (discs, cards, trading cards). Never on a page or section background.
3. Surfaces: page `#F8F8F8`, card `#FFFFFF`, recessed panel `#F6F5F4`, ink `#0D0D0D`. Never a pure-white page.
4. Geist owns display titles. Tuned Inter owns body, reading and UI. IBM Plex Mono is restricted to code, provenance and technical metadata. Production token migration remains pending.
5. Instrument Serif is contextual-only for genuine editorial work. It is never body or UI and is not a once-per-page quota.
6. The approved action-control radius is 12px. Broader surface geometry remains a migration backlog item; do not invent a new scale before that gate.
7. Spacing is the 4px scale: 4, 8, 12, 16, 24, 32, 48, 64. Nothing off-scale.
8. Product identity uses the approved Living Core expressions and exact static twins. Ambient glow and halo backgrounds remain retired.
9. Wings sit at 50% of the disc diameter, optically centred.
10. Trading-card wings are 32% of the card width, in a bottom-third lockup (glass eyebrow top-left, name and wings bottom-third).
11. The product name is "AI OS", with a space. Banned: "AIOS" and the retired codename "Atlas".
12. The site is light-only. No `prefers-color-scheme`, no dark mode. Dark is a section treatment, not a theme (`brand-system/12-states-and-forms.md`).
13. Australian English. No em dashes, no double hyphens.
14. Primary CTA is a dark ink pill. Never a bare text link.
15. States and focus rings follow `brand-system/12-states-and-forms.md`.
16. Structural interface motion remains restrained: no scroll reveal or parallax. `DEC-MOTION-002` permits slow continuous motion only inside an approved Living Core; Wings, labels, controls and layout remain static, and reduced motion uses the exact static twin.
17. Product screenshots stay in full colour inside the window frame (radius 14, 36px title bar, three mono dots). Never greyscale a screenshot; it is the one exception to the monochrome rule (`brand-system/18-imagery-and-og.md`).

## Creative latitude

Within the rules you have room. Compose layouts freely inside the page archetypes. Write
copy freely inside the voice rules. Reorder sections where `14-page-archetypes.md` marks the
order optional. Crop and frame imagery to suit. The system fixes the atoms, not every arrangement.

## Lock states

Decisions that are not yet signed off. Build with the working default, do not describe it as final. Product architecture and Living Core assignments are approved migration inputs through `DEC-PRODUCT-ARCHITECTURE-001`; the legacy registries remain frozen until the atomic migration snapshot is generated.

| Decision | State | Working default |
|----------|-------|-----------------|
| Nav links | OPEN | "Products · Pricing" with a dark ink pill CTA on the right. |
| Holdco mark | OPEN | The wings in near-black `#0D0D0D`; a final holdco lockup is not locked. |
| AI OS core | MIGRATION APPROVED | `MZ-G13`. |
| Context Engine core | MIGRATION APPROVED | `MZ-G12`. |
| AI Ads System core | MIGRATION APPROVED | `MZ-G06`. |
| Claude Code OS core | MIGRATION APPROVED | `MZ-G15`. |
| Organic Content OS core | MIGRATION APPROVED | `MZ-G20`. |
| Functional form colours | DEFAULT | Error `#B42318`, success `#15803D`. Functional only, never brand accents. |
| Section rhythm | DEFAULT | 72px vertical padding on mobile, 120px on desktop. |

Everything not listed here is locked. The five product assignments above become canonical together at cutover; they must not be partially promoted into the frozen legacy registries.
