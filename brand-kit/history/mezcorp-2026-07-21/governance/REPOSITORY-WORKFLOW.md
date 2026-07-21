# Repository workflow for Mez design-system work

Status: canonical cutover complete; internal archive boundary

Snapshot date: 2026-07-21

## Current state

- Everyday business checkout: `/Users/olivermerrick/mezcorp_claude_code`
- Design-system worktree: `/Users/olivermerrick/mez-design-system-worktree`
- Design-system branch: `codex/mez-gradient-system`
- Branch point: the existing `codex/mez-living-core` history at commit `20cb944`
- Canonical repository: `merrick143/mez-studios-design`
- Canonical branch: `codex/brand-kit-workbench` at activation-proof commit `6b1f0c4`
- Approved Living Core system checkpoint inside that branch: `8b5a262`
- Canonical path: `brand-kit/`
- Active identity release: `mez-systems-v0.1.0-alpha.1`
- Internal rollback checkpoint: `822aa91`
- The design branch contained 13 Mez design-system commits beyond local `main` before this checkpoint.
- The everyday checkout is approximately 91 GB and contains unrelated modified and untracked business files.
- The Git database is approximately 595 MB and the repository tracks approximately 2,845 files. Most disk usage is untracked business/media data.
- Local `main` was 112 commits ahead of `origin/main` at inspection time. The remote therefore must not be treated as a current recovery copy.

These are operational observations, not permanent brand-system data. Recheck them before merging or publishing.

## What a worktree solves

A Git worktree is a second folder attached to the same repository, checked out on a different branch. It provides:

- a clean design-system working directory;
- isolation from unrelated business-file changes;
- shared Git history and governance evidence;
- an easy diff and merge boundary;
- no duplication of the 91 GB everyday folder.

It is not a separate repository and not an off-device backup. Deleting or corrupting the underlying repository can still affect every worktree.

## Daily rule

- Use `mezcorp_claude_code` for ordinary business work.
- Use `mez-design-system-worktree` only for archive inspection, rollback evidence or consumer-reference maintenance.
- Use `mez-studios-design-brand-kit/brand-kit` for all new design-system work.
- Start each design checkpoint from a clean status and keep its diff bounded to the named task.
- Never mix homepage experiments, unrelated business edits and canonical system changes in one commit.
- Never switch the dirty everyday checkout between design branches merely to inspect this work.

## When to merge or cut over

Do not merge the archived design work through the dirty everyday checkout. `DEC-MIGRATION-SEQUENCE-001` completed the standalone authority cutover through `CUTOVER-2026-07-21-01`:

1. This branch remains recoverable and bounded to the Mez pack.
2. Product architecture closed through `DEC-PRODUCT-ARCHITECTURE-001`.
3. Internal rollback froze at `822aa91` and the transfer handshake at `6ac911e`.
4. The target migration snapshot validated from clean clones at prepared commit `698152e` and activation commit `19f1570`.
5. Rollback and dated artifact evidence are active in the target.
6. Rank-one authority now belongs to the target; this pack is a pinned archive and consumer reference.

Merging this branch into local `main` is no longer a prerequisite for canonical transfer. If retained for history, perform that merge only from a clean integration worktree after cutover evidence is preserved. Never switch the dirty everyday checkout merely to merge or inspect it.

No merge, push, deletion or branch cleanup is implied by this document. Each remains a deliberate repository action.

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
