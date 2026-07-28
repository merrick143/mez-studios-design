# Phase B · Functional Website Components

Status: canonical 1.0.0 · 46 unanimously kept functional specimens across six families

Task: `TASK-EXP-04-PRODUCT-CARD`

Approved human gate: `H-EXP-04B-CARD-FUNCTIONAL-PROOF`

Decision: `DEC-PRODUCT-COMPONENT-SYSTEM-001`

Production authority: bounded to the approved component design and interaction contracts

Machine contract: `brand-kit/expressions/product-card/phase-b/product-component-pantry.source.json`

Functional review: `brand-kit/workbench/expressions/product-card/phase-b/`

## Blunt decision

The original seven-component Phase B scope was necessary but too narrow. It covered the obvious leaf components—discovery, feature, pricing, checkout, bundle, upsell and mobile summary—but not the product heroes, menus, footers, bento, multi-pricing sections, explainers, comparison patterns and complete flows needed to build a real website.

Phase B is therefore a **functional website component system**:

- fifteen reusable components;
- thirteen product-aware website composition patterns;
- six complete journey fixtures;
- thirty-two unanimously approved Phase A expressions used as visual inputs;
- forty-six surviving functional website specimens across discovery, features, pricing, checkout, bundles, upsells and mobile;
- forty-six unanimously approved specimens in Round 04.

This is not permission to build unrelated art cards or a second Phase A gallery. The approved 32 expressions are the construction grammar underneath the functional contracts. One component contract owns its semantics and behavior; named variants adapt it to different jobs. Patterns compose components. Journeys prove the patterns work together.

The useful idea from 21st.dev was breadth: a designer should be able to review many real marketing and commerce components in context. It was never a request to build a search interface. Round 01 proved the functional inventory but compressed too much of the approved expression language into one repeated card posture. Round 02 overcorrected by displaying all 32 Phase A expressions as separate review candidates. Olli's feedback established the correct boundary: keep the Phase A visual language, remove the duplicate gallery, and judge how convincingly that language performs each functional website job.

## What Phase A contributes

Phase A provides the approved Product Card 02 1.0.0 visual grammar. Phase B applies it to functional website jobs:

- canonical public product name first, extended system name second;
- rounded outer geometry and bounded flat internal joins;
- filled product actions;
- deliberate corner, centred or mark-above Wings placement;
- F8, white, charcoal and contained-dark surface behavior;
- one automatically live Deep Mineral No. 5 core per viewport;
- exact static twins for repeated, reduced-motion and failure contexts;
- equal family geometry and registry-driven future-product behavior;
- the complete positive and negative design evidence in `PRODUCT-CARD-DESIGN-ETHOS.md`.

Round 04 does not render the 32 Phase A survivors as separate bridge specimens. Their 14 landing plates, four product-card anatomies, six bundle relationships and eight website sections remain the approved visual reference set. Each functional specimen names the exact Phase A sources it inherits, then proves that inheritance through its composition, hierarchy, geometry, action treatment and motion allocation.

Phase B may add function, state, responsive behavior and composition. It may not reopen the visual-direction competition, restore killed System Editions or introduce generic SaaS styling as a new design world.

## The five-layer architecture

### 1. Foundations and primitives

Canonical foundations own containers, grids, surfaces, typography, actions, fields, disclosures, feedback, focus, density and responsive profiles. Phase B consumes those contracts; it does not fork them.

### 2. Product-expression adapters

The approved identity and visual ingredients are adapted to functional jobs:

- `ProductIdentity`
- `ProductMaterial`
- `ProductCopyStack`
- `AvailabilityStatus`
- `PriceBlock`
- `FeatureList`
- `ProductAction`
- `SelectionControl`
- `OrderSummary`
- `StickyActionBar`
- `ProofRecordRenderer`

These adapters select a useful expression—plate, full field, portrait, disc, capsule, stack, fan or box—rather than forcing every expression into every component.

### 3. Reusable components

Components own semantic anatomy, applicable state dimensions, container behavior, accessibility and consumer events. They do not own a page layout or make network calls.

### 4. Website composition patterns

Patterns compose components into realistic product-aware sections: heroes, menus, explainers, bento, pricing, checkout, bundle, upsell and footer sections. A pattern defines purpose and hierarchy, not a fixed universal page order.

### 5. Journey fixtures

Journeys prove the same contracts across complete decisions. They are realistic fixtures, not a golden homepage and not production commerce.

## Semantic models behind the rendered components

The component system is data-driven around thirteen models:

| Model | Authority | Job |
|---|---|---|
| `Product` | Canonical registry | Stable identity, public and extended names, summary, availability and gradient assignment. |
| `Availability` | Registry plus consumer | Live, coming soon, waitlist, unavailable and sold-out behavior. |
| `Offer` | Fixture or consumer | One-time, subscription, usage, bundle, enterprise, trial, waitlist, free and add-on offers. |
| `Price` | Fixture or consumer | Amount, currency, cadence, tax status, discount and disclosure. |
| `Plan` | Fixture or consumer | SaaS tier, inclusions, limits, recommendation and billing options. |
| `Bundle` | Fixture or consumer | Included and optional products, savings and selection rules. |
| `LineItem` | Fixture or consumer | Product, bundle, add-on, discount, tax, credit and total rows. |
| `ProofRecord` | Evidence or fixture | Claim, input, mechanism, changed state, result, verification and limitations. |
| `Action` | Component contract | Label, intent, hierarchy, destination or callback and disabled reason. |
| `Media` | Canonical or consumer | Static material, one focal live core, screenshot, proof artifact or no media. |
| `Checkout` | Consumer | Provider and checkout state slots, without embedded payment logic. |
| `CommerceState` | Component contract | Empty, partial, ready, processing, confirmed and failure lifecycle. |
| `MotionAllocation` | Canonical motion rule | One live focal core and exact static allocation everywhere else. |

Only `Product` identity is currently production-authoritative. Phase B examples for prices, tiers, bundles, tax and checkout are visibly illustrative fixtures until an authorised consumer supplies them.

## The fifteen reusable components

| ID | Component | Core variants |
|---|---|---|
| `PC2-B-C01` | `ProductDiscoveryCard` | Compact, standard, portrait, horizontal, featured, selected, coming soon. |
| `PC2-B-C02` | `ProductFeatureCard` | Capability, use case, workflow, integration, annotated media, before/after. |
| `PC2-B-C03` | `ProductProofCard` | Mechanism, customer outcome, aggregate research, metric, integration, security, provenance. |
| `PC2-B-C04` | `ProductFeatureBento` | Mechanism map, workflow, evidence mosaic, product comparison. |
| `PC2-B-C05` | `ProductPricingCard` | One-time digital, SaaS subscription, usage, enterprise, trial, bundle, add-on, waitlist. |
| `PC2-B-C06` | `ProductPlanComparison` | Tier matrix, product matrix, feature difference, mobile disclosure. |
| `PC2-B-C07` | `ProductCheckoutSummary` | Sidebar, card, collapsed, drawer, sticky mobile, receipt. |
| `PC2-B-C08` | `ProductBundleOffer` | Integrated, stack, measured fan, boxed suite, contained dark, comparison. |
| `PC2-B-C09` | `ProductBundleBuilder` | Checklist, guided, compare, desktop aside, mobile sheet. |
| `PC2-B-C10` | `ProductUpsellRow` | Order bump, inline row, cart, upgrade, post-purchase. |
| `PC2-B-C11` | `ProductMobileStickySummary` | Product, pricing, checkout, bundle and upsell receivers. |
| `PC2-B-C12` | `ProductFamilyMatrix` | Catalogue, capability matrix, availability, compact list, future product. |
| `PC2-B-C13` | `ProductMenuItem` | Compact, proof, availability, selected and mobile. |
| `PC2-B-C14` | `ProductFooterCTA` | Single product, family, bundle, contained dark and slim. |
| `PC2-B-C15` | `ProductPurchaseConfirmation` | Digital access, SaaS onboarding, bundle access, receipt and post-purchase offer. |

## The thirteen website patterns

| ID | Pattern | What it proves |
|---|---|---|
| `PC2-B-P01` | Single-product hero | Product-first hierarchy, one proposition and one focal product field. |
| `PC2-B-P02` | Product-family hero | Equal family weight, extensible roster and live-product-first commerce. |
| `PC2-B-P03` | Product mega-menu | Product discovery from global navigation with keyboard-safe mobile behavior. |
| `PC2-B-P04` | Featured-product section | Claim, mechanism and evidence in one realistic placement. |
| `PC2-B-P05` | Product explainer | Sequence, workflow, architecture and comparison without magical diagrams. |
| `PC2-B-P06` | Feature/proof bento | Typed cell relationships rather than decorative micro-card grids. |
| `PC2-B-P07` | Product-family shelf | Equal sibling geometry, mixed availability and vertical mobile catalogue. |
| `PC2-B-P08` | Multi-pricing section | One-time, SaaS, multi-product and comparison-led pricing decisions. |
| `PC2-B-P09` | Product comparison | Products, plans, features and before/after with complete mobile access. |
| `PC2-B-P10` | Checkout layout | Consumer-owned fields and payment slots around a stable Mez summary. |
| `PC2-B-P11` | Bundle section | Fixed offer, builder, comparison, contained dark and mobile summary. |
| `PC2-B-P12` | Upsell/cross-sell section | Relevant additions with explicit consent and price delta. |
| `PC2-B-P13` | Product footer | Full, slim, product, commerce and legal page closure. |

Product-aware menus and footers are in scope because they consume the same product system. Phase B does not claim authority over every generic navigation, account or application-shell primitive.

## The six complete journeys

1. **Multi-product discovery** — mega-menu → family hero → family shelf → comparison → one product.
2. **One-time digital purchase** — discovery → single offer → checkout → processing → access → receipt.
3. **SaaS tier selection** — multi-plan pricing → billing interval → comparison → selection → checkout → onboarding.
4. **Configurable bundle purchase** — bundle offer → builder → selection recovery → sticky summary → checkout → access.
5. **Mixed availability and waitlist** — live and coming-soon family → waitlist action → loading/error → confirmation.
6. **Mobile purchase, upsell and confirmation** — discovery → sticky summary → collapsed checkout → optional addition → processing → confirmation.

These journeys deliberately include commercial models that Mez may need in the future. They do not assert that a current Mez product has those prices or business models.

## Digital product versus SaaS

The component silhouette may be related; the commercial semantics are not interchangeable.

### One-time digital product

- Use one price and one-time language.
- State what is delivered and how access works.
- Do not show `/month`, renewal, plan tiers or billing toggles.
- Checkout ends in digital access and receipt behavior.

### SaaS

- Price requires a billing cadence and renewal disclosure.
- Plan, limits, seats, trial and billing interval may be relevant.
- Multi-tier comparison must preserve complete criteria on mobile.
- Confirmation leads to onboarding or account handoff.

### Enterprise, waitlist and unavailable

- Enterprise may replace purchase with contact or demo intent.
- Waitlist is availability, not a fake disabled purchase button.
- An unavailable offer explains why and provides a truthful recovery route.

## Bento is a layout contract, not a style

`ProductFeatureBento` is valid only when every cell declares one of these jobs:

- product;
- proof;
- workflow;
- metric;
- media;
- integration;
- quote;
- action.

The grid must have a meaningful hierarchy, one reading order, one optional focal cell and a complete compact linearization. Empty filler cells, arbitrary spans, generic icon cards and multiple live gradient cells fail validation.

## State applicability

Phase B uses state dimensions rather than forcing every state onto every component:

- **Interaction:** rest, hover, focus-visible, pressed, disabled.
- **Choice:** unselected, selected.
- **Availability:** available, coming soon, unavailable.
- **Async:** idle, loading, error, success.
- **Commerce:** empty, partial, ready, processing, confirmed.

An interactive component proves interaction. A selectable component proves choice. An async owner proves loading and recovery. A purchase owner proves processing and double-submit prevention. Static feature cards do not fabricate error or success states merely to fill a matrix.

## Responsive and accessibility proof

Every applicable component is tested at:

- viewports: 320, 375, 430, 768, 1024, 1280 and 1440;
- containers: 240, 320, 480, 640, 960 and 1160;
- compact, medium, expanded and wide receiver profiles.

Required stress cases include zero, one, two, five, six and seven products; long and localised copy; missing media; unpriced offers; currency expansion; 200% zoom; keyboard only; reduced motion; WebGL failure; unavailable products; loading, processing and recovery.

The component responds to its container before it assumes a page viewport. Mobile preserves source order, makes the product family vertical, keeps essential comparison information available without swipe-only access, uses 48px touch targets and introduces sticky summaries only after purchase intent.

## Motion allocation

- One isolated focal `ProductMaterial` plate may run Deep Mineral automatically.
- Repeated products, pricing, comparisons, checkout, upsells, menus, footers and sticky summaries remain exact static twins. A focused bundle stack may cycle which static card is visually foremost, but its Wings, type and geometry stay fixed and it does not allocate another Living Core.
- Wings, type, controls and layout never move.
- There is no animate button.
- Reduced motion, no WebGL and runtime failure use the exact static twin without layout shift.

## Review programme

### PB0 · Models and component architecture — complete candidate

The internal source contract defines reusable semantics and composition rules behind the implemented specimens.

### PB1 · Functional breadth · Round 02 — feedback complete

Round 02 renders 80 independently reviewable specimens across ten families. It begins with 32 applications of every unanimously approved Phase A expression:

- `B-A-QC01–QF03` — 14 landing expressions mapped to launch, campaign, feature, waitlist and compact placements;
- `B-A-FC01–PO02` — four full-field and portrait product-card anatomies mapped to discovery, selection, pricing and checkout jobs;
- `B-A-ST01–BX02` — six stack, single, fan and boxed product relationships mapped to bundle and upsell jobs;
- `B-A-SH01–BO02` — eight complete website compositions mapped to hero, family, explainer and system-offer jobs.

The original 48 functional specimens remain present after those expression applications:

- `B-DS01–08` — discovery, product navigation and family selection;
- `B-FT01–10` — features, proof, bento and explainers;
- `B-PR01–10` — digital, SaaS, multi-tier and comparison pricing;
- `B-CK01–08` — checkout, summaries, processing and confirmation;
- `B-BU01–08` — bundles, builders, upsells and cross-sells;
- `B-MB01–04` — mobile summary, product footer and purchase continuity.

Round 02 feedback kept all 32 Phase A sources, requested revision across the functional layer and killed only `B-FT04`. The strongest positive functional signals were the product-aware footer, the full-bleed bento idea, the configurable bundle, the focused product stack and the side-by-side bundle comparison. The main failures were the separate inheritance gallery, generic or congested SaaS composition, undersized actions, forced Wings, inset bento cells and box-heavy integration treatments.

### PB2 · Feedback convergence · Round 03 — feedback complete

The Phase A keeps survive as visual inputs rather than duplicate candidates. `B-FT04` disappears. The 47 surviving functional specimens are rebuilt directly from the approved grammar and remain individually reviewable across six families:

- `B-DS01–08` — discovery, product navigation and family selection;
- `B-FT01–03` and `B-FT05–10` — features, proof, authored bento and explainers;
- `B-PR01–10` — digital, SaaS, multi-tier and comparison pricing;
- `B-CK01–08` — checkout, summaries, processing and confirmation;
- `B-BU01–08` — bundles, builders, upsells and cross-sells;
- `B-MB01–04` — mobile product, pricing, checkout and confirmation continuity.

Revisions follow the named dimensions in `round-02-feedback.json`: centred live identity for the single hero, less congested family discovery, a marketing rather than table-like starting-point comparison, full-bleed bento material, real integration marks, no Wings on the full-overlay enterprise offer, and stronger animated/static bundle relationships. The survivors are then composed into all six journeys.

Round 03 received 11 keeps, 35 revisions and one kill. The kept champions are the single and family heroes, featured split, digital and SaaS checkout, processing and recoverable-error states, configurable bundle, focused stack, bundle comparison and checkout order bump. `B-FT06` is killed and removed alongside the earlier `B-FT04`.

### PB2 · Feedback convergence · Round 04 — unanimously approved

Round 04 preserved the 11 champions, rebuilt the 35 revisions and received keep for all 46 functional specimens across the same six families:

- `B-DS01–08` — eight discovery and navigation candidates;
- `B-FT01–03`, `B-FT05` and `B-FT07–10` — eight feature, proof, card-bento and explainer candidates;
- `B-PR01–10` — ten digital, SaaS, comparison and availability candidates;
- `B-CK01–08` — eight checkout, processing, recovery and confirmation candidates;
- `B-BU01–08` — eight bundle, builder and upsell candidates;
- `B-MB01–04` — four mobile decision and continuity candidates.

The named Round 04 convergence dimensions are equal sibling and commercial-card geometry, a conventional premium bento made from actual Phase A-derived cards, real locally sourced integration assets, explicit use of a Phase A card in before/after explanation, automatic motion for the focal waitlist material, and controlled refinement rather than reset for the product-aware footer and operating-run story. Unnoted revisions improve the same approved hierarchy and component utility; they do not invent a new visual world.

### PB3 · State and responsive proof — closed with explicit follow-up

Representative state, interaction, one-live-core, static-fallback, equal-geometry, mobile-composition, export and desktop-overflow proof passed before approval. Exhaustive consumer-specific container, keyboard, 200% zoom, content-stress, missing-media and recovery matrices continue under EXP-08 and consumer proof. This follow-up cannot silently change the approved component grammar.

### PB4 · Candidate lock — complete

Only validator-passing survivors remain. Olli approved all 46 as keep and closed `H-EXP-04B-CARD-FUNCTIONAL-PROOF`; `DEC-PRODUCT-COMPONENT-SYSTEM-001` records canonical 1.0.0.

## Explicit exclusions

- live pricing or commercial authority;
- production Stripe fields, keys, endpoints or payment logic;
- a golden homepage choice;
- generic application UI and dashboards;
- Figma production library;
- consumer repository migration;
- System Editions and trading-card collector framing;
- new product names or gradient assignments.

## Next action

Product Card 02 is closed. Plan `EXP-05` Trading Card and full-field expression as a new bounded task with its own contract, review surface and human gate. Inherit the approved Product Card 02 ethos and foundations, but do not restore Product Card 02 System Editions or reopen the 46 approved functional specimens without a new named decision.
