# 17 · Voice and copy

Status: DEFAULT · working values, flag deviations to Olli

The LLM writes every word on the site, and until now it had two lines of guidance and a lot of licence, so builds kept inventing hype. This doc closes that. It sets the register (how a Mez Systems sentence sounds), the naming law (the exact strings for the product, the holdco and the endorsement), the verbs a call to action may start with, the words that are banned, and the character limits copy has to live inside. It then ships real approved copy for the home hero and the four suite cards, marked DEFAULT for Olli to sign off, so no build has to guess the words again.

Layout and slots come from [13-sections.md](13-sections.md); components from [07-ui-components.md](07-ui-components.md); the roster from [../products.json](../products.json). This doc governs the words that fill those slots, nothing about pixels.

---

## Language law

The voice is plain, calm and declarative. It describes what the system does in concrete nouns. It does not sell with adjectives.

| Rule | The law |
|------|---------|
| English | Australian English. Colour, organise, behaviour, licence, centre. |
| Case | Sentence case everywhere, including headings and buttons. "Get the AI OS", not "Get The AI OS". "One system your whole business runs on", not title case. |
| Dashes | No em dashes and no double hyphens anywhere. Use full stops, commas, colons, or an interpunct (·) for label separators. Single hyphens in real compound words (one-time, text-CTA) are fine. |
| Exclamation marks | None in UI copy. A full stop carries the line. |
| Oxford comma | No mandate either way. Keep it natural: add the comma when it removes ambiguity, drop it when the line reads clean without it. |
| Numbers | Prices and counts are shown plainly ($99 · one-time). Never dress a number up. Never show a price on a nav or a product card ([13-sections.md](13-sections.md)). |

> **The rule.** A Mez Systems line states what the system does, in Australian English, in sentence case, with no em dash and no exclamation mark. If a sentence needs an adjective to feel exciting, cut the adjective and name the thing instead.

---

## Naming law

These strings are fixed. Copy them exactly.

| Thing | Exact string | Notes |
|-------|--------------|-------|
| The product | **AI OS** | A space between "AI" and "OS". |
| The holdco | **Mez Systems** | The company that makes the products. |
| The endorsement | **A Mez Studios company** | The footer endorsement line ([13-sections.md](13-sections.md) · Footer). |
| Core codes | never in customer copy | MZ-G13, MZ-G20 and the rest are internal gradient IDs ([../products.json](../products.json)). They never appear on the site. |

**Banned spellings.** "AIOS" (no space) and "Atlas" (the retired codename) never appear in any copy ([../products.json](../products.json) is the authority).

**Casing carve-out.** Sentence case governs authored copy: headings, body, eyebrows, subs, buttons. Proper nouns keep their given casing. Those are the product names (AI OS, Aurora, Prism, Forge), the holdco (Mez Systems), the endorsement (A Mez Studios company), and the canonical function names from [../products.json](../products.json): AI Operating System, Auto Ads System, Analytics Pack, Claude Code OS. Where the design renders an eyebrow or a function label in uppercase, that is a typographic transform in CSS, not a change to the authored string.

---

## Call-to-action semantics

A CTA names the action and the product state honestly. Use the smallest approved action family
that fits the reader's next step.

| Intent | Approved verb | Example |
|--------|---------------|---------|
| Purchase | **Get** | Get the AI OS |
| Planned-product interest | **Join** | Join the waitlist |
| Discovery | **Explore** or **See** | Explore Aurora · See what it runs |
| Access | **Open** | Open the dashboard |
| Onboarding | **Start** | Start here |

The primary purchase CTA is locked to **"Get the AI OS"** ([07-ui-components.md](07-ui-components.md)).
The planned-product primary CTA is **"Join the waitlist"**. Do not force every functional action
through a five-verb whitelist. Choose from these semantic families, and log a gap before inventing
a new promise or action.

**Banned words.** These seven, and their variants, never appear in any copy:

| Banned | Variants also banned |
|--------|----------------------|
| Unlock | unlocks, unlocking, unlocked |
| Unleash | unleashes, unleashing |
| Supercharge | supercharges, supercharged, supercharging |
| Revolutionise | revolutionise, revolutionize, revolutionary, revolution |
| Elevate | elevates, elevated, elevating |
| Seamless | seamlessly |
| Empower | empowers, empowering, empowerment |

> **The rule.** A button uses the approved verb for its intent: Get for purchase, Join for
> planned-product interest, Explore or See for discovery, Open for access, and Start for
> onboarding. It never uses a hype verb. If none of these fits, log the missing action before
> inventing one.

---

## Headline register

Headlines are plain, declarative and built from systems language. They name what the system does with concrete nouns. They do not reach for hype adjectives.

The flagship line is:

> **One system your whole business runs on**

That is the register in one sentence: a concrete noun (system), a plain verb (runs), no adjective doing the selling. Write to it.

**Do**
- State the job the system does. "AI OS runs the work your business repeats every day."
- Use concrete nouns: system, dashboard, ads, analytics, one place, a weekend.
- Keep the verb plain: runs, ships, knows, sees, sets up.

**Avoid** (beyond the seven banned words above, these read as hype and weaken a declarative line): effortless, magical, game-changing, next-level, cutting-edge, world-class, best-in-class, blazing-fast, insanely, ultimate, powerful, robust. If a headline leans on one of these, it is describing a feeling, not the system. Name the system instead.

---

## Character limits

Copy lives inside the slot limits from [13-sections.md](13-sections.md). These are the real numbers from that doc's machine-readable block, restated here so a copywriter never has to leave this page. Limits cap the characters, not the pixels.

| Section | Slot | Max chars | Note |
|---------|------|-----------|------|
| Nav | Wordmark | 16 | "Mez Systems". |
| Nav | Nav link (×2) | 14 | "Products", "Pricing" by default. |
| Nav | CTA label | 14 | Locked "Get the AI OS". Never a price. |
| Hero | Eyebrow | 28 | |
| Hero | H1 | 60 | |
| Hero | Sub | 140 | |
| Hero | Primary CTA | 14 purchase / 20 planned | "Get the AI OS" or "Join the waitlist". |
| Hero | Ghost CTA | 24 | |
| Feature row | Eyebrow | 24 | |
| Feature row | Heading (H2) | 48 | |
| Feature row | Body | 180 | |
| Feature row | Bullet (×3) | 48 | |
| Feature row | Text-CTA | 24 | |
| Suite grid | Section eyebrow | 24 | Optional. |
| Suite grid | Section heading (H2) | 48 | Optional. |
| Suite grid | Product name | 16 | From [../products.json](../products.json). |
| Suite grid | Function label | 28 | |
| Suite grid | Status chip | 12 | Maps to `status` (Live / Planned). |
| Suite grid | Card body | 60 | One line. |
| Suite grid | Card text-CTA | 20 | Never a price on a card. |
| Pricing moment | Eyebrow | 24 | |
| Pricing moment | Heading | 40 | |
| Pricing moment | Price string | 16 | Plain "$99 · one-time". |
| Pricing moment | Price caption | 48 | |
| Pricing moment | Inclusion (×6) | 48 | |
| Pricing moment | CTA label | 14 | Locked "Get the AI OS". |
| Pricing moment | GST note | 80 | AU buyers, per [15-commerce.md](15-commerce.md). |
| FAQ | Section heading | 40 | |
| FAQ | Question (×8) | 80 | |
| FAQ | Answer | 280 | |
| CTA band | Eyebrow | 24 | |
| CTA band | Heading | 52 | |
| CTA band | Sub | 120 | |
| CTA band | CTA label | 14 | Locked "Get the AI OS". |
| Footer | Endorsement | 24 | Locked "A Mez Studios company". |
| Footer | Column heading (×4) | 20 | |
| Footer | Link label (×6 per column) | 24 | |
| Footer | Legal line | 80 | |
| Quote band | Pull-quote | 140 | Instrument Serif italic, one per page. |
| Quote band | Attribution | 48 | |
| Gradient strip | Eyebrow | 24 | |
| Gradient strip | Heading (H2) | 48 | |
| Gradient strip | Surface label (×3) | 20 | |

---

## Approved copy defaults

These are working copy, marked DEFAULT for Olli to sign off. Every string here obeys the language law, the naming law and the character limits above.

### Home hero (DEFAULT)

| Slot | Copy | Chars / limit |
|------|------|---------------|
| Eyebrow | The AI operating system | 23 / 28 |
| H1 | One system your whole business runs on | 38 / 60 |
| Sub | AI OS runs the work your business repeats every day, from one place, so you stop stitching ten separate tools together. | 119 / 140 |
| Primary CTA | Get the AI OS | 13 / 14 |
| Ghost CTA | See what it runs | 16 / 24 |

The eyebrow names the category, the H1 is the flagship line, the sub states the job in concrete nouns, the primary CTA is locked, and the ghost CTA uses an allowed verb (See).

### Suite grid cards (DEFAULT)

All four products, one card each ([13-sections.md](13-sections.md) · Suite grid). The function label is the canonical string from [../products.json](../products.json). Live products carry a "Get" CTA; planned products carry an "Explore" CTA so the wording does not imply a purchase that does not exist yet.

| Product | Function label | Status chip | Card body | Card text-CTA |
|---------|----------------|-------------|-----------|---------------|
| **AI OS** | AI Operating System | Live | Your whole business, one system. | Get the AI OS → |
| **Aurora** | Auto Ads System | Planned | Ads that run themselves. | Explore Aurora → |
| **Prism** | Analytics Pack | Planned | Know what is working. | Explore Prism → |
| **Forge** | Claude Code OS | Planned | Ship like a team of ten. | Explore Forge → |

Read as a card sentence, each product is "function. body.": AI OS is "The AI Operating System. Your whole business, one system."; Aurora is "Auto Ads System. Ads that run themselves."; Prism is "Analytics Pack. Know what is working."; Forge is "Claude Code OS. Ship like a team of ten."

---

## The rule

> **Plain words, fixed names, semantic actions.** Every Mez Systems line is Australian English, sentence case, no em dash, no exclamation mark. The product is "AI OS", the holdco is "Mez Systems", the endorsement is "A Mez Studios company", and core codes never surface. CTAs use the approved action family for purchase, planned interest, discovery, access or onboarding; the seven hype words are banned. Copy fits the slot limits from [13-sections.md](13-sections.md). The approved copy above is the working default until Olli signs off.

## Voice and copy (machine readable)

```json
{
  "doc": "17-voice-and-copy",
  "status": "DEFAULT",
  "language": {
    "english": "en-AU",
    "case": "sentence case everywhere, including headings and buttons",
    "dashes": "no em dashes, no double hyphens",
    "uiExclamationMarks": false,
    "oxfordComma": "no mandate, keep natural"
  },
  "naming": {
    "product": "AI OS",
    "holdco": "Mez Systems",
    "endorsement": "A Mez Studios company",
    "coreCodesInCustomerCopy": false,
    "bannedSpellings": ["AIOS", "Atlas"],
    "canonicalFunctionNames": ["AI Operating System", "Auto Ads System", "Analytics Pack", "Claude Code OS"]
  },
  "ctaActions": {
    "purchase": ["Get"],
    "plannedInterest": ["Join"],
    "discovery": ["Explore", "See"],
    "access": ["Open"],
    "onboarding": ["Start"]
  },
  "primaryCtaLocked": "Get the AI OS",
  "plannedProductCta": "Join the waitlist",
  "bannedWords": ["Unlock", "Unleash", "Supercharge", "Revolutionise", "Elevate", "Seamless", "Empower"],
  "bannedWordsNote": "and their variants: unlocking, unleashes, supercharged, revolutionary, elevates, seamlessly, empowering, and the like",
  "avoidHypeAdjectives": ["effortless", "magical", "game-changing", "next-level", "cutting-edge", "world-class", "best-in-class", "blazing-fast", "insanely", "ultimate", "powerful", "robust"],
  "flagshipHeadline": "One system your whole business runs on",
  "charLimits": {
    "nav": { "wordmark": 16, "navLink": 14, "ctaLabel": 14 },
    "hero": { "eyebrow": 28, "h1": 60, "sub": 140, "ctaPrimaryPurchase": 14, "ctaPrimaryPlanned": 20, "ctaGhost": 24 },
    "feature-row": { "eyebrow": 24, "heading": 48, "body": 180, "bullet": 48, "textCta": 24 },
    "suite-grid": { "sectionEyebrow": 24, "sectionHeading": 48, "productName": 16, "functionLabel": 28, "statusChip": 12, "cardBody": 60, "cardTextCta": 20 },
    "pricing-moment": { "eyebrow": 24, "heading": 40, "priceString": 16, "priceCaption": 48, "inclusion": 48, "ctaLabelPurchase": 14, "ctaLabelPlanned": 20, "gstNote": 80 },
    "faq": { "sectionHeading": 40, "question": 80, "answer": 280 },
    "cta-band": { "eyebrow": 24, "heading": 52, "sub": 120, "ctaLabelPurchase": 14, "ctaLabelPlanned": 20 },
    "footer": { "endorsement": 24, "columnHeading": 20, "linkLabel": 24, "legalLine": 80 },
    "quote-band": { "pullQuote": 140, "attribution": 48 },
    "gradient-strip": { "eyebrow": 24, "heading": 48, "surfaceLabel": 20 }
  },
  "approvedCopy": {
    "status": "DEFAULT",
    "homeHero": {
      "eyebrow": "The AI operating system",
      "h1": "One system your whole business runs on",
      "sub": "AI OS runs the work your business repeats every day, from one place, so you stop stitching ten separate tools together.",
      "ctaPrimary": "Get the AI OS",
      "ctaGhost": "See what it runs"
    },
    "suiteGrid": {
      "aios": { "name": "AI OS", "functionLabel": "AI Operating System", "statusChip": "Live", "cardBody": "Your whole business, one system.", "cardTextCta": "Get the AI OS →" },
      "aurora": { "name": "Aurora", "functionLabel": "Auto Ads System", "statusChip": "Planned", "cardBody": "Ads that run themselves.", "cardTextCta": "Explore Aurora →" },
      "prism": { "name": "Prism", "functionLabel": "Analytics Pack", "statusChip": "Planned", "cardBody": "Know what is working.", "cardTextCta": "Explore Prism →" },
      "forge": { "name": "Forge", "functionLabel": "Claude Code OS", "statusChip": "Planned", "cardBody": "Ship like a team of ten.", "cardTextCta": "Explore Forge →" }
    }
  }
}
```
