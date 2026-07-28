# Mez Systems design system audit and end-to-end roadmap

> Canonical transfer note · 21 July 2026
>
> This is the complete original audit and detailed end-to-end programme. Its analysis, quality bar, human/LLM model, channel scope, and task detail remain required. Repository timing and live status are now governed by `CURRENT-STATE.md` and `ROADMAP.md`. Paths that refer to the previous Mezcorp pack are historical unless an active document explicitly promotes them.

> Live reconciliation · 28 July 2026
>
> The standalone execution roadmap has completed foundations, the bounded expression suite, Global Navigation, Golden Homepage `1.0.0`, the non-authoritative production release boundary and the separate CMP-05/CMP-06 promotion gates. The next live task is `TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY`; use the active roadmap's Phase 4 portability sequence rather than the historical `NEXT-001` backlog below.

> Status: strategic execution plan
>
> Written: 2026-07-19
>
> Owner and final creative approver: Olli
>
> Intended operators: humans, Codex, Claude, and other LLM agents
>
> Scope: brand strategy, identity, tokens, web, product UI, ads, social, email, presentations, documents, data visualisation, motion, governance, packaging, and team adoption

## How to use this document

This document captures the complete July 2026 audit and turns it into a durable implementation programme. A fresh human or LLM should be able to use it to understand what exists, what is wrong, what must be preserved, what has to be built, which decisions require Olli, and how to verify that each phase is genuinely complete.

This is a roadmap, not a new source of brand truth. Until an item is implemented and approved through the governance process, the current precedence in `START-HERE.md` still applies. Where this roadmap identifies a contradiction, treat that contradiction as an open defect, not permission to choose whichever value is convenient.

This roadmap supersedes `docs/superpowers/plans/2026-07-17-mez-systems-brand-system-remediation.md` for strategic sequencing. The older plan remains useful implementation history for the original website remediation. Many of its tasks have already been completed, and its scope stops at the website layer.

### Contents

- [Executive summary](#executive-summary)
- [What is genuinely good](#what-is-genuinely-good)
- [Detailed audit findings](#detailed-audit-findings)
- [Channel coverage audit](#channel-coverage-audit)
- [What to keep, change, and retire](#what-to-keep-change-and-retire)
- [Target operating model](#target-operating-model)
- [Human and LLM collaboration model](#human-and-llm-collaboration-model)
- [Taste Reverse and inspiration workstream](#taste-reverse-and-inspiration-workstream)
- [End-to-end programme roadmap](#end-to-end-programme-roadmap)
- [Artifact and authoring matrix](#artifact-and-authoring-matrix)
- [Immediate execution sequence](#immediate-execution-sequence)
- [Fresh-session handoff protocol](#fresh-session-and-different-llm-handoff-protocol)
- [Programme stop gates](#programme-stop-gates)
- [Definition of done](#definition-of-done-for-the-end-to-end-system)
- [Decisions still requiring Olli](#decisions-still-requiring-olli)

### Required reading for a fresh session

1. Read `../START-HERE.md`, `CURRENT-STATE.md`, and `ROADMAP.md` first.
2. Read this document completely when planning or executing a programme phase.
3. Read `../governance/decisions.json`, the relevant registries, and the relevant research evidence.
4. Open the canonical local workbench and inspect the current rendered state.
5. Check the current git state before changing files. Existing unrelated changes belong to the user.
6. Locate the current phase and task status. Do not skip a stop gate.
7. Verify current files and outputs instead of assuming this dated audit is still current.

### Core programme rule

Keep a small number of unmistakable Mez signatures, then give creators a rich, testable grammar for variation. Do not lock every arrangement. Do not leave entire channels undefined.

### Migration-first reconciliation · 21 July 2026

`DEC-MIGRATION-SEQUENCE-001` supersedes this document's original repository timing, not its design outcomes. The programme does **not** need to complete original Phases 2 through 5 or begin Phases 6 through 11 before moving canonical authority. It must preserve completed Phase 2 evidence, close the Phase 3 product roster and gradient-assignment kernel, implement only the Phase 4 authority, schema, release and rollback minimum, then cut over. Foundations, product expressions, the golden homepage, consumer proof, Figma and channel systems continue in the new canonical repository as explicit backlog.

Read `CURRENT-STATE.md` and `ROADMAP.md` before using the older phase sequence for repository decisions. The original gate is preserved under `../history/mezcorp-2026-07-21/governance/MIGRATION-FIRST-GATE.md`.

## Executive summary

### Blunt verdict

The current Mez Systems pack is a strong V1 marketing-website kit. It is not yet an end-to-end design system.

At a trillion-dollar-software standard, it is a promising pre-1.0 foundation: visually disciplined, but too generic, too dependent on gradient objects, operationally contradictory, and missing most non-web channels. It can make outputs consistent. It cannot yet reliably make them exceptional.

The system is better at preventing a known set of mistakes than at helping a human or LLM produce distinctive, contextually excellent creative work.

### Current scorecard

| Dimension | Current score | Meaning |
|---|---:|---|
| Internal consistency | 8/10 | The visible Canvas follows a recognisable set of recurring treatments. |
| Marketing-web readiness | 6/10 | There is a useful V1 foundation, but it is rigid and contains quality failures. |
| Visual distinctiveness | 4/10 | The product cores carry most of the identity. The monochrome layer is generic. |
| Premium craft | 5/10 | Calm and credible, but predictable rather than authored. |
| Accessibility robustness | 5/10 | Some states and reduced-motion thinking exist, but measured failures remain. |
| Product-UI readiness | 2/10 | The system does not yet define how Mez software is designed. |
| Cross-channel readiness | 2/10 | Ads, social, decks, documents, data, and motion systems are mostly absent. |
| Governance and distribution | 3/10 | There is good intent, but manual duplication and conflicting authority create drift. |

### The central diagnosis

The system locks too many page arrangements while defining too little proprietary design language. That produces three predictable outcomes:

1. Pages become repetitive.
2. Products become gradient reskins.
3. Outputs can pass a compliance checklist while still feeling generic or mediocre.

The target is not maximum freedom. The target is controlled creative range: a few hard identity signatures, a larger grammar of approved transformations, and channel-specific rules that preserve the same identity without forcing every output into the same template.

### Priority map

| Priority | Work | Why it comes here |
|---|---|---|
| Critical now | Authority, canonical reference status, export completeness, review-gate repair, focus/forms, 320/375 reflow, core terminology | Current consumers and LLMs cannot use the baseline reliably |
| Before visual scaling | Taste research, strategy, identity territory, holdco/mark decisions, proprietary monochrome grammar, product differentiation | Scaling first would multiply a generic or unresolved identity |
| System engine | Schemas, token generation, asset registry, packages, CI, local design lab | Converts approved decisions into deterministic outputs |
| Experience system | Marketing patterns, real product UI, real proof, data, accessibility, Figma companion | Proves the brand in real responsive and interactive contexts |
| Channel expansion | Ads/social, presentations, documents, email, motion, OG/icons, later print/events | Makes the identity genuinely end-to-end |
| LLM and team scale | Task routing, golden examples, validators, receipts, versioning, consumer pilots | Enables safe reuse without hidden context or manual copying |
| Ongoing | Releases, deprecations, exceptions, drift audits, Taste Reverse refreshes | Prevents the system from decaying after launch |

## What is genuinely good

The current work should be evolved, not discarded.

- "One chassis, many cores" is a strong portfolio concept.
- Wings, product cores, discs, and trading-card decks form a recognisable family.
- The monochrome chassis is restrained, legible, and comparatively easy to govern.
- The product roster and gradient assignments are unusually explicit.
- Numeric rules around spacing, type, motion, radius, and responsive behaviour are more useful than a vague brand book.
- The runnable Canvas is an excellent review concept.
- Checkout and transactional email feel practical and credible.
- Sentence case, calm language, and the anti-hype position fit the company.
- Lock states, changelogs, checks, and the change loop show good governance intent.
- Reduced motion, focus treatment, and responsive checks are considered, even though the implementation needs correction.
- Commerce and screenshot guidance address real production needs instead of stopping at decorative identity boards.
- The pack already attempts to serve both humans and machines. The architecture needs to be made truthful and deterministic, but the intent is correct.

The strongest strategic asset is not a font, button, or gradient. It is the idea that Mez owns the chassis while each product owns a core.

## Detailed audit findings

### P0: structural blockers

#### DS-001: conflicting sources of truth

The handoff says the local pack is the only truth and Figma is a milestone mirror. The brand-system README calls Figma the visual source of truth. The portable agent instructions tell agents to match Figma when unsure, even though `START-HERE.md` places Figma last in precedence.

Impact: two capable LLMs can read different entry points and make different decisions. Every downstream output is vulnerable to drift.

Required correction: one canonical, machine-readable source owns values and decision status. All other formats, including Figma variables and documentation tables, are generated or explicitly mirrored from it.

#### DS-002: the canonical reference is not canonical

`/home` is described as the pattern-matching reference while pending approval. The handoff records known violations in that same build. In the current consumer checkout, the named commit exists but is not contained by any current branch, and the asserted design-system files are absent from the current checkout.

Impact: the final visual verifier is both operationally unreliable and knowingly off-system.

Required correction: label it `candidate` until it is reachable, remediated, tested, and approved. Only then may it become `certified`.

#### DS-003: the portable export is not portable

The export claims to be self-contained but omits production core assets, screenshots, OG files, favicons, app icons, wordmark lockups, type files and licensing information, email assets, production components, channel templates, and several documents referenced by its own agent instructions.

Impact: an LLM or team still needs the original repository and Figma access. Missing inputs encourage invention and fallback use.

Required correction: publish a complete, versioned distribution package with an asset manifest, checksums, documentation, examples, validators, and no links that escape the package.

#### DS-004: token formats are manually maintained and already differ

CSS, JSON, and Tailwind are described as identical mirrors, but their font stacks, gradient fallbacks, borders, ratios, aliases, and namespaces differ. Canvas also contains hardcoded values that the written rules say must be tokens.

Impact: the result depends on which implementation format a consumer uses.

Required correction: replace manual mirrors with one schema and generated outputs. Generated files must carry a header that says they are not hand-edited.

#### DS-005: the core concept contradicts customer copy

The product data defines a unique core for each product. Customer-facing copy says "One core, four products" and implies products share AI OS's core.

Impact: the strongest portfolio idea becomes semantically incoherent.

Required correction: reserve `core` for a product's owned gradient. Use "One chassis, four cores" or "One system, four products" for the suite. Use "the same product core across every surface" for cross-channel consistency.

#### DS-006: foundational identity decisions remain open

The final holdco mark, nav information architecture, and three of four product cores remain open or candidate. Mez Studios and Mez Systems often use the same wings and monochrome identity. Radius is supposed to communicate hierarchy, but that distinction disappears when the mark is free-floating.

Impact: teams can scale an identity that has not been fully distinguished or approved.

Required correction: finalise master lockups, endorsement rules, and portfolio identifiers before mass-generating channel assets.

#### DS-007: distribution is structurally prone to drift

A change must currently be repeated across docs, three token formats, Canvas, the website copy, and Figma. The handoff already records a critical missed sync.

Impact: human care cannot make this reliable at scale.

Required correction: build generation, packaging, link checking, asset validation, visual regression, release versioning, and automated consumer update checks.

### P1: identity and design weaknesses

#### DS-008: the identity disappears when gradients disappear

Without product cores, the remaining language is Inter, Instrument Serif, off-white pages, rounded white cards, black pill buttons, large whitespace, and soft shadows. These are common contemporary AI and SaaS conventions. The typography guidance explicitly describes the heading treatment as Notion-tuned, which signals reference dependence rather than ownership.

Required correction: define a proprietary monochrome composition grammar derived from the wings and chassis. Candidate primitives include paired panes, apertures, split fields, rails, notches, cropped wing geometry, technical plates, modular slots, and recurring alignment behaviour.

#### DS-009: consistency has become repetition

Home repeats structurally identical cards and familiar bands. Product pages repeat the same alternating text and browser-frame row. Fixed section rhythm creates long, predictable pages, especially on mobile.

Required correction: define controlled composition families such as editorial narrative, product mosaic, sticky proof, workflow sequence, architecture diagram, metrics, comparison, immersive demo, and testimonial proof.

#### DS-010: product differentiation is too shallow

A product currently owns only gradient, name, copy, and screens. Aurora, Prism, Forge, and AI OS have different jobs but no distinct graphic behaviour, diagram language, data style, motion personality, content density, or campaign territory.

Required correction: give each product a bounded expressive territory within the shared chassis. Product territories must be visibly related but not interchangeable.

#### DS-011: there is no convincing software visual language

The current product examples use generic window frames and placeholder screenshots. The documented component set does not cover application shells, navigation, tables, filters, search, charts, dashboards, loading, empty, error, offline, overlays, menus, toasts, permissions, onboarding, formatting, or density.

Required correction: build a real product-UI foundation and use real product evidence in marketing outputs.

#### DS-012: the expressive vocabulary is too narrow

The current vocabulary is primarily wings, a gradient disc, trading cards, monochrome panels, product screenshots, and one serif phrase. There is no complete iconography, illustration, diagram, pattern, texture, data-visualisation, editorial, or motion language.

Required correction: add expressive systems by role, not decoration. Every new vocabulary must state what it communicates, when it is allowed, and when it is noise.

#### DS-013: the signature devices lack clear semantics

The trading-card deck is distinctive but risks reading as gaming or collectibles when used repeatedly without product meaning. The "flat disc" uses mesh lighting and multiple shadows, so it reads as a glossy orb.

Required correction: decide whether the disc is truly flat or intentionally dimensional. Define what trading cards mean, when stacks communicate product architecture, and when the treatment is merely decorative and should be omitted.

#### DS-014: typography is too narrow and formulaic

The type system is effectively H1, H2, H3, body, button, caption, and eyebrow. "One serif use per page" is a quota rather than an art-direction principle. The rule that headings are never Semi Bold contradicts the H3 token at 600.

Required correction: build a role-based type system for marketing, product UI, editorial, data, decks, documents, email, and compact labels. Define behaviour, not just sizes.

#### DS-015: motion is a web micro-interaction rule, not a motion identity

Current motion is mostly hover lift, accordion, and mobile sheet behaviour. The prohibition on most expressive motion may suit a website baseline but cannot govern launch film, social video, product demonstrations, transitions, or motion graphics.

Required correction: separate functional UI motion, expressive brand motion, product demonstration, and film/social motion. Each layer needs principles, durations, easing families, choreography, and reduced-motion behaviour.

#### DS-016: voice is a website copy filter, not a messaging system

The copy guide has useful bans and slot limits, but it lacks audience definitions, positioning, competitive frame, promise, proof hierarchy, product message architecture, claim substantiation, and tones for sales, support, legal, error, success, founder, social, and lifecycle contexts. Five allowed CTA verbs cannot support every legitimate action.

Required correction: create a full messaging system, then allow channel-specific calls to action with clear semantic rules.

#### DS-017: fixed archetypes suppress excellent work

The constitution promises creative latitude while page documents prescribe fixed section counts and orders and describe new products as reskins.

Required correction: lock invariants and outcomes, then provide multiple approved composition modes. A page should be allowed to change order when its narrative and evidence demand it.

### P1: concrete quality and accessibility failures

#### DS-018: focus and form contrast failures

- The light focus ring measures approximately 2.29:1 against the light background.
- Placeholder text measures approximately 2.58:1 on white.
- The input border measures approximately 1.3:1 and is often the only visible field boundary.

Required correction: replace the canonical values, test them on every allowed surface, and add automated contrast assertions.

#### DS-019: responsive reflow failures

- Home overflows by approximately 27px at a 320px viewport and pushes the hamburger off-screen.
- The component reference grows to approximately 414px at a 375px viewport because of the fixed trading-card fan.
- The current review gate checks only 375px and therefore misses a common small-mobile failure.

Required correction: test at 320, 360, 375, 390, 768, 920, 1280, and 1440, plus content-driven stress cases. Fixed stack offsets should become proportional or container-aware.

#### DS-020: mobile interaction targets are weak

Standard buttons render around 40px high and the mobile menu trigger around 32px. The navigation script toggles `aria-expanded` but lacks a complete keyboard and state contract.

Required correction: use robust target sizes, `aria-controls`, Escape closing, focus movement/return, explicit open/close state, and keyboard tests.

#### DS-021: white lockups are unsafe on core imagery

White product names and wings are placed directly over arbitrary gradient areas with only a drop shadow. Sampling the shipped assets found that large portions of several lockup regions cannot support white text at 4.5:1. Forge's sampled lockup region failed throughout for white text.

Required correction: define validated crop anchors, contrast-safe placement zones, and controlled scrim or nameplate treatments. Do not rely on drop shadow as a contrast strategy.

#### DS-022: gradient fallbacks can change the product identity

Canvas uses WebP masters while the export exposes hand-built CSS gradients. Forge's fallback is gold and brown while its master asset is teal, green, and yellow. Fallbacks are not consistently wired below image URLs.

Required correction: ship the masters, generate verified fallbacks from them, and add screenshot tests for missing-asset mode.

#### DS-023: production assets do not meet their own specification

The four Canvas core assets are 1000 by 1000 while the gradient catalogue calls for roughly 1200 to 1600px exports. The wider library claims 53 stable IDs but only G01 to G20 are catalogued with hashes. G21 to G53 remain incomplete.

Required correction: complete the asset catalogue, export approved resolutions, add checksums, and prevent uncatalogued assets from being used in production.

### P1: governance and validation failures

#### DS-024: the locked checklist rejects approved work

- It rejects every `blur(` while approved navigation and glass treatments use backdrop blur.
- It rejects `subscription` and `monthly` while approved objection-handling copy says "No subscription" and "no monthly fee".
- It rejects values that documented bespoke components require.
- It mandates OG and favicon assets that are absent.
- It only checks 375px while reference surfaces fail at 320px and the component board fails at 375px.

Required correction: replace broad grep rules with scoped scripts and component-aware exceptions. A validator must pass the official fixtures before it can be locked.

#### DS-025: CTA rules contradict planned-product pages

The allowed CTA verbs and 14-character primary limit reject "Join the waitlist", while the planned-product archetype mandates that exact CTA.

Required correction: make CTA rules semantic and channel-aware. Test every approved default against its governing validator.

#### DS-026: machine readability is overstated

Only documents 11 to 19 contain machine-readable JSON blocks. Documents 00 to 10 do not. The token JSON mixes objects, strings, numbers, notes, and implementation specs without a schema, `$type`, aliases, or machine-readable governance states.

Required correction: create formal schemas, decision IDs, versions, scopes, types, aliases, and validators. Prose-embedded JSON should be generated from the same source as the main data files.

#### DS-027: manifest and Figma references drift

Some manifests exclude document 19 even though it is described as locked. Figma links and node IDs disagree between exported docs and the manifest. OG guidance gives conflicting home and non-product compositions.

Required correction: validate all internal links, node references, manifest membership, and cross-document assertions in CI.

#### DS-028: the checklist measures compliance, not excellence

The current gate does not meaningfully assess hierarchy, composition, pacing, density, distinctiveness, narrative, product truth, conversion clarity, emotional impact, or craft. A mediocre template can pass.

Required correction: operate two gates. Gate A is deterministic compliance. Gate B is a scored design-excellence review with blocking failures and observable criteria.

### Audit evidence map

Line numbers are the observed 2026-07-19 state and may move as files change. Re-run the audit before treating them as current.

| Finding | Primary evidence in the current pack |
|---|---|
| DS-001 | `HANDOFF.md:22`, `brand-system/README.md:3`, `design-system-export/AGENTS.md:25`, `START-HERE.md:17` disagree on pack/Figma authority |
| DS-002 | `START-HERE.md:14`, `HANDOFF.md:87`, and `brand-system/19-review-checklist.md:17` call the same pending, known-failing `/home` build a pattern reference |
| DS-003 | `design-system-export/README.md:1,7,31` claims self-containment while listing only wings and requiring Figma exports; `AGENTS.md:16` references files outside the export |
| DS-004 | `tokens.css`, `tokens.json`, `tailwind.tokens.cjs`, and literal values throughout `canvas/canvas.css` differ despite `HANDOFF.md:45` claiming identical mirrors |
| DS-005 | `products.json:10`, `brand-system/02-gradients.md:3`, `canvas/pages/home.html:6,95,286`, and `canvas/pages/product-aurora.html:181` use incompatible meanings of core |
| DS-006 | `START-HERE.md:73`, `brand-system/00-brand-architecture.md:16`, and `brand-system/04-the-mark.md:5` show open identity decisions and weak parent/holdco distinction |
| DS-007 | `HANDOFF.md:80,94` documents manual propagation and a previous critical missed sync |
| DS-008 | `brand-system/03-typography.md:3` describes the Inter treatment as Notion-tuned; Canvas pages show the identity dependence on the product objects |
| DS-009 | `brand-system/14-page-archetypes.md:27,52,269` and the rendered home/Aurora pages show fixed repeated page structures |
| DS-010 | `brand-system/10-product-template.md:7,42` limits product ownership to gradient, name, copy, and screens and calls a new product a reskin |
| DS-011 | `brand-system/07-ui-components.md:23`, `brand-system/12-states-and-forms.md:7`, and `canvas/pages/product-aurora.html:63` show the small component set and placeholder product evidence |
| DS-012 | `brand-system/18-imagery-and-og.md:76` removes major imagery routes while no complete icon, illustration, diagram, pattern, or data language replaces them |
| DS-013 | `brand-system/05-product-system.md:21`, `brand-system/06-trading-cards-and-stacks.md:9`, and shadows in `canvas/canvas.css` reveal the flat-disc/material contradiction and fixed stack geometry |
| DS-014 | `START-HERE.md:52`, `fonts.json:11`, `tokens.css:42`, and `brand-system/03-typography.md:23` conflict on Semi Bold H3 usage |
| DS-015 | `brand-system/16-motion.md:5,17,38` covers a narrow set of web interactions and prohibits most expressive motion |
| DS-016 | `brand-system/17-voice-and-copy.md:3,45,88` explicitly governs site words, five CTA verbs, and web slot limits rather than a complete messaging system |
| DS-017 | `START-HERE.md:67` promises latitude while `brand-system/14-page-archetypes.md:5,27,52,269` locks order and discourages invention |
| DS-018 | `tokens.css:24` and `canvas/canvas.css:164,171` produce measured focus 2.29:1, input boundary about 1.3:1, and placeholder about 2.58:1 |
| DS-019 | Live Canvas measured home `scrollWidth=347` at a 320px viewport and components `scrollWidth=414` at 375px; fixed fan geometry is in `canvas/canvas.css:403` |
| DS-020 | Button/nav dimensions and `canvas/canvas.js` show small targets and incomplete navigation state/focus behaviour |
| DS-021 | White lockups in `canvas/canvas.css:380` sit directly on core assets; sampled lockup regions fail required contrast across substantial portions of G06, G15, and G20 |
| DS-022 | `tokens.css:87` defines a gold/brown Forge fallback while `canvas/assets/mz-g15.webp` is teal/green/yellow |
| DS-023 | `gradients.json:13,25,47` requires larger assets and exposes only 20 catalogued hashes out of 53 IDs; Canvas masters are 1000 by 1000 |
| DS-024 | `brand-system/19-review-checklist.md:32,38,50,56` rejects sanctioned blur and approved subscription-objection copy in `canvas/canvas.css` and `canvas/sections.html` |
| DS-025 | `brand-system/17-voice-and-copy.md:47,65,96` rejects `Join the waitlist`, while `brand-system/14-page-archetypes.md:90` and Aurora specimens mandate it |
| DS-026 | `HANDOFF.md:39` claims every document ends in machine-readable JSON, while only documents 11 to 19 do; `tokens.json` has no single typed schema |
| DS-027 | `manifest.json`, exported Figma references, `START-HERE.md`, and `brand-system/18-imagery-and-og.md` contain document-range, node, and OG-composition drift |
| DS-028 | `brand-system/19-review-checklist.md:27` tests a narrow compliance set without a design-quality rubric |

## Channel coverage audit

| Channel | Current state | Required end state |
|---|---|---|
| Marketing website | Useful V1 foundation, too rigid | Multiple narrative modes, real proof, accessible components, certified reference pages |
| Product application UI | Essentially absent | Foundations, app shell, navigation, data, forms, feedback, overlays, workflows, states, density |
| Paid advertising | Absent | Campaign system, ratios, safe zones, proof/offer variants, motion variants, testing grammar |
| Organic social | Absent | Platform templates, series systems, carousels, statics, video covers, accessibility |
| Lifecycle email | One transactional specimen | Welcome, activation, education, launch, conversion, receipt, support, retention, win-back |
| Presentations | Absent | Master layouts, narrative structures, charts, diagrams, product proof, speaker notes |
| Documents and reports | Absent | Proposals, reports, briefs, PDFs, long-form type, tables, accessibility, exports |
| Data visualisation | Absent | Semantic palette, charts, annotation, uncertainty, dense/compact modes, accessibility |
| Editorial and research | Absent | Article templates, pull quotes, citations, figures, long-form rhythm, downloadable reports |
| Motion and video | Web micro-motion only | Functional motion, brand motion, demonstrations, social/video grammar, reduced-motion variants |
| OG, icons, app marks | Written spec, assets missing | Complete generated asset matrix with validation |
| Print and events | Absent | A later governed kit if business demand justifies it |
| Messaging | Website copy filter | Strategy, audiences, promise, proof, product messages, channel tones, claims rules |
| Localization and RTL | Absent | Expansion budgets, bidirectional layouts, font coverage, translated-output QA |

## What to keep, change, and retire

### Keep and strengthen

- One chassis, many cores.
- Wings, cores, discs, and the card/deck family.
- The restrained monochrome foundation.
- Product roster and explicit decision states.
- Local no-build Canvas as a universal review surface.
- Plain, calm language and anti-hype discipline.
- Change records, review gates, and the intent to support machines.
- Real product screenshots as evidence.

### Change materially

- Monochrome composition language.
- Product differentiation.
- Typography roles and behaviour.
- Page composition system.
- Product-UI coverage.
- Motion, messaging, data, and channel systems.
- Token architecture and distribution.
- Accessibility and responsive testing.
- Human review format.

### Retire or replace

- Conflicting Figma authority instructions.
- Hand-maintained token mirrors.
- Broad grep-based review rules.
- "One core, four products" language.
- Fixed page-order rules presented as universal law.
- "One serif use per page" as a quota.
- Unverified gradient fallbacks.
- Placeholder product proof.
- A canonical reference that is pending or knowingly failing.

## Target operating model

### One source, many renderers

The canonical system remains inside the Mez Systems pack until the migration-first cutover gate passes:

`departments/cmo/brand-library/brands/mez-systems/`

The recoverable target now exists at `merrick143/mez-studios-design`, branch `codex/brand-kit-workbench`. It remains non-canonical until the identity-kernel and minimum-engine gate in `governance/MIGRATION-FIRST-GATE.md` passes. Taste Reverse remains a separate research tool. Product and marketing repositories remain consumers. Figma remains a human exploration and milestone-mirror surface.

After that gate, transfer canonical ownership before building the remaining foundations and experience system. Do not maintain both locations as writable peers: freeze this pack at a named commit and convert it to a pinned archive or generated consumer reference.

### Recommended surface responsibilities

| Surface | Role | Canonical? | Editing rule |
|---|---|---:|---|
| Local pack | Decisions, schemas, tokens, source assets, docs, recipes, validators | Yes | Edit source here first |
| HTML Canvas | Responsive and interactive reference fixtures | Derived reference | Edit through source tokens/components, then certify |
| Production component package | Reusable coded components and patterns | Derived implementation | Generated or built against the canonical contracts |
| Figma | Vector exploration, art direction, human review, milestone library | No | Explore freely in drafts; mirror only approved decisions into the library |
| Taste Reverse | Evidence-backed external design research | No | Produces research inputs, never Mez truth |
| Website/product repos | Consumer applications | No | Pin a released system version; do not fork hidden values |
| LLM pack | Small task-routed machine context | Generated | Never hand-edit |
| Channel templates | Ads, social, email, slides, docs, video | Derived products | Pin version and declare approved exceptions |

### HTML first or Figma first

There is no single correct answer for every design task. Use two coordinated lanes.

#### Lane A: system and behaviour work

Use code and HTML first for:

- Tokens and themes.
- Responsive layout.
- Components and states.
- Accessibility and keyboard behaviour.
- Product UI.
- Email rendering.
- Data visualisation.
- Motion implementation.
- Any decision whose quality changes across viewport, content, or interaction state.

Sequence:

1. Define the decision and acceptance criteria in the canonical pack.
2. Implement multiple coded specimens in the local Canvas.
3. Render stress cases and compare them side by side.
4. Ask Olli to choose or redirect at a bounded review gate.
5. Lock the selected rule and generate downstream formats.
6. Mirror the approved result into the Figma library when the milestone is stable.

#### Lane B: identity and art-direction work

Use Figma or another visual exploration surface first for:

- Master mark and lockups.
- Proprietary geometry.
- Static composition concepts.
- Iconography and illustration.
- Campaign art direction.
- Motion storyboards.
- High-level visual territories where divergence matters more than implementation.

Sequence:

1. Start from a written design hypothesis and Taste Reverse evidence.
2. Produce three meaningfully different territories, not cosmetic variations.
3. Show each territory across several outputs, not on a single logo board.
4. Let Olli select, combine, or veto.
5. Codify the chosen territory into assets, tokens, recipes, and coded fixtures.
6. Validate originality, accessibility, responsiveness, and cross-channel transfer.
7. Promote approved Figma components into the milestone library.

#### The practical decision

The default Mez workflow should be local pack to coded Canvas to human approval to generated distributions to Figma mirror. Figma-first is an explicit exception for identity and art direction, not the default source-of-truth workflow.

### Why keep the no-build Canvas

The plain HTML/CSS/JS Canvas is valuable because every human and LLM can inspect it without installing a framework. Keep it as the universal reference fixture. Do not force it to become the production component library.

Build a separate production package beside it for framework components. The no-build Canvas proves the visual and behavioural contract. The production package proves reuse in real applications.

### Proposed pack structure

```text
mez-systems/
  README.md
  START-HERE.md
  AUDIT-AND-END-TO-END-ROADMAP.md
  CHANGELOG.md
  VERSION
  system.schema.json
  system.config.json

  strategy/
    audience.md
    positioning.md
    promise-and-proof.md
    messaging-architecture.md
    product-architecture.md

  governance/
    artifact-register.json
    consumer-register.json
    issue-register.json
    decision-register.json
    records/
    exceptions/
    deprecations/

  research/
    source-manifest.json
    taste-reverse/
    synthesis/
    anti-references/

  foundations/
    marks/
    typography/
    colour/
    gradients/
    composition/
    iconography/
    imagery/
    motion/
    data-visualisation/
    accessibility/

  tokens/
    source.tokens.json
    schemas/
    generated/

  grammar/
    signatures.md
    flexible-axes.md
    composition-modes.md
    product-territories.md
    quality-principles.md

  components/
    primitives/
    marketing/
    product-ui/
    patterns/
    fixtures/

  channels/
    web-marketing/
    product-ui/
    paid-social/
    organic-social/
    email/
    presentations/
    documents/
    editorial/
    data-visualisation/
    motion-video/
    og-icons/

  canvas/
    index.html
    foundations/
    components/
    pages/
    channels/
    adversarial/

  llm/
    TASK-ROUTER.md
    AGENTS.md
    manifest.json
    schemas/
    prompts/
    recipes/
    examples/
    evaluations/

  validators/
    schema/
    links/
    assets/
    contrast/
    accessibility/
    responsive/
    copy/
    visual-regression/

  dist/
    llm-pack/
    web-tokens/
    component-package/
    figma-import/
    email/
    slides/
    documents/
```

The exact folders may change during implementation. The boundaries should not: research is input, decisions are authority, source tokens generate formats, Canvas is a fixture, Figma is a mirror, and `dist` is disposable output.

## Human and LLM collaboration model

### Principle

Olli should provide taste, judgement, priority, and final approval. He should not have to audit every hex value, repeat decisions across files, or manually prove that a component is accessible.

LLMs should perform inventory, synthesis, implementation, measurement, stress testing, propagation, documentation, and evidence collection. They should not silently decide high-impact identity questions.

### What requires Olli

- The emotional and strategic ambition of the brand.
- Which references feel right and which feel wrong.
- Final holdco mark and endorsement architecture.
- Typography personality and proprietary monochrome territory.
- Product territory boundaries.
- Which compositions feel unmistakably Mez.
- Which golden outputs represent the quality bar.
- High-impact exceptions or changes to locked signatures.
- Final release approval at major milestones.

### What should not require Olli

- Copying approved values between formats.
- Finding contradictory documents.
- Measuring contrast, overflow, target size, or file resolution.
- Producing routine responsive variants.
- Checking links, schemas, assets, checksums, or package completeness.
- Writing migration notes and changelogs from approved decisions.
- Propagating a released version to consumer fixtures.
- Re-running approved validators.

### Bounded review packet

Every human gate should arrive as one compact packet:

1. Decision being made.
2. Why it matters now.
3. Three meaningfully different options at most.
4. The recommended option and rationale.
5. Each option shown on at least three representative outputs.
6. Risks and what becomes expensive to change later.
7. A clear response format: approve, choose, combine, veto, or comment.
8. A decision ID that can be recorded immediately.

Olli should never receive a folder of unexplained experiments and be asked, "What do you think?"

### Human gates

| Gate | Human decision | Suggested burden | Agent responsibility before review |
|---|---|---:|---|
| H0 | Brand ambition, desired feeling, anti-goals | 20 to 30 minutes | Prepare a one-page brief and contradictions to resolve |
| H1 | Reference and anti-reference shortlist | 20 minutes | Collect candidates, cluster traits, recommend a balanced set |
| H2 | Master identity territory | 30 to 45 minutes | Show three territories across web, ad, deck, product, and email |
| H3 | Typography and monochrome grammar | 20 to 30 minutes | Supply stress tests, not isolated type specimens |
| H4 | Product differentiation model | 30 minutes | Show all four products together and separately |
| H5 | Marketing and product reference outputs | 30 minutes | Present certified desktop/mobile/state comparisons |
| H6 | Channel family approval | 15 to 20 minutes per family | Show a small golden set and failure examples |
| H7 | Release approval | 15 minutes | Provide validator results, changes, migrations, and known exceptions |

These gates can be combined when the work is mature. Olli's total burden should be concentrated into high-leverage decisions rather than continuous supervision.

## Taste Reverse and inspiration workstream

### Role of Taste Reverse

Taste Reverse remains a separate research engine and evidence vault. It should never become the source of Mez identity truth.

Its current local repository is `/Users/olivermerrick/Documents/taste-reverse`. On 20 July 2026 its live project, package, CLI, and new outputs were normalised to Taste Reverse `0.2.0`, and a validated findings-export contract was added. The repository still has no committed baseline because its historical media boundary needs owner confirmation. Mez may use the provisional validated export for controlled research, but must not describe it as an immutable Git-pinned dependency.

Its real current pipeline is:

```text
CLI
  -> representative page discovery
  -> Playwright capture
  -> rendered DOM and style extraction
  -> deterministic clustering
  -> manual synthesis bundle
  -> report writer
  -> deterministic package validation
```

It is already useful for public-site screenshots, rendered measurements, evidence IDs, recurring value clusters, and structured research packages. Rich taste interpretation remains a manual human/LLM synthesis step. The OpenAI provider is not yet connected to the main pipeline, and the current collector does not deeply analyse ads, decks, PDFs, email, video, private product interfaces, hover systems, or complete motion behaviour.

The rich Prism and ElevenLabs packages are valuable examples of the desired output quality. They should not be treated as proof that every package is automatically produced to the same depth.

### Research principle

Do not ask, "Which brand should Mez look like?"

Ask:

1. Which design problem does Mez need to solve?
2. Which mechanisms solve that problem well?
3. What is the transferable principle?
4. What would an original Mez expression of that principle be?
5. Does the result still look like the source, or has it become recognisably Mez?

Every influence must pass through this abstraction ladder:

```text
Observed expression
  -> underlying problem and mechanism
  -> transferable principle
  -> original Mez hypothesis
  -> tested Mez artifact
  -> approved Mez decision
```

Never move directly from an observed expression to a copied token, layout, illustration, motion sequence, or component.

### Source cohorts

Use a deliberately mixed reference panel:

1. Direct competitors: identify table stakes, proof expectations, and category clichés.
2. Craft exemplars: study one narrow area of excellence such as typography, product evidence, motion, systems thinking, or data density.
3. Mature design systems: study governance, distribution, documentation, contribution, and multi-channel consistency.
4. Cross-category references: editorial, architecture, industrial design, fashion, media, gaming, culture, and other fields that can help Mez escape SaaS convergence.
5. Channel specialists: brands with exceptional ads, decks, reports, email, video, product UI, or data visualisation.
6. Anti-references: successful work that is intentionally wrong for Mez.

The original recommendation was 8 to 12 sources tied to the highest-priority questions. At H1 on 20 July 2026, Olli deliberately narrowed cycle one to Notion, Linear, Stripe, ElevenLabs, and Ramp, all at deep depth. Treat the missing standalone design-system, cross-category, and dedicated anti-reference coverage as an explicit limitation, not an invitation to add sources without approval.

### Research questions for the first cycle

- How can Mez remain recognisable without a gradient, logo, or product name?
- How can a quiet chassis support expressive product cores without becoming generic SaaS?
- How should four products feel related without becoming reskins?
- How do excellent software brands make product proof literal, credible, and legible?
- How should composition density change between marketing, application UI, ads, reports, and email?
- How can trading-card and deck behaviour communicate systems and products instead of gaming?
- What motion characteristics feel controlled, intelligent, and unmistakably Mez?
- How should a holdco, parent, and product family signal hierarchy at very small sizes?
- What makes an identity survive across web, paid social, decks, documents, and product UI?
- Which current AI/SaaS patterns should Mez explicitly reject?

### Taste Reverse ingestion boundary

Raw evidence remains in Taste Reverse. Mez ingests only a curated, sanitised, versioned findings export.

Proposed future contract:

```json
{
  "schemaVersion": 1,
  "findingId": "TR-FINDING-0001",
  "sourcePackage": "source-slug/run-id",
  "sourcePackageHash": "sha256",
  "surface": ["marketing-web"],
  "problem": "How product proof supports a claim",
  "observedExpression": "Measured or visible fact",
  "underlyingMechanism": "Why the expression appears to work",
  "transferablePrinciple": "Abstract principle",
  "confidence": 0.86,
  "epistemicStatus": "observed|strong-inference|tentative|unknown",
  "transferCategory": "adopt|adapt|avoid|unknown",
  "mezProblem": "The Mez-specific need",
  "proposedMezTranslation": "Original hypothesis",
  "sourceSignaturesToExclude": [],
  "originalityRisk": "low|medium|high",
  "decisionStatus": "unreviewed|approved|rejected|trial",
  "decisionReason": "",
  "humanApproval": {
    "reviewer": "",
    "date": "",
    "status": ""
  },
  "prototypeRefs": [],
  "validationResults": []
}
```

The distributed Mez pack must never include source screenshots, copied competitor tokens, competitor logos, competitor copy, or a raw Taste Reverse package. It may include approved Mez conclusions and internal decision IDs.

### Normalized measurement taxonomy

`observedExpression` prose is not sufficient for reliable comparison. Taste Reverse exports should retain normalized, evidence-linked measurements for:

- Colour and material: observed colour, role hypothesis, coverage, contrast context, gradients, opacity, blend, texture, and lighting.
- Typography: family, fallback, weight, style, size, line height, tracking, measure, case, role, and responsive changes.
- Shape: radius, border width/style/colour, clipping, aspect ratio, and recurring geometry.
- Spacing and grid: gaps, padding, margins, gutters, columns, container width, alignment, and section intervals.
- Depth: shadows, blur, overlays, layering, overlap, and elevation frequency.
- Composition: module type, focal count, symmetry/asymmetry, density, hierarchy, sequence, and responsive transformation.
- Components: role, anatomy, state, morphology, frequency, and contextual exceptions.
- Imagery and icons: type, crop, framing, prominence, literalness, annotation, stroke/fill behaviour, and asset role.
- Motion and interaction: trigger, property, duration, easing, sequence, state purpose, and reduced-motion behaviour.
- Content and voice: role, length, sentence structure, CTA intent, claim/proof relationship, and tone.
- Channel and viewport: surface type, dimensions, state, locale, and capture conditions.

Each measurement record should include `value`, `unit`, `normalizedValue`, `role`, `sourceEvidenceIds`, `viewport`, `selectorOrElementRole`, `frequency`, `exceptions`, `epistemicStatus`, and `confidence`. Exact source values remain research evidence and are never promoted directly into Mez tokens.

### Inspiration workstream tasks

#### TR-0: stabilise Taste Reverse before dependency

- [x] Choose one project/product name and update its manifests and docs.
- [ ] Create a first committed checkpoint and tag its current schema version.
- [x] Document which rich exemplar artifacts are manual additions.
- [x] Define a stable source-research export schema.
- [x] Add the normalized measurement taxonomy and provenance fields.
- [x] Add schema validation and package checksums.
- [x] Ensure an export can be consumed without relying on paths that exist only in one local run.

Exit gate: Mez can pin a Taste Reverse version and validate a findings export without importing the research repository.

#### TR-1: define the brief

- [x] Convert the audit into 6 to 10 explicit research questions.
- [x] Rank the three most important questions.
- [x] Separate competitive-convention research from inspiration research.
- [x] Define supported and unsupported channels for the first cycle.
- [x] Define capture dates, source rights, and evidence limitations.
- [x] Define success and stop criteria before choosing brands.

Outputs: `INSPIRATION-BRIEF.md`, `research-questions.yaml`.

Human gate: Olli approves priorities in 15 to 20 minutes.

#### TR-2: build the source panel

- [x] Select the H1 panel. Original 8 to 12-source recommendation amended by Olli to five deep sources.
- [x] Record why each source is present and which question it helps answer.
- [x] Add the exact public URLs and desired surface categories.
- [x] Record anti-reference rationale.
- [x] Check that no one brand dominates the panel.
- [x] Add manual evidence plans for non-web channels the tool cannot capture.

Outputs: `source-register.yaml`, `CAPTURE-PLAN.md`.

Human gate: Olli adds, removes, or flags favourites in one 20-minute review.

#### TR-3: collect and qualify evidence

- [x] Capture representative desktop, laptop, and mobile surfaces.
- [x] Capture safe states where supported.
- [x] Check page selection instead of accepting discovery blindly.
- [x] Record unavailable private product surfaces and motion uncertainty.
- [x] Add manual adapters for ads, emails, video, decks, PDFs, and product screenshots.
- [x] Emit normalized colour, typography, radius, spacing, grid, border, shadow, imagery, motion, density, component, and content records with evidence IDs.
- [x] Produce a dated immutable package and hash per source.
- [x] Label every finding observed, inferred, tentative, or unknown.

Stop gate: insufficient evidence can support a tentative experiment but cannot establish a Mez rule.

#### TR-4: synthesise across sources

- [x] Normalize findings to the common export contract.
- [x] Build a matrix of problem, observation, evidence, mechanism, transferable principle, exact expression to avoid, scope, confidence, and originality risk.
- [x] Cluster recurring mechanisms and contradictions.
- [x] Identify category clichés and underused opportunities.
- [x] Keep exact source values in the evidence layer. Recompute Mez values from Mez requirements.
- [x] Produce a pattern atlas and anti-pattern atlas.

Outputs: `COMPARATIVE-MATRIX.md`, `comparative-matrix.json`, `PATTERN-ATLAS.md`, `ANTI-PATTERN-ATLAS.md`, `taste-dimensions.json`.

#### TR-5: calibrate human taste

- [x] Preserve and invalidate the low-fidelity A/B pilot. It has no synthesis or production authority.
- [x] Keep all source screenshots and derivatives inside Taste Reverse.
- [x] Curate 35 high-quality reference plates across the five approved sources and five review lenses.
- [x] Build a lightweight review using love, useful, indifferent, reject, or not useful.
- [x] Capture up to three causal reason tags, an optional note, time viewed, and revisions.
- [x] Olli completes the 35-plate reference taste review and exports the record.
- [x] Synthesise positive signals, rejection signals, contradictions, and source-bias risks.
- [x] Use the findings to brief three original, high-fidelity Mez directions.
- [x] Build the complete cross-channel directions before testing isolated variables again.
- [ ] Olli reviews the complete cross-channel directions before any isolated-variable testing resumes.
- [ ] Run only four to six final controlled comparisons, with two production-worthy options, for unresolved questions.

Outputs: invalid-pilot record, source-level taste record, three direction briefs, later `preference-log.jsonl`, `HUMAN-TASTE-PROFILE.md`, uncertainty list.

Human gate: 35 lightweight reference reactions in 20 to 30 minutes. A later direction review replaces broad low-fidelity pair testing.

#### TR-6: establish the Mez homepage foundation

- [x] Preserve and invalidate the first three-route build and its review record. It has no preference or production authority.
- [x] Record the process, translation, execution, and review-instrument failures.
- [x] Reframe the work around the real Mez Systems product model and the approved Notion homepage.
- [x] Reopen colour, typography, radius, spacing, composition and components for research while keeping gradients locked.
- [x] Build four production-grade homepage foundation studies using the same approved copy.
- [x] Review each study full-size using module annotations, not a forced route verdict.
- [x] Synthesise retained, rejected and unresolved foundation behaviours from the review.
- [x] Build one coherent complete homepage from retained behaviours, then preserve it as invalid after all eight reviewed sections received `change`.
- [x] Record the authority reset: locked identity inputs, reopened generated system rules and rejected research patterns.
- [x] Build the six-truth and six-refusal visual evidence board in Taste Reverse.
- [x] Olli completes the visual truth review: all six truths locked and all six refusals approved for avoidance.
- [x] Build identity and product-object calibration 01, record the three-edit result, and build expression atlas 02.
- [x] Promote only the Living Core motion slice through `DEC-MOTION-002`; leave the remaining static expression morphology unapproved.
- [x] Build the hero and first-viewport calibration plate using only the approved copy, Wings and Living Core inputs.
- [x] Olli reviews the hero and first-viewport calibration plate. The composition is rejected. Typography advances to dedicated calibration only. Controls and mobile remain unresolved.
- [x] Build and approve typography system calibration 01. Use tuned Inter for primary UI and body, Geist for display, contextual-only Instrument Serif, restricted IBM Plex Mono, and revise mobile around the split.
- [x] Build and approve the button and control system across shape, surface, state, hierarchy and semantic use through `DEC-CONTROL-001`.
- [x] Judge remaining static product expressions in the product-family and commerce context rather than through an isolated nine-decision atlas. Approve static cores only for repeated family contexts.
- [x] Build and review the product-family and commerce calibration plate using aligned multi-product compositions. Approve behaviour through `DEC-FAMILY-001`; withhold approval from the plate's visual execution.
- [ ] Rebuild and approve a centred, mobile-first, multi-product hero after its dependencies pass. Hero First Viewport 02 is built; five-decision review open.
- [ ] Record the approved expression grammar and build one golden homepage.
- [ ] Extract approved behaviours into explicit system amendments and machine-readable tokens.
- [ ] Prove product shelves, one-time purchase, bundles, checkout and mixed availability states.
- [ ] Expand only the approved system to ad, email, deck/report, social, small identity, and motion.
- [ ] Run controlled comparisons only for remaining isolated variables, with two production-worthy options.

Stop gate: no direction advances if it can be described as "another brand with Mez gradients".

#### TR-7: originality review

- [ ] Keep source screenshots research-only.
- [ ] Check logo-free thumbnails and grayscale silhouettes.
- [ ] Compare component morphology and composition hierarchy.
- [ ] Check motion fingerprints where relevant.
- [ ] Reject copied source combinations even when individual values are common.
- [ ] Ask a blind reviewer which existing brand the route resembles.
- [ ] Escalate medium and high similarity risk to Olli and, where needed, legal review.

Outputs: `ORIGINALITY-RISK-REGISTER.yaml`, `SOURCE-SIGNATURE-BLACKLIST.yaml`, `ORIGINALITY-DECISION.md`.

#### TR-8: validate transfer and promote

- [ ] Build one new-context marketing page, dense product view, ad set, lifecycle email, and deck/report spread.
- [ ] Score problem-solving, Mez recognition, cross-channel coherence, originality, accessibility, and production quality.
- [ ] Approve a small golden set.
- [ ] Promote only approved hypotheses through a Mez decision record.
- [ ] Give promoted rules new Mez IDs, assets, and tokens.
- [ ] Remove external evidence from the team and LLM distribution packs.

Stop gate: research never edits production tokens directly.

## End-to-end programme roadmap

### Programme states

Use these task states consistently:

- `BACKLOG`: understood but not scheduled.
- `READY`: dependencies and inputs are available.
- `IN_PROGRESS`: active work has an owner.
- `HUMAN_REVIEW`: bounded decision packet is waiting for Olli.
- `BLOCKED`: the documented stop condition has been met and work cannot safely continue.
- `VALIDATING`: implementation is complete and independent verification is running.
- `DONE`: exit criteria are evidenced and the result is released or merged.
- `SUPERSEDED`: replaced by a later decision or task.

Each task must record owner, dependencies, affected files, deliverables, verification commands or procedures, human gate, and completion evidence.

### Phase map

| Phase | Primary outcome | Main deliverables | Human gate |
|---|---|---|---|
| 0 | Preserved baseline and programme control | Governance registers, baseline evidence, and minimum agent task/context/receipt contracts | H0 programme boundary |
| 1 | Safe current baseline | Authority repair, validator repair, accessibility/reflow fixes, complete export | Only repository/owner boundary if needed |
| 2 | Approved strategy and north star | Taste profile, research matrix, strategy, messaging, three directions | H1 references, H2 direction |
| 3 | Ownable identity | Marks, type, monochrome grammar, cores, product territories, motion/data language | H3 identity, H4 product family |
| 4 | Canonical engine scaffold | Schemas, stable IDs, generator/release infrastructure, asset registry, CI, repository decision | Repository extraction approval |
| 5 | Robust generated foundations | Channel-aware source tokens, accessibility contracts, generated adapters, baseline packages and clean-consumer release | Visible identity changes only |
| 6 | Executable design grammar | Canvas, components, marketing/product patterns, golden experiences | H5 experience goldens |
| 7 | Human design companion | Versioned Figma variables, components, templates, mappings | Divergence review only |
| 8 | End-to-end channel system | Native channel packs, templates, examples, validators | H6 channel goldens |
| 9 | Hardened LLM execution | Expand the Phase 0 contracts into routing, prompts, receipts, evaluators, and multi-model certification | New visual family only |
| 10 | Transfer and adoption | Packages, initializer, doctor, pilots, upgrade/rollback | Pilot exception decisions |
| 11 | Certified operating system | Release, governance, metrics, recurring audits | H7 major release |

### Phase 0: preserve the baseline and establish programme control

Goal: prevent the redesign from losing useful work or treating stale assumptions as truth.

Status: `DONE`. Implementation and H0 programme authority were approved on 19 July 2026.

#### P0.1: baseline inventory

- [x] Record the current git commit, branch, and dirty state of the pack repository.
- [x] Record the current state of the website consumer and any other known consumers.
- [x] Export dated screenshots of every Canvas page at supported widths.
- [x] Record the current Figma file key, relevant pages, publication status, and node maps.
- [x] Build an inventory of every document, data file, token file, asset, component, fixture, and channel specimen.
- [x] Hash important source assets and gradient masters.
- [x] Mark every item as source, mirror, generated output, consumer, candidate, deprecated, or archive.
- [x] Preserve the July 17 remediation plan as implementation history and mark this roadmap as its strategic successor.

Deliverables: baseline manifest, screenshot archive, `governance/artifact-register.json`, `governance/consumer-register.json`.

#### P0.2: defect and decision registers

- [x] Convert DS-001 to DS-028 into a machine-readable issue register.
- [x] Give every current open decision a stable decision ID.
- [x] Record status, owner, scope, rationale, introduced date, and affected artifacts.
- [x] Separate defects from taste choices.
- [x] Separate reversible defaults from expensive identity decisions.
- [x] Record which current `LOCKED` rules are deliberately reopened by this programme.

Deliverables: `governance/issue-register.json`, `governance/decision-register.json`, `governance/reopened-decisions.md`.

#### P0.3: programme charter

- [x] Confirm the supported first-release channels.
- [x] Assign the owner model and deadlines: Olli holds executive, interim design, and interim verbal ownership; dedicated system, engineering, and channel owners remain intentionally unassigned until the approved phase gates.
- [x] Define contribution, exception, and escalation paths.
- [x] Define what "end-to-end" means and what is explicitly deferred.
- [x] Define metrics and stop gates.
- [x] Confirm that Taste Reverse is upstream research, Figma is a review/mirror surface, and production repos are consumers.

#### P0.4: minimum LLM operating contract

Do not wait until Phase 9 to make the programme LLM-first. Create a minimal contract now and use it for every task in Phases 1 to 8.

- [x] Define the standard task record used later in this document.
- [x] Define a minimal context-bundle manifest with task, phase, required files, decisions, assets, and stop conditions.
- [x] Define a minimal output receipt with files changed, rules/decisions applied, tests, artifacts, human status, and exceptions.
- [x] Define the first compliance/evaluation result schema.
- [x] Require every programme task to emit a receipt.
- [x] Capture where an agent needed hidden context or made an avoidable assumption.
- [x] Feed those failures into the eventual task router and examples.

Deliverables: `llm/task.schema.json`, `llm/context-bundle.schema.json`, `llm/output-receipt.schema.json`, `llm/evaluation-result.schema.json`, and one completed example from Phase 0.

Human gate H0: approve programme boundary, brand ambition, owner model, and first-release channel scope.

Phase exit criteria:

- Every existing artifact has a role and migration disposition.
- No known consumer or source is invisible.
- The current pack can be restored or compared throughout the programme.
- The next phase has one named canonical working location.
- Every subsequent task can be handed to a fresh LLM with an explicit context bundle and produces a receipt.

### Phase 1: repair authority, portability, and critical quality failures

Goal: make the current baseline safe enough to evolve without multiplying contradictions.

Status: `DONE`. Authority, critical quality repairs, the complete portable release, and clean-consumer validation passed on 19 July 2026. The Canvas remains a candidate until the separate design-excellence and human certification requirements pass.

#### P1.1: resolve authority

- [x] Write one authority model covering declarative, behavioural, and visual truth.
- [x] Remove "match Figma when unsure" from all agent guidance.
- [x] Mark the current `/home` reference `candidate`, not canonical.
- [x] Define certification requirements for a reference artifact.
- [x] Reconcile `START-HERE.md`, `HANDOFF.md`, manifest, README, export guidance, and Figma map.
- [x] Add a validator that fails on conflicting authority statements.

#### P1.2: fix contradictions that prevent deterministic use

- [x] Replace "One core, four products" with approved chassis/core language.
- [x] Resolve Bold versus Semi Bold typography rules.
- [x] Resolve allowed CTA verbs and waitlist CTA contradictions.
- [x] Resolve OG composition contradictions.
- [x] Include document 19 everywhere the numbered set is enumerated.
- [x] Resolve incorrect Figma node references.
- [x] Scope blur rules to product glow rather than legitimate backdrop blur.
- [x] Replace banned-word grep with context-aware copy assertions.
- [x] Document sanctioned component exceptions instead of pretending none exist.

#### P1.3: correct immediate accessibility and responsive failures

- [x] Replace the focus-ring value and verify at least 3:1 on every allowed adjacent surface.
- [x] Replace placeholder and field-boundary values with accessible tokens.
- [x] Fix the 320px navigation and hero overflow.
- [x] Fix the 375px component-board trading-card overflow.
- [x] Increase mobile target sizes where needed.
- [x] Complete keyboard behaviour for navigation and accordions.
- [x] Test 320, 360, 375, 390, 768, 920, 1280, and 1440.
- [x] Add long-copy, large-text, 200% zoom, reduced-motion, and forced-colour checks.

#### P1.4: make the current export honest and complete

- [x] Include all approved core assets at production resolution.
- [x] Include marks, lockups, favicon/app icon matrix, OG assets, email assets, and font/licensing information.
- [x] Include every document referenced by the export.
- [x] Remove references to external private files or nodes required for basic use.
- [x] Add asset checksums and an export manifest.
- [x] Test in a clean temporary consumer with no Figma or source-repo access.

#### P1.5: stabilise gradient assets

- [x] Export approved core assets at the required resolution.
- [x] Complete or explicitly limit the gradient catalogue.
- [x] Add hashes connecting source, exported file, and product assignment.
- [x] Generate visually faithful fallbacks or remove misleading fallbacks.
- [x] Add safe lockup zones or scrim/nameplate treatments per core.
- [x] Test lockup contrast against actual pixels.

Phase exit criteria:

- A fresh agent receives one unambiguous authority path.
- The official fixtures pass their own validators.
- No P0 accessibility or reflow defect remains.
- A clean consumer can use the baseline package without external access.
- The current reference remains candidate until separately certified.

### Phase 2: research, strategy, and north-star direction

Goal: establish the strategic and taste foundation before scaling components.

#### P2.1: run the Taste Reverse workstream

- [ ] Complete TR-0 through TR-5.
- [ ] Produce the reference matrix, pattern atlas, anti-pattern atlas, and human taste profile.
- [ ] Record which current Mez rules are supported, challenged, or unresolved by the research.
- [ ] Separate category table stakes from desired differentiation.

#### P2.2: define brand strategy

- [ ] Define priority audiences, jobs, fears, desired outcomes, and buying context.
- [ ] Define Mez Systems positioning and competitive frame.
- [ ] Define the brand promise and proof hierarchy.
- [ ] Define reasons to believe and claim substantiation rules.
- [ ] Define personality traits and anti-traits.
- [ ] Define the relationship between Mez Studios, Mez Systems, and each product.
- [ ] Define future naming rules and endorsement behaviour.

#### P2.3: build the messaging architecture

- [ ] Create company and product message hierarchies.
- [ ] Define primary, supporting, and proof messages by audience.
- [ ] Define founder, corporate, sales, support, legal, product, error, success, social, and lifecycle tones.
- [ ] Expand CTA rules by intent and channel.
- [ ] Create claim-to-proof requirements.
- [ ] Create short, medium, and long-form narrative structures.
- [ ] Add Australian English, localization, and expansion rules.

#### P2.4: create three cross-channel north-star directions

- [ ] Complete TR-6 and TR-7.
- [ ] Apply each direction to the same content and artifact set.
- [ ] Include at least: home hero, product proof section, product UI view, paid ad, organic social asset, email, deck/report spread, and motion frame.
- [ ] Explain trade-offs, not just aesthetic differences.
- [ ] Score each direction for distinctiveness, strategy fit, product credibility, cross-channel range, accessibility, originality, and implementation cost.

Human gates H1 and H2:

- H1 selects reference priorities and anti-references.
- H2 selects one primary north-star direction, one reserve, or rejects all.

Stop gate: do not build the new token/component factory until strategy and a north-star direction are approved.

Phase exit criteria:

- The system has an approved strategic brief and taste profile.
- References have evidence and originality boundaries.
- One direction works across multiple channels and remains recognisably Mez.
- The output cannot be described as a single reference brand with Mez gradients.

### Phase 3: resolve the core identity and proprietary grammar

Goal: turn the north-star direction into an ownable identity system that survives without any one device.

#### P3.1: portfolio and mark architecture

- [ ] Finalise the Mez Studios, Mez Systems, and product endorsement hierarchy.
- [ ] Decide whether parent and holdco share, modify, or pair the wings with distinct wordmarks.
- [ ] Define horizontal, vertical, compact, and icon lockups.
- [ ] Define endorsement lines and co-branding rules.
- [ ] Test free-floating marks where radius cannot communicate hierarchy.
- [ ] Define clear space, minimum sizes, monochrome, inverse, emboss, print, and motion variants.
- [ ] Store canonical vectors in the repository with exported SVG, PNG, and PDF assets.
- [ ] Give every mark and lockup a stable asset ID and checksum.

#### P3.2: typography direction

- [ ] Re-evaluate whether Inter plus Instrument Serif is sufficiently ownable.
- [ ] If retained, define proprietary behaviour beyond a borrowed Notion tuning.
- [ ] Test display, editorial, UI, data, deck, document, email, and mono roles.
- [ ] Define optical sizes, weights, line lengths, leading, tracking, and wrapping behaviour.
- [ ] Define numeral, tabular, currency, code, and data-label behaviour.
- [ ] Define fallback stacks and font loading.
- [ ] Verify language coverage, licensing, and document/email availability.
- [ ] Replace "one serif moment" with contextual art-direction rules.

#### P3.3: monochrome chassis grammar

- [ ] Develop at least three candidate geometric vocabularies derived from the wings and chassis.
- [ ] Test paired panes, apertures, rails, notches, split fields, slots, frames, and cropped wing geometry.
- [ ] Select 3 to 5 primitives that remain useful across different channels.
- [ ] Define primitive construction, proportions, alignment, repetition, cropping, and exclusion rules.
- [ ] Test all primitives in black/white without gradients, marks, or product names.
- [ ] Apply them to web, UI, ad, deck, report, email, and video frames.
- [ ] Reject any grammar that becomes decorative texture without meaning.

#### P3.4: product-core material

- [ ] Decide whether the core is flat, dimensional, or has explicit modes.
- [ ] Define lighting, texture, shadow, edge, and background behaviour.
- [ ] Define core lockup zones and contrast protection.
- [ ] Define crop, scale, animation, print, small-size, and low-bandwidth fallbacks.
- [ ] Resolve sphere, disc, and gradient-M terminology.
- [ ] Define when a core may fill a field and when it must remain contained.
- [ ] Approve or reselect Aurora, Prism, and Forge cores.
- [ ] Complete the full gradient catalogue or formally scope the production library.

#### P3.5: trading-card and stack semantics

- [ ] Define what a single card means.
- [ ] Define what a stack, fan, and bundle mean.
- [ ] Define when the device communicates a suite, product family, artifact, tier, or release.
- [ ] Replace fixed pixel fan offsets with proportional geometry.
- [ ] Define finish escalation without copying gaming rarity systems.
- [ ] Test cards at favicon, social, web, deck, email, and motion sizes.
- [ ] Define maximum repetition per composition and decorative-use limits.

#### P3.6: product territories

For each product, define:

- [ ] Owned core and approved fallback.
- [ ] Graphic motif and allowed transformation.
- [ ] Diagram behaviour.
- [ ] Data emphasis and proof style.
- [ ] Motion personality.
- [ ] Content density.
- [ ] Illustration/icon emphasis.
- [ ] Campaign territory.
- [ ] Product UI accent behaviour.
- [ ] Prohibited divergence from the chassis.

Test all four products in a family contact sheet and as independent campaigns. They must be related but not interchangeable.

#### P3.7: imagery, iconography, diagrams, and data

- [ ] Define screenshot art direction and real-product-proof requirements.
- [ ] Define annotation, cursor, highlight, crop, zoom, and sequencing behaviour.
- [ ] Define icon geometry, stroke/fill logic, optical sizing, and semantic coverage.
- [ ] Define diagram primitives for systems, workflows, automation, and architecture.
- [ ] Define illustration and photography roles, even if the initial rule is deliberate absence.
- [ ] Define data-visualisation principles, semantic colour, comparison, uncertainty, annotation, and accessible alternatives.
- [ ] Define what must remain literal versus what may become abstract.

#### P3.8: motion identity

- [ ] Define functional UI motion separately from expressive brand motion.
- [ ] Define product demonstration choreography.
- [ ] Define social/video transitions, title behaviour, core movement, and wing behaviour.
- [ ] Define duration and easing families by role.
- [ ] Define continuity, interruption, loading, and reduced-motion principles.
- [ ] Produce static storyboards and working prototypes.
- [ ] Ensure motion communicates state, hierarchy, mechanism, or story rather than decoration alone.

#### P3.9: validate transfer and promote research decisions

Complete TR-8 after the selected identity and product territories have been tested, but before Phase 4 canonicalises them.

- [ ] Build the new-context marketing page, dense product view, ad set, lifecycle email, deck/report spread, and motion example.
- [ ] Run recognition, originality, accessibility, strategy-fit, and production-quality evaluation.
- [ ] Approve the initial golden candidates and mark their outcome-validation status.
- [ ] Convert approved hypotheses into Mez decision records with new Mez rule, token, and asset IDs.
- [ ] Link internal provenance to Taste Reverse finding IDs without importing raw evidence into distributions.
- [ ] Record rejected hypotheses and why they failed.
- [ ] Confirm that no research artifact edits canonical Mez tokens directly.

Human gates H3 and H4:

- H3 approves mark architecture, typography direction, monochrome grammar, and core material.
- H4 approves the product-territory family and signature semantics.

Phase exit criteria:

- Mez remains recognisable when logo, names, and gradients are removed.
- Parent, holdco, and product levels remain distinguishable at small sizes.
- Each product has more than a colour swap.
- Signatures have meaning and usage limits.
- The approved system works in all initial channel prototypes.
- All costly decisions have stable decision records and lock states.
- Every research-derived rule has crossed the reviewed promotion boundary in P3.9.

### Phase 4: scaffold the canonical engine and decide repository extraction

Goal: create the schemas, generator infrastructure, asset system, repository boundary, and release machinery that Phase 5 will populate with final foundation semantics. Do not claim a production token/package release before Phase 5 defines and validates the actual values.

#### Repository decision

Use the current Mez Systems pack as the canonical migration workspace through Phases 0 to 3. This avoids moving a contradictory system and losing context while foundational decisions are still changing.

At the start of Phase 4, evaluate extraction into a dedicated internal repository such as `mez-design-system` or `mez-brand-os`.

Extract when all of the following are true:

- The identity direction is approved.
- The source schema is defined.
- The pack has independent owners and release cadence.
- Multiple teams or repositories need versioned consumption.
- CI and packaging are ready to make the move safer than continued in-place evolution.

If these conditions are met, create one central monorepo. Do not create separate repositories per channel. The existing brand-library path then becomes a pinned consumer or generated human-readable mirror, not a second editable source.

#### P4.1: formal authority model

Define three coordinated forms of truth:

1. Declarative truth: structured decisions, schemas, tokens, and asset metadata.
2. Behavioural truth: executable components and tests that prove interaction and responsiveness.
3. Visual truth: human-approved golden outputs registered by version, source, viewport, and checksum.

Figma and Canvas are authoring/review surfaces. Neither may silently override declarative truth.

#### P4.2: schemas and stable IDs

- [ ] Create schemas for system manifest, products, decisions, tokens, assets, components, channels, tasks, and golden outputs.
- [ ] Add schema and system versions.
- [ ] Give every consequential rule a stable ID.
- [ ] Encode status: candidate, trial, approved, locked, deprecated, retired.
- [ ] Encode scope, rationale, owner, introduced version, exceptions, and replacement.
- [ ] Add migration rules for schema changes.
- [ ] Validate every source file before generating outputs.

#### P4.3: token tiers

Create four explicit tiers:

1. Primitive tokens: raw colour, size, font, duration, and numerical values.
2. Semantic tokens: surface, text, border, focus, status, data, spacing role, elevation role.
3. Component tokens: values owned by a component contract.
4. Channel tokens: safe aliases or transformations specific to email, slides, documents, motion, and other media.

- [ ] Use a DTCG-shaped source or another formally documented typed structure.
- [ ] Use aliases instead of duplicated values.
- [ ] Encode modes and scopes explicitly.
- [ ] Record governance state separately from token values.
- [ ] Reject undeclared hardcoded values in source components unless documented as calculated geometry.
- [ ] Use representative fixture values to validate the schema only. Approved foundation values are defined in Phase 5.

#### P4.4: generator infrastructure

Implement and test generators against representative fixtures for:

- [ ] CSS custom properties.
- [ ] JSON for generic consumers.
- [ ] TypeScript types and constants.
- [ ] Tailwind adapter.
- [ ] Figma variable import/mapping.
- [ ] Email-safe values.
- [ ] Presentation theme values.
- [ ] Document styles.
- [ ] Motion constants.
- [ ] Human-readable token tables.
- [ ] Task-scoped LLM context files.

Generated files must include source version and a `do not hand-edit` notice.

Production adapters are regenerated and certified only after Phase 5 completes the source foundations.

#### P4.5: asset system

- [ ] Create a source asset directory and generated asset directory.
- [ ] Record stable asset ID, type, role, dimensions, colour mode, checksum, source decision, and licensing.
- [ ] Generate required sizes and formats.
- [ ] Validate SVG structure and raster dimensions.
- [ ] Use immutable versioned paths in distributions.
- [ ] Add safe-area and crop metadata.
- [ ] Add a replacement and deprecation process.

#### P4.6: package and release infrastructure

- [ ] Define semantic versioning.
- [ ] Create release manifest, checksums, changelog, migration guide, compatibility matrix, and validator report.
- [ ] Scaffold packages such as tokens, assets, CSS, React, email, validation, and agent kit using fixtures where needed.
- [ ] Scaffold offline ZIP/TGZ channel-pack generation.
- [ ] Define how a matching Figma library version is pinned.
- [ ] Make `dist/` completely generated and disposable.
- [ ] Test the packaging path with a fixture release; the first approved foundation release occurs in Phase 5.

#### P4.7: CI and validation foundation

- [ ] Schema validity and stable-ID uniqueness.
- [ ] Broken links and unresolved references.
- [ ] Token semantic parity.
- [ ] Missing assets and checksum drift.
- [ ] Font licensing and required formats.
- [ ] Generated-document parity.
- [ ] Figma mapping consistency.
- [ ] Clean package installation fixtures.

Phase exit criteria:

- Schema and generator fixtures rebuild with zero unexplained diff.
- Every planned adapter has one documented source mapping and generated-output path.
- Every locked decision is machine-addressable.
- A clean project can install the fixture package without reaching into the source workspace.
- The repository boundary is explicit and no second editable copy exists.

### Phase 5: foundations and accessibility system

Goal: convert the approved identity into robust, channel-aware foundations.

#### P5.1: colour and modes

- [ ] Define brand, neutral, functional, status, and data palettes separately.
- [ ] Define allowed background and foreground pairings.
- [ ] Decide light/dark boundaries per channel instead of applying one marketing-site rule globally.
- [ ] Define high-contrast and forced-colour fallbacks.
- [ ] Define print, email-client, and projection behaviour.
- [ ] Validate every semantic pair, including actual gradient lockups.

#### P5.2: typography system

- [ ] Define display, title, heading, body, UI, label, caption, mono, code, tabular, and data roles.
- [ ] Define responsive behaviour and content-driven wrapping.
- [ ] Define long-form measure and editorial rhythm.
- [ ] Define compact application and data modes.
- [ ] Define slide and document mappings.
- [ ] Define localization expansion, RTL, and fallback behaviour.

#### P5.3: spatial and layout system

- [ ] Define spacing roles rather than only a numeric scale.
- [ ] Define grids, containers, gutters, max widths, and full-bleed behaviour.
- [ ] Define density modes.
- [ ] Define responsive/container breakpoints from 320px upward.
- [ ] Define proportional stack/fan geometry.
- [ ] Define content-driven exceptions and document them.

#### P5.4: shape, border, and elevation

- [ ] Resolve radius hierarchy and brand-tier semantics.
- [ ] Define border roles and accessible component boundaries.
- [ ] Define elevation roles and when shadows are prohibited.
- [ ] Separate calculated brand geometry from ordinary component radii.
- [ ] Test every role on light, dark, gradient, image, print, and email surfaces where applicable.

#### P5.5: accessibility contracts

- [ ] Semantic HTML and landmark expectations.
- [ ] Keyboard patterns for interactive components.
- [ ] Focus visibility and focus management.
- [ ] Error identification and field association.
- [ ] Non-colour status communication.
- [ ] Alt text, complex-image descriptions, captions, and transcripts.
- [ ] Reflow, zoom, target size, and orientation.
- [ ] Reduced motion and pause/stop controls.
- [ ] Forced colours and contrast modes.
- [ ] Accessible data visualisation.
- [ ] Email, document, and presentation accessibility.
- [ ] Localization and RTL test fixtures.

#### P5.6: foundation adversarial fixtures

Create fixtures for:

- [ ] 320px and intermediate widths.
- [ ] 200% and 400% text zoom.
- [ ] Very long and very short copy.
- [ ] Missing and broken images.
- [ ] Missing core asset with fallback.
- [ ] Translation expansion.
- [ ] RTL.
- [ ] Keyboard-only use.
- [ ] Screen-reader spot checks.
- [ ] Reduced motion.
- [ ] Forced colours.
- [ ] Dark email clients and print/PDF export.

#### P5.7: generate, package, and certify the foundation release

- [ ] Populate canonical primitive, semantic, component-foundation, and channel-foundation tokens with the approved Phase 5 values.
- [ ] Run the Phase 4 generators for CSS, JSON, TypeScript, Tailwind, Figma mapping, email, slides, documents, motion, docs, and LLM context.
- [ ] Build the approved foundation token, asset, CSS, validation, and agent packages.
- [ ] Generate a complete versioned foundation archive.
- [ ] Run exact semantic-parity and unexplained-diff checks.
- [ ] Install the release into clean static HTML, React/Vite, email, and document fixtures.
- [ ] Run the adversarial foundation suite in every applicable fixture.
- [ ] Produce the release manifest, checksums, changelog, migration notes, and known limitations.
- [ ] Mark the release `foundation-certified`, not `1.0`, until later channel and adoption gates pass.

Phase exit criteria:

- Applicable digital outputs meet WCAG AA.
- Reflow works from 320px upward.
- Every foundation adapter matches the canonical semantics.
- No human is required to manually prove token parity or contrast.
- Channel-specific needs are handled through explicit aliases, not hidden overrides.
- The foundation release installs cleanly without Figma or source-repository access.
- Regenerating every foundation adapter creates zero unexplained diff.

### Phase 6: design grammar, components, and local design lab

Goal: make the identity executable without reducing every output to one template.

#### P6.1: signatures and flexible axes

For every rule, classify it as:

- `SIGNATURE`: required for recognition.
- `CONSTRAINT`: required for accessibility, strategy, or production safety.
- `PREFERENCE`: recommended default with allowed alternatives.
- `OPTION`: approved expressive choice.
- `EXCEPTION`: bounded, recorded deviation.
- `PROHIBITION`: known failure or identity conflict.

- [ ] Define the minimum signature set for Mez Systems.
- [ ] Define which signatures are global versus product-specific.
- [ ] Define variation axes for composition, density, emphasis, imagery, motion, and proof.
- [ ] Define combinations that are valid and invalid.
- [ ] Replace universal fixed section orders with outcome-driven composition modes.

#### P6.2: composition modes

Build and document at least these modes:

- [ ] Statement-led.
- [ ] Product-proof-led.
- [ ] Editorial narrative.
- [ ] Workflow/process.
- [ ] Architecture/system map.
- [ ] Metrics/evidence.
- [ ] Comparison.
- [ ] Mosaic/index.
- [ ] Conversion/offer.
- [ ] Dense application/data.

Each mode must define purpose, hierarchy, content requirements, desktop/mobile behaviour, density curve, approved devices, anti-patterns, and representative outputs.

#### P6.3: keep and evolve the local Canvas

- [ ] Preserve a no-build HTML/CSS/JS reference surface.
- [ ] Generate its token layer from canonical source.
- [ ] Split foundations, components, patterns, pages, channels, and adversarial fixtures.
- [ ] Add viewport and state controls.
- [ ] Add light/dark or channel modes only where approved.
- [ ] Add copy-length, localization, missing-asset, and reduced-motion controls.
- [ ] Show source rule IDs and component IDs beside specimens.
- [ ] Add one-click or command-driven screenshot capture.
- [ ] Do not treat Canvas-specific hardcoded values as new truth.

#### P6.4: primitive components

- [ ] Buttons, links, icon buttons, and split actions.
- [ ] Inputs, text areas, selects, checkboxes, radios, switches, and date/time inputs.
- [ ] Labels, helper text, validation, and grouped fields.
- [ ] Chips, tags, badges, status, and product pills.
- [ ] Cards, panels, separators, lists, and media frames.
- [ ] Avatars, marks, icons, tooltips, and popovers.
- [ ] Disclosure, accordion, tabs, pagination, and stepper.
- [ ] Loading, progress, skeleton, empty, error, offline, and success.

For each component, define semantics, anatomy, variants, sizes, states, keyboard behaviour, content limits, responsive behaviour, tokens, accessibility, and prohibited uses.

#### P6.5: marketing patterns

- [ ] Navigation families.
- [ ] Hero families mapped to composition modes.
- [ ] Product/suite presentation.
- [ ] Feature and workflow proof.
- [ ] Metrics and evidence.
- [ ] Testimonials and customer proof.
- [ ] Pricing and conversion.
- [ ] Comparison.
- [ ] FAQ and objection handling.
- [ ] CTA bands and footers.
- [ ] Editorial and research modules.
- [ ] Legal and trust modules.

Build multiple approved variants. Do not describe one arrangement as the only valid page.

#### P6.6: product-UI components and patterns

- [ ] App shell, global navigation, product switcher, and account area.
- [ ] Side navigation, command/search, breadcrumbs, and contextual navigation.
- [ ] Tables, sorting, filters, pagination, selection, bulk actions, and density.
- [ ] Metrics, charts, legends, annotations, comparison, and export.
- [ ] Forms, builders, editors, uploads, and complex validation.
- [ ] Menus, dialogs, drawers, sheets, toasts, alerts, and notifications.
- [ ] Onboarding, setup, progress, permissions, and destructive actions.
- [ ] Loading, empty, error, offline, stale, partial, and no-permission states.
- [ ] Audit trail, history, versioning, and automation status.
- [ ] Responsive application behaviour and narrow-screen prioritisation.

#### P6.7: real product proof

- [ ] Replace every placeholder with real or intentionally fictionalised product evidence.
- [ ] Map each marketing claim to a visible mechanism or proof artifact.
- [ ] Define screenshot datasets that are safe, current, and readable.
- [ ] Add annotations and sequences that show cause and effect.
- [ ] Keep product UI literal enough to be credible.
- [ ] Prevent decorative fake dashboards and magical automation claims.

#### P6.8: production packages and fixtures

- [ ] Build a framework-neutral CSS package.
- [ ] Build the primary production component package, initially React if that matches active consumers.
- [ ] Create static HTML and React/Vite fixture consumers.
- [ ] Add code-to-Figma mappings where useful.
- [ ] Test tree-shaking, bundle size, responsiveness, and supported browsers.
- [ ] Keep API and visual contracts versioned.

#### P6.9: compliance and excellence evaluation

Hard compliance checks:

- [ ] Schema, tokens, assets, naming, required states, accessibility, responsive behaviour, and channel format.

Design-excellence rubric:

- [ ] Hierarchy.
- [ ] Composition.
- [ ] Pacing and density.
- [ ] Typography.
- [ ] Product truth and proof.
- [ ] Distinctiveness.
- [ ] Narrative.
- [ ] Conversion clarity.
- [ ] Emotional impact.
- [ ] Craft.
- [ ] Originality.

Use blocking failures plus a weighted score. Passing compliance does not imply excellent design.

Human gate H5:

- Approve one marketing golden page, one product page, and two representative product workflows.
- Review complete experiences at desktop and mobile, not isolated tokens.

Phase exit criteria:

- No horizontal overflow in the supported matrix.
- Key interactions work by keyboard and assistive-technology spot check.
- No placeholder proof remains in golden outputs.
- Pages demonstrate controlled variation instead of template repetition.
- Production and no-build fixtures implement the same contracts.
- Golden outputs pass both compliance and excellence thresholds.

### Phase 7: publish the Figma companion library

Goal: give humans a powerful design surface without creating a second source of truth.

#### P7.1: Figma foundations

- [ ] Import or generate variables from the canonical token release.
- [ ] Create typography, colour, spacing, radius, elevation, motion, and grid documentation.
- [ ] Add asset IDs and source decision IDs.
- [ ] Add clear lock, candidate, trial, and deprecated labels.
- [ ] Publish source version and release date inside the file.

#### P7.2: components and mappings

- [ ] Build Figma component sets from approved contracts.
- [ ] Match names, variants, sizes, states, and properties to production components.
- [ ] Configure resizing and responsive behaviour.
- [ ] Add Code Connect or equivalent mappings where supported.
- [ ] Validate that no Figma-only variant silently appears.
- [ ] Record intentionally non-code design components separately.

#### P7.3: composition and channel templates

- [ ] Build composition-mode boards.
- [ ] Build marketing and product pattern boards.
- [ ] Build ad/social, email, presentation, document, and data templates as those channels become approved.
- [ ] Include good, bad, and edge-case examples.
- [ ] Attach rule IDs and content requirements.

#### P7.4: Figma operating rules

- [ ] Document what may be explored freely in draft pages.
- [ ] Require approved decisions before library publication.
- [ ] Require before/after screenshots for milestone edits.
- [ ] Define token, asset, and component parity checks.
- [ ] Record Figma file key, library publication state, and matching system version in every release.
- [ ] Move volatile node IDs into a generated or validated Figma map.

Phase exit criteria:

- Figma variables match the release.
- Designers do not recreate marks, cores, or tokens manually.
- Key Figma and production components have explicit mappings.
- No undocumented Figma decision can override the repository.
- The published Figma library version is traceable to a release.

### Phase 8: build channel systems

Goal: prove that Mez identity works across the real outputs teams and LLMs must create.

### Standard channel-pack contract

Every supported channel contains:

```text
channel/
  manifest.json
  README.md
  AGENTS.md
  strategy-and-use-cases.md
  content-model.schema.json
  tokens/
  assets/
  templates/
  components/
  examples/golden/
  examples/anti/
  outcomes/
    measurement-plan.md
    results/
  prompts/
  validator/
  export-settings.json
  checksums.json
```

Each pack must define artifact taxonomy, dimensions, safe zones, content structure, composition families, asset rules, accessibility, export behaviour, good examples, failure examples, and output receipts.

Every golden candidate also carries an outcome status:

- `CRAFT_APPROVED`: passes brand, accessibility, production, and design-quality review but has not been tested in use.
- `PILOT`: deployed in a controlled real context with a measurement plan.
- `OUTCOME_VALIDATED`: achieved its defined comprehension, task, engagement, conversion, or recognition threshold with enough evidence.
- `RETIRED`: later evidence or strategy made it unsuitable.

Do not confuse visual approval with proven effectiveness. Also do not attribute every business result to visual design alone. Record audience, offer, copy, placement, traffic quality, and other material variables in the measurement plan.

#### Wave A: marketing web

- [ ] Flexible home, product, pricing, launch, editorial, research, legal, and campaign archetypes.
- [ ] Multiple composition modes per archetype.
- [ ] Real proof requirements.
- [ ] SEO, metadata, OG, icons, performance, and accessibility.
- [ ] Static HTML and production framework examples.
- [ ] Certified desktop/mobile golden set.

#### Wave B: paid advertising

- [ ] Define platform ratios and safe zones.
- [ ] Define offer-led, proof-led, statement-led, launch, testimonial, and retargeting families.
- [ ] Define hierarchy at one-second and three-second attention windows.
- [ ] Define price, claim, legal, and CTA behaviour.
- [ ] Define static, carousel, and motion variants.
- [ ] Build editable native templates and coded/raster export routes.
- [ ] Add legibility, cropping, safe-zone, and file-size validation.
- [ ] Test without a logo and without a gradient to measure recognition.

#### Wave C: organic social

- [ ] Define static, carousel, thread, quote, product update, educational, founder, launch, and case-study families.
- [ ] Define covers, pagination, progression, and final-frame CTAs.
- [ ] Define safe zones and platform ratios.
- [ ] Define subtitle, caption, and accessibility behaviour.
- [ ] Define recurring series that feel related without becoming one repeated template.
- [ ] Build native editable templates and publishing exports.

#### Wave D: presentations

- [ ] Define narrative structures for sales, product, strategy, training, investor, and internal review decks.
- [ ] Build cover, agenda, thesis, section, comparison, workflow, product proof, data, quote, and closing layouts.
- [ ] Define slide density and progressive disclosure.
- [ ] Map presentation typography and colour from canonical tokens.
- [ ] Build accessible charts, tables, diagrams, and speaker-note conventions.
- [ ] Provide native Figma Slides, Google Slides, or PPTX templates according to team workflow.
- [ ] Test projection, PDF export, and 16:9/4:3 where required.

#### Wave E: documents and reports

- [ ] Define proposals, briefs, reports, research papers, playbooks, and one-page summaries.
- [ ] Build page styles, cover systems, running headers, footers, tables of contents, citations, footnotes, figures, tables, and appendices.
- [ ] Define long-form type, widows/orphans, page breaks, and print behaviour.
- [ ] Create native DOCX/Google Docs/PDF templates as needed.
- [ ] Add tagged-PDF and document-accessibility requirements.
- [ ] Test short and long documents with real content.

#### Wave F: lifecycle and transactional email

- [ ] Welcome, activation, education, launch, conversion, reminder, receipt, success, support, retention, and win-back families.
- [ ] Tested HTML email and plain-text counterparts.
- [ ] System-font and hosted-font fallback rules.
- [ ] Dark-client behaviour and image-off mode.
- [ ] Subject, preheader, CTA, proof, and legal content models.
- [ ] Deliverability-safe image and file-size rules.
- [ ] Client test matrix and accessible semantic structure.

#### Wave G: product UI and data visualisation

- [ ] Shared application shell and four product workflows.
- [ ] Semantic status and data palettes.
- [ ] Chart selection guidance.
- [ ] Annotations, comparison, thresholds, uncertainty, and empty/error states.
- [ ] Accessible tables and text alternatives.
- [ ] Compact, comfortable, and presentation density modes.
- [ ] Export behaviour for images, CSV, reports, and decks.

#### Wave H: motion and video

- [ ] Mark/core animation and product transitions.
- [ ] Type entrance, emphasis, and continuity.
- [ ] Product demo framing and cursor/action language.
- [ ] Social aspect ratios, title cards, lower thirds, captions, and end cards.
- [ ] Audio and sound principles if required.
- [ ] Reduced-motion/static equivalents.
- [ ] Native templates and rendered reference files.
- [ ] Motion duration, frame-rate, compression, and export rules.

#### Wave I: OG, icons, print, and environments

- [ ] Complete generated OG and social-preview families.
- [ ] Product and holdco favicon/app-icon matrices.
- [ ] Print colour and minimum-size behaviour.
- [ ] Event/signage/merchandise rules only when justified by real demand.

Human gate H6:

- Review one batched cross-channel contact sheet.
- Approve one golden artifact per high-visibility channel.
- Technical size and format variants inherit approval when validators pass.

Phase exit criteria for each channel:

- A clean consumer can create the artifact without hidden context.
- Native editable source and required exports exist.
- The result passes channel compliance and the design-excellence rubric.
- At least one golden and three contrastive/failure examples exist.
- The brand is recognisable without forcing the exact same template everywhere.
- Every golden candidate declares an outcome hypothesis, measurement plan, and current outcome status.

### Phase 9: harden the LLM-first operating layer

Goal: expand the minimum Phase 0 task/context/receipt contract, already dogfooded throughout Phases 1 to 8, into production routing, evaluation, and multi-model certification while preserving human taste authority.

#### P9.1: expand the task router

Do not ask an LLM to read the entire system for every task. Create a router that assembles the smallest sufficient context pack.

Each task definition should include:

- Stable task ID and version.
- Channel and artifact type.
- Objective and audience.
- Required strategy, product, channel, and component context.
- Required assets and content.
- Allowed variation axes.
- Output contract.
- Hard validators.
- Quality rubric.
- Golden and anti-examples.
- Human-gate rule.
- Stop conditions for missing or conflicting inputs.

Example:

```yaml
id: paid-social-product-proof
version: 1
channel: paid-social
objective: product-proof-ad
requiredContext:
  - strategy/brand-platform
  - strategy/messaging-architecture
  - grammar/signatures
  - products/{product}
  - channels/paid-social/spec
requiredAssets:
  - product-core
  - approved-mark
  - proof-screenshot
allowedVariation:
  composition: [proof-led, statement-led, product-led]
  density: [sparse, standard]
outputContract:
  formats: [1080x1080, 1080x1350]
  files: [editable-source, png, receipt]
hardValidators:
  - schema
  - assets
  - contrast
  - safe-zone
qualityRubric:
  - distinctiveness
  - hierarchy
  - proof-clarity
  - craft
goldenExamples:
  - GOLD-PAID-001
antiExamples:
  - ANTI-PAID-004
humanGate: only-if-new-composition-family
```

#### P9.2: agent stages

Use separate logical roles, even when one model performs several:

1. Planner: identifies artifact type, context, dependencies, and missing inputs.
2. Generator: creates deliberate variants within the allowed grammar.
3. Critic: scores hard constraints and design quality.
4. Reviser: corrects the selected route.
5. Verifier: independently runs deterministic checks and does not trust self-assessment.
6. Receipt writer: records exactly how the artifact was produced.

#### P9.3: context profiles

- [ ] Build minimal profiles for every supported task.
- [ ] Ensure marketing copy tasks do not receive irrelevant application internals.
- [ ] Ensure product UI tasks receive accessibility, state, and data contracts.
- [ ] Include current lock states and unresolved candidates.
- [ ] Include required assets by ID, not vague path hints.
- [ ] Add schema validation for context bundles.
- [ ] Add a maximum context budget and priority rules.

#### P9.4: prompts and recipes

- [ ] Planning recipe.
- [ ] Variant-generation recipe.
- [ ] Critique recipe.
- [ ] Revision recipe.
- [ ] Accessibility review recipe.
- [ ] Originality review recipe.
- [ ] Channel export recipe.
- [ ] Change-proposal recipe.
- [ ] Exception-request recipe.
- [ ] Migration recipe.

Prompts should reference stable rule IDs and structured inputs. Do not duplicate the full brand book inside every prompt.

#### P9.5: golden and anti-example registry

Every golden artifact records:

- ID and channel.
- System version.
- Product and task ID.
- Source template/component IDs.
- Decision/rule IDs.
- Asset IDs and checksums.
- Renderer and viewport/output dimensions.
- Approval owner and date.
- Screenshot/output hash.
- Known limitations.

Anti-examples must state exactly why they fail. Include examples that are compliant but dull, not only obvious brand violations.

#### P9.6: output receipts

Every generated output should emit a machine-readable receipt containing:

- Design-system version.
- Task/channel/product IDs.
- Model and prompt-profile version.
- Rules and decisions applied.
- Templates and components used.
- Assets and checksums used.
- Validator results.
- Quality score.
- Human approval status.
- Exceptions and expiry.

#### P9.7: validator orchestration

- [ ] Schema and output contract.
- [ ] Asset presence, dimensions, and safe zones.
- [ ] Token and hardcoded-value checks.
- [ ] Contrast and accessibility.
- [ ] Responsive and content stress tests.
- [ ] Copy semantics and claims.
- [ ] Golden comparison.
- [ ] Originality/confusion checks where appropriate.
- [ ] Channel-native export checks.

#### P9.8: multi-model benchmark

Run the same fresh-context suite across multiple model families and capability levels:

- [ ] Marketing page.
- [ ] Product workflow.
- [ ] Paid ad.
- [ ] Social carousel.
- [ ] Lifecycle email.
- [ ] Deck sequence.
- [ ] Report spread.
- [ ] Data graphic.
- [ ] Motion storyboard.

Inject failures:

- [ ] Long copy.
- [ ] Missing image or wrong image dimensions.
- [ ] Missing core asset.
- [ ] Conflicting stale instruction.
- [ ] Localization and RTL.
- [ ] Unsupported output format.
- [ ] Old system version.
- [ ] Low-contrast custom colour.
- [ ] Request to copy a reference brand.

Update routing, schemas, examples, or validators when models fail. Do not merely add vague warning prose.

#### P9.9: stop behaviour

An LLM must stop and request a decision when:

- A required locked asset is missing.
- Two current canonical rules conflict.
- A task requires an unsupported channel.
- A requested change would alter a locked identity signature.
- The output would require an unapproved claim.
- A source/reference request creates material cloning risk.
- A candidate decision would be published as final.

Phase exit criteria:

- Different LLMs choose the same required context and rules for the same task.
- Lower-capability models can complete representative tasks without hidden knowledge.
- The verifier catches seeded failures.
- Output receipts fully explain provenance.
- Hard compliance and design quality are reported separately.
- No autonomous mass production occurs before benchmarks pass.

### Phase 10: distribution, team transfer, and adoption

Goal: let any team consume the system without maintaining a private shadow version.

#### P10.1: distribution products

Publish versioned artifacts such as:

- `@mez/design-tokens`
- `@mez/assets`
- `@mez/css`
- `@mez/react`
- `@mez/email`
- `@mez/validation`
- `@mez/agent-kit`
- Offline channel packs.
- Immutable asset URLs or archives.
- Published Figma library with matching system version.
- Native slide, document, and motion templates.

Names are illustrative until package/repository naming is approved.

#### P10.2: consumer contract

Every consumer declares an exact system version and relevant scope:

```json
{
  "schemaVersion": 1,
  "designSystemVersion": "1.2.0",
  "product": "aurora",
  "channels": ["web-marketing", "product-ui"],
  "framework": "react-vite",
  "exceptions": []
}
```

- [ ] Pin exact versions instead of consuming an uncontrolled latest release.
- [ ] Record product and channel scope.
- [ ] Record exceptions with owner, rationale, expiry, and affected rule IDs.
- [ ] Expose the system version in build metadata or an output receipt.

#### P10.3: initializer and doctor

Target commands:

```bash
mez-ds init
mez-ds context --task paid-social-product-proof --product aurora
mez-ds scaffold --channel email --template delivery
mez-ds validate ./output --profile paid-social
mez-ds compare ./output --golden GOLD-PAID-001
mez-ds explain RULE-CORE-004
mez-ds doctor
```

- [ ] `init` installs correct packages and local agent guidance.
- [ ] `doctor` reports copied assets, unpinned versions, stale manifests, missing validators, and hidden local overrides.
- [ ] `validate` runs the channel contract.
- [ ] `compare` renders and compares against a golden artifact.
- [ ] `explain` resolves a rule ID to rationale, scope, and examples.

#### P10.4: update and rollback

- [ ] Generate update proposals with release notes and migrations.
- [ ] Render before/after golden and consumer diffs.
- [ ] Keep updates explicit and reversible.
- [ ] Add compatibility checks before installation.
- [ ] Deprecate before removing.
- [ ] Prevent automated breaking upgrades.

#### P10.5: team ingestion routes

Code teams receive:

- Versioned packages, initializer, fixtures, validators, and migration tools.

Design teams receive:

- Published Figma library, native templates, assets, golden examples, and contribution workflow.

Marketing/content teams receive:

- Channel-specific editable templates, asset pack, content models, LLM recipes, and export validators.

LLMs receive:

- Task router, minimal context pack, schemas, examples, anti-examples, and validators.

External or isolated projects receive:

- A complete offline archive containing everything needed for the selected channels and product.

No team should be instructed to copy a folder and remember to copy it again later.

#### P10.6: pilot adoption

- [ ] Integrate one marketing repository.
- [ ] Integrate one product repository.
- [ ] Integrate one non-code design/marketing workflow.
- [ ] Generate one artifact in an isolated clean project.
- [ ] Measure time to first valid output.
- [ ] Capture installation failures and hidden dependencies.
- [ ] Resolve pilot exceptions upstream where appropriate.
- [ ] Verify upgrade and rollback.

Phase exit criteria:

- A fresh team can install the system and create a valid artifact without contacting the system author.
- Every consumer can identify the exact version used.
- Updates are explicit, reviewable, and reversible.
- No pilot team maintains private tokens or untracked core assets.
- Exceptions are visible, owned, and temporary.

### Phase 11: certification and ongoing governance

Goal: keep the system coherent after launch as products, channels, tools, and teams change.

#### P11.1: release certification

Before a major release:

- [ ] Run full schema, token, link, asset, and package validation.
- [ ] Run accessibility and responsive suites.
- [ ] Run channel-native export checks.
- [ ] Run golden visual diffs.
- [ ] Run cross-channel recognition tests.
- [ ] Run multi-model LLM benchmarks.
- [ ] Run clean-consumer installation tests.
- [ ] Review unresolved exceptions and candidates.
- [ ] Produce release manifest, changelog, migration guide, and known limitations.

Human gate H7: approve the release contact sheet, benchmark summary, golden diffs, and named unresolved risks.

#### P11.2: versioning

- Major: breaking token semantics, locked identity change, removed component, incompatible template or channel-contract change.
- Minor: additive channel, component, template, token, product territory, or approved golden family.
- Patch: compatible correction, documentation repair, implementation bug fix, or generated-output repair that preserves intended semantics.

#### P11.3: contribution and exception governance

- [ ] Define how teams propose components, templates, assets, and rules upstream.
- [ ] Require problem, evidence, proposed scope, examples, and migration impact.
- [ ] Assign approval level by change class.
- [ ] Time-limit exceptions and require expiry review.
- [ ] Prevent one consumer's local need from silently redefining the global system.

Change classes:

| Change | Required approval |
|---|---|
| Generated refresh or documentation correction | Automatic after validation |
| Internal implementation with unchanged output | Automatic after tests |
| Minor component or additive template | System maintainer |
| New channel pattern | Senior design review |
| Locked identity, core, type, or messaging change | Brand owner |
| Breaking release | Brand owner plus system owner |

#### P11.4: recurring health checks

- [ ] Token and asset drift.
- [ ] Consumer version adoption.
- [ ] Unresolved exceptions and expired waivers.
- [ ] Candidate decisions awaiting promotion or rejection.
- [ ] Accessibility, browser, email-client, and platform changes.
- [ ] Golden-output coverage.
- [ ] Most common validator failures.
- [ ] Template usage and abandoned components.
- [ ] Multi-model benchmark regression.
- [ ] Brand recognition as the system grows.
- [ ] Periodic Taste Reverse refresh and annual identity review.

#### P11.5: success metrics

- Zero manual token drift across generated targets.
- Zero broken references or missing required assets in a release.
- Applicable WCAG AA conformance and documented exceptions.
- Reflow from 320px upward.
- Multiple fresh LLMs produce zero P0 brand violations on benchmark tasks.
- Compliance and design quality are measured separately.
- Teams reach a valid first artifact without system-author intervention.
- Every artifact records the system version.
- Every supported channel has golden and failure examples.
- The identity passes recognition tests without relying only on logo, product name, or gradient.

Outcome metrics by channel:

- Product UI: task completion, time on task, error/recovery rate, support burden, accessibility success, and user confidence.
- Marketing web: message comprehension, navigation success, proof recall, CTA clarity, conversion, and qualified downstream action.
- Paid advertising: thumb-stop/attention where measurable, click-through, qualified conversion, creative fatigue, and brand recognition, normalised for offer and audience.
- Organic social: comprehension, completion/swipe-through, saves/shares, qualified response, and series recognition.
- Email: deliverability, image-off comprehension, click/action completion, unsubscribe/complaint signals, and lifecycle goal completion.
- Presentations and documents: comprehension, decision recall, task completion, accessibility, and stakeholder action.
- Data visualisation: interpretation accuracy, time to answer, uncertainty comprehension, and accessible alternative use.
- Motion/video: completion, key-message recall, caption comprehension, reduced-motion equivalence, and recognition.
- Cross-channel brand: unaided/aided recognition, correct product-family attribution, perceived distinctiveness, and confusion with reference brands.

Promotion rule: a `CRAFT_APPROVED` output may define visual quality before enough real-world data exists, but it must not be described as outcome-proven. High-volume templates should progress through `PILOT` to `OUTCOME_VALIDATED`, or be revised/retired based on evidence.

Phase exit criteria:

- The system remains coherent under new products, channels, and teams.
- Exceptions do not become permanent undocumented forks.
- Releases are reconstructable, auditable, and reversible.
- Olli reviews only consequential creative or breaking changes.

## Artifact and authoring matrix

This matrix answers what should be designed, coded, rendered, mirrored, or packaged at each layer.

| Artifact | First authoring surface | Canonical storage | Validation | Delivered to teams |
|---|---|---|---|---|
| Strategy and messaging | Markdown plus structured manifests | Repository source | Schema, decision status, review | Human docs and scoped LLM context |
| Research evidence | Taste Reverse | Taste Reverse vault | Evidence links, package hash, limitations | Not distributed directly |
| Approved research findings | Structured findings export | Mez research/synthesis | Schema, human decision, originality | Internal decision context only |
| Tokens | Typed JSON source | Repository source | Schema, aliases, semantic parity | CSS, JSON, TS, Tailwind, Figma mapping, channel adapters |
| Marks and vectors | Figma/vector exploration | Versioned SVG/source assets | Geometry, safe area, size, checksum | Asset packages and Figma library |
| Product cores | Source image/vector workflow | Versioned source assets | Resolution, checksum, crop/contrast | WebP/PNG/SVG/fallback packages |
| Static art direction | Figma or local visual lab | Decision record plus source artifact | Cross-channel tests, originality | Templates and golden renders |
| Responsive marketing layout | HTML/CSS first | Components/templates in repository | Reflow, accessibility, visual regression | Static HTML and framework packages |
| Interactive product UI | Code with parallel Figma component work | Tested component implementation | Unit, interaction, accessibility, visual | Production packages and Figma mappings |
| Email | Email HTML first | Email package/templates | Client rendering, accessibility, image-off | HTML, plain text, editable content model |
| Ads and social | Figma/SVG exploration, renderer where useful | Native template plus manifest | Dimensions, safe zones, legibility, export | Editable source plus PNG/JPG/MP4 |
| Presentations | Native slides | Native template plus spec | Layout, overflow, accessibility, PDF | Figma Slides/Google Slides/PPTX |
| Documents and reports | Native document tooling | Native template plus spec | Pagination, links, accessibility, PDF | DOCX/Google Docs/PDF |
| Data visualisation | Code/specification plus Figma examples | Chart grammar and components | Data accuracy, colour, text alternatives | Code, SVG/PNG, deck/document adapters |
| Motion and video | Code or timeline tool | Parameters, source template, rendered reference | Timing, captions, reduced motion, export | Editable source and rendered media |
| Canvas | Generated/local HTML | Repository fixture | Screenshot, responsive, state matrix | Internal review and portable reference |
| Figma library | Generated variables plus approved components | Figma companion, version recorded in repo | Token/component parity | Published design library |
| Golden outputs | Native source plus immutable render | Golden registry | Human approval, checksum, rubric | Examples for teams and LLMs |
| LLM pack | Generated | `dist/llm-pack` | Schema, context completeness, benchmark | Task-scoped pack |

## Immediate execution sequence

Do not begin by creating dozens of components or rebuilding the entire Figma file. The correct first sequence is:

1. Preserve current state, create the governance registers, and establish the minimum LLM task/context/receipt contract.
2. Repair source-of-truth contradictions and P0 accessibility/reflow defects.
3. Make the current baseline export genuinely self-contained.
4. Stabilise and checkpoint Taste Reverse enough to provide versioned findings.
5. Run the first research/taste cycle.
6. Approve strategy, identity direction, and product differentiation.
7. Build the canonical schema and generator engine.
8. Build foundations and the local design lab.
9. Build marketing and product golden outputs.
10. Publish the Figma companion library.
11. Expand into channel waves.
12. Add the LLM operating layer and multi-model benchmarks.
13. Pilot distribution with real teams.
14. Certify the first major release.

### First execution backlog

These are the first concrete tasks a new session should pick up, in order:

#### NEXT-001: create current-state registers

- Inputs: this roadmap, current pack, current Canvas, current Figma metadata, current consumer repo state.
- Outputs: `governance/artifact-register.json`, `governance/consumer-register.json`, `governance/issue-register.json`, `governance/decision-register.json`, baseline screenshots.
- Human input: none.
- Verification: every file and DS finding is represented; schema parses; current git hashes recorded.

#### NEXT-001A: establish the minimum LLM contract

- Inputs: P0.4 and the standard task record in this roadmap.
- Outputs: task, context-bundle, output-receipt, and evaluation-result schemas plus one completed Phase 0 example.
- Human input: none.
- Verification: a fresh agent can execute one bounded inventory task from only the context bundle, and its receipt fully explains the work and evidence.

#### NEXT-002: write the authority decision

- Inputs: DS-001 to DS-007.
- Outputs: `governance/AUTHORITY.md`, updated entry points, conflict validator.
- Human input: approve only the repository/owner boundary if not already delegated.
- Verification: searching all active guidance finds one consistent authority model.

#### NEXT-003: replace the broken review gate

- Inputs: current checklist and its self-failing examples.
- Outputs: scoped validator scripts plus a separate quality rubric.
- Human input: approve rubric weighting only.
- Verification: official fixtures pass; seeded glow, naming, asset, accessibility, and overflow failures are caught; legitimate blur and objection-handling copy pass.

#### NEXT-004: correct critical accessibility and 320px/375px failures

- Inputs: current tokens and Canvas.
- Outputs: accessible focus/form tokens, responsive component fixes, automated tests.
- Human input: none unless the visible correction materially changes the approved identity.
- Verification: measured contrast, keyboard pass, viewport matrix, zoom, reduced motion.

#### NEXT-005: produce a complete baseline export

- Inputs: current source assets and docs.
- Outputs: versioned portable archive with checksums and no escaping references.
- Human input: none.
- Verification: clean isolated consumer install with no Figma/source access.

#### NEXT-006: prepare Taste Reverse cycle one

- Inputs: research questions in this roadmap and Taste Reverse current state.
- Outputs: tool checkpoint, source export schema, inspiration brief, source register.
- Human input: H1 source shortlist review.
- Verification: every source maps to a research question; raw evidence remains outside the Mez distribution.

Do not proceed to broad visual-system generation until NEXT-001 through NEXT-006 are complete and the Phase 2 human direction gate is scheduled.

## Fresh-session and different-LLM handoff protocol

### Start of session

1. Read this roadmap.
2. Inspect current status files and the latest decision register.
3. Run `git status` in every repository in scope.
4. Verify the active system version and current phase.
5. Open the relevant golden/current fixtures.
6. Select one `READY` task whose dependencies are complete.
7. Restate the task, files, acceptance criteria, and human gate before editing.

### During a task

- Work only inside the stated scope.
- Preserve unrelated user changes.
- Change canonical source before generated outputs.
- Use generators instead of manually editing mirrors.
- Save visual evidence for meaningful design changes.
- Run the named validators.
- Record unresolved ambiguity instead of inventing a hidden rule.
- Escalate only at the task's explicit human gate.

### End of session

- Update task status and completion evidence.
- Record files changed and commands/tests run.
- Record visual artifacts and validator outputs.
- Record decisions made and any new exceptions.
- Update changelog/release notes where required.
- Name the exact next `READY` task.
- Do not call a phase complete if its exit criteria are unverified.

### Standard task record

```yaml
id: P6.4-COMPONENT-BUTTON
title: Build the canonical button contract
status: READY
owner: unassigned
dependencies:
  - DEC-TYPE-002
  - TOKENS-FOUNDATION-1
scope:
  - components/primitives/button
inputs:
  - ruleIds: []
  - assetIds: []
deliverables:
  - component.schema.json
  - HTML fixture
  - React implementation
  - Figma mapping
  - accessibility tests
verification:
  - schema
  - keyboard
  - contrast
  - visual-regression
humanGate: none
stopConditions:
  - unresolved locked token conflict
completionEvidence: []
```

### Evidence standard

A task is not done because an agent says it is done. Completion evidence must include the relevant combination of:

- Passing command output.
- Parsed schema or manifest.
- Screenshot or rendered artifact.
- Before/after comparison.
- Accessibility/contrast result.
- Clean consumer installation.
- Human decision record.
- Golden registry update.
- Release/package checksum.

## Programme stop gates

1. Do not scale visual work before authority and portability are repaired.
2. Do not mass-build components before taste, strategy, and identity direction are approved.
3. Do not publish Figma as authoritative before canonical tokens and golden references exist.
4. Do not build every channel before one cross-channel identity test passes.
5. Do not let research packages edit Mez tokens directly.
6. Do not enable autonomous mass production before multi-model benchmarks pass.
7. Do not call the system transferable before an unrelated team installs it successfully.
8. Do not promote a candidate core, mark, or reference as locked without a recorded human decision.
9. Do not accept a validator until it passes official fixtures and catches seeded failures.
10. Do not trade distinctiveness for mere compliance, or accessibility for visual preference.

## Definition of done for the end-to-end system

The programme is complete only when all of the following are true.

### Identity

- [ ] Mez is recognisable without relying solely on logo, name, or gradient.
- [ ] Parent, holdco, and products remain distinct and related.
- [ ] Product territories are meaningfully differentiated.
- [ ] Marks, type, cores, monochrome grammar, imagery, icons, diagrams, data, and motion are governed.

### System integrity

- [ ] One canonical source generates every implementation format.
- [ ] Every consequential rule has an ID, state, owner, scope, and version.
- [ ] No manually maintained token mirrors remain.
- [ ] Assets are versioned, hashed, licensed, and complete.
- [ ] Figma, code, docs, and distributions declare the same release version.

### Quality and accessibility

- [ ] Applicable digital outputs meet WCAG AA.
- [ ] Supported layouts reflow from 320px upward.
- [ ] Keyboard, focus, reduced-motion, forced-colour, localization, and RTL cases are tested.
- [ ] Real product proof replaces placeholders.
- [ ] Outputs pass both compliance and design-excellence review.

### Channel completeness

- [ ] Every supported channel has a specification, native source, templates, examples, anti-examples, validator, and export rules.
- [ ] Golden outputs cover web, product UI, ads/social, email, presentations, documents/reports, data, and motion for the agreed release scope.
- [ ] The identity adapts across channels without collapsing into one repeated template.

### LLM readiness

- [ ] Task routing supplies minimal deterministic context.
- [ ] Multiple fresh model families complete benchmark tasks without hidden knowledge.
- [ ] Seeded failures are caught independently.
- [ ] Outputs include provenance receipts.
- [ ] Agents stop on missing, conflicting, unsupported, or unapproved inputs.

### Transfer and adoption

- [ ] A clean team can install and use the system without contacting its author.
- [ ] Consumers pin exact versions.
- [ ] Updates are reviewable, reversible, and documented.
- [ ] No consumer maintains a hidden shadow system.
- [ ] Human and machine consumers receive only the context and packages they need.

### Governance

- [ ] Contributions, exceptions, deprecations, and releases have explicit workflows.
- [ ] Olli is involved only in consequential taste, identity, golden-output, and breaking-release decisions.
- [ ] The system has named ongoing owners.
- [ ] Drift, adoption, exception, accessibility, and benchmark health are monitored.

## Decisions still requiring Olli

These should be batched into the human gates rather than asked one by one:

1. Brand ambition, desired traits, and explicit anti-traits.
2. Reference and anti-reference shortlist.
3. Whether the current Inter/Instrument Serif direction is retained, transformed, or replaced.
4. Final holdco/parent/product mark architecture.
5. Flat versus dimensional core behaviour.
6. Aurora, Prism, and Forge final core assignments.
7. Proprietary monochrome grammar.
8. Product differentiation model.
9. Selected north-star identity direction.
10. Golden cross-channel outputs.
11. Initial release channel scope.
12. Dedicated-repository extraction at the Phase 4 gate.
13. Major release approval.

## Final recommendation

Build Mez Systems as a versioned internal brand operating system, not a larger static brand book.

Use Taste Reverse as the evidence-producing research engine. Use the local repository as declarative truth. Use HTML and code as behavioural truth for responsive and interactive artifacts. Use Figma as the primary expressive exploration and human design surface, then publish it as a versioned companion library. Use human-approved golden outputs as visual truth. Distribute task-scoped, self-contained packages to teams and LLMs.

The human should choose taste, direction, and expensive-to-reverse identity decisions. LLMs and validators should handle repetitive implementation, measurement, testing, packaging, and channel adaptation.

The strategic change is simple:

> Keep a small number of unmistakable Mez signatures, create a richer grammar for variation, and make every output a traceable, validated expression of one governed system.
