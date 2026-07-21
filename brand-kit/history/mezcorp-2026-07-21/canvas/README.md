# Canvas

A zero-build, plain-HTML live showroom of the Mez Systems design system, inside the pack itself.

**Open it:** double-click `index.html`, or run `python3 -m http.server 8901` from the pack root (`mez-systems/`) and open `http://localhost:8901/canvas/`. Serving from `canvas/` itself breaks the token import, so serve from the pack root.

**The loop:** docs and tokens are the truth. The canvas renders them. Edit `tokens.css` or a brand-system doc, refresh, judge, lock. Mirror locked states to Figma at milestones.

**The rule:** the canvas never invents a value. `canvas.css` imports `../design-system-export/tokens/tokens.css` and every remaining literal is annotated with the doc that states it. Markup patterns live in `SNIPPETS.md`; use them exactly.

`assets/wings.svg` uses `currentColor`: one file, coloured by CSS, no white or ink variants needed.
