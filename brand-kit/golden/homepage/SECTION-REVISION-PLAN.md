# Golden Homepage — Section Revision Plan (post-r14 section review)

Source of truth for the revisions Olli requested in `round-14-section-review-feedback.json`.
Hero (GH-S01) and Footer are keeps. This plan covers the revises. Nothing here is built yet —
it is the agreed plan before bounded section rounds begin.

## Cross-cutting decision — product-card animation

All non-hero product cards animate **on hover**: exact static twin at rest, the live Deep Mineral
core spins up only while hovered. At most one core is ever live (the hovered one), so this stays
inside the one-live-core-per-ordinary-section rule — no motion exception needed. The locked hero
keeps its bounded 5-live treatment unchanged.

## Section plan

### GH-S02 · The problem — rebuild
- Current right-side "window pile" reads like generic chat bubbles, not the Mez grammar.
- Rebuild the visualisation as a structured *fragmentation* motif using the canonical tile grammar
  (charcoal, hairline borders, rounded geometry, mono labels) — disconnected interface tiles that
  clearly do not join up, resolving into the "operating layer it controls" line.
- Keep the locked copy and the three failure columns; restyle for one coherent system look.
- Exact visual shown in-round for approval.

### GH-S03 · The principle — real logomarks
- Keep the interchangeable-vs-owned instrument (direction approved).
- Replace text chips with **standalone greyscale logomarks**, sourced cleanly by me as monochrome
  SVGs: Claude, ChatGPT, Gemini, Perplexity (+ any others with a real mark). For coined/placeholder
  names without a real mark (e.g. OpenClaw), use a consistent quiet monogram fallback — flagged in-round.
- Greyscale keeps the row quiet and unified (on-ethos), not a colour logo-soup.
- Marks stored under a tracked assets path with provenance; used nominatively in an interchangeable-tools context.

### GH-S04 · Why — fix indent + split into two sections  (STRUCTURAL round)
- **Indent bug:** `.why-head` is capped at `max-width:860px` and centred as a block while its body runs
  full width, so the title sits ~260px inboard of its own content. Fix: left-align the header to the section edge.
- **Split:** break the crammed section into two — **"Built on ourselves first"** (the Build→Run→Break→
  Refine→Package process) and **"Operating proof"** (the three evidence cards, given room to breathe).
- Page goes **9 → 10 sections**: renumber GH-S05..GH-S09 down by one, and update the section contract
  (`homepage.source.json` sections, `homepage.schema.json` count + `GH-S0[1-9]` id pattern) and the round verifier.
  This is the heaviest round because of the renumber; do it first so later rounds work on final ids.

### GH-S05 · AI OS — bento + HL01 card + overlay removed  (new id after split)
- Rebuild as a **bento**: top = the AI OS product card on the **HL01 "Launch · corner hierarchy"** layout
  (wide dark chassis, large "AI OS" + extended name + description + filled action, vibrant gradient panel
  with corner Wings). This removes the non-canonical full-card darkening (`.ai-os-field--identity::after`) —
  the material stays vibrant; the dark is a deliberate chassis, not a murky overlay.
- Below: a **two-column split** — **How it works** (business context → AI OS → the AI that fits the job)
  on one side, **Features** (the four capability tiles) on the other.

### GH-S06 · Ecosystem — real product cards + hover animation  (new id after split)
- Replace the four tall full-bleed gradient cards with the **PO02 "Portrait · centred hierarchy"** product
  card: material tile with large **centred Wings** on top, **public name first**, extended name, description,
  and a **filled action** below (Coming soon · waitlist).
- Cards: Context Engine, AI Ads System, Claude Code OS, Organic Content OS.
- Animate on hover (per the cross-cutting rule).

### GH-S07 · Proof / testimonials — my call
- Keep it honest (testimonials stay consent-pending; nothing fabricated).
- Refresh the card design to the new grammar (cleaner hierarchy, consistent with the product cards),
  tighten the rhythm, keep the small product-core avatars. Options shown in-round.

### GH-S08 · Final route — my call
- Apply the consistent card treatment (same vibrant, non-darkened AI OS card as the new S05) and tighten
  the closing layout/hierarchy so it lands as a strong final CTA. Options shown in-round.

## Proposed round order

1. **R15 — GH-S04** indent fix + split + renumber (structural; settles ids)
2. **R16 — GH-S02** problem rebuild
3. **R17 — AI OS** bento + HL01 + overlay fix
4. **R18 — Ecosystem** PO02 cards + hover
5. **R19 — GH-S03** greyscale logomarks
6. **R20 — Proof + Final route** refinements

Each round follows the lockstep contract: workbench + source/schema/verifier + docs + LLM records, verified,
then presented. The whole-page human gate `H-GOLD-01-HOMEPAGE-PROOF` stays open throughout.

## Open items to confirm before R15
- Order above OK, or start with the AI OS darkening fix since it's the one bugging you?
- S03 fallback for coined names (OpenClaw etc.): quiet monogram vs drop — decide when we reach R19.
