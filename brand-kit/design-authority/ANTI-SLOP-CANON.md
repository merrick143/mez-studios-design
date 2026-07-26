# Anti-slop canon

The ban list of AI design tells, reconciled to Mez Systems. Every rule here is a **defect**, not a
taste call. If a rendered surface breaks one, it is objectively wrong and it gets fixed, cited by ID.

**What this file is not.** It does not tell you what Mez looks like. That is
`brand-kit/docs/PRODUCT-CARD-DESIGN-ETHOS.md` and the foundations. Passing this canon means you
have not produced slop. It does not mean you have produced good design. That is
[`GATE-B-DESIGN-EXCELLENCE.md`](GATE-B-DESIGN-EXCELLENCE.md).

**Values come from tokens, never from this file.** Every hex and every measurement below is quoted
from `brand-kit/foundations/*/dist/tokens.css` for orientation. If a quoted value and the generated
token ever disagree, the token is right and this file has a defect to fix.

## Citing a rule

`{CATEGORY}-{NN}` plus a severity and an observable problem at a location.

> `LAY-02 CRITICAL: the S02 hero centres eyebrow, heading, lead and both chips on one axis at index.html:412`

| Category | Prefix | | Severity | Meaning |
|---|---|---|---|---|
| Colour | `COL` | | **CRITICAL** | Ships as recognisable AI slop. Blocks the gate. |
| Typography | `TYP` | | **MAJOR** | Reads as generic or templated. Fix before the gate. |
| Layout | `LAY` | | **MINOR** | Craft defect. Worth fixing, does not block. |
| Motion | `MOT` | | | |
| Icons and marks | `ICO` | | | |
| Content and copy | `CPY` | | | |
| Materiality and depth | `MAT` | | | |

IDs are stable. Never renumber. A retired rule keeps its ID, marked RETIRED with a date and reason.

---

## The default clusters

A surface can pass every individual rule below and still be slop because it lands inside one of
these whole aesthetics. Naming the cluster is a valid CRITICAL finding on its own.

| Cluster | Signature | Why it is a tell | Instead |
|---|---|---|---|
| **CL-01 · Warm cream editorial** | Cream `#FAF7F2` page, high-contrast serif display at 72px+, terracotta accent, letter-spaced small caps | The 2026 default "premium" preset. Every AI agency site. | Mez canvas `#F8F8F8`, greyscale text, Instrument Serif as a garnish on one phrase, never the display face. |
| **CL-02 · Near-black plus one acid accent** | `#0A0A0A` page, one saturated accent (acid lime, electric cyan, hot magenta) on every CTA, badge and dot | The default "technical startup" preset. Reads as a Vercel or Linear tribute. | Dark is the charcoal ramp, never `#0A0A0A` or `#000000`. The only colour is product gradient material. |
| **CL-03 · Broadsheet hairline columns** | Hairline rules between every block, multi-column body, uppercase tracked metadata, running `01 / 02 / 03`, faux masthead | The default "editorial" preset. The rules do no structural work; they are decoration cosplaying as a grid. | Whitespace and section rhythm separate. A hairline does structural work or it is cut. |
| **CL-04 · Generative-geometry theatre** | Point clouds, orbital rings, flow fields, oscilloscope traces and node graphs deployed as a section's whole idea | The 2026 "AI company" preset, and the specific failure of Golden Homepage GH-S02 lab round 2. Complexity substituting for an argument. | One authored device that carries the section's actual claim. Sophistication is in what the device *means*, never in how many primitives it has. |

**The check.** Screenshot the surface. Ask: could this be any of a thousand AI-built pages with the
logo swapped? If yes, name the cluster. CRITICAL.

---

## COL · Colour

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **COL-01** | CRITICAL | The AI purple/blue aesthetic. Any hue in the 250–280° band as an accent. `indigo-*`, `violet-*`, `purple-*`, `#6366F1`, `#8B5CF6`, `#7C3AED`. | Greyscale plus product gradient material. Nothing else. | `grep -riE "indigo-|violet-|purple-|#6366f1|#8b5cf6|#7c3aed"`. Any hit is a finding. |
| **COL-02** | CRITICAL | Coloured glow shadows. `box-shadow: 0 0 40px rgba(139,92,246,.4)` and every chromatic bloom under a card. | The depth tokens, tinted to ink: `--mz-depth-contact`, `--mz-depth-raised`, `--mz-depth-overlay`. Nothing else. | Any `box-shadow` colour that is not the ink `rgb(13 13 13 / …)` family. |
| **COL-03** | CRITICAL | Gradient-mesh backgrounds. Stacked blurred radial blobs behind a section, `filter: blur(120px)` orbs, aurora backdrops. | A flat surface token. Gradient material appears as an **object** with edges, never as atmosphere. | `grep -E "radial-gradient"` in any background or pseudo-element; `blur\((8|9|1[0-9])[0-9]px\)`. |
| **COL-04** | CRITICAL | Multi-hue gradient text. `background-clip: text` on a two-plus-hue gradient. | Solid `--mz-text-primary`. Emphasis is weight, size and space, never a gradient fill. | `grep -E "background-clip:\s*text|-webkit-background-clip"` on any heading. |
| **COL-05** | CRITICAL | Pure black `#000000` (`--mz-colour-neutral-1000`) as a surface, a text colour or a border. | The charcoal ramp: `#171715` base, `#1B1B19` recessed, `#252523` raised, `#2E2E2E` secondary. Pure black exists as a token for computation only. | `grep -iE "#000\b|#000000|rgb\(0,\s*0,\s*0\)"` on any surface, text or border declaration. |
| **COL-06** | MAJOR | More than one colour source in a viewport. Two products' gradients competing, or a gradient plus a chromatic accent. | One material carries the colour. Everything structural is greyscale. | Count distinct non-greyscale sources in the render. More than one is a finding. |
| **COL-07** | MAJOR | Bespoke greyscale literals where a token exists. `rgba(25,25,25,.42)` for a card outline. | `--mz-border-default` `#DADAD6`, `--mz-border-strong` `#8A8A84`, `--mz-text-muted` `#666662`. Olli found a bespoke outline "harsh" precisely because it was off-token. | Every colour literal in a component. If a token matches within a few percent, the literal is a finding. |
| **COL-08** | MAJOR | Two grey families in one build: a cool slate next to a warm stone next to a neutral zinc. | One ramp, `--mz-colour-neutral-*`. It is warm-neutral by design. | Sample every grey. Hue varying more than a few degrees across them is a finding. |
| **COL-09** | MAJOR | Colour as the only carrier of a state or meaning. | Pair colour with text, icon, weight or border. The feedback tokens exist for forms and feedback, never for decoration. | Render in greyscale. Every state must still read. |
| **COL-10** | MAJOR | Gradient material on a page background, a section background, a bundle container, or behind the Wings mark. | Material belongs to a **product object**: disc, sphere, plate, field, portrait, capsule, card. | Every gradient must resolve to a product element with a registry ID. |
| **COL-11** | MINOR | Colour animating on hover. A CTA that shifts hue, a link changing to an accent. | Lift `--mz-control-hover-lift`, an underline, a border change. Hue is not an interaction language here. | `grep -E "transition[^;]*(background-color|color)"` on controls. |
| **COL-12** | MINOR | Dark treated as a theme in a light context, reusing light tokens on a dark surface. | A dark band is a **named treatment** carrying `data-mz-mode="dark"`, which swaps the whole token set. | Every dark surface. Text inside it resolving to a light-mode token is a finding. |

---

## TYP · Typography

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **TYP-01** | CRITICAL | Default-metric display type. Any heading over 32px at `letter-spacing: 0` and `line-height: 1.2+`. This is the single most common AI tell. | The locked scale, which is aggressive on purpose: hero `-0.064em` tracking at `0.91` leading, section `-0.052em` at `0.98`, title `-0.044em` at `1.0`. The negative tracking and sub-1 leading are the whole point. | Computed style of every heading over 32px. Tracking ≥ 0 or leading > 1.1 is a finding. |
| **TYP-02** | CRITICAL | A font family that is not in the foundation. Geist, Outfit, Satoshi, Space Grotesk, system stack as display. | `--mz-font-display` Mez Geist, `--mz-font-body` Mez Inter, `--mz-font-editorial` Instrument Serif, `--mz-font-technical` IBM Plex Mono. Four roles, no fifth. | Every `font-family`. Anything outside the four tokens is a finding. |
| **TYP-03** | MAJOR | An off-scale size. A heading at `52px` because it looked right. | The named roles: display hero/section/title, heading section/subsection, body lead/default/compact, ui control/label, caption, technical, numeric display/tabular, editorial accent. | Every rendered `font-size` must trace to a `--mz-type-*` token. |
| **TYP-04** | MAJOR | Decorative `01 / 02 / 03` numbering or `STEP 01` eyebrows where no real sequence exists. | Name the function in the eyebrow. Number only a genuine ordered process. Olli has rejected decorative IDs, numbers, slashes and archive codes by name. | `grep -E "STEP\s*0|^\s*0[1-9]\s*$"` in markup. |
| **TYP-05** | MAJOR | Body measure wider than roughly 65 characters. | `--mz-content-reading` `720px`, or a `ch` cap. | Widest body line at desktop. Over ~75 characters is a finding. |
| **TYP-06** | MAJOR | Title Case in headings, buttons, eyebrows or nav. | Sentence case. Proper nouns keep their casing (AI OS, Mez Systems, Wings). Uppercase eyebrows are `text-transform`, never an authored string. | Any capitalised non-proper-noun mid-string. |
| **TYP-07** | MAJOR | Faded body achieved with a light weight (`font-weight: 300`) or opacity on the text node. | `--mz-text-muted`. Body weights are 400–450; the system has no 300. | `grep -E "font-weight:\s*(100|200|300)"`, and `opacity` on text nodes. |
| **TYP-08** | MAJOR | Centred body paragraphs longer than two lines. | Left align body. Centring is for one short line. | Any `text-align: center` on a block wrapping past two lines. |
| **TYP-09** | MINOR | Instrument Serif as the display face, as body, or on more than one phrase per surface. | One accent phrase, one place, doing a turn the sans cannot. `--mz-type-editorial-accent`. | Count serif runs. More than one per section is a finding. |
| **TYP-10** | MINOR | Mono used decoratively because it "looks technical". Mono nav, mono body, mono headings. | `--mz-type-technical` is for code, paths, and technical labels only. Gradient IDs like `MZ-G13` never appear in customer copy. | Every mono node must contain a genuine technical string. |
| **TYP-11** | MINOR | Uppercase runs longer than about four words, or uppercase without positive tracking. | `--mz-type-ui-label`, `0.09em` tracking, short. | Any uppercase string over four words. |

---

## LAY · Layout

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **LAY-01** | CRITICAL | Three equal cards in a row as the default content shape, repeated down the page. | Vary count and weight. Two with one dominant, four asymmetric, one hero plus a list. If three is genuinely right, make them structurally different, not three clones. | Sibling groups of exactly three with identical class strings. Two or more such groups is CRITICAL. |
| **LAY-02** | CRITICAL | The centred-everything stack. Centred eyebrow, heading, sub, button pair and chip row all on one axis. | Asymmetry. Left-anchored type with visual weight offset, or an authored split. At most one centred element in a stack. | Count centred axes in the subtree. Three or more is a finding. |
| **LAY-03** | MAJOR | A page that is a vertical run of visually identical bands: same width, same alignment, same density, seven times. | Vary density and rhythm. Alternate dense against sparse. This is the recorded DS-009 weakness and Olli's "cramming too much in" note on GH-S04. | Screenshot the full page at 25%. Identical silhouettes down the page is a finding. |
| **LAY-04** | MAJOR | Icon-plus-heading-plus-two-lines feature grids as the answer to every section. | Show the product. Real material, real UI, a real number. A feature grid is one tool, not the page. | Two or more feature-grid sections on one page is a finding. |
| **LAY-05** | MAJOR | An off-scale radius, or a literal radius value in a component. | The closed set: `--mz-radius-fine` 4, `compact` 8, `control` 12, `container` 16, `panel` 24, `frame` 32, `full` 9999. | Every `border-radius`. Anything not resolving to a token is a finding. |
| **LAY-06** | MAJOR | Off-scale spacing, or a section inventing its own vertical rhythm. | The 4px scale to 160, and `--mz-section-compact` / `default` / `spacious` between sections. | Every gap and padding must resolve to a `--mz-space-*` or section token. |
| **LAY-07** | MAJOR | Sharp outer corners on a card, plate, field or control. | Rounded is the brand default. An internal join where two surfaces meet may go flat; the outside silhouette stays rounded. Approved invariant 2. | Any outer container at `border-radius: 0`. |
| **LAY-08** | MAJOR | Content that does not reflow. Horizontal scroll on the page body at 320px. | Wide content scrolls inside its own `overflow-x: auto`. The body never scrolls horizontally. | Load at 320px. `document.body.scrollWidth > window.innerWidth` is a finding. |
| **LAY-09** | MAJOR | A layout that breaks when the registry returns a different number of products. Hardcoded counts, fixed five-across grids. | Count-independent layouts reading canonical registry data. Approved invariant 10. | Render with n−1 and n+1 products. Any break is a finding. |
| **LAY-10** | MINOR | Full-width containers with no cap, so text runs the whole monitor. | `--mz-content-standard` 1160, `--mz-content-wide` 1380, `--mz-content-reading` 720. | Load at 2560px. Body spanning full width is a finding. |
| **LAY-11** | MINOR | Hairline rules as page-wide texture (see CL-03). | Whitespace separates. A hairline is `--mz-border-default` doing structural work on a card, table or split. | Standalone full-width dividers. More than two per page is a finding. |
| **LAY-12** | MINOR | Small inset cards nested inside larger cards. | A cell is a full composition: full-bleed material, media, proof or overlay filling it. Phase B pantry rule 4. | Any card whose direct child is another bordered card. |

---

## MOT · Motion

**This category is where the superseded MezCorp pack was most wrong.** That pack banned animated
gradients outright. In this system the living Deep Mineral core is the point. What is banned is
motion without a job, and motion that escapes its allocation.

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **MOT-01** | CRITICAL | More than one live core in a viewport. A second WebGL context. `mountLivingCore` where a shared renderer exists. | Exactly one `data-mz-core`. One renderer from `mountLivingCores`, then `renderer.mount(el, id, …)`, `renderer.surfaces.delete(oldEl)`, remove the old canvas. Approved invariant 6. | Count `data-mz-core`. Count WebGL contexts. Anything above 1 is a finding. |
| **MOT-02** | CRITICAL | No reduced-motion fallback, or a fallback that shifts layout. | The exact static twin, same box, no reflow. `prefers-reduced-motion: reduce` holds the composition fully legible. | Emulate reduced motion. Any layout shift or blank box is a finding. |
| **MOT-03** | CRITICAL | Mounting a core on an empty layer div positioned by stylesheet `position: absolute`. | Mount only on intrinsically sized elements, such as the aspect-ratio material div. `mount()` stamps inline `position: relative`, inline beats the stylesheet, and the layer collapses to 0×0 showing only the static twin. This was the R03–R05 "not animated" defect. | Measure the mounted host's client rect. 0×0 is a finding. |
| **MOT-04** | CRITICAL | Motion applied to Wings, type or layout. Typewriter effects, counting numbers, scrambling characters, word-by-word fades. | The material moves. Identity and structure hold still. Approved invariant 6, and rejected by name. | `grep -iE "typewriter|typed|countup|text-scramble"`, plus any keyframe targeting a Wings or text node. |
| **MOT-05** | MAJOR | Content that does not exist without JavaScript, or entrance animation applied ungated. | Entry reveal is gated behind the canonical JS-added body class (`entry-armed`). Content must survive with JS off. | Disable JS. Any invisible content is a finding. |
| **MOT-06** | MAJOR | Parallax, scroll-driven layout, or `addEventListener('scroll', …)` driving animation. | `IntersectionObserver` or CSS scroll-driven animation, for entry only. | `grep -E "addEventListener\(\s*['\"]scroll"`, `grep -iE "parallax"`. |
| **MOT-07** | MAJOR | A manual "animate" control, a play button, or a motion toggle. | A focal core is alive by default. Rejected explicitly in Product Card round 06. | Any control whose only job is to start motion. |
| **MOT-08** | MAJOR | Off-token duration or easing. `150ms` here, `0.3s` there, `ease-in-out`. | `--mz-motion-fast` 120ms, `--mz-motion-default` 180ms, `--mz-motion-control-ease` `cubic-bezier(.2,.7,.2,1)`. Core rendering runs on its own clock and is not bound by these. | Every literal duration or easing keyword in a transition. |
| **MOT-09** | MAJOR | Canvas count accepted as proof of animation. | Wrap `drawArrays`/`drawElements` on the GL prototypes and count calls, **and** diff two element screenshots seconds apart. Expect >10% changed pixels on a live surface. | A round claiming "animated" with no frame evidence is a finding. |
| **MOT-10** | MINOR | Motion with no job. A hover that confirms nothing, an entrance that orients nothing. | Name the action each animation confirms. If you cannot, cut it. | Per animation, state the job. |

---

## ICO · Icons and marks

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **ICO-01** | CRITICAL | Invented, fake or lookalike brand logos. Drawing a "Claude-ish" mark because the real one was not to hand. | `brand-kit/assets/third-party-marks/registry.json`. If a name has no real mark, cut the slot. GH-S03 failed on this twice. | Every logo traces to a registry entry. |
| **ICO-02** | MAJOR | Hand-rolled SVG icon paths written by the model. | A real icon set at one stroke weight, or a registry mark. In workbench HTML, note that the verifier bans `http://` anywhere, so an inline `<svg xmlns=…>` fails the round: use rotated hairline divs for rules and geometry. | Any inline `<path d="…">` not traceable to a named set or the registry. |
| **ICO-03** | MAJOR | Emoji as interface icons. | Real icons. | `grep -P "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]"` in markup. |
| **ICO-04** | MAJOR | Filled logo boxes. Each mark in its own coloured plate, rounded square or circle. | Freestanding symbols, greyscale, optically sized, no container. "Integration identity must be real and quiet." Phase B pantry rule 5. | Any logo with a background that is not the page surface. |
| **ICO-05** | MAJOR | Wings sprinkled wherever they fit: forced onto a card, doubled over material that already fills the field. | Wings are composed. Larger when identity is the focal event, smaller as corner support, **omitted** when material already fills the field. Approved invariant 4, pantry rule 6. | Per Wings instance, name its identity job. |
| **ICO-06** | MINOR | An icon on every card, list item and heading, as decoration. | Icons carry meaning or they are cut. | Remove each icon. If nothing is lost, it is a finding. |
| **ICO-07** | MINOR | Mixed icon sets, or a Wings asset rendered off-colour. | One set, one stroke. `wings.svg` is `fill="currentColor"`: as an `<img>` it needs `filter: brightness(0) invert(1)` to render white. | Every icon source; every Wings render. |

---

## CPY · Content and copy

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **CPY-01** | CRITICAL | Placeholder identity content. "John Doe", "Acme", "Company Name", "Lorem ipsum". | Real Mez content, or nothing. An empty state beats a fake person. | `grep -iE "john doe|jane smith|acme|lorem ipsum|your company"`. |
| **CPY-02** | CRITICAL | Fabricated statistics. `99.99% uptime`, `10x faster`, `500+ customers`, `4.9/5 from 2,000 reviews`. | Only numbers that are true and sourced. With no number, write the sentence without one. | Every numeral traces to a real record. |
| **CPY-03** | CRITICAL | Fabricated testimonials, invented customer companies, stock faces presented as users. | Real quotes with real attribution, or no testimonial. | Every quote traces to a real person and source. |
| **CPY-04** | CRITICAL | The banned hype words: **unlock, unleash, supercharge, revolutionise, elevate, seamless, empower**. | Name what the system does, in concrete nouns. If a sentence needs an adjective to feel exciting, cut the adjective and name the thing. | `grep -iE "unlock|unleash|supercharge|revolutionis|elevate|seamless|empower"`. |
| **CPY-05** | CRITICAL | Em dashes and double hyphens in any authored string, doc, review or comment. | Full stops, commas, colons, or an interpunct `·` for label separators. | `grep -P ":|--"` outside code and CLI flags. |
| **CPY-06** | CRITICAL | American spellings. | Australian English: colour, organise, behaviour, centre, licence, prioritise. | `grep -iE "\bcolor\b|\borganiz|\bbehavior\b|\bcenter\b"` outside CSS properties and code identifiers. |
| **CPY-07** | MAJOR | Extended system names leading the public product name. Internal codes, gradient IDs, slashes or edition language in customer hierarchy. | Public name first, extended system name second, job sentence third. Approved invariant 1. | Every product lockup's first line. |
| **CPY-08** | MAJOR | Generic AI phrasing. "in today's fast-paced world", "the future of X", "harness the power of", "take X to the next level", "it's not just X, it's Y". | Say what it does. One concrete noun beats three adjectives. | `grep -iE "fast-paced|the future of|harness the power|next level|it's not just"`. |
| **CPY-09** | MAJOR | Collector, scarcity or edition framing in ordinary product discovery. | System Editions were removed from Product Card. Collectible language belongs to the Trading Card expression and nowhere else. | `grep -iE "edition|limited|collect|rare|drop"` in product copy. |
| **CPY-10** | MAJOR | Exclamation marks, or an invented CTA verb. | A full stop carries the line. CTA verbs: **Get**, **Join**, **Explore**, **See**, **Open**, **Start**. Log a gap before inventing. | Every button label's first word. |
| **CPY-11** | MINOR | A sub-line that restates the heading in longer words. | The sub adds what the heading could not carry. If it restates, cut it. | Read heading plus sub as one sentence. |
| **CPY-12** | MINOR | Missing alt text, or alt that says "image" / "screenshot". | Describe what it shows and why it is there. Decorative gets `alt=""`. | Every `<img>`. |

---

## MAT · Materiality and depth

| ID | Sev | Ban | Instead | Check |
|---|---|---|---|---|
| **MAT-01** | CRITICAL | Glassmorphism. `backdrop-filter: blur()` panels, frosted cards, translucent navs. | Opaque surfaces from the token stack. Glass was rejected by name as a premium shortcut. | `grep -E "backdrop-filter|backdrop-blur"`. Any hit is a finding. |
| **MAT-02** | CRITICAL | Glow, halo, bloom or diffuse spread behind a disc, sphere, core or mark. | Hard edge. The material's own light is the whole effect. Glow is retired and never rebuilt. | Any `box-shadow`, `filter: drop-shadow` or radial layer behind a product object. |
| **MAT-03** | MAJOR | Ambient decorative shadow on an editorial card. | Editorial and split-card surfaces are **hairline only**: `--mz-border-default`, no shadow. The depth tokens exist for controls, overlays and genuine elevation, not for making a flat card feel premium. | Every `box-shadow` on a static content card. |
| **MAT-04** | MAJOR | Stacked depth cues: border **and** shadow **and** background tint **and** hover lift on one element. | One depth cue per element. | Count cues per card. More than one is a finding. |
| **MAT-05** | MAJOR | Grey placeholder blocks standing in for the product. A rectangle labelled "Product screenshot". | Show the real thing: a real render, real material, real output. If it does not exist, cut the slot rather than fake it. | Any solid-fill rectangle in a proof slot. |
| **MAT-06** | MAJOR | Noise, grain, scanline or paper-texture overlays for "premium" feel. | Nothing. The surfaces are clean. | `grep -iE "noise|grain|scanline|texture"` in backgrounds and overlays. |
| **MAT-07** | MAJOR | Fake 3D: model-drawn isometric mockups, perspective-skewed browser chrome, floating device frames. | A real render in a plain frame, or no frame. | `rotateX`, `rotateY` or `perspective` on a product image. |
| **MAT-08** | MAJOR | A white outline stroke on a dark object. | Rejected by name. Use a charcoal-ramp border or none. | Any light border on a dark surface outside the dark-mode token set. |
| **MAT-09** | MINOR | Borders heavier than the hairline token without cause. | `--mz-border-width-hairline` 1px. Emphasis 2px and focus 3px exist for their named jobs. | `grep -E "border[^;]*[2-9]px"` outside focus and emphasis. |
| **MAT-10** | MINOR | A focus ring removed, or replaced by a colour change only. | `--mz-focus-ring`, `--mz-focus-width` 3px at `--mz-focus-offset` 3px. | `grep -E "outline:\s*(none|0)"` without a replacement ring. |

---

## Where a generic field rule collides with a Mez decision

Cite the exception, do not raise the generic rule.

| Generic rule | Mez position | Why |
|---|---|---|
| "Never animate a gradient" | The living Deep Mineral core is **canonical and alive by default**. | The gradients are the point of the system. What is bounded is allocation: one core per viewport, exact static twins, no motion on Wings, type or layout. See MOT-01 to MOT-04. |
| "No scroll reveal, ever" | One canonical entry reveal, gated behind the `entry-armed` body class. | Content must survive with JS off, and there is no parallax and no per-element stagger cascade. See MOT-05. |
| "Ban Inter" | Mez Inter is the body face; Mez Geist is display. | The tell is default metrics, not the typeface. TYP-01 checks metrics. |
| "Never use a dark section mid-page" | Dark is a named treatment carrying `data-mz-mode="dark"`. | It swaps the whole token set rather than reusing light tokens on dark. See COL-12. |
| "Cards need elevation to read" | Editorial cards are hairline-only. | Ambient shadow was rejected as a premium shortcut. See MAT-03. |
| "Never centre" | One centred element is fine; the centred **stack** is the tell. | See LAY-02. |

---

## Using this file

**Read it before generating.** It constrains what you make. Running it as a post-hoc filter produces
work that is slop with the worst tells filed off, and it is visible.

**Sweep in ID order after rendering.** Screenshot first. Never audit from source alone.

**Cite IDs when reviewing.** "The hierarchy is weak" is useless. "LAY-02 CRITICAL: the hero centres
eyebrow, heading, sub and both buttons on one axis" is a finding.

**Adding a rule.** Next free ID in its category, correct severity, concrete check. Never renumber.

**A defect is not a taste call.** A defect is objectively wrong and you fix it. A taste call is
Olli's, and it goes to him as a bounded packet. If a rule here would force a change to an approved
decision, stop and escalate.
