# 03 · Typography

> **LOCKED (2026-07-10):** the family is **Inter** (Notion-tuned), with **Instrument Serif** as an occasional editorial accent and **IBM Plex Mono** for code. Headings are **Inter Bold** with negative tracking + tight leading (H1 -3%/lh100, H2 -2.5%/lh104). Full scale also in [`../design-system-export/typography.md`](../design-system-export/typography.md). The earlier SF Pro exploration is superseded (see history at the bottom).

## Family

**Inter** is the workhorse family across the whole system: UI, body, and headings. It is open-licence, embeds well on web, and its metrics match the Notion feel we want.

- **Default → Inter** (Regular 400, Medium 500, Semi Bold 600, Bold 700)
- **Serif → Instrument Serif**, italic, for the occasional editorial accent phrase. Never body or UI.
- **Mono → IBM Plex Mono**, for code, gradient IDs, technical labels.

Only ever one sans family. The Notion feel is not a different font; it is Inter run **Bold for headings with negative tracking and tight leading**, not the default look.

## Scale (locked)

| Role | Weight | Size | Tracking | Leading |
|------|--------|------|----------|---------|
| **H1** | Bold (700) | 72 | -3% | 100% |
| **H2** | Bold (700) | 40 | -2.5% | 104% |
| **H3** | Semi Bold (600) | 22 | -1.5% | 125% |
| **Body** | Regular (400) | 17 | -1% | 150% |
| **Button** | Semi Bold (600) | 16 | -1% | n/a |
| **Caption** | Regular (400) | 13 | -0.5% | n/a |
| **Eyebrow** | Medium (500) | 12 | +6% | UPPERCASE |
| **Serif accent** | Instrument Serif Italic | contextual | n/a | n/a |
| **Mono** | IBM Plex Mono | 14 to 15 | n/a | n/a |

Tokens: `--mz-h1-*` … in [`../design-system-export/tokens/tokens.css`](../design-system-export/tokens/tokens.css). Utility classes: `.mz-h1`, `.mz-h2`, `.mz-h3`, `.mz-body`, `.mz-caption`, `.mz-eyebrow`, `.mz-serif`, `.mz-mono`.

## Rules

- **Display headings H1 and H2 are Inter Bold** (700). H3 is Inter Semi Bold (600). Each role uses the negative tracking and leading above. Extra Bold and default metrics are never used.
- Always apply the negative tracking and tight leading. Default Inter (0 tracking, 1.2+ leading) is what makes it feel generic.
- **Serif is a garnish.** Instrument Serif italic for one accent phrase at a time, never for body, UI, or whole headings.
- **Mono for the technical register**: code, gradient IDs (`MZ-G13`), file paths. Not decoration.
- Body copy is never faded via a lighter weight; use `--mz-text-muted` for muted text. Eyebrows are tracked (+6%) and uppercase. Do not write "STEP 0X" style eyebrows; use the function ("AI OPERATING SYSTEM").

---

## Superseded (history)

An earlier exploration set **SF Pro** as the working family with Inter "under review". That is retired: **Inter is the locked family** and the scale above (Inter Bold, Notion-tuned) is authoritative. Five type systems (Geist, Editorial/Instrument Serif, Inter+JetBrains Mono, Space Grotesk, Fraunces) were compared in Figma; the Notion (Inter Bold) direction won.
