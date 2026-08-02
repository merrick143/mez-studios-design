# LLM operating layer

This folder contains model-neutral machine contracts for bounded tasks, context bundles, output receipts, and evaluations.

## Current use

- `task.schema.json`: define a bounded implementation task.
- `context-bundle.schema.json`: record the exact authority and evidence supplied to an agent.
- `output-receipt.schema.json`: report changes, validation, assumptions, and next action.
- `evaluation-result.schema.json`: evaluate contract compliance and design quality separately.
- `tasks/TASK-FND-01-TYPOGRAPHY.json`: the completed canonical typography task.
- `tasks/TASK-FND-02-COLOUR-SURFACES.json`: the completed canonical colour and surfaces task.

- `tasks/TASK-FND-03-SPACE-LAYOUT.json`: the completed canonical space, layout, density, and responsive task.
- `examples/CTX-FND-03-SPACE-LAYOUT.json`, `RCP-FND-03-SPACE-LAYOUT.json`, and `EVAL-FND-03-SPACE-LAYOUT.json`: the canonical context, output receipt, and completed evaluation.
- `tasks/TASK-FND-04-GEOMETRY-CONTROLS.json`: the completed canonical geometry, borders, depth, focus and controls task.
- `examples/CTX-FND-04-GEOMETRY-CONTROLS.json`, `RCP-FND-04-GEOMETRY-CONTROLS.json`, and `EVAL-FND-04-GEOMETRY-CONTROLS.json`: the canonical context, output receipt, and completed evaluation.
- `tasks/TASK-FND-05-FOUNDATION-RELEASE.json`: the completed canonical foundation integration and release task.
- `examples/CTX-FND-05-FOUNDATION-RELEASE.json`, `RCP-FND-05-FOUNDATION-RELEASE.json`, and `EVAL-FND-05-FOUNDATION-RELEASE.json`: the canonical release context, output receipt and completed evaluation.
- `tasks/TASK-EXP-01-DISC-CONTRACT.json`: the completed canonical product-disc expression task.
- `examples/CTX-EXP-01-DISC-CONTRACT.json`, `RCP-EXP-01-DISC-CONTRACT.json`, and `EVAL-EXP-01-DISC-CONTRACT.json`: the canonical disc context, completed output receipt, and post-gate evaluation.
- `tasks/TASK-EXP-02-SPHERE-CONTRACT.json`: the completed canonical focal-sphere expression task.
- `examples/CTX-EXP-02-SPHERE-CONTRACT.json`, `RCP-EXP-02-SPHERE-CONTRACT.json`, and `EVAL-EXP-02-SPHERE-CONTRACT.json`: the canonical sphere context, completed receipt and post-gate evaluation.
- `tasks/TASK-EXP-03-WINGS-MARK.json`: the completed canonical Wings and mark task.
- `examples/CTX-EXP-03-WINGS-MARK.json`, `RCP-EXP-03-WINGS-MARK.json`, and `EVAL-EXP-03-WINGS-MARK.json`: the canonical mark context, completed receipt and post-gate evaluation.
- `tasks/TASK-EXP-04-PRODUCT-CARD.json`: the completed two-phase Product Card 02 task; Phase A visual grammar and Phase B functional components are canonical 1.0.0.
- `examples/CTX-EXP-04-PRODUCT-CARD.json`, `RCP-EXP-04-PRODUCT-CARD.json`, and `EVAL-EXP-04-PRODUCT-CARD.json`: the frozen approved Phase A context, completed receipt and post-gate evaluation.
- `examples/CTX-EXP-04B-PRODUCT-COMPONENTS.json`, `RCP-EXP-04B-PRODUCT-COMPONENTS.json`, and `EVAL-EXP-04B-PRODUCT-COMPONENTS.json`: the canonical Phase B context, completed receipt and post-gate evaluation. Round 04 received 46 keeps; `DEC-PRODUCT-COMPONENT-SYSTEM-001` locks the bounded component system while illustrative commerce and consumer-specific stress proof remain excluded.
- `tasks/TASK-EXP-05-TRADING-CARD.json`: the complete Trading Card 01 task. Candidate `trading-card-01-r03` received 23 unanimous keeps across faces, information backs, decks or packs and website placements. `H-EXP-05-TRADING-CARD-PROOF` is closed by `DEC-TRADING-CARD-EXPRESSION-001`; canonical version 1.0.0 has bounded expression authority.
- `tasks/TASK-EXP-07-CHANNEL-MOTION.json`: the complete canonical Website Motion task. Seven Round 03 specimens are approved through `DEC-WEBSITE-MOTION-SYSTEM-001`; `MOT-W02` is deferred to the planned `TASK-CMP-01-GLOBAL-NAVIGATION` rather than promoted as a component.
- `tasks/TASK-EXP-08-EXPRESSION-STRESS-PROOF.json` plus its context, receipt and evaluation: the complete canonical certification. Six adversarial suites and fourteen representative fixtures test the inherited expression system without creating a new visual direction; `DEC-EXPRESSION-STRESS-CERTIFICATION-001` preserves the later consumer/provider boundary.
- `tasks/TASK-CMP-01-GLOBAL-NAVIGATION.json` plus its context, completed receipt and post-gate evaluation: Global Navigation `1.0.0` is canonical through `DEC-GLOBAL-NAVIGATION-COMPONENT-001`. The five-circle compact cue, calm footer-free registry, five automatically animated spheres, exact fallbacks and bounded motion exception are approved.
- `tasks/TASK-GOLD-01-GOLDEN-HOMEPAGE.json`: the active first golden-homepage task. Round 00 locks the supplied copy through `DEC-GOLDEN-HOMEPAGE-COPY-001` and defines the ten-region composition, five-product mobile solution, page-motion allocation, proof intake and separate technical-consumer boundary. Round 01 structural composition is next.
- `examples/CTX-GOLD-01-GOLDEN-HOMEPAGE.json`: the bounded Round 04 handoff pack. It pins the exact copy, cumulative hero feedback, named hero-motion decision, canonical component lineage, positive and negative design evidence, stop conditions and unresolved technical-consumer boundary so implementation does not depend on chat history.
- `examples/RCP-GOLD-01-GOLDEN-HOMEPAGE.json` and `EVAL-GOLD-01-GOLDEN-HOMEPAGE.json`: the partial task receipt and Round 00 evaluation. Planning passes; visual composition and the final human gate remain pending.
- `tasks/TASK-PORT-01-RELEASE-BOUNDARY.json` plus its context, completed receipt and evaluation: the first production-release boundary is complete as a non-authoritative plan. It classifies the Golden Homepage dependency graph, defines release-safe proof and clean consumer evidence, and names `CON-MEZ-SYSTEMS-WEB-001` without modifying a consumer.
- `tasks/TASK-PORT-02-HOMEPAGE-DEPENDENCY-GATES.json`: complete. Its closed packet records separate Olli approvals for CMP-05 and CMP-06, frozen dated follower evidence, accepted limitations and reconfirmed bounded motion exceptions.
- `tasks/TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY.json` plus its context, completed receipt and evaluation: complete. Olli approved the exact isolated `1.0.0-rc.1` package and separately approved redacted operating-proof derivatives for named-consumer proof; publication, deployment and production version `1.0.0` remain unauthorised.
- `tasks/TASK-FIG-01-FIGMA-COMPANION.json`: complete. Olli approved the Phase 0 scope and the completed repository-backed companion; Figma remains an authoring mirror without independent authority.
- `tasks/TASK-UI-01-PRODUCT-UI-DATA-VISUALISATION.json`: complete through `H-UI-01-PRODUCT-UI-FOUNDATION`. It establishes an approved non-production Product UI and accessible data foundation without inventing production product evidence.
- `tasks/TASK-CHAN-01-FIRST-RELEASE-CHANNEL-SYSTEMS.json`: priority-deferred. The named low-priority channel families retain future contracts and gates and are not implied complete.
- `tasks/TASK-CERT-01-SYSTEM-CERTIFICATION.json` plus its context, completed receipt and evaluation: complete through `H-CERT-01`. Exact deterministic `1.0.0-rc.2` is approved for final named-consumer proof; deferred channel families remain named as uncertified.
- `tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json`: the completed final transition task. Exact `1.0.0-rc.2` supplied the immutable adapter input to the live `mezcorp-studio/ceos-notion-landingpage` consumer. The package remains unpublished and the consumer remains outside design authority.

The older phase examples remain useful schema fixtures but may contain historical Mezcorp paths. They do not override `brand-kit/START-HERE.md`, `brand-kit/docs/CURRENT-STATE.md`, or canonical authority.

Skills live canonically under `brand-kit/skills/`. `llm/skills/`, `.agents/skills/`, and `.claude/skills/` are discovery adapters only.
