# Migration-first authority gate

Status: complete; canonical authority transferred

Decision: `DEC-MIGRATION-SEQUENCE-001`

Approved by: Olli

Approved: 21 July 2026

Target canonical repository: `merrick143/mez-studios-design`

Target path: `brand-kit/`

Canonical target branch: `codex/brand-kit-workbench` at `6b1f0c4`

Clean-clone validated snapshot: `698152e`

Canonical activation: `19f1570`

Activation proof: `6b1f0c4`

Product-architecture decision: `DEC-PRODUCT-ARCHITECTURE-001` at `3e5a276`

Approved Living Core system checkpoint: `8b5a262`

## Decision

Migrate the Mez Systems control plane before completing the entire end-to-end roadmap. Canonical means one explicit place to make decisions; it does not mean every foundation, component, channel or golden output is finished.

Continuing to build foundations, product expressions and the golden homepage inside the Mezcorp repository would deepen the authority split the programme is intended to remove. The dedicated target already contains a validated non-canonical workbench and recoverable Living Core system, so the correct sequence is to close a small identity-and-authority kernel, cut over once, and continue the unfinished roadmap in the new canonical location.

## What must close before cutover

### 1. Recovery and reconciliation

- Push the standalone workbench branch without merging it.
- Record all approved research-system decisions in this control plane.
- Preserve invalid and superseded research as evidence with zero authority.
- Produce one machine-readable migration task and validator.
- Confirm both repositories are recoverable before changing authority.

### 2. Product architecture and assignment gate — complete

The bounded human review approved:

- literal public product names only, with no alternate naming layer;
- `AI OS` (`mz.systems.product.aios`) with `MZ-G13`;
- `Context Engine` (`mz.systems.product.context-engine`) with `MZ-G12`;
- `AI Ads System` (`mz.systems.product.ai-ads-system`) with `MZ-G06`;
- `Claude Code OS` (`mz.systems.product.claude-code-os`) with `MZ-G15`;
- `Organic Content OS` (`mz.systems.product.organic-content-os`) with `MZ-G20`.

This was the only creative human gate required before repository cutover. No further human review is required until the migration snapshot and authority mechanics are complete.

The approved review record is tracked in the standalone recovery branch. It uses the shared Living Core renderer, the approved Deep Mineral finish and exact source twins. The five-product identity kernel is generated atomically in `0.1.0-alpha.1`; the frozen internal product and gradient registries remain unedited historical evidence.

### 3. Identity kernel

The migration snapshot must contain:

- the canonical Wings asset and its checksum;
- the complete approved source-gradient library and alias map;
- exact static twins and deterministic Living Core data;
- the selected Deep Mineral finish under `DEC-LIVING-CORE-FINISH-001`;
- product IDs, names, states and gradient assignments from the human gate;
- approved typography, control, product-family, hero and motion decisions as decisions, even where implementation remains pending;
- provenance for every imported artifact.

### 4. Minimum canonical engine

Before cutover the target had to contain the following. Every item is complete and activation proof is preserved at target commit `6b1f0c4`:

- an authority manifest naming the old and new locations;
- a new dated artifact manifest for the migration snapshot; do not overwrite the 19 July Phase 0 evidence manifest, whose hashes and local-only archive paths intentionally describe an older filesystem state;
- stable IDs and schemas for products, gradients, assets, decisions and releases;
- deterministic builders and validators for the migrated identity kernel;
- a versioned migration snapshot such as `0.1.0-alpha.1`;
- a clean-clone validation procedure;
- rollback instructions that restore the old canonical commit;
- a rule that the old Mezcorp pack becomes a pinned archive and consumer after cutover.

## What does not need to close before cutover

The following move as explicit backlog and are built in the new canonical repository:

- the remainder of original Phase 2 strategy, messaging and cross-channel north-star work;
- holdco and product mark exploration beyond the canonical Wings asset;
- complete typography implementation and font packaging;
- semantic colour, surface, spacing, grid, radius, border, shadow and elevation systems;
- the complete control state system;
- the product-expression component suite;
- the revised mobile hero and premium primary-button refinement;
- the golden homepage;
- consumer proof and the first production release;
- Figma variables, components, templates and Code Connect;
- channel packs, multi-model certification and team adoption.

These items are not cancelled or declared done. They are transferred with stable task IDs, dependencies and authority states.

## Original-roadmap disposition

| Original phase | Required before migration | Disposition |
|---|---|---|
| Phase 0 | Yes | Already complete; migrate its registers and contracts. |
| Phase 1 | Yes | Already complete as baseline history; preserve rather than repeat. |
| Phase 2 | Partial only | Freeze completed evidence and decisions; transfer unfinished strategy and messaging as backlog. |
| Phase 3 | Identity kernel only | Close roster and gradient assignments; defer the broader proprietary grammar. |
| Phase 4 | Minimum engine only | Build authority, schemas, release manifest, validators and rollback required for cutover. |
| Phase 5 | No | Build foundations after cutover in the new canonical repository. |
| Phases 6 to 11 | No | Do not start broadly before cutover; carry them forward as governed backlog. |

## Cutover sequence

1. Protect and reconcile both recovery branches.
2. Present the product architecture and gradient-assignment board. Complete at `3e5a276`.
3. Record the approved roster, assignments and Context Engine source. Complete through `DEC-PRODUCT-ARCHITECTURE-001`.
4. Generate and validate the `0.1.0-alpha.1` migration snapshot in `mez-studios-design/brand-kit`. Complete; clean-clone snapshot `698152e`.
5. Freeze the final internal Mezcorp pack commit. Transfer-prepared through `governance/AUTHORITY-TRANSFER.json`.
6. Import canonical governance and required history into the target.
7. Mark the target path as rank-one canonical authority.
8. Replace the writable Mezcorp pack with a pinned archive or generated consumer reference.
9. Verify a clean clone and rollback path.
10. Continue foundations and product-expression work only in the new canonical repository.

## Figma timing

Do not build the production Figma library before cutover. Figma may still be used for bounded mark or static-composition exploration, but the shared library should be generated or mirrored from approved foundations and components in the new canonical repository. This avoids creating a third authority during migration.

## Exit gate

Cutover passed because:

- the recovery branches are pushed;
- the programme ledger and migration task agree;
- the product roster and gradient assignments are approved;
- Context Engine has a genuine selected source;
- the identity kernel rebuilds deterministically;
- the target migration snapshot validates from a clean clone;
- the old canonical commit and rollback procedure are recorded;
- no two writable locations claim equal authority.
