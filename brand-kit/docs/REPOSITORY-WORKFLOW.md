# Repository workflow for Mez design-system work

Status: canonical target workflow; internal archive boundary

Snapshot date: 2026-07-21

## Canonical working state

- Canonical repository: `merrick143/mez-studios-design`
- Migration branch: `codex/brand-kit-workbench`
- Canonical path: `brand-kit/`
- Active identity release: `mez-systems-v0.1.0-alpha.1`
- Internal rollback checkpoint: `822aa91`

After the migration branch is merged, `main:brand-kit/` becomes the ordinary working authority. Feature work should use bounded branches and merge back through normal review.

## What a worktree solves

A Git worktree is a second folder attached to the same repository, checked out on a different branch. It provides:

- a clean design-system working directory;
- isolation from unrelated business-file changes;
- shared Git history and governance evidence;
- an easy diff and merge boundary;
- no duplication of the 91 GB everyday folder.

It is not a separate repository and not an off-device backup. Worktrees used for migration may be removed after their branches are merged, pushed, and verified.

## Daily rule

- Use the normal `mez-studios-design/brand-kit` checkout after migration cleanup.
- Use Mezcorp only for ordinary business work or its pinned consumer/archive reference.
- Start each design checkpoint from a clean status and keep its diff bounded to the named task.
- Never mix homepage experiments, unrelated business edits and canonical system changes in one commit.
- Never switch the dirty everyday checkout between design branches merely to inspect this work.

## Branch and release workflow

For each design-system change:

1. Start from an up-to-date clean `main`.
2. Create a bounded `codex/` or team feature branch.
3. Name the roadmap task and decision dependencies.
4. Change owning sources, not generated mirrors.
5. Run the shared and task-specific validators.
6. Record human approval where required.
7. Regenerate release outputs and write an output receipt.
8. Merge and publish a version when the release gate passes.

## Canonical target timing

The target is active inside `merrick143/mez-studios-design/brand-kit`. The promotion minimums passed:

- canonical product roster and stable IDs;
- approved product-gradient assignments and a genuine Context Engine source;
- source-gradient authority, Living Core ingestion, renderer and selected finish;
- authority manifest, schemas, validators, versioned migration snapshot and rollback.

The responsibility boundary is now:

- `mez-studios-design/brand-kit` owns canonical brand data, documentation, assets, generators, validators and releases;
- Mezcorp consumes a pinned version;
- consumer teams never fork tokens or copy arbitrary working files;
- Figma mirrors a named release;
- release notes and migrations explain every breaking change.

Foundations, the product-expression suite, golden homepage, consumer proof and Figma library are post-cutover work in the canonical target. Building them in Mezcorp would recreate the dual-authority problem.
