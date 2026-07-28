# Third-party marks

Other companies' logos, held here so a Mez surface never invents, fakes or hand-draws one.

Status: **reference**. Not Mez brand data. These never enter `brand-kit/registry/`, never appear in
a release, and carry no production authority of their own.

## Why this exists

Golden Homepage GH-S03 needs to say "interchangeable intelligence" using the real marks of the
model providers. Earlier rounds failed twice: first with invented brand logos, then with filled
logo boxes. Both are defects. `ICO-02` and `LAY-13` in
[`design-authority/ANTI-SLOP-CANON.md`](../../design-authority/ANTI-SLOP-CANON.md) now ban both
outright, and this folder is the only sanctioned source that satisfies them.

## Resolve a mark through the registry, never by path

`registry.json` is generated. Read it, take the path, use it. A hardcoded asset path in a component
is a defect because it silently breaks when a mark is refreshed.

```bash
python3 brand-kit/assets/third-party-marks/build_mark_registry.py
```

Re-run it after adding, removing or refreshing any mark folder. Never hand-edit `registry.json`.

## The variants, and which one to use

| Role | File | What it is | Use it for |
|---|---|---|---|
| `mark` | `logos/mark.svg` | **Freestanding symbol. No enclosing shape, no plate, no rounded square.** | The default for any Mez surface. This is the one GH-S03 wants. |
| `mark-light` | `logos/mark-light.svg` | Symbol tuned for a light surface | Only when `mark` renders illegibly on `--mz-canvas`. |
| `mark-dark` | `logos/mark-dark.svg` | Symbol tuned for a charcoal surface | Only when `mark` renders illegibly on a dark band. |
| `appIcon` | `logos/app-icon.png` | The full normal icon, **with** its enclosing shape and brand colour | Product/integration contexts where the app is being named as an app. Never in a row of peers. |
| `raster.mark` | `logos/raster/mark-{256,512,1024}.png` | PNG of the freestanding symbol | Raster-only pipelines: OG cards, email, video, thumbnails. |
| `raster.app-icon` | `logos/raster/app-icon-{256,512,1024}.png` | PNG of the full icon | Same, where the enclosed icon is right. |

58 brands. 37 carry a freestanding `mark.svg`; the rest are raster-only. Check the registry before
you promise a section a vector mark. Every current model provider (OpenAI, Claude, Gemini, Grok,
Mistral, DeepSeek, Perplexity, ChatGPT) has one.

## How they render on a Mez surface

These are foreign brands entering a monochrome system. The system wins.

1. **Greyscale by default.** A row of peer marks is monochrome. Their brand colours would each fight
   the product gradient, which is the only colour a Mez surface permits. Use
   `filter: grayscale(1)` plus an opacity or brightness trim to sit the mark at the weight of the
   text beside it, or recolour a single-path SVG to `currentColor`.
2. **Freestanding symbol, no container.** No filled box, no rounded plate, no circle, no card per
   logo. The Phase B pantry calls this "integration identity must be real and quiet"; a soup of
   filled logo boxes was rejected on sight.
3. **Optical size, not box size.** Marks have wildly different bounding-box-to-ink ratios. Set them
   by eye against a shared cap height, never by giving every `<img>` the same `width`.
4. **Never restyle the mark itself.** No cropping, no rotating, no stretching, no filling with a
   gradient, no Wings mashups. Greyscale plus scale is the whole permitted operation.
5. **Never imply endorsement.** A mark says "this model plugs in", never "this company partners
   with Mez Systems". Copy beside a mark row must not claim a relationship that does not exist.
6. **Only real marks.** If a name has no real mark in this registry, it does not go in the row. Do
   not draw one. Do not substitute a lookalike. Cut the slot instead.

## Refreshing

The upstream source was `mezcorp_claude_code/departments/cmo/brand-library/brands/` on
2026-07-25. That repo is an **archive boundary**, not an authority: it does not get to change Mez
truth, and nothing here is synced back. To refresh a mark, replace the files under
`marks/<slug>/logos/` and re-run the registry build.

`mez-systems` was deliberately **not** copied. That folder holds the superseded 2026-07 Mez pack
(`#F8F8F8` page, `#0D0D0D` ink, Inter, static discs). This repository's foundations supersede it.
The historical copy already lives at `brand-kit/history/mezcorp-2026-07-21/`.
