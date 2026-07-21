# Canvas snippets

Copy-paste markup for every class in `canvas.css`. Page builders use these patterns exactly, so every page produces identical markup. Values never go inline unless the token itself is inline (spacing between blocks via `style="margin-top: var(--mz-s-N)"` is fine).

## Head boilerplate

Every canvas page starts with this. Pages inside `pages/` change the two paths to `../canvas.css` and `../canvas.js`, and asset references to `../assets/`.

```html
<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mez Systems · Page name</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="canvas.css">
</head>
<body class="mz-page">
  <!-- page -->
  <script src="canvas.js"></script>
</body>
</html>
```

## The wings (inline SVG)

`assets/wings.svg` uses `currentColor`, so one file covers every colour: inline the SVG and set `color` in CSS. No white or ink file variants exist or are needed. This block is the mark everywhere it appears (discs, nav, footer, trading cards).

```html
<svg class="mz-wings" viewBox="9 16 340 241" xmlns="http://www.w3.org/2000/svg" fill="currentColor" aria-hidden="true"><path d="M9.31894 227.388C9.31894 243.442 22.3337 256.457 38.3883 256.457H141.746C157.801 256.457 170.815 243.442 170.815 227.388V172.807C170.815 168.476 169.848 164.201 167.984 160.292L107.284 33.0283C102.46 22.9142 92.2519 16.4734 81.0462 16.4734H38.3883C22.3337 16.4734 9.31894 29.4882 9.31894 45.5427V227.388Z"/><path d="M348.462 227.388C348.462 243.442 335.447 256.457 319.392 256.457H216.034C199.98 256.457 186.965 243.442 186.965 227.388V172.807C186.965 168.476 187.932 164.201 189.797 160.292L250.497 33.0283C255.321 22.9142 265.529 16.4734 276.734 16.4734H319.392C335.447 16.4734 348.462 29.4882 348.462 45.5427V227.388Z"/></svg>
```

Below, `<svg class="mz-wings" …>…</svg>` stands for that whole block.

## Layout

```html
<main class="mz-container">
  <section class="mz-section">…</section>
  <section class="mz-section mz-section--hero">…</section> <!-- hero: extra top headroom -->
</main>
```

Grids:

```html
<div class="mz-grid-suite">…four product cards…</div> <!-- 1 / 2 / 4 columns -->
<div class="mz-grid-2">…text column + media column…</div> <!-- hero, feature row -->
<div class="mz-grid-3">…three tiles…</div> <!-- gradient strip -->
```

## Type

```html
<p class="mz-eyebrow">The AI operating system</p>
<h1 class="mz-h1">One system your whole business runs on</h1>
<h2 class="mz-h2">Section heading</h2>
<h3 class="mz-h3">Card heading</h3>
<p class="mz-body-lg">Emphasised body, holds 17px at every width. Hero subs.</p>
<p class="mz-body">Standard body. 16px under 920, 17px at 920 and up.</p>
<p class="mz-caption">Caption and meta, muted ink.</p>
<span class="mz-serif">one serif accent phrase</span> <!-- once per page, maximum -->
<code class="mz-mono">MZ-G13</code> <!-- technical labels; core codes never in customer copy -->
```

## Buttons and links

```html
<a class="mz-btn" href="#">Get the AI OS</a>
<a class="mz-btn mz-btn-ghost" href="#">See what it runs</a>
<a class="mz-btn mz-btn-ondark" href="#">Get the AI OS</a> <!-- inside .mz-dark-band only -->
<button class="mz-btn" type="submit" disabled>Get the AI OS</button>
<a class="mz-link" href="#">Get the AI OS &rarr;</a> <!-- text CTA -->
```

## Forms

```html
<label class="mz-label" for="email">Email</label>
<input class="mz-input" id="email" type="email" placeholder="you@company.com">

<!-- error state -->
<label class="mz-label" for="email2">Email</label>
<input class="mz-input" id="email2" type="email" aria-invalid="true" aria-describedby="email2-error">
<p class="mz-field-error" id="email2-error">Enter a valid email address.</p>

<label class="mz-label" for="country">Country</label>
<select class="mz-select" id="country"><option>Australia</option></select>

<label style="display: inline-flex; align-items: center; gap: var(--mz-s-2);">
  <input class="mz-checkbox" type="checkbox"> <span class="mz-body">Email me the receipt</span>
</label>
```

## Chips and product pills

```html
<span class="mz-chip">Live</span>
<span class="mz-chip">Planned</span>

<button class="mz-pill-product" type="button">
  <span class="mz-disc mz-disc--aios mz-disc--flat"><svg class="mz-wings" …>…</svg></span>
  AI OS
</button>
<button class="mz-pill-product mz-pill-product--unselected" type="button">…</button>
<button class="mz-pill-product mz-pill-product--ghost" type="button">…</button>
```

## The disc

Set the width; the disc stays square and the wings sit at 50% of the diameter, nudged 2% up. Cores: `--aios` `--aurora` `--prism` `--forge`.

```html
<div class="mz-disc mz-disc--aios" style="width: 160px;">
  <svg class="mz-wings" …>…</svg>
</div>
```

`mz-disc--flat` drops the free-floating shadow (inside pills or tight chrome).

## The product card

```html
<div class="mz-card-product">
  <div class="mz-disc mz-disc--aios"><svg class="mz-wings" …>…</svg></div>
  <div>
    <h3 class="mz-card-product__name">AI OS</h3>
    <p class="mz-card-product__function">AI Operating System</p>
  </div>
  <span class="mz-chip">Live</span>
  <p class="mz-card-product__body">Your whole business, one system.</p>
  <a class="mz-link" href="#">Get the AI OS &rarr;</a>
</div>
```

## The trading card

The frame sets the width; every part of the card scales from it (container query units). Cores as above.

```html
<div class="mz-trading-card-frame" style="width: 280px;">
  <div class="mz-trading-card mz-trading-card--aios">
    <span class="mz-trading-card__chip">MEZ SYSTEMS</span>
    <div class="mz-trading-card__lockup">
      <svg class="mz-wings" …>…</svg>
      <p class="mz-trading-card__name">AI OS</p>
    </div>
  </div>
</div>
```

## The stack (deck / fan)

Cards listed back to front: the last child is the newest and sits on top. `mz-fan` is the same class.

```html
<div class="mz-stack">
  <div class="mz-trading-card-frame" style="width: 240px;">…Forge card…</div>
  <div class="mz-trading-card-frame" style="width: 240px;">…Prism card…</div>
  <div class="mz-trading-card-frame" style="width: 240px;">…Aurora card…</div>
  <div class="mz-trading-card-frame" style="width: 240px;">…AI OS card…</div>
</div>
```

## Nav

```html
<nav class="mz-nav">
  <div class="mz-container mz-nav__inner">
    <a class="mz-nav__brand" href="index.html"><svg class="mz-wings" …>…</svg> Mez Systems</a>
    <div class="mz-nav__cluster">
      <div class="mz-nav__links">
        <a class="mz-link" href="#">Products</a>
        <a class="mz-link" href="#">Pricing</a>
      </div>
      <a class="mz-btn" href="#">Get the AI OS</a>
      <button class="mz-nav__toggle" type="button" aria-label="Menu">
        <svg width="16" height="12" viewBox="0 0 16 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1h14M1 6h14M1 11h14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
  <div class="mz-nav__sheet">
    <a class="mz-link" href="#">Products</a>
    <a class="mz-link" href="#">Pricing</a>
  </div>
</nav>
```

Add `mz-nav--hairline` for the static bottom hairline. `canvas.js` wires the toggle.

## Footer

```html
<footer class="mz-footer">
  <div class="mz-container">
    <div class="mz-footer__grid">
      <div class="mz-footer__brand">
        <svg class="mz-wings" …>…</svg>
        <span class="mz-footer__wordmark">Mez Systems</span>
        <span class="mz-caption">A Mez Studios company</span>
      </div>
      <div class="mz-footer__col">
        <h3 class="mz-footer__heading">Products</h3>
        <a class="mz-link" href="#">AI OS</a>
        <a class="mz-link" href="#">Aurora</a>
      </div>
      <!-- up to four link columns -->
    </div>
    <div class="mz-footer__legal">
      <span class="mz-caption">&copy; Mez Studios Pty Ltd</span>
      <span class="mz-caption">Terms · Privacy</span>
    </div>
  </div>
</footer>
```

## Dark band (CTA band)

A section treatment, never a theme. The CTA inverts to the white pill.

```html
<section class="mz-section">
  <div class="mz-container">
    <div class="mz-dark-band">
      <p class="mz-eyebrow">The AI operating system</p>
      <h2 class="mz-h2" style="margin-top: var(--mz-s-3);">Run the whole business from one system</h2>
      <p class="mz-body-lg" style="margin-top: var(--mz-s-4);">Set up in a weekend. Yours after one payment.</p>
      <a class="mz-btn mz-btn-ondark" style="margin-top: var(--mz-s-6);" href="#">Get the AI OS</a>
    </div>
  </div>
</section>
```

## FAQ

`name="faq"` keeps one item open at a time (native exclusive accordion, no JS).

```html
<div class="mz-faq">
  <details class="mz-faq__item" name="faq">
    <summary>
      What do I get?
      <svg class="mz-faq__chevron" viewBox="0 0 12 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1.5 6 6.5 11 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </summary>
    <p class="mz-faq__answer">The full AI OS, installed into your Notion workspace, with the setup guide.</p>
  </details>
  <!-- more items, same name -->
</div>
```

## Quote band

```html
<figure class="mz-quote">
  <blockquote class="mz-quote__text">&ldquo;It runs the parts of the business I used to carry in my head.&rdquo;</blockquote>
  <figcaption class="mz-quote__attribution">A solo founder, on the AI OS</figcaption>
</figure>
```

The quote is the page's one serif accent: nothing else on that page uses `.mz-serif`.

## Window frame (screenshots)

The screenshot stays in full colour. Never greyscale it.

```html
<figure class="mz-window">
  <div class="mz-window__bar">
    <span class="mz-window__dot"></span><span class="mz-window__dot"></span><span class="mz-window__dot"></span>
  </div>
  <img class="mz-window__img" src="assets/screenshot.png" alt="The AI OS dashboard in Notion">
</figure>
```
