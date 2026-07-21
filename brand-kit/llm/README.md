# LLM operating layer

This folder contains model-neutral machine contracts for bounded tasks, context bundles, output receipts, and evaluations.

## Current use

- `task.schema.json`: define a bounded implementation task.
- `context-bundle.schema.json`: record the exact authority and evidence supplied to an agent.
- `output-receipt.schema.json`: report changes, validation, assumptions, and next action.
- `evaluation-result.schema.json`: evaluate contract compliance and design quality separately.
- `tasks/TASK-FND-01-TYPOGRAPHY.json`: the next active programme task.

The older phase examples remain useful schema fixtures but may contain historical Mezcorp paths. They do not override `brand-kit/START-HERE.md`, `brand-kit/docs/CURRENT-STATE.md`, or canonical authority.

Skills live canonically under `brand-kit/skills/`. `llm/skills/`, `.agents/skills/`, and `.claude/skills/` are discovery adapters only.
