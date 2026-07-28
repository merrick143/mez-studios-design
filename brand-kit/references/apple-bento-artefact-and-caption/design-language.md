# Apple feature bentos · what carries a cell

| | |
|---|---|
| **Slug** | `apple-bento-artefact-and-caption` |
| **Source** | Four Apple feature-summary bentos supplied in chat 2026-07-26: iPadOS 26, iPhone 17 Pro (light), iOS 26, iPhone 15 Pro (dark) |
| **Provided by** | Olli, screenshot |
| **Studied** | 2026-07-26 |
| **Question** | Why an Apple bento reads clean and dense at once, when a Mez bento of the same cell count reads sparse and wordy |
| **Mez problem it serves** | GH-S04. Version A was picked and the note was "make the cards look better" |
| **Originality risk** | Medium. High on two elements: Apple's product photography and its own app icons are its signature and cannot travel in any form |
| **Captures** | Four stills supplied in chat. Not committed |

## 1 · Observed expression

**The cell holds an object, and the words are a caption.** Almost every cell is an artefact first:
an app icon, a chip die, a device render, a UI screenshot, a glyph. The text sits under or over it at
roughly 13 to 15px, quiet, usually centred, and never competes. Where there is no artefact the text
*becomes* one: "48MP", "5x", "A18", "Titanium", "iPadOS" are set enormous and are the object of the
cell rather than a label on it.

**The gutter is tight and absolutely constant.** Roughly 8 to 10px between every cell, no exceptions,
which is what lets the mosaic run dense without looking crowded. Cell sizes vary far more than the
gutter ever does.

**Size variance is extreme.** Within one bento there are cells at roughly 1:1, 1:3, 3:1 and 2:2, and a
hero cell spanning three or four rows. Nothing is a uniform row of four.

**Surfaces are almost entirely neutral.** White or near-white in the light bentos, near-black in the
dark one. Colour arrives through the artefacts, so the surface never has to carry it.

**Captions are short.** Two to five words: "Window tiling", "Custom folders", "Action button". No
sentence anywhere.

## 2 · Underlying mechanism

The density is affordable because **the reading unit is an image, not a paragraph**. The eye parses an
icon in a fraction of the time a sentence takes, so forty cells scan faster than eight paragraphs.
Once the artefact carries the meaning, the caption can shrink to a label, and once the caption is a
label the cell can be small, and once cells are small you can vary their size wildly without any of
them becoming unreadable. Each property depends on the one before it.

The constant gutter is what stops that variance reading as chaos: with one spacing value, every size
difference is legible as intent rather than accident.

Remove the artefacts and the whole thing collapses into a wall of small type, which is exactly what a
Mez bento of eight cells with a title and a subline each already is.

## 3 · Transferable principle

**Put an object in the cell and let the words be its caption.** A cell whose content is a title plus a
sentence is a paragraph in a box, and paragraphs cannot be packed densely or sized freely. A cell
whose content is one artefact plus two to five words can be small, can vary in size, and stays
scannable at any density.

**Vary cell size hard and gutter not at all.** One spacing value across wild size variance reads as a
system; varying both reads as an accident.

## 4 · Original Mez expression

**Family**: Product mosaic, per `design-authority/CRAFT.md` §1.
**Protagonist**: the AI OS material, held in the centre as the hero cell.

| Source element | Mez translation | Why |
|---|---|---|
| App icons and chip dies as artefacts | The gradient identity token, at artefact scale rather than badge scale | We have exactly one native object language and it is material |
| Product photography | Not taken | No photo library, and it is Apple's signature |
| Giant numerals as the object of a cell | Taken directly: real registry-derivable figures set large | Already legal, and `metric` is a declared cell job |
| Giant wordmark cell ("iPadOS", "Titanium") | The product name at display scale on the material cell | The hero cell already exists; this makes it read as the anchor |
| Sentence sublines | Cut to two-to-five-word captions | The whole density argument depends on this |
| Uniform four-across rows | Cut. Hero centre, varied sizes around it | LAY-01 and the size-variance principle agree |
| Apple's app icons | `brand-kit/assets/third-party-marks/` or nothing | ICO-01, never invent a mark |
| Near-black dark bento | The charcoal ramp | COL-05, CL-02 |

## 5 · What not to take

- **The product photography.** Every device render, every lifestyle photo. This is the single most
  identifiable thing in the set.
- **Apple's app icons**, including any pastiche of the rounded-square icon grid.
- **The exact caption voice.** "Breakthrough battery life" is Apple copy.
- **The frosted, softly-lit cell backgrounds** in the iPhone 17 bento. That is glass, and MAT-01 bans
  it by name.

## 6 · Open questions for Olli

- Apple's captions are two to five words. Ours are currently short sentences. Shrinking them is the
  change that makes the density work, but it means rewriting the eight sublines a third time.
- The dark bento is a genuinely different register. Worth deciding whether GH-S04 stays on paper or
  becomes the page's first charcoal surface before GH-S06.
