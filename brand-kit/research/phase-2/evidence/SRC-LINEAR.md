# Deep source study: Linear

Status: `EVIDENCE_CAPTURED`
Source ID: `SRC-LINEAR`
Captured: 20 July 2026, Australia/Sydney
Research role: direct competitor and software craft exemplar
Questions addressed: `RQ-01`, `RQ-02`, `RQ-03`, `RQ-04`, `RQ-06`, `RQ-07`
Rights boundary: observation only. Linear names, copy, assets, interface compositions, colours, marks, screenshots, and interaction signatures are excluded from Mez outputs.

## Capture metadata

- Scope: current public marketing, brand, method, documentation, integration, changelog, and design-process surfaces.
- Access: unauthenticated public pages only.
- Capture mode: rendered page text, accessible image descriptions, page structure, and official written explanations.
- Viewport confidence: desktop structure is well evidenced. Mobile recomposition and reduced-motion behaviour were not directly captured.
- Evidence standard: an observation is only stated as high confidence where an official public surface shows it or Linear describes the decision directly.
- Interpretation standard: mechanisms and transfer principles are analyst interpretations, not Linear claims.

## Official sources

| Ref | Surface | URL | Use |
| --- | --- | --- | --- |
| `LIN-S01` | Current homepage | https://linear.app/homepage | Product narrative, staged workflow proof, interface demonstrations, channel density |
| `LIN-S02` | Brand guidelines | https://linear.app/brand | Naming, mark hierarchy, monochrome preference, asset usage |
| `LIN-S03` | Linear Method | https://linear.app/method | Editorial system and transfer of product principles |
| `LIN-S04` | Current docs | https://linear.app/docs | Information architecture and dense instructional surface |
| `LIN-S05` | Integrations directory | https://linear.app/integrations | Taxonomy, scanning, cards, ecosystem proof |
| `LIN-S06` | March 2026 UI refresh | https://linear.app/changelog/2026-03-12-ui-refresh | Current consistency and hierarchy decisions |
| `LIN-S07` | 2024 interface redesign release | https://linear.app/changelog/2024-03-20-new-linear-ui | Density, contrast, hierarchy, theme evidence |
| `LIN-S08` | Design reset, part I | https://linear.app/now/a-design-reset | Governance, concept-first direction, whole-system redesign |

## Observed evidence

### Identity and recognition

#### `LIN-E01` Monochrome brand use is the default, not the fallback

- Surface: brand guidelines.
- Observation: Linear explicitly prefers monochrome wordmark use. Its brand colour is described as more suitable for backgrounds than for constant logo colouring. The wordmark is preferred when space permits; the logomark and icon form a deliberate small-space hierarchy.
- Mechanism: recognition is carried by name discipline, mark geometry, restraint, and context-sensitive mark selection rather than persistent colour saturation.
- Questions: `RQ-01`, `RQ-07`.
- Confidence: high.

#### `LIN-E02` Spacious presentation is part of the identity contract

- Surface: brand guidelines.
- Observation: Linear requires substantial breathing room around brand assets and discourages cramped presentation. The guidance is behavioural and easy to apply at different sizes.
- Mechanism: an invariant compositional attitude can be more portable than a decorative device. Restraint becomes recognisable through repetition.
- Questions: `RQ-01`, `RQ-04`, `RQ-07`.
- Confidence: high.

#### `LIN-E03` The public identity is reinforced by numbered system language

- Surface: homepage and Linear Method.
- Observation: homepage product stages are labelled as a sequence such as intake, plan, build, diffs, and monitor, with figure-like numbering. The Method is also organised into numbered principles and practices.
- Mechanism: repeated indexing, sequence, and editorial labelling make the brand feel like an operating system even when the logo is not the focus.
- Questions: `RQ-01`, `RQ-02`, `RQ-07`.
- Confidence: high.

### Product family and architecture

#### `LIN-E04` One workflow is divided by jobs, not by cosmetic sub-brands

- Surface: homepage.
- Observation: intake, planning, building, reviewing, and monitoring are separate product chapters. Each chapter uses a different work object and proof view, while the shared application shell, content model, and interaction vocabulary remain visible.
- Mechanism: shared chassis plus job-specific proof. Family resemblance comes from the underlying model and shell; distinction comes from the task, data, and state being demonstrated.
- Questions: `RQ-02`, `RQ-03`.
- Confidence: high.

#### `LIN-E05` Capability hierarchy survives expansion through stable objects

- Surface: homepage, docs, and integrations directory.
- Observation: issues, projects, initiatives, cycles, documents, agents, reviews, and insights recur across marketing and documentation. They are not renamed for each channel.
- Mechanism: durable object names reduce translation loss between acquisition, onboarding, product use, support, and agent integration.
- Questions: `RQ-02`, `RQ-07`.
- Confidence: high.

### Claim to literal proof

#### `LIN-E06` The homepage demonstrates claims with populated product states

- Surface: homepage.
- Observation: broad promises are followed by realistic issue titles, statuses, labels, comments, project timelines, code diffs, analytics, risk states, and agent activity. The examples contain enough operational detail to be read as plausible work rather than empty interface frames.
- Mechanism: claim, product object, state transition, and outcome are presented as one evidence chain.
- Questions: `RQ-03`.
- Confidence: high.

#### `LIN-E07` Agent capability is shown through traceable work, not a magical chat bubble

- Surface: homepage and March 2026 changelog.
- Observation: the agent example exposes assignment, session activity, repository context, changed files, draft review state, and handoff back to a person. The changelog connects coding-tool launchers to issues and says mobile sessions expose current and previous agent activity.
- Mechanism: AI is made credible by showing provenance, intermediate state, bounded action, and review.
- Questions: `RQ-03`, `RQ-06`, `RQ-07`.
- Confidence: high.

#### `LIN-E08` Changelog entries make product proof routine

- Surface: changelog.
- Observation: release entries pair concise statements of intent with named interface changes, operational detail, screenshots, availability notes, improvements, fixes, shortcuts, and API changes.
- Mechanism: proof is an ongoing publishing system, not a one-off launch-page treatment.
- Questions: `RQ-03`, `RQ-04`, `RQ-07`.
- Confidence: high.

### Density across channels

#### `LIN-E09` Density changes by task while hierarchy remains stable

- Surface: homepage, integrations directory, docs, and changelog.
- Observation: the homepage begins with low-density narrative and progressively exposes dense interface states. The directory uses scan-first categories and repeated cards. Docs use persistent taxonomy and compact lists. Changelog pages allow high detail after a short release summary.
- Mechanism: preserve hierarchy rules while varying the amount and granularity of evidence. Calm framing leads into task-appropriate density.
- Questions: `RQ-04`.
- Confidence: high.

#### `LIN-E10` The application refresh reduces chrome competition before increasing content density

- Surface: March 2026 refresh and 2024 redesign release.
- Observation: Linear says headers, navigation, and controls were standardised, sidebars were dimmed, icons redrawn, and contrast improved. Earlier redesign notes describe less visual noise while allowing the inbox to become denser.
- Mechanism: density is made usable by lowering the visual weight of the shell and increasing consistency, not by making every element larger or sparser.
- Questions: `RQ-01`, `RQ-04`.
- Confidence: high.

### Motion and state

#### `LIN-E11` Motion is implied by meaningful workflow transitions

- Surface: homepage and changelog.
- Observation: public proof is structured around status changes, agent progress, issue routing, roadmap stages, diff comparison, and changing project health. The March 2026 release describes mobile access to live agent-session activity.
- Mechanism: the useful motion vocabulary is state transition, progress, routing, reveal, and comparison. Motion should explain where work moved or what changed.
- Questions: `RQ-06`.
- Confidence: medium. The state model is strongly evidenced, but timing and easing were not measured.

### System transfer and governance

#### `LIN-E12` Product philosophy is packaged as a separate, navigable method

- Surface: Linear Method.
- Observation: principles are organised into direction and building practices with stable numbered entries. This makes behavioural standards available outside the interface itself.
- Mechanism: a transferable system contains operating doctrine and examples, not only visual assets.
- Questions: `RQ-07`.
- Confidence: high.

#### `LIN-E13` The integration directory makes interoperability visible

- Surface: integrations directory.
- Observation: integrations are grouped by user job and provenance, including products made by Linear, third-party agents, AI clients, engineering, automation, and collaboration tools. Each item explains the action it enables.
- Mechanism: transfer becomes easier when objects, actions, ownership, and connection paths are explicit and searchable.
- Questions: `RQ-02`, `RQ-07`.
- Confidence: high.

#### `LIN-E14` Large visual resets are treated as holistic governance work

- Surface: Design reset, part I.
- Observation: Linear describes accumulated design debt as a whole-system concern, advocates evaluating all affected surfaces together, and uses concept work to establish direction before production translation.
- Mechanism: establish a coherent north star, secure leadership support, then resolve the system across surfaces as one programme.
- Questions: `RQ-07`.
- Confidence: high.

## Mechanism synthesis

| Mechanism | Evidence | Why it works | Mez relevance |
| --- | --- | --- | --- |
| Recognition through restraint | `LIN-E01`, `LIN-E02`, `LIN-E03` | Repeated composition and editorial structure survive monochrome and logo-light contexts | Tests whether Mez can be known through layout behaviour rather than wings or gradients |
| Shared chassis, job-specific proof | `LIN-E04`, `LIN-E05` | Products feel related because they share objects and grammar, while each demonstrates a different task | Strong model for avoiding four colour-swapped product pages |
| Claim to object to state to result | `LIN-E06`, `LIN-E07`, `LIN-E08` | Concrete work states let the audience inspect the promised capability | Direct input to the Mez proof grammar |
| Calm shell, variable evidence density | `LIN-E09`, `LIN-E10` | Stable hierarchy absorbs denser content without turning into clutter | Useful across executive pages, product UI, reports, ads, and email |
| State-led motion | `LIN-E11` | Animation has semantic work to perform | Supports motion that communicates orchestration rather than atmosphere alone |
| Doctrine plus interoperable objects | `LIN-E12`, `LIN-E13`, `LIN-E14` | Humans and tools inherit the same language and intent | Useful for Figma, code, templates, LLM instructions, and governance |

## Category conventions versus distinctive mechanisms

### Category conventions

- Dark and light software themes.
- Product UI placed prominently in marketing.
- Integration cards and customer logos as credibility devices.
- Changelogs, documentation, and customer stories as proof channels.
- Short hero promise followed by feature chapters.
- AI agent activity represented through conversational and progress states.

These are table stakes. They should not be treated as evidence of a unique Linear expression.

### More distinctive Linear mechanisms

- Numbered, editorial treatment that connects company method to product stages.
- Unusually realistic and operationally legible interface proof on the homepage.
- Restraint used consistently enough to become a recognisable compositional behaviour.
- A product family organised as an end-to-end workflow rather than as disconnected feature cards.
- AI proof that includes provenance, work state, artefact change, and human review.
- Public design governance that links visual reset to company direction and accumulated design debt.

## Transfer principles for Mez

These principles are abstracted. They do not authorise use of Linear styling.

1. Define a small set of Mez compositional invariants that remain visible in monochrome, without marks, and without product colours.
2. Build the product family around shared objects and verbs, then give each product a different proof object, state model, and outcome.
3. Require every major capability claim to name or show a real object, a before or active state, an action, and an observable result.
4. Let low-density narrative frame dense proof rather than forcing one density level across every channel.
5. Reduce shell contrast and visual competition before adding denser operational information.
6. Specify motion as a change in state, ownership, confidence, progress, or relationship.
7. Publish the Mez method as operational doctrine that can be referenced by people, prompts, code comments, and component documentation.
8. Preserve canonical object names and actions across marketing, UI, documentation, email, and LLM contexts.

## Source signatures to exclude

- Linear's mark, wordmark, icon construction, or desaturated blue identity.
- Linear's exact numbered figure notation or stage names.
- Its homepage compositions, interface mockups, example issue content, or product object names.
- Its characteristic dark, restrained software aesthetic as a wholesale art direction.
- Exact navigation, sidebar, command menu, card, status, or diff treatments.
- Linear copy, customer proof, method language, motion curves, timing, or interaction sequences.
- Any combination that a reviewer could reasonably describe as Linear with Mez branding.

## Candidate Mez hypotheses, unapproved

| ID | Hypothesis | Based on | Required test before promotion |
| --- | --- | --- | --- |
| `MEZ-H-LIN-01` | A logo-free Mez page could remain recognisable through a fixed evidence rhythm: premise, system map, live state, verified outcome, decision. | `LIN-E03`, `LIN-E06`, `LIN-E09` | Produce monochrome pages for all four products and run blind family and originality review |
| `MEZ-H-LIN-02` | AI OS, Aurora, Prism, and Forge should share object grammar but each own one dominant proof form and state transition. | `LIN-E04`, `LIN-E05`, `LIN-E07` | Create a four-product contact sheet with colour removed and test both family recognition and job distinction |
| `MEZ-H-LIN-03` | Mez AI claims will become more credible if every agent action exposes origin, current state, changed artefact, confidence or exception, and human decision point. | `LIN-E06`, `LIN-E07` | Prototype one website section, one ad, one report panel, and one product state using the same evidence chain |
| `MEZ-H-LIN-04` | Mez channel density can vary safely if shell hierarchy and evidence order stay invariant. | `LIN-E09`, `LIN-E10` | Transform one approved proof story across web, ad, email, report, and UI, then compare information loss |
| `MEZ-H-LIN-05` | Mez motion should be authored from a state-transition vocabulary before visual animation styles are explored. | `LIN-E11` | Storyboard orchestration, progress, exception, handoff, and completion in static frames and reduced-motion equivalents |
| `MEZ-H-LIN-06` | A concise Mez operating method could act as a bridge between design principles, component behaviour, and LLM production rules. | `LIN-E12`, `LIN-E13`, `LIN-E14` | Encode one principle in prose, Figma guidance, code constraints, a prompt contract, and an automated check |

None of these hypotheses is a Mez decision, token, component, or production direction. Human approval and cross-source synthesis are required.

## Limitations and uncertainty

- No authenticated Linear workspace was inspected, so application-wide consistency is inferred from public product demonstrations and official release notes.
- Mobile layouts were not captured at controlled widths.
- Motion duration, easing, sequencing, hover behaviour, and reduced-motion fallbacks were not measured. `LIN-E11` is therefore a state-model finding, not an animation specification.
- Public homepage examples are curated demonstrations and may not represent all real-world product states.
- The current interface was refreshed in March 2026. Older 2024 design-process material remains useful for governance reasoning but should not be treated as a current visual specification.
- Exact visual values and source assets were deliberately not recorded because they are not transferable Mez inputs.

## Study conclusion

Linear's most useful lesson is not its dark interface or polished minimalism. It is the tight coupling between product language, believable work states, editorial sequence, and a restrained shell. The transferable opportunity for Mez is to make the identity emerge from how evidence is organised and how work changes state. The risk is superficial imitation: a dark page, sparse type, thin borders, and purple-blue atmosphere would copy category appearance without inheriting the underlying rigour.
