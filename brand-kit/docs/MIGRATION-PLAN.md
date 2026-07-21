# Standalone brand-kit migration plan

Status: active planning and proof branch

Target repository: `mez-studios-design`

Target branch: `codex/brand-kit-workbench`

The goal is not to copy the unfinished internal pack and call the move complete. The goal is to close each authority gap, produce one stable portable release, then deliberately transfer canonical ownership.

## Phase 0: make the truth visible

- Preserve the existing `/play-orb/` unchanged as the Claude Code benchmark.
- Import the current systemised pack as a pinned snapshot with source commit and hashes.
- Show animated output, exact static twins and authority state together.
- Record the Claude-versus-WebP palette drift as an explicit decision gate.
- Keep the workbench labelled non-canonical.

Exit gate: a human can identify where every file came from and which source currently wins.

## Phase 1: lock the Living Core

- Treat the 43 original PNG masters as the only extraction authority.
- Preserve all supplied IDs, while recording the ten exact duplicate-ID groups and the MZ-G01 source-quality exception.
- Generate the full palette cache, runtime catalogue and static fallback library from those PNGs.
- Judge source, idle animation, motion character and cross-shape coherence across the full board.
- Select or edit product assignments separately; never fork palette data to create a product-specific variant.
- Rebuild the complete source library without drift.
- Verify one shared WebGL context, reduced motion, offscreen pause, fallback and white Wings.
- Lock the candidate ingestion contract and its pinned Python environment.

Human decision: select, edit or reject product-to-gradient assignments. The source and extraction law no longer require a dataset choice.

Exit gate: one renderer, a deterministic complete source catalogue, one frozen core dataset per ID, one static twin per ID, approved product assignments, and no contradictory skill instructions.

## Phase 2: lock foundations

### Typography

- Acquire and licence the actual Geist display font files.
- Implement Geist for display and tuned Inter for body/UI.
- Define desktop and mobile scales, line lengths, tracking and fallbacks.
- Remove stale Inter-only claims from the portable release.

### Colour and surfaces

- Resolve semantic neutrals, contrast, feedback colours and light/dark-section behaviour.
- Keep product gradients as the only identity colour.
- Prove email-safe and document-safe values.

### Geometry and layout

- Lock spacing, grid, content widths and responsive breakpoints.
- Extend the approved 12px control radius into a coherent surface scale.
- Lock border, hairline, shadow and elevation rules.

### Controls

- Keep the approved solid, outline and text hierarchy.
- Compare the approved micro-lift against the proposed restrained stroke, tonal gradient and glow finish.
- Complete focus, loading, disabled, destructive and mobile behaviour.

Human decisions: final display-font proof, surface grammar and primary-button finish.

Exit gate: tokens, examples and responsive tests agree across code and documentation.

## Phase 3: lock the product-expression suite

Build one focused plate for each primitive:

1. Disc: scale, mark placement, clearspace, static and animated states.
2. Sphere: hero scale, crop, depth and motion use.
3. Product card: aligned chassis, core placement, copy, price, status and CTA.
4. Trading card: full-bleed gradient field, edition finish and accessibility.
5. Wings: holdco, white product mark and gradient-mask expression.
6. Collection: five-product stack, catalogue, bundle, upsell and checkout summary.
7. Channel map: website, email, ads, social, video, documents, icons and OG images.

Context Engine enters through the candidate workflow, not by borrowing an existing core. Supply genuine square source gradients, generate exact-versus-animated plates, then select, edit or reject.

Human decisions: Context Engine core and final expression family.

Exit gate: every expression has anatomy, usage law, responsive behaviour, static fallback and named channel rules.

## Phase 4: build portable release candidate 1

- Generate a self-contained release from canonical data.
- Include tokens, assets, fonts, Wings, exact gradients, renderer, component contracts, channel rules, LLM instructions and validators.
- Include source hashes, decision IDs, release version and migration notes.
- Validate in a clean temporary directory with no access to the source repository.
- Integrate into one real website consumer without copying or forking values.

Exit gate: a human or LLM can build a credible output using only the release, and automated checks detect drift.

## Phase 5: transfer canonical ownership

Only after Phases 1 through 4 pass:

1. Freeze the final internal pack commit.
2. Generate the first accepted portable release.
3. Import the relevant history and canonical files into this repository.
4. Record the new repository as rank-one canonical location.
5. Change the Mezcorp repository to a pinned consumer/reference.
6. Update Figma and all skills to point at the new release.
7. Merge the internal branch through a clean integration worktree.
8. Push and verify both repositories before deleting any worktree or branch.

Exit gate: there is one canonical repository, one release line and zero writable mirrors claiming equal authority.

## Branch-close checklist

- [x] Source-PNG extraction authority resolved.
- [ ] Complete 43-ID board reviewed and product assignments decided.
- [ ] Context Engine source and candidate decision complete.
- [ ] Geist asset and updated typography release complete.
- [ ] Foundation tokens and responsive tests pass.
- [ ] Product-expression suite approved.
- [ ] Portable release validates in isolation.
- [ ] One consumer ingests the release successfully.
- [ ] New authority model approved.
- [ ] Both repositories pushed and recoverable.
- [ ] Internal design branch merged through a clean worktree.
- [ ] Old worktrees removed only after verification.
