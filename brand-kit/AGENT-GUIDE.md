# Mez Systems shared agent guide

This is the tool-neutral operating contract for humans, Claude Code, Codex, and other repository-capable LLMs.

## Authority

- Canonical repository: `merrick143/mez-studios-design`.
- Canonical path: `brand-kit/`.
- Current machine authority: `brand-kit/authority/current.json`.
- Immutable migration activation record: `brand-kit/authority/authority.json`.
- Approved decisions: `brand-kit/governance/decisions.json`.
- Canonical identity data: `brand-kit/registry/`.
- Generated releases: `brand-kit/releases/`.
- Research, historical imports, Figma, consumer websites, and `play-orb/` are evidence or consumers. They cannot create brand truth.

## Required reading

For any new task under `brand-kit/`, read in this order:

1. `brand-kit/START-HERE.md`.
2. `brand-kit/docs/CURRENT-STATE.md`.
3. `brand-kit/docs/ROADMAP.md`.
4. `brand-kit/governance/decisions.json`.
5. The documentation and skill relevant to the requested task.

Read `brand-kit/docs/END-TO-END-ROADMAP.md` when planning a phase, changing programme sequencing, or judging whether the system is end to end.

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
