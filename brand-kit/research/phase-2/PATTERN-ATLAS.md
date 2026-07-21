# Phase 2 pattern atlas

Status: `UNAPPROVED_RESEARCH`
Prepared: 20 July 2026
Evidence base: Notion, Linear, Stripe, ElevenLabs, Ramp
Purpose: convert observed source evidence into testable mechanisms without importing source expressions

## How to use this atlas

This atlas is a bridge between evidence and experiments. It is not a visual direction, token source, component library, style guide, or production specification.

Every pattern separates two things:

- **Mechanism:** the abstract relationship that may solve a Mez problem.
- **Source expression:** the source-owned visual, verbal, product, or interaction treatment that demonstrated the mechanism and must not be copied.

A pattern may move forward only when it:

1. answers a named Mez requirement;
2. combines evidence from at least two sources or one source plus a direct Mez operational requirement;
3. is translated into an original Mez hypothesis;
4. is prototyped with real or explicitly staged Mez content;
5. passes the stated tests and originality boundary;
6. receives approval at the named human gate.

## Pattern maturity scale

| Maturity | Meaning |
| --- | --- |
| `M0 observed` | Seen in one source and not eligible for promotion |
| `M1 corroborated` | Evidenced by at least two sources as a mechanism |
| `M2 prototyped` | Translated into an original Mez prototype |
| `M3 validated` | Passed functional, cross-channel, accessibility, and originality tests |
| `M4 approved` | Human-approved for the canonical system |

All patterns in this document are currently `M1 corroborated`. None is approved.

## Promotion gates

- `H2`: approve structural and visual territories after monochrome and originality testing.
- `H3`: approve interaction, motion, accessibility, and product-family behaviour.
- `H4`: approve machine-readable contracts, Figma and code mappings, template rules, LLM context, governance, and validators.

## Atlas index

| Pattern | Group | Core question | Confidence | Maturity | Gate |
| --- | --- | --- | --- | --- | --- |
| `PAT-REC-01` | Recognition | Can identity survive removal of obvious assets? | High | M1 | H2 |
| `PAT-REC-02` | Recognition | Can operating behaviour become recognisable? | Medium-high | M1 | H2 |
| `PAT-POR-01` | Portfolio | What creates family coherence? | High | M1 | H2 |
| `PAT-POR-02` | Portfolio | What makes products meaningfully distinct? | High | M1 | H2 |
| `PAT-PRF-01` | Proof | How does a claim become inspectable? | High | M1 | H2 |
| `PAT-PRF-02` | Proof | How should different evidence classes be handled? | High | M1 | H2 |
| `PAT-PRF-03` | Proof | How can proof become a publishing system? | High | M1 | H2 |
| `PAT-DEN-01` | Density | How should detail change by receiver intent? | High | M1 | H2 |
| `PAT-DEN-02` | Density | How can density rise without clutter? | High | M1 | H2 |
| `PAT-MOT-01` | Motion | What should motion communicate? | Medium-high | M1 | H3 |
| `PAT-MOT-02` | Motion | How should human and agent ownership be shown? | High | M1 | H3 |
| `PAT-PORT-01` | Portability | What must remain stable across renderers? | High | M1 | H4 |
| `PAT-PORT-02` | Portability | How can variation remain bounded? | High | M1 | H4 |
| `PAT-TRU-01` | Trust and provenance | How is an output made trustworthy? | High | M1 | H3 and H4 |
| `PAT-TRU-02` | Trust and provenance | How should uncertainty and evidence class appear? | High | M1 | H3 and H4 |

## Recognition

### `PAT-REC-01` Distributed recognition stack

**Mechanism**

Recognition is distributed across composition, type hierarchy, relationship geometry, proof framing, density transition, language, and state behaviour. Removing one device does not collapse authorship.

**Cross-source evidence**

- Notion: `NTN-E01`, `NTN-E02`, `NTN-E03`.
- Linear: `LIN-E01`, `LIN-E02`, `LIN-E03`.
- Stripe: `STRIPE-E-001`, `STRIPE-E-002`.
- Ramp: `RAMP-E-001`, `RAMP-E-002`.

**Source expressions, not transferable**

Notion's editorial black-and-white hero and inline software-like object, Linear's numbered figure language and restrained dark shell, Stripe's ruled grid and diagonal transitions, and Ramp's green action colour and operational activity treatment remain source property.

**Applicability**

- Brand-light or logo-free product demonstrations.
- Small ads and email modules where the full identity cannot appear.
- Reports, charts, and generated outputs that need recognisable authorship.
- Product UI where decoration must remain subordinate to work.

**Non-applicability**

- Legal or partner contexts where an explicit Mez mark is required.
- One-off experimental art where deliberate family recognition is not an objective.
- Cases where accessibility or legibility would be reduced to preserve a stylistic behaviour.

**Failure modes**

- Counting generic sans-serif type, cards, whitespace, and dark mode as distinctive behaviours.
- Repeating one composition so rigidly that every output becomes a reskin.
- Using four weak signals instead of a coherent relationship among them.
- Treating wings or gradient as one of the required non-colour behaviours.

**Originality boundary**

The Mez stack must encode Mez's own operating model. It cannot reproduce a selected source's characteristic asset combination, spatial sequence, colour role, typography, interface chrome, or editorial notation.

**Confidence:** high. Four sources show recognition distributed across multiple behaviours. Causal recognition still needs blind testing.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** remove wings, names, product names, gradients, and serif accents from five channel outputs. Test whether reviewers group them as one author and whether any source brand is named as the template.
**Promotion gate:** `H2`, after above-chance family grouping, accessibility review, and an originality review with no dominant source attribution.

### `PAT-REC-02` Operating behaviour as identity

**Mechanism**

The way information changes can become recognisable. A repeated grammar for intake, transformation, validation, exception, result, and decision can carry identity across static and interactive media.

**Cross-source evidence**

- Linear: `LIN-E03`, `LIN-E06`, `LIN-E07`, `LIN-E11`.
- ElevenLabs: `ELV-E01`, `ELV-E03`, `ELV-E13`, `ELV-E14`.
- Ramp: `RAMP-E-002`, `RAMP-E-004`, `RAMP-E-011`.
- Notion: `NTN-E09`, `NTN-E11`, `NTN-E20`.

**Source expressions, not transferable**

Linear's product-stage numbering, ElevenLabs' pause association and audio-derived graphics, Ramp's live-looking finance activity, and Notion's block and slash-command metaphors cannot become Mez signatures.

**Applicability**

- AI orchestration, agent activity, workflow explanation, and before-to-after proof.
- Motion storyboards and static sequences.
- Reports and campaign modules that explain how an outcome was produced.

**Non-applicability**

- Purely emotional brand moments where no system behaviour is being claimed.
- Decorative motion or illustration that is not intended to explain state.
- Claims where the real mechanism cannot safely or truthfully be disclosed.

**Failure modes**

- Making every surface look like a workflow diagram.
- Using fake activity to imply live product behaviour.
- Encoding a process so densely that the audience cannot see the outcome.
- Mistaking arrows, nodes, or progress bars for an ownable behaviour.

**Originality boundary**

Mez must derive the sequence, objects, and transition logic from its own system. Generic workflow shapes may be used only when combined into a distinct Mez evidence grammar that survives source-comparison review.

**Confidence:** medium-high. The operational principle is strongly supported, while logo-free recognition from behaviour remains an untested inference.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** define a Mez-native six-state workflow and express it as a product UI, homepage sequence, report panel, email update, and static ad.
**Promotion gate:** `H2` for structural identity, with later `H3` approval for interactive behaviour.

## Portfolio

### `PAT-POR-01` Shared semantic chassis

**Mechanism**

A family remains coherent when products share stable parent attribution, approved nouns and verbs, primitive anatomy, state semantics, control logic, accessibility behaviour, and evidence anatomy.

**Cross-source evidence**

- Notion: `NTN-E04`, `NTN-E06`, `NTN-E07`, `NTN-E18`.
- Linear: `LIN-E04`, `LIN-E05`.
- Stripe: `STRIPE-E-003`, `STRIPE-E-005`, `STRIPE-E-007`.
- ElevenLabs: `ELV-E04`, `ELV-E06`, `ELV-E15`.
- Ramp: `RAMP-E-005`, `RAMP-E-006`, `RAMP-E-012`.

**Source expressions, not transferable**

No source's product names, marks, navigation, object vocabulary, shell, icon system, or extension model may be reused. The transferable element is the existence of a shared contract, not its source implementation.

**Applicability**

- AI OS, Aurora, Prism, and Forge.
- Parent and product endorsement rules.
- Components and patterns that appear across multiple products or channels.
- LLM generation that must preserve family relationships.

**Non-applicability**

- A product-specific proof object that has no meaningful family equivalent.
- Campaign art that intentionally sits outside product navigation while still respecting identity and accessibility.
- Shared visuals whose only justification is engineering convenience.

**Failure modes**

- Defining the chassis as one page template.
- Sharing appearance while product nouns and states drift.
- Making every product use the same density, proof form, or motion.
- Creating an abstract design language with no mapping to real product objects.

**Originality boundary**

The chassis must be specified from Mez requirements and content. Source shells, cards, grids, navigation patterns, and naming logic are evidence that contracts can exist, not assets for reconstruction.

**Confidence:** high. All five sources show meaningful shared systems below product variation.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** define the minimum shared chassis, then render one neutral component, one proof record, and one state sequence for all four products without colour.
**Promotion gate:** `H2`, after family recognition, accessibility, and product-distinction tests.

### `PAT-POR-02` Product-owned territory contract

**Mechanism**

Each product owns a primary user and job, dominant information object, action model, proof primitive, result type, density range, state-transition emphasis, and campaign posture. Colour and product name reinforce this territory but do not define it.

**Cross-source evidence**

- Notion: `NTN-E05`, `NTN-E06`, `NTN-E07`, `NTN-E08`, `NTN-E15`.
- ElevenLabs: `ELV-E04`, `ELV-E05`, `ELV-E06`.
- Stripe: `STRIPE-E-003`, `STRIPE-E-005`, `STRIPE-E-006`.
- Ramp: `RAMP-E-004`, `RAMP-E-005`, `RAMP-E-006`.
- Linear: `LIN-E04`, `LIN-E05`.

**Source expressions, not transferable**

Notion's pages, messages, calendar, and block model, ElevenLabs' colour and motif allocation, Stripe's local-product indicator system, Ramp's finance cards, and Linear's workflow chapters must not be recast as Mez products.

**Applicability**

- Product-family design, product launches, sales material, and campaigns.
- Choosing product-specific component variants and motion roles.
- Evaluating whether a new product belongs in the family.

**Non-applicability**

- Parent-only corporate material.
- Shared platform controls where product variation would reduce learnability.
- Technical states that must remain semantically identical across products.

**Failure modes**

- Differentiating products only by gradient, accent colour, name, and screenshot.
- Creating four unrelated brands with no common semantics.
- Inventing a visual territory before defining the job and evidence.
- Forcing one motif into every channel regardless of task.

**Originality boundary**

Each Mez territory must originate from the product's own work and evidence. It cannot borrow a source product's palette-motif pairing, dominant object, or campaign formula.

**Confidence:** high. All five sources differentiate work through semantic or operational territory.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** complete an eight-axis territory card for every Mez product and render a monochrome, nameless contact sheet.
**Promotion gate:** `H2`, only if reviewers can distinguish all four products while still grouping them as one family.

## Proof

### `PAT-PRF-01` Claim-to-proof adjacency

**Mechanism**

A claim sits beside the input, mechanism, changed state, output, result, control, or verification that makes it inspectable. The proof object directly answers the adjacent claim.

**Cross-source evidence**

- Notion: `NTN-E09`, `NTN-E10`, `NTN-E11`, `NTN-E12`.
- Linear: `LIN-E06`, `LIN-E07`.
- Stripe: `STRIPE-E-004`, `STRIPE-E-012`.
- ElevenLabs: `ELV-E07`, `ELV-E08`, `ELV-E09`, `ELV-E10`.
- Ramp: `RAMP-E-002`, `RAMP-E-003`, `RAMP-E-004`, `RAMP-E-008`, `RAMP-E-009`.

**Source expressions, not transferable**

No source screenshot, sample data, metric, customer, interface composition, media player, or demonstration sequence may be reproduced. Only the adjacency and evidence relationship are candidates.

**Applicability**

- Product and capability marketing.
- Ads, email, reports, case studies, release notes, and product onboarding.
- AI claims that need to show bounded action and human control.

**Non-applicability**

- Pure brand awareness where no capability claim is made.
- Confidential mechanisms that cannot be shown safely.
- Claims with no substantiated evidence, which should be removed rather than decorated.

**Failure modes**

- Decorative interface frames unrelated to the claim.
- One generic montage supporting several incompatible claims.
- Staged UI presented as a measured customer result.
- A proof object that needs a long caption to explain its relevance.

**Originality boundary**

Use real Mez objects and states. Staged content must be labelled internally and must not imply a live customer result. The composition cannot recreate a source's characteristic claim and screenshot arrangement.

**Confidence:** high. All five sources repeatedly use adjacent, inspectable evidence.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** select one real Mez claim and create a single proof record containing input, mechanism, changed state, result, source, and control. Render it in five channels.
**Promotion gate:** `H2`, after evidence accuracy, content integrity, and cross-channel retention review.

### `PAT-PRF-02` Evidence-class separation

**Mechanism**

System activity, literal mechanism, customer outcome, and aggregate research are visibly and semantically distinct. One class never impersonates another.

**Cross-source evidence**

- Ramp: `RAMP-E-002`, `RAMP-E-003`, `RAMP-E-007`, `RAMP-E-008`, `RAMP-E-009`, `RAMP-E-010`.
- Stripe: `STRIPE-E-004`, `STRIPE-E-010`, `STRIPE-E-012`.
- Linear: `LIN-E06`, `LIN-E07`, `LIN-E08`.
- Notion: `NTN-E09`, `NTN-E12`, `NTN-E13`.
- ElevenLabs: `ELV-E08`, `ELV-E09`.

**Source expressions, not transferable**

Ramp's research cards and savings language, Stripe's company metrics, Linear's activity feed, Notion's workspace examples, and ElevenLabs' performance counters are not reusable proof assets.

**Applicability**

- Any output containing numbers, customer attribution, activity, research, or simulated UI.
- Reports and LLM-generated summaries where provenance can drift.
- Product marketing that combines demonstration and outcome evidence.

**Non-applicability**

- Non-claim decorative material.
- Purely instructional UI labels that do not assert an outcome.

**Failure modes**

- A live-looking ticker with no declared source or status.
- A testimonial used as proof of how the product works.
- A staged interface presented as current system activity.
- Aggregate research without sample, method, date, or limitation.

**Originality boundary**

Mez must create its own evidence markers and terminology. They may not visually mimic a source's badges, report cards, data displays, or interface states.

**Confidence:** high. Evidence-class distinctions are well supported across all sources and directly answer a Mez trust risk.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** label a mixed set of Mez claims by evidence class, then test whether independent reviewers identify source, status, and limits without additional explanation.
**Promotion gate:** `H2` for visible grammar, with `H4` required for machine-readable enforcement.

### `PAT-PRF-03` Proof as a publishing system

**Mechanism**

Evidence is maintained across launches, changelogs, research, documentation, reports, help content, and product states using stable objects and an explicit update rhythm.

**Cross-source evidence**

- Linear: `LIN-E08`, `LIN-E12`.
- Ramp: `RAMP-E-007`, `RAMP-E-008`, `RAMP-E-009`, `RAMP-E-010`, `RAMP-E-011`.
- Notion: `NTN-E13`, `NTN-E17`, `NTN-E19`, `NTN-E20`.
- Stripe: `STRIPE-E-009`, `STRIPE-E-010`, `STRIPE-E-011`, `STRIPE-E-012`.

**Source expressions, not transferable**

The sources' release formats, report identities, editorial structures, research card styles, and documentation layouts remain theirs.

**Applicability**

- Mez release notes, reports, case studies, research, product documentation, and campaign proof.
- Long-lived claims that need refresh and deprecation behaviour.
- LLM contexts that require current evidence rather than memorised copy.

**Non-applicability**

- Temporary internal exploration with no downstream claim.
- Sensitive evidence that cannot be published or safely summarised.

**Failure modes**

- Treating a launch page as the only source of product truth.
- Republishing inconsistent numbers across channels.
- Letting outdated claims remain available to LLMs.
- Producing research as content marketing without method and limitations.

**Originality boundary**

Mez publishing formats must derive from its evidence model and audience needs. Source editorial identities and report compositions cannot be used as templates.

**Confidence:** high. Four sources show durable proof channels tied to stable product objects.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** create one versioned evidence record and publish it as a release entry, product proof module, report excerpt, and LLM context fragment.
**Promotion gate:** `H4`, after versioning, expiration, source-of-truth, and cross-channel consistency tests.

## Density

### `PAT-DEN-01` Receiver-led density modes

**Mechanism**

The same truth is compressed according to receiver intent and inspection time. Executive, operational, promotional, lifecycle, and analytical modes retain different depths but do not invent different facts.

**Cross-source evidence**

- Notion: `NTN-E14`, `NTN-E15`, `NTN-E17`.
- Linear: `LIN-E09`, `LIN-E10`.
- Stripe: `STRIPE-E-010`, `STRIPE-E-011`.
- ElevenLabs: `ELV-E11`, `ELV-E12`.
- Ramp: `RAMP-E-007`, `RAMP-E-008`, `RAMP-E-009`, `RAMP-E-010`.

**Source expressions, not transferable**

No source's page rhythm, card density, report layout, documentation shell, or information visualisation is a Mez density template.

**Applicability**

- Website, product UI, ad, email, sales material, and report transformation.
- Responsive and small-format design.
- LLM generation where output length and evidence depth vary.

**Non-applicability**

- Safety-critical details that cannot be omitted.
- Legal disclosures and required methodology.
- Cases where compression would change the evidence class or meaning.

**Failure modes**

- Rewriting facts separately for each channel.
- Treating low density as large type and empty space only.
- Removing source, qualification, or uncertainty from compact formats.
- Putting report density into an ad or promotional density into an analytical report.

**Originality boundary**

Density rules must specify retained meaning, not visual imitation. Mez cannot use a source's card, table, editorial, or report composition as the default renderer.

**Confidence:** high. All five sources adapt presentation depth to task and channel.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** transform one proof record into five density modes and measure information loss, scan path, comprehension, and action clarity.
**Promotion gate:** `H2` for visual modes and `H4` for transformation rules.

### `PAT-DEN-02` Calm shell, concentrated evidence

**Mechanism**

Low-competition framing establishes orientation, then detail concentrates around the object under evaluation. Shell hierarchy stays stable while evidence density changes.

**Cross-source evidence**

- Linear: `LIN-E09`, `LIN-E10`.
- Notion: `NTN-E14`, `NTN-E16`.
- ElevenLabs: `ELV-E11`, `ELV-E12`.
- Stripe: `STRIPE-E-010`, `STRIPE-E-011`.

**Source expressions, not transferable**

Linear's dimmed sidebars, Notion's exact adjacency treatment, ElevenLabs' media layouts, and Stripe's documentation or editorial shell cannot be duplicated.

**Applicability**

- Dense product views and reports.
- Long marketing pages that move from orientation to evaluation.
- Interfaces where operational scanning and executive comprehension coexist.

**Non-applicability**

- Emergency or exception states that require immediate prominence.
- Small formats with only one proof unit.
- Content whose hierarchy is genuinely flat.

**Failure modes**

- Lowering contrast below accessibility thresholds.
- Hiding essential controls to create visual calm.
- Allowing dense evidence to lose grouping and priority.
- Applying uniform spacing where semantic neighbours require compression.

**Originality boundary**

Mez must define its own hierarchy and adjacency rules from content semantics. Exact source contrast, spacing, shell, and component treatments are excluded.

**Confidence:** high. Multiple sources explicitly stage or document density transitions.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** prototype one executive-to-operational surface with three evidence concentrations and test scanning, comprehension, and keyboard order.
**Promotion gate:** `H2`, with accessibility and responsive checks required.

## Motion

### `PAT-MOT-01` Semantic state motion

**Mechanism**

Motion communicates state meaning: preparing, active, waiting, changed, verified, exception, handed off, complete, or reversible. Static and reduced-motion equivalents carry the same meaning.

**Cross-source evidence**

- Linear: `LIN-E07`, `LIN-E11`.
- ElevenLabs: `ELV-E03`, `ELV-E10`, `ELV-E13`, `ELV-E14`.
- Notion: `NTN-E12`, `NTN-E20` supports logged and reversible system state, although public motion behaviour was not measured.

**Source expressions, not transferable**

ElevenLabs' playback semantics, wave-like media behaviour, kinetic type, and audio synchronisation, plus Linear's agent-session and workflow presentation, remain source expressions.

**Applicability**

- Product UI and demonstrations.
- Marketing sequences that explain transformation.
- Agent, generation, verification, and exception states.
- Static storyboard systems that need later animation.

**Non-applicability**

- Ambient backgrounds with no state meaning.
- Situations where motion would impair comprehension or access.
- Decorative logo animation presented as proof of intelligence.

**Failure modes**

- Adding glow, particles, or orbiting forms without semantic work.
- Encoding status by movement alone.
- Animating before state naming and reduced-motion behaviour exist.
- Using constant movement that obscures exception or completion.

**Originality boundary**

Motion must be authored from Mez states and objects. No source timing, easing, transition composition, waveform, playback metaphor, or agent animation may be inferred or copied.

**Confidence:** medium-high. State semantics are strongly supported, but durations, easing, responsive motion, and accessibility behaviour were not captured.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** storyboard eleven shared Mez states in animated, static, and reduced-motion forms before specifying any motion values.
**Promotion gate:** `H3`, after comprehension, interruption, reduced-motion, performance, and originality tests.

### `PAT-MOT-02` Ownership and handoff choreography

**Mechanism**

Human and system work is communicated through explicit current owner, permission, interruption, review, continuation, and rollback states.

**Cross-source evidence**

- ElevenLabs: `ELV-E09`, `ELV-E10`, `ELV-E14`, `ELV-E17`.
- Linear: `LIN-E06`, `LIN-E07`, `LIN-E11`.
- Notion: `NTN-E12`, `NTN-E20`.

**Source expressions, not transferable**

ElevenLabs' studio timeline and turn-taking interface, Linear's coding-session feed, and Notion's run and workspace treatments cannot be recreated.

**Applicability**

- Agent execution, approvals, generated artefacts, escalation, review, and recovery.
- Marketing proof that claims human control.
- Email or report updates that describe ownership changes.

**Non-applicability**

- Fully manual workflows with no ownership transition.
- Background automation that has no meaningful user intervention point, unless failure or audit states still require one.

**Failure modes**

- A human-in-the-loop claim with no visible intervention point.
- Confusing assigned owner with current actor.
- Handoff motion that hides what changed.
- No path for interruption, rejection, or rollback.

**Originality boundary**

Mez must use its own role, permission, state, and artefact model. Source avatars, timelines, activity feeds, control layouts, and chat sequences are excluded.

**Confidence:** high. Three sources provide direct evidence for permissions, traceability, intervention, and reversal.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** prototype successful execution, interrupted execution, recoverable failure, human correction, and resumption using one real Mez workflow.
**Promotion gate:** `H3`, followed by `H4` validation of event and permission contracts.

## Portability

### `PAT-PORT-01` Portable semantic object contract

**Mechanism**

Every reusable object has a stable ID, purpose, supported claims, required content, states, permissions, relationships, accessibility behaviour, channel adaptations, allowed transformations, prohibited transformations, provenance, version, and deprecation state.

**Cross-source evidence**

- Notion: `NTN-E18`, `NTN-E19`, `NTN-E20`.
- Stripe: `STRIPE-E-006`, `STRIPE-E-007`, `STRIPE-E-008`, `STRIPE-E-009`.
- ElevenLabs: `ELV-E15`, `ELV-E16`, `ELV-E17`.
- Ramp: `RAMP-E-010`, `RAMP-E-011`, `RAMP-E-012`, `RAMP-E-013`.
- Linear: `LIN-E12`, `LIN-E13`, `LIN-E14`.

**Source expressions, not transferable**

No source's schema, API, component name, documentation layout, Figma library, implementation, or object model may be copied. Public evidence does not reveal all private architecture.

**Applicability**

- Components, patterns, proof records, templates, charts, generated modules, and brand architecture.
- Figma, code, HTML references, creative tooling, and LLM context.
- Team-to-team pack transfer and versioned ingestion.

**Non-applicability**

- Unique, non-reusable artwork with no system role.
- Early visual exploration before a pattern's purpose is understood.
- Source material that cannot legally or operationally enter a shared registry.

**Failure modes**

- Figma as the only source of truth.
- Code and prompt schemas that use different names for the same object.
- Tokens without semantic intent or validation.
- An enormous contract that lower-tier models and humans cannot apply.
- Version changes without migration or deprecation guidance.

**Originality boundary**

The contract structure must reflect Mez's products, rights, and workflow. Source schema details and component APIs are not available and must not be reverse-engineered into a clone.

**Confidence:** high for the need for stable semantics. Medium for any claim about the sources' private Figma-to-code architecture.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** encode one proof component in a machine-readable contract, human guide, HTML reference, Figma mapping plan, LLM context, and validator.
**Promotion gate:** `H4`, after one human and two different LLMs produce semantically equivalent outputs without hidden context.

### `PAT-PORT-02` Bounded variation by relationships

**Mechanism**

Templates compose typed objects through explicit relationship, hierarchy, density, and responsive rules. Variation is allowed inside named bounds instead of relying on fixed pages or unlimited generation.

**Cross-source evidence**

- Notion: `NTN-E03`, `NTN-E16`, `NTN-E18`.
- Stripe: `STRIPE-E-006`, `STRIPE-E-007`, `STRIPE-E-008`.
- Linear: `LIN-E09`, `LIN-E10`, `LIN-E13`.
- ElevenLabs: `ELV-E12`, `ELV-E15`, `ELV-E16`.

**Source expressions, not transferable**

Notion's adjacency system and blocks, Stripe's extension rules, Linear's shell and integrations, and ElevenLabs' platform identities cannot become Mez implementation templates.

**Applicability**

- LLM-generated pages, ads, emails, reports, and campaign modules.
- Responsive composition and content-aware spacing.
- Product-family variants that share anatomy but not exact layout.

**Non-applicability**

- One-off art direction where deliberate manual composition is the outcome.
- Safety or legal modules whose structure must remain fixed.
- Cases with too little evidence to define a meaningful rule.

**Failure modes**

- One template repeated across every channel.
- Unlimited generative layouts that lose identity and hierarchy.
- Responsive rules based only on viewport width, ignoring content type.
- Too many allowed variants for humans or models to choose reliably.

**Originality boundary**

Relationship rules must be derived from Mez content and tested output needs. Exact source spacing, component anatomy, extension methods, and responsive behaviours are excluded.

**Confidence:** high. Four sources provide evidence for semantic composition and constrained extension.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** give the same semantic record to one human and two LLMs with bounded composition choices, then compare consistency, useful variation, and error rate.
**Promotion gate:** `H4`, after determinism, flexibility, accessibility, and failure-recovery tests.

## Trust and provenance

### `PAT-TRU-01` Visible control and provenance anatomy

**Mechanism**

Trust is represented through visible source, status, timestamp, owner, permission, run history, verification, human decision, reversal, and exception fields. These are design primitives, not hidden governance metadata.

**Cross-source evidence**

- Notion: `NTN-E12`, `NTN-E19`, `NTN-E20`.
- Linear: `LIN-E06`, `LIN-E07`.
- ElevenLabs: `ELV-E09`, `ELV-E10`, `ELV-E17`.
- Ramp: `RAMP-E-007`, `RAMP-E-008`, `RAMP-E-009`, `RAMP-E-011`, `RAMP-E-013`.
- Stripe: `STRIPE-E-007`, `STRIPE-E-009`, `STRIPE-E-012`.

**Source expressions, not transferable**

Source audit interfaces, activity feeds, research cards, badges, controls, customer metrics, and documentation structures remain source-owned.

**Applicability**

- LLM-generated creative and product outputs.
- Agent actions, reports, research, analytics, and customer claims.
- Approval, review, publishing, and transfer workflows.

**Non-applicability**

- Public creative where all metadata would overwhelm the receiver. The underlying record still applies, but only necessary trust markers should be rendered.
- Sensitive metadata that would expose private information.

**Failure modes**

- Provenance that exists in a database but is invisible at the decision point.
- Decorative trust badges without inspectable evidence.
- A human review label with no named decision or timestamp.
- An irreversible action presented as ordinary automation.

**Originality boundary**

Mez trust markers must be created from its own governance model and tested for clarity. They cannot visually reproduce source status chips, audit feeds, report cards, or approval controls.

**Confidence:** high. Five sources connect trust to observable control, evidence, or governance.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** add a compact provenance anatomy to one generated design, one report claim, and one agent action. Test whether receivers can identify source, status, owner, and review point.
**Promotion gate:** `H3` for visible interaction and `H4` for schema, storage, validation, and retention.

### `PAT-TRU-02` Method and uncertainty disclosure

**Mechanism**

Research and quantitative claims disclose evidence class, method, source, date, scope, and uncertainty at a depth appropriate to the channel. Compression may reduce detail but cannot remove the ability to trace the claim.

**Cross-source evidence**

- Ramp: `RAMP-E-007`, `RAMP-E-008`, `RAMP-E-009`, `RAMP-E-010`.
- Stripe: `STRIPE-E-010`, `STRIPE-E-012`.
- Notion: `NTN-E12`, `NTN-E13`, `NTN-E19`.
- ElevenLabs: `ELV-E09`, `ELV-E17`.

**Source expressions, not transferable**

Ramp's research identity and card format, Stripe's metric presentations, Notion's control interfaces, and ElevenLabs' performance-proof styling cannot be used as Mez disclosure templates.

**Applicability**

- Reports, research, quantified claims, benchmarks, case studies, and AI evaluations.
- Ads and email that compress a larger evidence record.
- LLM outputs that summarise or transform research.

**Non-applicability**

- Non-quantitative brand language that makes no factual claim.
- Private raw data that should remain inaccessible, although a safe methodology record may still be required.

**Failure modes**

- Precision without methodology.
- A current-looking number with no date.
- Hiding limitations in an inaccessible document.
- Allowing an LLM to strengthen a qualified finding during compression.
- Treating confidence as a visual flourish instead of an evidence judgement.

**Originality boundary**

Mez must define its own disclosure anatomy and language. Source report structures, metric cards, citations, and confidence displays remain excluded.

**Confidence:** high. Four sources provide direct evidence for attributable, bounded, or governed claims.
**Maturity:** `M1 corroborated`.
**Candidate experiment:** express one dated research finding as a report, website proof unit, email module, and ad. Verify that method, source, and uncertainty remain traceable.
**Promotion gate:** `H3` for receiver comprehension and `H4` for evidence schema and automated checks.

## Tensions and contradictions

### Quiet identity versus immediate distinction

Linear and Notion show that restraint can become recognisable through repeated behaviour. Stripe, ElevenLabs, and Ramp demonstrate stronger graphic or colour punctuation. Mez must not assume that quietness is inherently premium or that stronger expression is inherently distinctive.

Resolution test: compare restrained and expressive implementations of the same Mez mechanism in monochrome before colour or source-adjacent devices are introduced.

### Shared chassis versus product individuality

All five sources support family coherence, but their strategies differ. Linear leans towards one workflow and shell. ElevenLabs gives platforms visibly separate territories. Notion changes primary information objects. Stripe uses bounded local-product extensions. Ramp emphasises job and proof differences on a stable corporate chassis.

Resolution test: establish which elements must be shared for usability and transfer, then require each product to remain identifiable through work and proof with names and colour removed.

### Literal proof versus narrative clarity

Linear, ElevenLabs, Ramp, and Notion frequently make proof highly inspectable. That detail can compete with simple positioning. A proof-heavy opening may reduce comprehension, while an overly calm opening may feel unsubstantiated.

Resolution test: stage the same claim at three evidence depths and measure initial understanding, credibility, and recall.

### Sensory expression versus operational credibility

ElevenLabs demonstrates a sensory product where sound and time legitimately drive identity. Linear and Ramp gain credibility from operational states and telemetry. Mez must decide which products benefit from sensory expression and which require visibly disciplined evidence.

Resolution test: require every expressive behaviour to map to a real Mez object, state, or transformation. Remove any effect that cannot explain its role.

### Flexible generation versus deterministic control

Notion's relational primitives and Stripe's bounded extension support flexibility. Trust, accessibility, and family coherence require limits. A system optimised only for deterministic production may become repetitive, while unrestricted LLM generation will drift.

Resolution test: compare fixed, bounded, and open composition modes using the same semantic record. Measure consistency, useful variation, accessibility, and human correction time.

### Visible provenance versus channel overload

Ramp, Notion, ElevenLabs, and Linear support rich trust evidence. Small ads and email cannot show a full audit trail. Hiding it completely weakens accountability.

Resolution test: define a compact trust marker with a traceable path to the full record, then verify that the compressed claim remains correctly qualified.

### Current brand equity versus new structural identity

The research challenges dependence on wings, discs, gradients, and trading-card structures, but it does not prove those assets should disappear. Existing recognition may be valuable even if it is not sufficient.

Resolution test: compare current-device, reduced-device, and device-free prototypes using the same mechanisms. Judge recognition, originality, credibility, and product distinction separately.

## Underused opportunities

### Evidence behaviour as the primary identity layer

Most software systems standardise appearance before standardising how claims are proven. Mez could make observed input, system action, result, verification, exception, and decision into a recognisable grammar across every output.

Potential value: stronger credibility, transferable generation, and recognition that does not depend on colour or logo.

### Product-specific failure and control territories

Portfolio systems usually differentiate happy-path visuals. Each Mez product could also own a characteristic exception, review, recovery, and verification model derived from its job.

Potential value: deeper product distinction and more credible enterprise communication.

### Provenance-native creative outputs

Ads, emails, reports, and generated designs could carry machine-readable lineage even when the visible surface shows only a compact trust marker.

Potential value: safer LLM reuse, faster review, claim refresh, and controlled team ingestion.

### Static and reduced-motion identity designed first

Motion systems are often created as visual effects, then reduced-motion behaviour is retrofitted. Mez can define state meaning in static frames first and allow animation only when it adds information.

Potential value: accessibility, consistency across static channels, and resistance to generic AI animation.

### Evidence-preserving compression

One structured proof record could power product UI, marketing, an ad, email, and a report while preserving evidence class and qualification.

Potential value: less claim drift, lower production effort, and better cross-team consistency.

### Semantic registry as the real handoff pack

A transferable Mez pack could be ingested as versioned objects, rules, examples, source records, and validators rather than as a PDF or Figma library alone.

Potential value: consistent output from humans and different LLMs, with lower hidden-context dependence.

### Human taste as a bounded approval function

Machine-readable rules can handle semantic correctness, provenance, and prohibited transformations. Human input can remain concentrated on territory, authorship, emotional quality, and final judgement.

Potential value: meaningful human influence without requiring the human to approve every component or output.

## Cross-pattern experiment sequence

### `EXP-01` Monochrome authorship

Patterns: `PAT-REC-01`, `PAT-REC-02`, `PAT-DEN-01`.
Output: homepage hero, product workflow, ad, email module, and report page.
Pass: reviewers group the family above chance, core claims remain comprehensible, and no source is named as the dominant template.

### `EXP-02` Four-product territory matrix

Patterns: `PAT-POR-01`, `PAT-POR-02`, `PAT-MOT-02`.
Output: one nameless, colour-free contact sheet for AI OS, Aurora, Prism, and Forge.
Pass: products remain related and distinguishable through job, object, proof, state, and control.

### `EXP-03` Evidence-preserving channel transformation

Patterns: `PAT-PRF-01`, `PAT-PRF-02`, `PAT-DEN-01`, `PAT-TRU-02`.
Output: one real proof record rendered for website, product UI, ad, email, and report.
Pass: all channels retain the correct evidence class, qualification, and trace path without inventing facts.

### `EXP-04` Orchestration and handoff storyboard

Patterns: `PAT-MOT-01`, `PAT-MOT-02`, `PAT-TRU-01`.
Output: preparing, active, waiting, needs input, exception, handoff, verification, completion, and reversal in static, animated, and reduced-motion forms.
Pass: state, owner, permission, and next action remain clear without decorative effects.

### `EXP-05` Portable object pilot

Patterns: `PAT-PORT-01`, `PAT-PORT-02`, `PAT-PRF-03`.
Output: machine-readable contract, human guidance, HTML reference, Figma mapping plan, LLM context fragment, and validator for one pattern.
Pass: one human and two LLMs produce semantically equivalent, visibly related outputs with bounded variation and complete receipts.

## Global promotion gate

No pattern in this atlas may become canonical until the relevant experiment and human gate pass. Promotion requires:

- a direct Mez requirement;
- evidence IDs and a documented translation rationale;
- a prototype using Mez content;
- accessibility and responsive validation;
- static and reduced-motion behaviour where relevant;
- cross-channel or cross-renderer testing where relevant;
- evidence-class and provenance validation;
- source-signature review against all five exclusion lists;
- a human decision with owner, date, status, and rationale;
- a versioned registry entry and deprecation path.

Failure at any requirement keeps the pattern `UNAPPROVED`. A polished prototype is not an approval.

## Explicit exclusions

This atlas does not approve:

- any colour, typeface, radius, shadow, grid, spacing, or motion value;
- any source mark, motif, illustration, interface, screenshot, asset, copy, sample data, or composition;
- a dark developer-tool style, neutral editorial style, iridescent platform style, green finance style, or sensory audio style as a Mez direction;
- four product reskins differentiated by colour and name;
- Figma, code, prose, or prompt instructions as an isolated source of truth;
- a full component factory before H2 approves an original direction.
