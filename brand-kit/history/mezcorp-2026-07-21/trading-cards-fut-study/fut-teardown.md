# FUT Card Design Language — A Teardown

Design reference for the Mez Systems collectible trading-card system. This studies the *visual grammar* of EA Sports FC / FIFA Ultimate Team (FUT) cards, not the sport. No EA marks, badges, player likenesses or crests are copied. Covers latest (EA FC 26 / FC 25) and the greatest-ever designs (FIFA 13-23 era).

Compiled 2026-07-11 from a web sweep of FUT design databases, card-evolution histories, and community design rankings (sources listed at the end).

---

## 0. Why FUT is worth stealing from

FUT is arguably the most successful digital trading-card system ever built. Its genius is that a single, rigidly consistent template carries a *huge* amount of information (a rating, a role, three affiliations, six numbers, a photo, a rarity) yet still reads in a fraction of a second and still feels precious. It solved the hardest problem in collectible design: make every card feel like the same product family, but make some cards feel like winning the lottery. It does this almost entirely through **colour, metal and finish escalation** layered on top of a **fixed anatomy**. That separation, fixed skeleton, escalating skin, is the thing to steal.

---

## 1. CARD ANATOMY — the layout grammar

A FUT card is a **portrait rectangle**, roughly a **3:4 to 5:7 ratio** (taller than a standard playing card; think a phone-screen aspect, not a square). The modern silhouette locked in from FIFA 14 onward. Before that (FIFA 09-13) cards were **wider, almost square** — that older squarer format now reads as "retro/nostalgic" and is worth knowing as a deliberate throwback lever.

The face is organised into four zones: a **top-left data stack**, a **hero photo** that dominates the upper two-thirds, a **name bar** across the waist, and a **stat grid** across the bottom. Approximate positions (as fractions of card height/width, origin top-left):

### Top-left data stack (the "identity column")
Runs vertically down the **left edge, roughly x: 8-22%, y: 8-45%**. Read top to bottom:

1. **Overall rating (OVR)** — the single **largest number on the card**, top-left corner (~x:10%, y:10%). Two digits, huge, tight. This is the card's headline; it is sized to be legible at thumbnail scale. Everything else is subordinate to it.
2. **Position abbreviation** — directly beneath the OVR (~y:20%), much smaller, 2-3 letters (ST, CB, GK, CAM). Same colour treatment as the OVR.
3. **Nation flag** — beneath the position (~y:28%), a small rectangle/oval.
4. **Club badge / crest** — beneath the flag (~y:36%), a small shield.
5. **(League)** — league identity is usually *implied* by the club badge rather than drawn as a separate mark on the face; in some eras a small league mark sits in the same stack or the badge carries it. Treat league as the *third affiliation tier* even when it is not a distinct glyph.

This stack is the "spine". It is always in the same order so the eye learns it once and never re-hunts.

### Hero photo (the burst)
The player render occupies the **upper 60-65%** of the card, centred-right, and critically **breaks/bursts the top frame** — the head, and often a raised arm or the ball, crosses *above* the card's top border and sits proud of the frame. This "breaking the frame" is the single most important trick for making a flat card feel 3D and alive. On premium/special cards the burst is exaggerated (fuller body, more of the figure escaping the rectangle, motion blur, particles trailing off the top edge). On base cards the crop is tighter (head-and-shoulders inside the frame).

### Name bar (the waist)
A **horizontal band across ~y:62-70%**, full width, containing the **player name** in condensed uppercase, centred. It visually divides the "portrait half" (above) from the "data half" (below). Often sits on a subtle rule or a slight tonal shift.

### Stat grid (the numbers)
The **bottom ~y:72-95%**, the six core stats in a **2-column × 3-row grid**, split by a faint central divider:

| Left column | Right column |
|---|---|
| **PAC** (Pace) | **DRI** (Dribbling) |
| **SHO** (Shooting) | **DEF** (Defending) |
| **PAS** (Passing) | **PHY** (Physical) |

Each cell is a **two-digit value (0-99) + a 3-letter label**, value first/larger, label smaller and to the side. Left column = "attacking/tempo" attributes, right column = "control/resilience" attributes. For goalkeepers the same six slots swap to DIV/HAN/KIC/REF/SPE/POS, proving the grid is a *container*, not fixed content — a reusable slot system.

### Finish / foil area
The **background plane behind the photo and stats** is where all the rarity magic happens (Sections 2-3). On base cards it is a flat metallic field with a geometric pattern (triangles/facets in the FIFA 16 / FC 25 gold treatment). On specials it becomes gradients, crystalline shards, holographic sweeps, or animated shimmer. The photo, data stack and stat grid stay put; only this plane's **colour + material** changes across the ladder.

**Anatomy summary:** one skeleton — OVR (dominant, top-left) → identity stack (position, flag, badge) → frame-breaking hero photo → name bar → 2×3 stat grid. Memorised once, scannable forever.

---

## 2. RARITY LADDER AS A FINISH SYSTEM

The base ladder is gated by the player's overall rating, and each tier reads as a **metal + finish upgrade**, not just a hue change:

| Tier | OVR band | Metal / colour | Finish |
|---|---|---|---|
| **Bronze** | ≤ 64 | Copper / brown | **Matte, dark, low-shine** cast metal. Muddy, cheap-on-purpose. |
| **Silver** | 65-74 | Pewter / grey | **Brushed metal**, cooler, a slight sheen but still restrained. |
| **Gold** | 75+ | Warm gold | **Polished/rich golden hue** with a faceted geometric pattern. The "you've arrived" tier. FC 25 lightened the gold and made it wider/more compact vs FC 24. |
| **Special** | any | (edition-specific) | Leaves the metal ladder entirely — gradients, holo, animation. |

**Within each metal tier there is a rare vs non-rare split**, and this is the key lesson: the *rare* variant is the **same colour with more finish energy**. Rare cards "look shiny and have a brighter colour" than their common counterpart. A rare gold is a glossier, brighter gold than a common gold — identical layout, elevated material. So the system actually has *two* escalation axes running at once:

- **Axis A (tier):** bronze → silver → gold → special. A **colour + metal** climb.
- **Axis B (rarity within tier):** common → rare. A **finish/shine** climb.

The reason it works: matte-dark-cheap at the bottom, polished-warm-precious at the top, so value is legible pre-cognitively. You know a card's worth before you read a single number. That is the whole trick — **let material encode value**.

---

## 3. METALLIC FOIL & HOLO TREATMENTS

How the finishes actually escalate, tier by tier:

- **Matte metal (bronze):** flat, almost no specular highlight. Reads as base/common. Deliberately un-shiny so everything above it can shine.
- **Brushed metal (silver):** directional grain, soft cool sheen. One step of light.
- **Polished / faceted gold (gold):** warm reflective field broken into **geometric facets/triangles** so light catches at angles. This faceting is the bridge into "premium" — it is a static pattern doing the work a foil would do.
- **Foil / gloss (rare):** the rare variant adds a brighter, glossier pass over the same colour. In-pack this shows as **glitter rain** behind the reveal gate and a warmer/oranger light-sweep for rare gold vs a white/faded sweep for common gold.
- **Crystalline / shattered-glass background (top specials, esp. TOTY):** a faceted glass texture with **intricate filigree**, radiating "class". FIFA 17 TOTY used a "subtle crystalline background"; FIFA 19 TOTY layered a "complex, shattered glass effect" over deep royal blue and gold — widely called the greatest card design ever.
- **Holographic / iridescent sheen (modern specials):** rainbow interference that shifts with angle. Used to signal "this is not a normal card" instantly.
- **Animated shimmer / light-sweep (premium modern era, FIFA 20 → FC 26):** the background literally moves — "shimmering backgrounds, glowing highlights, and moving patterns", a slow light bar traveling across the foil. Motion = the top of the value ladder. A still card can be gold; only the best cards *move*.
- **Duotone / two-tone edition colour (promo specials):** many promos are essentially the gold template re-skinned in a single dominant edition colour + one metallic accent (e.g. green + acid for Radioactive, blue + gold for TOTY, icy-blue + white for Winter Wildcards). The duotone is what makes a promo instantly nameable across a pack of 20.

**Rule extracted:** finish escalates in this order — *matte → brushed → polished/faceted → glossy foil → crystalline → holographic → animated*. Each step up the special ladder should add exactly one finish tier, never skip. Motion is reserved for the very top.

---

## 4. SPECIAL-EDITION ESCALATION (ranked)

Ranked roughly by drama/prestige. Each entry: dominant colour + finish, signature move, why it's iconic, and how hard it breaks the frame.

### 1. TOTY — Team of the Year *(the prestige benchmark)*
- **Colour/finish:** deep royal/navy **blue + gold**, crystalline / shattered-glass background, filigree detailing, animated shimmer in modern versions.
- **Signature move:** the blue-and-gold combination = "the best 11 players on earth this year". FIFA 13 introduced it and "instantly communicated prestige, rarity, and power"; FIFA 19's shattered-glass TOTY is the community's all-time GOAT design.
- **Why iconic:** rarest annual drop, hardest to pack, blue is otherwise *never* used on base cards so it reads as pure status. FC 26 even spun off **TOTY Icons** (91-95 rated) to extend the prestige.
- **Frame break:** high — full upper body, particles off the top edge.

### 2. TOTS — Team of the Season
- **Colour/finish:** **per-league themed bright colour** on a smooth vibrant gradient (Premier League purple/teal, La Liga orange, Bundesliga red, etc.), gold accents. The FIFA/FC **2020 (FIFA 20) TOTS** is the acclaimed peak — "smooth gradients and vibrant colours", "mind-blowing".
- **Signature move:** end-of-season maximum-stat cards, colour-coded by league so a squad of TOTS cards looks like a rainbow of leagues.
- **Why iconic:** highest stats of the whole cycle + the most saturated, "loud" design of the year. FIFA 19 TOTS is the cautionary tale — a hated thin dividing line down the middle broke the look.
- **Frame break:** high.

### 3. Icons — the all-time greats
- **Colour/finish:** **white + gold**, minimal, a single **diagonal gold line behind the head** (FC 25 refinement), timeless. Prime Icons were "stark white and gold", "the pinnacle of desirability".
- **Signature move:** restraint. In a sea of loud promos, Icons win by being the *quietest, cleanest* card. White = premium negative space.
- **Why iconic:** retired legends only; scarcity + the clean look that never dates. A dedicated flared pack animation announces an Icon pull.
- **Frame break:** moderate-high, dignified rather than explosive.

### 4. Heroes — cult/fan-favourite players
- **Colour/finish:** **comic-book aesthetic**, vivid multi-colour, energetic patterns, league-themed hues, "like something out of a comic book". A dramatic departure from earlier boring orange.
- **Signature move:** pop-art/graphic-novel energy, halftone-ish vibrancy, bold graphics per league.
- **Why iconic:** celebrates cult heroes (not GOATs) so the *design* carries the prestige the player rating doesn't. The loudest, most illustrative tier.
- **Frame break:** high, playful.

### 5. Future Stars — young breakout talents
- **Colour/finish:** **neon cyan/teal + magenta/pink**, futuristic gradient, light-streak/swoosh motion graphics.
- **Signature move:** the "electric future" palette (cool neon) that no other card uses — signals youth/potential.
- **Why iconic:** predictive hype (these are tomorrow's stars), dynamic upgradeable stats, and a palette that is unmistakably its own.
- **Frame break:** high, motion-forward.

### 6. Winter Wildcards — mid-season holiday event
- **Colour/finish:** **icy shimmering blue + white**, frost/crystal texture, snow-glint shimmer — "frosty flair… shimmering blue cards".
- **Signature move:** the frozen/ice treatment; a seasonal re-skin that still uses the duotone-promo formula.
- **Why iconic:** festive scarcity, and the icy-blue is a beloved recurring look. FC 26 added **Winter Wildcards Icons**.
- **Frame break:** moderate.

### 7. Radioactive — chaos/power promo
- **Colour/finish:** **toxic/acid green**, hazard glow, radioactive theme, boosted look.
- **Signature move:** the sickly green glow = "dangerously overpowered". Colour telegraphs the gimmick (all-99 style boosts + a broken chemistry mechanic, see §5).
- **Why iconic:** menacing, unmistakable, tied to a memorable "makes any squad work" chemistry hack.
- **Frame break:** moderate-high.

### 8. Trophy Titans — trophy/glory celebration
- **Colour/finish:** **metallic silver + gold trophy sheen**, engraved-metal texture, polished-cup reflectivity.
- **Signature move:** literal "trophy metal" — reads like the card was cast from a silverware cup.
- **Why iconic:** celebrates trophy-winners; the metallic sheen is a distinct step beyond normal gold. FC 26 fields Trophy Titan Icons and Heroes variants.
- **Frame break:** moderate.

### 9. Flashback — a player's past peak season
- **Colour/finish:** historically **teal/green** with a retro, slightly muted throwback treatment.
- **Signature move:** "remember when this player was *this* good" — a nostalgia re-issue of a past-form card.
- **Why iconic:** memory/nostalgia lever; the muted retro palette signals "from the archive".
- **Frame break:** moderate.

### 10. Showdown — fixture/rivalry duel
- **Colour/finish:** **split / two-tone diagonal** design pairing two players from an upcoming match; dynamic — the card upgrades based on the real fixture result.
- **Signature move:** the *duel* framing — two cards designed as a matched pair, sometimes a diagonal split composition.
- **Why iconic:** ties the card to a real, dated event with a live outcome — a card that changes based on reality.
- **Frame break:** moderate.

### 11. TOTW / Inform — weekly best performers *(the workhorse)*
- **Colour/finish:** **black + gold**, faceted geometric triangles (echoing the gold card), dark background, "bold and sophisticated".
- **Signature move:** black is the "one notch above gold" everyday special — the most-seen non-base card. FC 25 made it wider/shorter with darker shades.
- **Why iconic:** the gateway special; black+gold became shorthand for "in-form/upgraded". High frequency, so it *defines* the "special-but-common" middle rung.
- **Frame break:** moderate.

### 12. Ultimate / Fantasy FC / RTTK / Thunderstruck — dynamic & finale promos
- **Fantasy FC:** **purple/violet + teal**, a "live" card whose stats can upgrade through a real tournament run.
- **RTTK (Road to the Knockouts):** team-coloured, dynamic-upgrade on European qualification.
- **Thunderstruck:** dark + electric blue/purple lightning energy.
- **Ultimate:** the cycle-closing celebration tier, premium dark/gold or multi-colour, "best of the year" retrospective.
- **Signature move (shared):** the **living card** — the artwork/stat plane is a container for an evolving value, tying the collectible to an ongoing narrative.

**Frame-breaking champions (art bursting hardest out of the rectangle):** TOTY, TOTS, Future Stars, Heroes. These lean into full-body renders, motion trails and particles escaping the top edge. Base bronze/silver and TOTW keep the crop contained. *The amount a figure escapes the frame is itself a rarity signal.*

---

## 5. ULTIMATE TEAM META — the systems around the card

The card is only half the product; the *game around collecting* is the other half. Three mechanics matter for design:

### Chemistry (links between cards)
Cards gain power by **linking to other cards** that share an affiliation — **same Nation, same League, or same Club**. In the modern system each card earns **0-3 Chemistry Points**, and full **Team Chemistry is out of 33** (11 players × 3). Thresholds: e.g. **+3 when 8 players share a country or league**. A card only contributes chemistry if it's **played in its correct position**. Some promos rewrite the rules — **Radioactive** cards start with +2 and count for +2 on every link type, so a single shared league maxes them out.
- **Design lesson:** the three affiliations on the card face (nation flag, club badge, league) are not decoration — they are the **connection sockets** of a network game. The identity stack *is* the multiplayer API. If you build a card system, decide early which fields are "link sockets" and draw them as such.

### Collection / set-building drive
Value comes from **completing sets** — a full Team of the Year, a league's full TOTS, an Icon collection. Squad-Building Challenges (SBCs) let you *consume* duplicate cards to *forge* a specific higher card. So cards are simultaneously **collectibles, ingredients, and currency**.
- **Design lesson:** give cards a second life as inputs to build rarer cards. Sets create the "gotta finish it" itch; forging creates a sink so commons still matter.

### Pack-opening drama (the reveal as a design moment)
This is where the finish system pays off as *motion*. The reveal is a staged sequence engineered to withhold and then release information:
- **The tunnel / gate:** the card emerges from a stadium tunnel. **Seeing the tunnel at all = a walkout (a big pull).**
- **Progressive disclosure:** for top cards, **flag → league → club appear in order** before the player, so you can guess the identity and the tension builds.
- **The light-sweep as a tell:** a bar of light runs across the panel — **white/faded = common gold, orange/gold = rare gold**. **Rare cards add glitter rain** behind the gate and **black stripes** on the gate.
- **The walkout:** high-rated players (~86+) don't just flip — the figure **runs/jumps out of the card onto a stage**, with **confetti, flames and lights** scaled to rarity. A **double walkout** stages two players together.
- **The flip:** the card turns to reveal the face; specials get a "flared" bespoke animation (Icons have their own).
- **Design lesson:** the single most valuable UX in the whole product is the **delay before the reveal**. Rarity is dramatised through *time and light*, not just the static card. Build a reveal that leaks clues in sequence (a colour, then a category, then the item) and reserve confetti/flare/motion for the top tiers. The card is the noun; the walkout is the verb.

---

## 6. STEAL vs LEAVE

For a **premium, abstract product-card system** (Mez Systems), not a football game:

### STEAL

- **Fixed skeleton, escalating skin.** One rigid anatomy across every card; all differentiation lives in colour + material of the background plane. Consistency is what makes rarity legible.
- **Dominant headline number, top-left, oversized.** One hero metric sized to be readable at thumbnail scale. Everything else subordinate. (For Mez: a score, tier, version, or index number.)
- **The identity stack as a spine.** A fixed-order vertical column of small glyphs (your equivalent of position/flag/badge/league). Same order every time so the eye learns it once. Make these your "link sockets" if cards relate to each other.
- **The 2×3 attribute grid.** Six numbers in two columns of three with 3-letter labels — a container, not fixed content (it swaps GK stats for outfield). A brilliant reusable slot system for any six-metric object.
- **Material encodes value.** Matte → brushed → polished/faceted → glossy foil → crystalline → holographic → animated. Bottom tier deliberately cheap/matte so the top can shine. Let finish do the pricing.
- **Two escalation axes.** Tier (colour/metal climb) *and* rarity-within-tier (finish/shine climb) running simultaneously. Same colour, more shine = the rare variant.
- **Duotone promo re-skins.** Each special = the base template in one dominant colour + one metallic accent, so a set is nameable at a glance across a full pack.
- **The frame-break.** Let the hero art/photo burst above the top border. The *amount* it escapes the frame is itself a rarity signal. Cheapest, highest-impact 3D trick.
- **Motion reserved for the top.** Only the rarest cards animate (light-sweep, shimmer). A still card can be premium; a moving one is elite.
- **The staged reveal.** Progressive disclosure — leak a colour, then a category, then the item. Withhold, then release. Confetti/flare only at the top. This is the highest-ROI piece of the whole system.
- **Blue-and-gold = top prestige.** A colour used *nowhere* on base cards, held in reserve for the single best tier, reads as pure status (TOTY). Reserve one signature palette for your apex tier only.
- **Clean/white = premium, not loud.** The Icon lesson: in a sea of loud promos, the quietest, whitest, most-restrained card can be the most desirable. Restraint is a rarity move too.
- **Cards as collectibles + ingredients + currency.** Give commons a second life (forge/consume into rares). Sets create completion drive.

### LEAVE

- **Sport-specific fields.** Nation flags, club crests, league marks, positions (ST/CB/GK), the literal PAC/SHO/PAS/DRI/DEF/PHY labels. Keep the *slots*, replace the *content* with your domain's metrics/affiliations.
- **Player likenesses / real photos.** Legally and brand-wise off-limits, and unnecessary — the frame-break trick works with any hero asset (a product render, an orb, an icon, a 3D object).
- **EA's exact colours and marks.** The specific TOTY blue, the exact gold facets, the Icon lockup — study the *grammar*, don't clone the *marks*.
- **The 99-cap rating obsession.** FUT's "all-99, cheat-code, overpowered" power-creep is a game-balance artefact. A premium product-card system wants *credible* values, not inflation.
- **Gambling/lootbox framing.** The paid-pack, odds-based, spend-to-pull loop is the controversial core of FUT. Steal the *reveal drama*, not the paid-randomised-purchase mechanic.
- **Visual clutter of late-era cards.** Loyalty pips, contract counts, fitness bars, chemistry-style badges — FUT's HUD cruft. Community praised FC 25's Icon precisely for having *less* clutter. Keep the face clean; push metadata to a back/detail view.
- **The hated thin divider line (FIFA 19).** A cautionary tale — a single mis-placed structural line broke an entire year's look. Don't add structural lines that fight the composition.
- **The squarer FIFA 09-13 proportion** (unless you *want* a deliberate retro throwback lever — then it's a tool, not a default).
- **Per-league rainbow logic.** TOTS colour-codes by league; only borrow "colour-code by category" if you actually have meaningful categories to encode. Don't add colour taxonomy you can't fill.

---

## Appendix — the one-paragraph thesis

FUT works because it decouples a **fixed, instantly-learnable anatomy** (oversized top-left headline number → vertical identity stack of link-sockets → frame-breaking hero art → name bar → 2×3 metric grid) from an **escalating finish system** (matte → brushed → polished/faceted → foil → crystalline → holographic → animated) that lets *material encode value* pre-cognitively, and then it **dramatises the finish through a staged, information-withholding reveal** (tunnel → progressive flag/league/club disclosure → light-sweep rarity tell → walkout with rarity-scaled confetti). Copy the *system*, not the sport: keep the skeleton, the two-axis escalation, the frame-break, the reserved-apex palette, and the staged reveal; drop the flags, crests, positions, likenesses, lootbox loop and HUD clutter.

---

## Sources

- [FIFA Ultimate Team Cards — EA Sports FIFA Wiki (Fandom)](https://easportsfifa.fandom.com/wiki/FIFA_Ultimate_Team_Cards)
- [FC 25 Player Cards Guide — FUTUTeam](https://fifauteam.com/fc-25-player-cards-guide/)
- [FUT Player Cards — FIFPlay glossary](https://www.fifplay.com/glossary/fut-player-cards/)
- [The Evolution of FUT Cards: FIFA 09 to EA FC 24 — FutGraphics](https://futgraphics.com/articles/the-evolution-of-fut-cards-a-visual-history-from-fifa-09-to-ea-fc-24)
- [Ranking FIFA TOTS Card Designs — zLeague](https://www.zleague.gg/theportal/ranking-fifa-tots-card-designs-which-one-steals-your-heart/)
- [9 Best Cards in EA Sports Ultimate Team History (Ranked) — GiveMeSport](https://www.givemesport.com/ea-sports-ultimate-team-best-cards-ever-ranked/)
- [Everything About EA FC 25 Card Designs — MrGeek](https://www.mrgeek.net/blog/every-thing-about-ea-fc-25-card-designs)
- [FC 25 All Card Designs in Ultimate Team — RealSport101](https://realsport101.com/article/fc-25-card-designs)
- [Radioactive Promo — FUT.GG](https://www.fut.gg/news/radioactive-everything-you-need-to-know-about-the-latest-promo-in-ea-sports-fc-24/)
- [EA FC 24 Radioactive Promo — Dexerto](https://www.dexerto.com/ea-sports-fc/ea-fc-24-radioactive-promo-2404560/)
- [FC 26 Walkout Player — FUTUTeam](https://fifauteam.com/fc-26-walkout-player/)
- [How to tell if you've packed a walkout — FUT.GG](https://www.fut.gg/news/how-to-tell-if-youve-packed-a-walkout-in-ea-sports-fc-24/)
- [FIFA 20: Recognizing Walkouts — Mein-MMO](https://mein-mmo.de/en/fifa-20-recognizing-walkouts-pay-attention-to-this-pack-animation,398165/)
- [FC 26 Chemistry Explained — FUTUTeam](https://fifauteam.com/fc-26-chemistry/)
- [FIFA 23 New FUT Chemistry System Explained — FUTBIN](https://www.futbin.com/news/articles/644/fifa-23-new-fut-chemistry-system-explained)
- [EA FC 26 TOTY Icons — FUT.GG](https://www.fut.gg/rarities/toty-icon/)
- [FC 26 TOTY guide and schedule — GamesRadar+](https://www.gamesradar.com/games/ea-sports-fc/ea-fc-26-toty-release-schedule/)
- [FC 25 Winter Wildcards — EA Sports](https://www.ea.com/en/games/ea-sports-fc/fc-25/news/fc-25-winter-wildcards)
- [Football Card Abbreviations (FIFA) — CardsPlug](https://cardsplug.com/blogs/football-card-guides/football-card-abbreviations-fifa)
