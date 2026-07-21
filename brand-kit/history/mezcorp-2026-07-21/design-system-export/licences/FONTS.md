# Font files and licences

This release vendors the exact web-font files required for a self-contained build:

| Family | Bundled file | Roles | Licence |
|---|---|---|---|
| Inter variable | `assets/fonts/inter-variable.woff2` | H1, H2, H3, body, UI, buttons | SIL Open Font License 1.1 in `Inter-OFL.txt` |
| Instrument Serif Regular / Italic | `assets/fonts/instrument-serif-regular.woff2`, `instrument-serif-italic.woff2` | One editorial accent per page | SIL Open Font License 1.1 in `Instrument-Serif-OFL.txt` |
| IBM Plex Mono Regular | `assets/fonts/ibm-plex-mono-regular.woff2` | Code, technical labels, gradient IDs | SIL Open Font License 1.1 in `IBM-Plex-Mono-OFL.txt` |

The files were acquired on 2026-07-19 from the official Google Fonts repositories and
converted from the upstream TTF files to WOFF2 without changing family names or outlines.
The complete upstream character sets and layout features are retained. Do not distribute a
font file without its corresponding licence file. Do not rename a modified derivative with a
reserved font name unless the licence permits it.

The `@font-face` declarations already live in `tokens/tokens.css`. A clean consumer does not
need Google Fonts, Figma, a network request, or a local font installation.

Official sources:

- Inter: `https://github.com/google/fonts/tree/main/ofl/inter`
- Instrument Serif: `https://github.com/google/fonts/tree/main/ofl/instrumentserif`
- IBM Plex Mono: `https://github.com/google/fonts/tree/main/ofl/ibmplexmono`
