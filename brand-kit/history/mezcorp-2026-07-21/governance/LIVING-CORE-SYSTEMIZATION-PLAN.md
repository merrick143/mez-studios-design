# Living Core systemization plan

Status: active gradient-system lock · homepage work paused

Decision inputs: `DEC-MOTION-002`, `DEC-HERO-001`

This plan turns the approved Claude Code Living Core into a repeatable identity system that a human or LLM can operate without redesigning the visual language. It preserves the exact source gradients while making animated expressions reproducible.

## Locked direction

- The Hero 03 direction is approved. Typography, centred hierarchy, layout, button fundamentals, five-card family composition, animation use and product-family read may be carried forward.
- The mobile opening is not approved and needs a dedicated composition revision.
- Homepage construction is paused until the gradient system is reproducible and its expression rules are recorded.
- The Living Core is **one renderer with multiple masks**, not independently styled card, disc, sphere and Wings components.
- A gradient is both canonical source art and parametric runtime data. The source art owns exact colour reproduction; the parametric core owns approved motion.
- Context Engine needs a genuinely new candidate gradient. No existing product core may be relabelled or algorithmically invented as its production identity.
- The complete source library, Living Core animation and cross-shape expression family are approved through `DEC-GRADIENT-LIBRARY-001`.
- `05 · Deep Mineral` is the approved research-system finish through `DEC-LIVING-CORE-FINISH-001`.

## Work order

### 1. Preserve evidence and authority

- Store the Hero 03 export verbatim.
- Record the five approved decisions and one mobile edit in the manifest and decision register.
- Keep `productionAuthority` and `sourceExpressionApproved` false.
- Quarantine further homepage synthesis until this plan reaches the candidate-review gate.

### 2. Freeze the renderer contract

- Keep one shared offscreen WebGL context for every live surface.
- Keep linear-space colour mixing, warped coordinates and mismatched anchor orbits.
- Keep Wings, labels, borders and layout static above the field.
- Allow hover to accelerate only the field; never scale or move the object.
- Pause hidden and offscreen surfaces.
- Fall back to the exact static twin for reduced motion, unavailable WebGL, shader failure, missing data or runtime failure.

### 3. Freeze deterministic ingestion

- Require a square source image of at least `512 × 512` pixels.
- Downsample to `160 × 160`.
- Run seeded `k=5` extraction with seed `7`.
- Assign the darkest cluster to shade and the remaining four to anchors.
- Preserve each anchor's source position and relative weight.
- Pin Python dependencies and verify that a clean rebuild creates no diff.

### 4. Separate canonical rebuilds from candidate generation

- Canonical rebuilds operate only on already assigned products and may refresh generated boards.
- Candidate generation writes to a new isolated directory and may not alter canonical product or gradient registries.
- Every candidate contains source metadata, extraction constants, core data, an exact static twin and a multi-expression review plate.
- Candidate promotion remains a human decision, followed by one atomic canonical update.

### 5. Resolve product architecture and gradient assignments

Complete through `DEC-PRODUCT-ARCHITECTURE-001` at target commit `3e5a276`.

- The literal five-product roster and stable IDs are approved.
- The alternate historical-name layer is retired from active architecture.
- Final migration assignments are AI OS `MZ-G13`, Context Engine `MZ-G12`, AI Ads System `MZ-G06`, Claude Code OS `MZ-G15` and Organic Content OS `MZ-G20`.
- Exact sources and Living Core expressions were reviewed through the shared renderer.
- The frozen legacy registries remain unchanged; generate the approved product and gradient registries atomically in the versioned migration snapshot.

### 6. Build the product-expression component suite

Run these as focused calibration plates after canonical cutover and the Context Engine gradient is chosen:

1. Disc: scale, clearspace, Wings placement, light/dark/static/animated states.
2. Sphere: hero scale, crop, depth, static and authored-motion use.
3. Card: aligned chassis, core placement, copy hierarchy, price, status and CTA states.
4. Wings: white product mark, holdco mark and gradient-mask expression; never substitute invented geometry.
5. Collection: five-product stack, aligned catalogue, bundle and upsell compositions.
6. Channel mapping: website, email, ad still, social, video, document, app icon and OG image.

Each plate should decide anatomy and usage law—not attempt to finish a homepage around an unresolved primitive.

### 7. Continue in the new canonical repository

- Complete canonical cutover under `DEC-MIGRATION-SEQUENCE-001` before broad foundation or page construction.
- Build the approved typography and control systems plus the remaining surface, geometry and layout foundations in the new canonical repository.
- Rebuild the mobile hero using the approved product-object suite.
- Revisit primary-button finish as a bounded control refinement: restrained stroke, tonal gradient, micro-lift and glow must be compared against the approved simple control.
- Produce one golden homepage from approved foundations and components.
- Validate responsive behaviour and output consistency before considering Figma library generation or a live consumer migration.

## Human involvement

The human is needed at four high-leverage gates only:

1. Choose or reject Context Engine gradient candidates.
2. Approve the product-expression suite as one coherent family.
3. Approve the revised mobile hero and primary-button finish.
4. Approve the golden homepage and promotion to a named consumer after cutover.

Extraction, generation, static fallbacks, manifests, responsive variants and validation are agent-owned. The human should judge credible, polished plates—not implementation scaffolding.

## Repository and release boundary

### Now

Work in a clean Git worktree on `codex/mez-gradient-system`. This gives the design-system effort its own folder and branch while retaining the governance and research history already built in the Mezcorp repository. The original business checkout must remain untouched.

### Before returning to main

1. Complete and validate this bounded gradient-system checkpoint.
2. Review the diff and commit it on the design-system branch.
3. Merge only after the checkpoint is accepted.
4. Back up or push the accepted history before relying on `main` as recovery.
5. Keep future experimental plates in separate worktrees instead of the everyday business checkout.

### Dedicated repository

Do not maintain two unfinished writable authorities. Promote `mez-studios-design/brand-kit` after the product architecture, identity kernel and minimum canonical engine in `MIGRATION-FIRST-GATE.md` pass. At that point:

- `mez-studios-design/brand-kit` owns canonical brand data, rules, assets, generators, validators and versioned distributions;
- the Mezcorp business repository consumes a pinned release;
- website, email, ad and product teams consume the same versioned pack rather than copying files;
- Figma mirrors an approved release and never becomes an independent source of token truth.

The current worktree remains the bridge and rollback source. Foundations, components, the golden homepage and Figma are built after cutover in the new canonical repository, with this internal pack frozen as history.

## Exit criteria for the gradient-system lock

- Hero 03 feedback exists verbatim and its disposition is machine-readable.
- The assigned four gradients rebuild deterministically with no diff.
- The renderer uses one WebGL context and passes static-fallback checks.
- Dependency versions and rebuild commands are documented.
- A candidate can be generated without mutating canonical authority.
- Static/animated and cross-channel selection rules are documented.
- The old texture-coordinate workflow is no longer presented as canonical.
- Context Engine is assigned to the genuine `MZ-G12` source through `DEC-PRODUCT-ARCHITECTURE-001`.
- The product architecture human gate is complete. The next gate is agent-owned migration-snapshot, clean-clone and rollback validation.
