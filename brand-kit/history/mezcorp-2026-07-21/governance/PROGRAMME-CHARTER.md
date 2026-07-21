# Mez Systems design-system programme charter

Status: proposed for H0 approval  
Version: 0.1.0  
Prepared: 19 July 2026  
Programme: Lock the Brand Kit, then Ship Mez Systems

## Purpose

Build one transferable, testable design system that lets humans and LLMs create websites, product interfaces, ads, social assets, emails, presentations, reports, and future formats with recognisable Mez Systems identity and reliable production quality.

The programme is not complete when a style guide looks polished. It is complete when the same approved decisions can travel through tokens, Figma, code, templates, prompts, evaluation, and shipped outputs without identity drift.

## Recommended first-release scope

The v1 release should prove the system across five representative channel families:

1. Marketing web: one flagship home page and one product page.
2. Product UI: one authenticated workflow containing navigation, data, form, loading, empty, error, and success states.
3. Paid and organic social: a modular campaign set covering static feed, story, carousel, and performance-ad variants.
4. Email: one lifecycle template and one transactional template with dark-mode and client constraints documented.
5. Presentations and reports: one executive deck and one operating-report template.

Data visualisation and motion are horizontal foundations inside v1, but they do not each need a full standalone channel pack before the first release. Print, events, merchandise, environmental design, and exhaustive platform-specific UI libraries are deferred unless H0 expands scope.

## Definition of end to end

A channel is end to end only when it has:

- an approved visual and verbal intent;
- canonical primitive, semantic, component, and channel tokens;
- Figma variables, components, variants, and examples where Figma is appropriate;
- coded components or robust production templates where code is appropriate;
- asset references with stable IDs, rights status, checksums, and fallbacks;
- human-readable guidance with positive and negative examples;
- an LLM context bundle that names all required inputs and stop conditions;
- deterministic validation plus human quality review;
- migration notes, versioning, ownership, and a release receipt;
- at least one realistic golden output and one adversarial stress test.

## Recommended authority model

Use a staged source-of-truth model:

- Canonical decisions and token data live in a dedicated, versioned package once Phase 4 begins.
- Code-generated token outputs feed web, product, email, and other machine consumers.
- Figma consumes the same semantics and is the canonical visual authoring environment for components and composed examples, not an independent token authority.
- Guidance, examples, and evaluation contracts live beside the canonical package and reference stable decision and artifact IDs.
- Channel teams consume released versions. They do not fork unnamed local copies.

Until the dedicated package exists, this brand-library directory is the programme control plane. `START-HERE.md`, the numbered foundation documents, root token JSON, `products.json`, and approved entries in `decision-register.json` are the current authoritative set. `canvas/`, `design-system-export/`, and `aios-website/` are implementations or mirrors, not independent authorities.

## Roles and decision rights

Names below are recommendations and remain subject to H0 confirmation.

| Role | Recommended owner | Decision right |
|---|---|---|
| Executive brand owner | Olli | Final identity, ambition, public-release, and expensive-to-reverse decisions |
| Design-system owner | Dedicated owner, currently unassigned | Backlog, release train, contribution review, documentation quality, and cross-channel coherence |
| Design lead | Olli as interim | Visual direction, component quality, Figma library, and golden-output approval |
| Engineering lead | Confirm at H0 | Package architecture, code components, tests, distribution, and migrations |
| Content and verbal lead | Olli as interim | Voice, naming, messaging primitives, and content-pattern approval |
| Channel owners | Confirm per channel | Adoption, channel constraints, golden outputs, and regression acceptance |
| Contributors | Named per task | Work within approved scope and return an output receipt |

No unconfirmed person is treated as having accepted ownership.

## Contribution path

1. Open or select a task with a stable ID.
2. Generate a bounded context bundle from approved sources.
3. Confirm dependencies, decision state, deliverables, tests, and stop conditions.
4. Produce the smallest reviewable change.
5. Return an output receipt and evaluation result.
6. Obtain required human approval.
7. Merge into the canonical source, regenerate mirrors, and publish a version.
8. Record affected consumers and migration actions.

## Exception path

An exception request must include the affected rule, channel, duration, business reason, risk, proposed mitigation, owner, expiry date, and screenshots or prototypes. The design-system owner may approve reversible implementation exceptions. The executive brand owner must approve identity exceptions or public-facing deviations. Expired exceptions fail validation.

## Escalation and stop rules

Execution stops when:

- two authoritative sources disagree;
- a required decision is open or proposed but the task would make it public or expensive to reverse;
- a required asset lacks rights, provenance, or a stable checksum;
- responsive, accessibility, contrast, or content stress tests fail;
- the target consumer cannot identify the release version it consumes;
- a generated output cannot produce a complete receipt;
- a contributor would need to invent brand intent not expressed in an approved source.

## Quality bar

The system should be recognisable without relying on a logo or product gradient, remain coherent across dense product UI and expressive marketing work, survive realistic content and accessibility constraints, and make the correct path easier than a local workaround.

Success is measured by:

- 100 percent of released artefacts traceable to decision and artifact IDs;
- zero unresolved authority conflicts at release;
- all required breakpoint, accessibility, and adversarial tests passing;
- golden outputs approved by the channel owner and design lead;
- consumers pinned to a version with migration state visible;
- LLM tasks completing with valid context, receipt, and evaluation contracts;
- fewer unmanaged local copies and fewer exceptions release over release.

## Phase sequence

0. Establish truth, ownership, evidence, and execution contracts.
1. Reverse engineer taste, competitors, references, and anti-patterns.
2. Decide identity, ambition, and cross-channel creative territory.
3. Rebuild foundations and token architecture.
4. Create the canonical package and generated distribution layer.
5. Build Figma variables, components, documentation, and Code Connect mappings.
6. Build channel systems and golden outputs.
7. Add automated validation, visual regression, accessibility, and LLM evaluation.
8. Migrate consumers, train teams, version, and release.

Each phase ends in a human gate. Work may be explored before a gate, but it may not be promoted as canonical until the gate is approved.

## Migration-first sequence amendment

`DEC-MIGRATION-SEQUENCE-001`, approved 21 July 2026, changes repository timing without declaring the unfinished system complete. The programme will close the product architecture, gradient assignments and minimum authority engine, then move the canonical control plane to `merrick143/mez-studios-design/brand-kit` before building the remaining foundations, product-expression suite, golden homepage, Figma library or channel packs.

The complete pre-cutover contract, deferred backlog and rollback requirements are in `MIGRATION-FIRST-GATE.md`. The original phase outcomes remain valid; their unfinished work moves with stable status rather than blocking cutover merely because it is unfinished.

## H0 approval required

H0 must confirm or amend:

- the recommended v1 channel scope;
- the staged source-of-truth and future dedicated-package model;
- the owner for design-system operations and engineering;
- who holds final approval for each channel;
- the brand ambition and risk tolerance used in Phase 1 research;
- whether the current Figma file should be rebuilt, replaced, or retained only as research;
- whether the website consumer is a live migration target or merely historical evidence.

The detailed response form is in `H0-DECISION-PACKET.md`.
