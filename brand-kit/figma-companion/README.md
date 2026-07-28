# Mez Systems Figma companion

Status: approved companion mirror. Olli closed `H-FIG-02-FIGMA-COMPANION-APPROVAL` on 28 July 2026 after Phases 1–4, the detach audit and Gate B passed.

This directory records the repository side of the Figma companion. Figma mirrors the canonical code contracts under `brand-kit/`; it never becomes an independent source of values, component behaviour or product identity.

The historical file `Mez Systems — branding` (`HU0GVaDhatjWrKCiSg3wlU`) remains research evidence. Discovery found five historical pages but no local variables, styles, components or component sets. It will not be converted in place. After Olli approves the Phase 0 scope, the implementation will create a new dedicated companion file and record its exact file key here.

Phase artifacts:

- `phase-00-discovery.json` — read-only source inventory, Figma inventory, conflict map and proposed v1 scope.
- `phase-00-approval.json` — Olli's approval of the scope and conflict resolutions.
- `verify_phase_00.py` — proves the discovery record, programme sequence and frozen-candidate boundary agree.
- `phase-01-foundations.json` — exact live Figma inventory and source-parity results for variables and styles.
- `verify_phase_01.py` — proves the Phase 1 receipt retains the approved mirror boundary and audited counts.
- `phase-02-documentation.json` — ordered page inventory, visual inspection results and live page audit.
- `verify_phase_02.py` — proves the documentation receipt and page ledger agree.
- `phase-03-identity-expressions.json` — exact product identity, expression components, asset truth and rendered Phase 3 audit.
- `verify_phase_03.py` — proves the six expression sets, live inventory and runtime boundary agree with the build ledger.
- `phase-04-functional-components.json` — exact functional component inventory, runtime static-twin boundaries, content truth, rendered repairs, detach proof and final live audit.
- `phase-04-gate-b.json` — the agent design-excellence review before Olli's completed-library gate.
- `verify_phase_04.py` — proves the eighteen sets, 105 variants, fixture truth, detach audit, Gate B result and open human-gate boundary agree.
- `approval.json` — Olli's completed-library approval and the exact non-authority, publishing and consumer boundaries it preserves.

Olli closed the Phase 0 human gate on 28 July 2026. The dedicated companion is now `Mez Systems — Design System Companion` (`QxZT3FJ8BDXOZfBQDt0qPW`); `build-state.json` is the durable repository ledger for the phased build.

Phase 1 created eight local variable collections, 255 variables, 215 semantic alias values, fifteen semantic text styles and five depth styles. The live audit found zero broken aliases, zero missing WEB syntax declarations and zero implicit `ALL_SCOPES` assignments. Figma uses the exact upstream authoring family names recorded by the repository; Mez-prefixed font names remain runtime CSS aliases.

Phase 2 created four ordered, repository-traceable documentation pages: Cover, Foundations, Responsive & Runtime, and Source & Governance. All four were rendered and inspected. The final live audit found 409 text nodes, 638 variable-bound nodes and zero missing fonts; components remain intentionally absent until the later build phases.

Phase 3 created six component sets across six rendered and inspected pages: Product Material, Wings & Mark, Disc, Sphere colour fallback, Product Card Grammar and Trading Card. The whole-file audit found 29 components, six component sets, 29 instances and zero missing fonts. Figma fills use exact canonical PNG source masters because accepted WebP uploads rendered blank; runtime distribution continues to use the canonical hashed WebPs. The Sphere remains explicitly labelled a colour fallback, not a reproduction of renderer-owned depth.

Phase 4 created the fifteen canonical Phase B functional component sets plus static authoring twins for Global Navigation, Halftone Portrait and Testimonial Marquee: eighteen sets and 105 variants in total. Every set exposes editable component properties, all eighteen default variants detached without geometry or child-count loss, and the final whole-file audit found 134 components, 24 sets, 247 instances and zero missing fonts. Render inspection repaired footer collision, navigation overlap, portrait scaling, bento inset-card chrome and fabricated testimonial placeholder content before Gate B passed at 67/75. Olli then approved the completed structure through `H-FIG-02-FIGMA-COMPANION-APPROVAL`. The file is an approved companion mirror with no independent canonical, publishing, consumer or production authority.
