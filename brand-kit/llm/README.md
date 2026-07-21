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
- `tasks/TASK-EXP-04-PRODUCT-CARD.json`: the active two-phase Product Card 02 task; Phase A visual directions are active and Phase B functional components are held.
- `examples/CTX-EXP-04-PRODUCT-CARD.json`, `RCP-EXP-04-PRODUCT-CARD.json`, and `EVAL-EXP-04-PRODUCT-CARD.json`: the Phase A visual-lab context, pending-gate receipt, and pre-approval evaluation.

The older phase examples remain useful schema fixtures but may contain historical Mezcorp paths. They do not override `brand-kit/START-HERE.md`, `brand-kit/docs/CURRENT-STATE.md`, or canonical authority.

Skills live canonically under `brand-kit/skills/`. `llm/skills/`, `.agents/skills/`, and `.claude/skills/` are discovery adapters only.
