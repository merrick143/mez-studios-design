# Typography (locked)

Mez Systems uses a **Notion-inspired** type system: one workhorse sans, an editorial serif used sparingly, and a mono for technical/code.

## Fonts

| Role | Font | Where |
|------|------|-------|
| **Default** | **Inter** | Everything: UI, body, headings |
| **Serif** | **Instrument Serif** (italic) | Occasional editorial accent (a highlighted phrase). Never body or UI. |
| **Mono** | **IBM Plex Mono** | Code, IDs, technical labels |

Notion substitutes: Notion's own faces are Lyon Text (serif) and a typewriter mono; **Instrument Serif** and **IBM Plex Mono** are the closest freely-available matches.

## The scale

The Notion feel is not a different font: it's Inter run **heavy for display, with negative tracking and tight leading.**

| Role | Weight | Size | Tracking | Line-height |
|------|--------|------|----------|-------------|
| **Heading 1** | Bold (700) | 72 | -3% | 100% |
| **Heading 2** | Bold (700) | 40 | -2.5% | 104% |
| **Heading 3** | Semi Bold (600) | 22 | -1.5% | 125% |
| **Body / subtext** | Regular (400) | 17 | -1% | 150% |
| **Buttons** | Semi Bold (600) | 16 | -1% | — |
| **Captions / meta** | Regular (400) | 13 | -0.5% | — |
| **Eyebrow** | Medium (500) | 12 | +6% | — (UPPERCASE) |
| **Serif accent** | Instrument Serif Italic | contextual | — | — |
| **Mono** | IBM Plex Mono | 14 to 15 | — | — |

Tokens: `--mz-h1-*` … in [`tokens/tokens.css`](tokens/tokens.css). Utility classes: `.mz-h1`, `.mz-h2`, `.mz-h3`, `.mz-body`, `.mz-caption`, `.mz-eyebrow`, `.mz-serif`, `.mz-mono`.

## Rules

- **Display headings H1 and H2 are Inter Bold** (700). H3 is Inter Semi Bold (600). Extra Bold and default metrics are never used.
- Always apply the **negative tracking and tight leading** above. Default Inter (0 tracking, 1.2+ leading) is what makes it feel generic.
- **Serif is a garnish.** Use Instrument Serif italic for one accent phrase at a time, never for body, UI, or whole headings.
- **Mono for the technical register**: code snippets, gradient IDs (`MZ-G13`), file paths. Not decoration.
- Body never below Regular; muted text via colour (`--mz-text-muted`), not lighter weight.

## History

Five type systems were explored (Geist, Editorial/Instrument Serif, Inter+JetBrains Mono, Space Grotesk, Fraunces) plus this Notion system, side by side on the Figma "Website Foundation · Type Tests" page. **Notion (Inter Bold) is the chosen direction.** The others remain in Figma for reference.
