# Mez Systems shared agent guide

This is the tool-neutral operating contract for humans, Claude Code, Codex, and other repository-capable LLMs.

## Authority

- Canonical repository: `merrick143/mez-studios-design`.
- Canonical path: `brand-kit/`.
- Current machine authority: `brand-kit/authority/current.json`.
- Immutable migration activation record: `brand-kit/authority/authority.json`.
- Approved decisions: the hash-locked cutover ledger at `brand-kit/governance/decisions.json` plus the current supplement at `brand-kit/governance/post-cutover-decisions.json`.
- Canonical identity data: `brand-kit/registry/`.
- Generated releases: `brand-kit/releases/`.
- Research, historical imports, Figma, consumer websites, and `play-orb/` are evidence or consumers. They cannot create brand truth.

## Required reading

For any new task under `brand-kit/`, read in this order:

1. `brand-kit/START-HERE.md`.
2. `brand-kit/docs/CURRENT-STATE.md`.
3. `brand-kit/docs/ROADMAP.md`.
4. `brand-kit/governance/decisions.json`.
5. `brand-kit/governance/post-cutover-decisions.json`.
6. The documentation and skill relevant to the requested task.

Read `brand-kit/docs/END-TO-END-ROADMAP.md` when planning a phase, changing programme sequencing, or judging whether the system is end to end.

For any task that produces or judges a **visual**, additionally read `brand-kit/design-authority/` before generating. The canon is a constraint on what you make, not a filter on what you made.

## Design authority

`brand-kit/` can prove a build is correct. It cannot prove a build is good, and a mediocre build passes every verifier. `brand-kit/design-authority/` closes that gap:

- `ANTI-SLOP-CANON.md`: cited defect IDs. Objectively wrong, no taste involved. Read before generating.
- `CRAFT.md`: positive craft. Composition families, pacing, hierarchy, depth, motion allocation, words.
- `GATE-B-DESIGN-EXCELLENCE.md`: the scored eleven-dimension review with four blocking tests.
- `FEEDBACK-DISCIPLINE.md`: the round protocol, and how to read Olli's feedback without correcting on the wrong axis.

Supporting material:

- `brand-kit/references/`: outside design studied through the abstraction ladder. Ethos only, never components, never values.
- `brand-kit/assets/third-party-marks/`: real third-party logos, resolved through `registry.json`. The only sanctioned source; never invent or draw a brand mark.

Two rules override an agent's instinct to skip this. **Look at the render before judging anything**, including your own work. And **ideate in plain sentences before building** when a surface has been rejected before.

## Working rules

1. Inspect Git status before editing. Existing unrelated changes belong to the user.
2. Select one named roadmap task and keep the diff bounded to it.
3. Read canonical data; do not infer current state from screenshots or historical files.
4. Keep research candidates outside canonical registries until an explicit human promotion decision exists.
5. Never hand-edit a generated release or derived gradient asset. Change the owning source and regenerate.
6. Preserve exact source-gradient authority, the canonical Wings asset, reduced-motion fallbacks, and recorded product assignments.
7. A plausible visual is not automatically a Mez visual. Use approved references, anti-patterns, responsive evidence, and a bounded human review packet.
8. Stop when authoritative sources disagree, a required human decision is missing, provenance is unknown, or required validation fails.

## Human versus agent decisions

Human approval is required for identity direction, product naming or assignment, visible foundation direction, expression-family promotion, golden-output promotion, and public release.

Agents own inventory, deterministic generation, documentation maintenance, evidence capture, accessibility checks, responsive checks, schema validation, release assembly, and drift detection. Do not ask the human to verify facts that code can verify.

## LLM output contract

Every implementation task should identify:

- task and decision IDs;
- inputs and authority paths;
- files changed;
- validations run and their results;
- unresolved risks or human decisions;
- whether the output is research, candidate, approved, canonical, generated, or released.

Use the schemas under `brand-kit/llm/` when producing formal task, receipt, or evaluation records.

## Core validation

From the repository root, use the pinned environment described in `brand-kit/START-HERE.md`, then run:

```bash
python3 brand-kit/scripts/verify_portability.py
python3 brand-kit/scripts/verify_llm_contracts.py
python3 brand-kit/scripts/verify_workbench.py
python3 brand-kit/gradient-library/verify_library.py
python3 brand-kit/product-architecture/verify_architecture.py
python3 brand-kit/scripts/verify_authority.py
python3 brand-kit/scripts/verify_release.py --release brand-kit/releases/0.1.0-alpha.1
```

Run task-specific visual and responsive checks in addition to these mechanical checks.

## Shared skills

The canonical skill source is `brand-kit/skills/`. Tool discovery locations are symlinks:

- Codex: `.agents/skills/`.
- Claude Code: `.claude/skills/`.

Never edit a discovery symlink as if it were an independent skill. Change the canonical folder and validate both discovery paths.

Current skills:

- `codex-made-it`: build and validate the Living Core gradient system.
- `design-critique`: Gate B. Score a surface for design excellence before Olli sees it.
- `reference-ingest`: turn a design Olli likes into a reusable Mez principle.

Claude Code additionally has the `design-critic` subagent at `.claude/agents/design-critic.md`, which carries the same authority and reads the same files.

## Mechanical validation is not design validation

Run the seven verifiers, then run `design-critique`. Green verifiers on rejected work is the normal case, not the exception: Product Card rounds 01 to 06 passed compliance and were rejected as vibe-coded. Reporting "all checks pass" about a surface you have not looked at is a failure of this contract.
