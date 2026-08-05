/* Native console panels.
 *
 * Principle: the approved page IS the page. For every item that has a crafted
 * workbench/golden page, the console embeds that page's real <main> and real
 * stylesheet at runtime — fetched from the canonical file, never copied, never
 * iframed. Scripts are stripped and replaced by the console's own canonical
 * mounts: the shared Living Core renderer and the real custom-element modules.
 * The console adds evidence on top (live contrast verification, source notes);
 * it never redraws an approved surface in its own hand.
 */

const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char],
  );

const shead = (title, note = '') =>
  `<div class="shead"><h2>${esc(title)}</h2><p>${esc(note)}</p></div>`;

/* ── Canonical runtime mounts ────────────────────────────────── */

let cataloguePromise = null;
const catalogue = () =>
  (cataloguePromise ??= fetch('../gradient-library/catalogue.json').then((r) => r.json()));

async function mountCores(container) {
  if (!container.querySelector('[data-mz-core], .gx[data-p]')) return;
  try {
    const [{ mountLivingCores }, cat] = await Promise.all([
      import('../source-pack/design-system-export/mz-core.js'),
      catalogue(),
    ]);
    /* staticBaseUrl resolves against mz-core.js itself, not this page. */
    const result = await mountLivingCores(container, {
      catalogue: cat,
      staticBaseUrl: '../../gradient-library/assets/static/',
      forceStatic: matchMedia('(prefers-reduced-motion: reduce)').matches,
    });
    container.dataset.coreMode = result.mode;
  } catch (error) {
    container.dataset.coreMode = 'static';
    console.error('[console] Living Core mount failed; static twins retained.', error);
  }
}

const injectedCss = new Set();
function injectCss(href) {
  if (injectedCss.has(href)) return;
  injectedCss.add(href);
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = href;
  document.head.appendChild(link);
}

/* ── Embedding the original page ─────────────────────────────── */

/* Fetches a page stylesheet, absolutises its url() references, then rewrites
 * every selector under a scope attribute so the page's styles apply to the
 * embedded copy and nothing else in the console. */
const scopedCssDone = new Set();
async function injectScopedCss(cssUrl, scope) {
  const key = `${scope}::${cssUrl}`;
  if (scopedCssDone.has(key)) return;
  scopedCssDone.add(key);

  const response = await fetch(cssUrl);
  if (!response.ok) return;
  let text = await response.text();
  text = text.replace(
    /url\(\s*(['"]?)(?![a-z]+:|\/|#|data:)([^'")]+)\1\s*\)/gi,
    (_, __, path) => `url(${new URL(path, cssUrl).href})`,
  );

  const sheet = new CSSStyleSheet();
  try {
    sheet.replaceSync(text);
  } catch {
    return;
  }

  const prefix = (selectorText) =>
    selectorText
      .split(',')
      .map((selector) => {
        const trimmed = selector.trim();
        if (/^(html|body)\b/i.test(trimmed)) return trimmed.replace(/^(html|body)/i, scope);
        return `${scope} ${trimmed}`;
      })
      .join(', ');

  const serialise = (rules) => {
    let out = '';
    for (const rule of rules) {
      if (rule.type === CSSRule.STYLE_RULE) {
        out += `${prefix(rule.selectorText)}{${rule.style.cssText}}\n`;
      } else if (rule.type === CSSRule.MEDIA_RULE) {
        out += `@media ${rule.conditionText}{${serialise(rule.cssRules)}}\n`;
      } else if (rule.type === CSSRule.SUPPORTS_RULE) {
        out += `@supports ${rule.conditionText}{${serialise(rule.cssRules)}}\n`;
      } else {
        out += `${rule.cssText}\n`; /* keyframes, font-face — safe unscoped */
      }
    }
    return out;
  };

  const style = document.createElement('style');
  style.dataset.scopedFor = key;
  style.textContent = serialise(sheet.cssRules);
  document.head.appendChild(style);
}

async function embedOriginal(pageDir, scopeId, container) {
  const base = new URL(pageDir, location.href);
  const response = await fetch(new URL('index.html', base));
  if (!response.ok) throw new Error(`fetch ${base} → ${response.status}`);
  const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
  const main = doc.querySelector('main') ?? doc.body;

  main.querySelectorAll('script').forEach((node) => node.remove());
  for (const el of main.querySelectorAll('[src], [href], [poster]')) {
    for (const attr of ['src', 'href', 'poster']) {
      const value = el.getAttribute(attr);
      if (!value || value.startsWith('#') || /^[a-z]+:/i.test(value)) continue;
      el.setAttribute(attr, new URL(value, base).href);
    }
  }

  const host = document.createElement('div');
  host.className = 'orig';
  host.dataset.origPage = scopeId;
  host.dataset.mzMode = 'light';
  host.innerHTML = main.innerHTML;
  container.appendChild(host);

  await injectScopedCss(new URL('styles.css', base).href, `[data-orig-page="${scopeId}"]`);
  return host;
}

/* ── Colour: live contrast verification (console value-add) ──── */

const hexToRgb = (hex) => {
  const clean = String(hex).replace('#', '');
  const full = clean.length === 3 ? clean.split('').map((c) => c + c).join('') : clean;
  return [0, 2, 4].map((offset) => parseInt(full.slice(offset, offset + 2), 16));
};

const luminance = (hex) => {
  const [r, g, b] = hexToRgb(hex).map((channel) => {
    const value = channel / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

const contrast = (a, b) => {
  const [high, low] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (high + 0.05) / (low + 0.05);
};

function colourExtras(source) {
  const primitives = source.primitives ?? {};
  const resolve = (ref) => primitives[ref] ?? ref;
  const lightRoles = source.modes?.light?.roles ?? {};
  const pairs = (source.contrastPairs ?? []).map((pair) => {
    const fg = resolve(lightRoles[pair.foreground] ?? pair.foreground);
    const bg = resolve(lightRoles[pair.background] ?? pair.background);
    const ratio = contrast(fg, bg);
    return { ...pair, fg, bg, ratio, pass: ratio >= (pair.minimum ?? 0) };
  });
  const failures = pairs.filter((pair) => !pair.pass);

  return `
    ${shead('Live contrast verification', `${pairs.length} declared pairs, recomputed from the source file at load`)}
    ${
      failures.length
        ? `<div class="flag"><strong>${failures.length} pair(s) below the declared minimum.</strong></div>`
        : `<p class="plede">All ${pairs.length} pairs meet their declared minimum. If a token edit ever broke one, this section would go red on load.</p>`
    }
    <div class="pairs">
      ${pairs
        .map(
          (pair) => `
        <div class="pair">
          <span class="pair__demo" style="background:${esc(pair.bg)};color:${esc(pair.fg)}">Aa</span>
          <span class="pair__id mono">${esc(pair.id)}</span>
          <span class="pair__ratio mono">${pair.ratio.toFixed(2)}:1</span>
          <span class="badge" data-tone="${pair.pass ? 'go' : 'alert'}">${pair.pass ? 'pass' : 'fail'} · min ${esc(pair.minimum)}</span>
        </div>`,
        )
        .join('')}
    </div>
  `;
}

/* ── Panel registry ──────────────────────────────────────────── */

/* page: the original crafted page embedded as-is.
 * source + extras: console-owned evidence appended below the original.
 * modules/css: canonical element modules the embedded markup needs. */
export const PANELS = {
  colour: {
    page: '../workbench/foundations/colour/',
    source: '../foundations/colour/colour.source.json',
    extras: colourExtras,
  },
  typography: { page: '../workbench/foundations/typography/' },
  'space-layout': { page: '../workbench/foundations/space-layout/' },
  'geometry-controls': { page: '../workbench/foundations/geometry-controls/' },
  'foundation-release': { page: '../workbench/foundations/release/' },
  disc: { page: '../workbench/expressions/disc/' },
  sphere: { page: '../workbench/expressions/sphere/' },
  'wings-mark': { page: '../workbench/expressions/wings-mark/' },
  'product-card': { page: '../workbench/expressions/product-card/' },
  'trading-card': { page: '../workbench/expressions/trading-card/' },
  'channel-motion': { page: '../workbench/expressions/channel-motion/' },
  'stress-proof': { page: '../workbench/expressions/stress-proof/' },
  'global-navigation': {
    page: '../workbench/components/global-navigation/',
    modules: ['../components/global-navigation/mez-global-navigation.js'],
    css: ['../components/global-navigation/mez-global-navigation.css'],
  },
  'halftone-portrait': {
    page: '../workbench/components/halftone-portrait/',
    modules: ['../components/halftone-portrait/mez-halftone-portrait.js'],
    css: ['../components/halftone-portrait/mez-halftone-portrait.css'],
  },
  'testimonial-marquee': {
    page: '../workbench/components/testimonial-marquee/',
    modules: ['../components/testimonial-marquee/mez-testimonial-marquee.js'],
    css: ['../components/testimonial-marquee/mez-testimonial-marquee.css'],
  },
  'golden-homepage': {
    page: '../workbench/golden/homepage/',
    css: [
      '../components/global-navigation/mez-global-navigation.css',
      '../components/testimonial-marquee/mez-testimonial-marquee.css',
      '../components/halftone-portrait/mez-halftone-portrait.css',
    ],
    modules: [
      '../components/global-navigation/mez-global-navigation.js',
      '../components/testimonial-marquee/mez-testimonial-marquee.js',
      '../components/halftone-portrait/mez-halftone-portrait.js',
    ],
  },
};

async function loadJson(path) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(String(response.status));
    return await response.json();
  } catch {
    return null;
  }
}

/* Orchestrates a full native panel into `mount`. Called by app.js. */
export async function renderPanel(id, mount) {
  const panel = PANELS[id];
  if (!panel) return;
  mount.innerHTML = '<p class="card__note">Loading the canonical page…</p>';

  try {
    for (const href of panel.css ?? []) injectCss(href);
    await Promise.all((panel.modules ?? []).map((module) => import(module)));

    mount.innerHTML = '';
    if (panel.page) {
      await embedOriginal(panel.page, id, mount);
    }
    if (panel.source && panel.extras) {
      const source = await loadJson(panel.source);
      if (source) {
        const extras = document.createElement('div');
        extras.innerHTML = panel.extras(source);
        mount.appendChild(extras);
      }
    }

    const note = document.createElement('p');
    note.className = 'card__note src';
    note.innerHTML = panel.page
      ? `This is the canonical page at <code>${esc(panel.page.replace(/^\.\.\//, 'brand-kit/'))}</code>, embedded live — same markup, same stylesheet, scripts replaced by the console's canonical mounts.`
      : `Rendered live from <code>${esc((panel.source ?? '').replace(/^\.\.\//, 'brand-kit/'))}</code>.`;
    mount.appendChild(note);

    await mountCores(mount);
  } catch (error) {
    mount.innerHTML = `<div class="flag">Could not embed the canonical page: ${esc(error.message)}</div>`;
  }
}
