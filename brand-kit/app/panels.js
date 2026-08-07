/* Native console panels — the working-reference layer.
 *
 * Every panel renders from the same *.source.json contract the build and
 * verify scripts read, so the panel and the system cannot drift. These are
 * deliberately dense, scannable reference views: palettes, tokens, bands,
 * rules. The crafted editorial proof pages stay at their own addresses and
 * every item links out to its visual page — reference here, showcase there.
 * Live stages import the canonical runtime and custom elements directly —
 * the real modules, never copies.
 */

const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char],
  );

/* ── Shared helpers ──────────────────────────────────────────── */

const WINGS = '../source-pack/design-system-export/assets/wings.svg';
const STATIC_TWIN = (id) => `../gradient-library/assets/static/${String(id).toLowerCase()}.webp`;

/* A relative url() inside a custom property is resolved against the
 * stylesheet that consumes the var(), not against this document — so any
 * value handed to canonical CSS must be absolute. */
const STATIC_TWIN_ABS = (id) =>
  new URL(`../gradient-library/assets/static/${String(id).toLowerCase()}.webp`, document.baseURI).href;
const PRODUCT_CORES = [
  ['MZ-G13', 'AI OS'],
  ['MZ-G12', 'Context Engine'],
  ['MZ-G06', 'AI Ads System'],
  ['MZ-G15', 'Claude Code OS'],
  ['MZ-G20', 'Organic Content OS'],
];

let cataloguePromise = null;
const catalogue = () =>
  (cataloguePromise ??= fetch('../gradient-library/catalogue.json').then((r) => r.json()));

async function mountCores(container) {
  try {
    const [{ mountLivingCores }, cat] = await Promise.all([
      import('../source-pack/design-system-export/mz-core.js'),
      catalogue(),
    ]);
    /* staticBaseUrl resolves against mz-core.js itself, not this page; the
     * module-local wings default is already correct and must not be
     * overridden with a page-relative path. */
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

const kv = (rows) =>
  `<dl class="meta">${rows
    .filter((row) => row.length && row[1] !== undefined && row[1] !== null && row[1] !== '')
    .map(([k, v, mono]) => `<dt>${esc(k)}</dt><dd${mono ? ' class="mono"' : ''}>${v}</dd>`)
    .join('')}</dl>`;

const pills = (items, tone = 'idle') =>
  `<div class="pillrow">${items.map((t) => `<span class="badge" data-tone="${tone}">${esc(t)}</span>`).join('')}</div>`;

const shead = (title, note = '') =>
  `<div class="shead"><h2>${esc(title)}</h2><p>${esc(note)}</p></div>`;

const bandsTable = (bands) => `
  <div class="log">
    ${bands
      .map(
        (band) => `<div class="log__row log__row--bands">
          <span class="mono">${esc(band.id)}</span>
          <span class="log__title">${esc(band.role ?? '')}<span class="log__id">${esc(band.policy ?? '')}</span></span>
          <span class="mono band-range">${esc(band.minimumPx)}–${esc(band.maximumPx ?? '∞')}px${band.crop ? ` · crop ${esc(band.crop)}` : ''}${band.state ? ` · ${esc(band.state)}` : ''}</span>
        </div>`,
      )
      .join('')}
  </div>`;

/* ── Cloning specimens from the canonical pages ──────────────── */

/* The canonical proof pages build their specimens with their own
 * controllers. Rather than re-implement those builders here — which is how
 * a second, drifting copy of the design gets created — we load the real page
 * in a hidden same-origin frame, let its own code run, then adopt the
 * finished nodes. The console never draws the specimen; it borrows it. */

const scopedCssDone = new Set();

/* Rewrites a stylesheet so its rules only apply beneath `scope`, and makes
 * its relative url()s absolute (they would otherwise resolve against this
 * document once the rules are re-hosted here). */
async function injectScopedCss(cssUrl, scope) {
  const key = `${scope}::${cssUrl}`;
  if (scopedCssDone.has(key)) return;
  scopedCssDone.add(key);

  const response = await fetch(cssUrl);
  if (!response.ok) return;
  let text = await response.text();
  text = text.replace(
    /url\(\s*(['"]?)(?![a-z]+:|\/|#|data:)([^'")]+)\1\s*\)/gi,
    (_, __, path) => `url("${new URL(path, cssUrl).href}")`,
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
        return /^(html|body)\b/i.test(trimmed)
          ? trimmed.replace(/^(html|body)/i, scope)
          : `${scope} ${trimmed}`;
      })
      .join(', ');

  const serialise = (rules) => {
    let out = '';
    for (const rule of rules) {
      if (rule.type === CSSRule.STYLE_RULE) out += `${prefix(rule.selectorText)}{${rule.style.cssText}}\n`;
      else if (rule.type === CSSRule.MEDIA_RULE) out += `@media ${rule.conditionText}{${serialise(rule.cssRules)}}\n`;
      else if (rule.type === CSSRule.SUPPORTS_RULE) out += `@supports ${rule.conditionText}{${serialise(rule.cssRules)}}\n`;
      else out += `${rule.cssText}\n`; /* keyframes, font-face — safe unscoped */
    }
    return out;
  };

  const style = document.createElement('style');
  style.dataset.scopedFor = key;
  style.textContent = serialise(sheet.cssRules);
  document.head.appendChild(style);
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/* Loads `pageUrl` off-screen, waits for its controller to produce `selector`,
 * and returns adopted clones. `?static` is appended so the hidden frame uses
 * exact static twins instead of spinning up a WebGL context we would throw
 * away. */
async function cloneFromPage(pageUrl, selector, { expect = 1, strip = [], timeout = 12000 } = {}) {
  const frame = document.createElement('iframe');
  frame.setAttribute('aria-hidden', 'true');
  frame.setAttribute('tabindex', '-1');
  frame.style.cssText =
    'position:absolute;left:-99999px;top:0;width:1280px;height:900px;border:0;visibility:hidden;';
  const url = new URL(pageUrl, document.baseURI);
  url.searchParams.set('static', '');
  frame.src = url.href;
  document.body.appendChild(frame);

  try {
    await new Promise((resolve, reject) => {
      frame.addEventListener('load', resolve, { once: true });
      frame.addEventListener('error', () => reject(new Error('frame failed')), { once: true });
      setTimeout(() => reject(new Error('frame load timed out')), timeout);
    });

    const doc = frame.contentDocument;
    if (!doc) throw new Error('frame document unavailable');

    const deadline = Date.now() + timeout;
    let nodes = [];
    while (Date.now() < deadline) {
      nodes = [...doc.querySelectorAll(selector)];
      if (nodes.length >= expect) break;
      await wait(120);
    }
    if (!nodes.length) throw new Error(`no nodes matched ${selector}`);

    /* Adopted nodes carry URLs written relative to the source page. Once they
     * live in this document they would re-resolve against /brand-kit/app/ and
     * break, so every relative reference is absolutised against the frame. */
    const base = frame.contentWindow.location.href;
    const absolutise = (clone) => {
      for (const el of [clone, ...clone.querySelectorAll('*')]) {
        for (const attr of ['src', 'href', 'poster']) {
          const value = el.getAttribute?.(attr);
          if (value && !/^([a-z]+:|\/\/|#|data:)/i.test(value)) {
            el.setAttribute(attr, new URL(value, base).href);
          }
        }
        const style = el.getAttribute?.('style');
        if (style?.includes('url(')) {
          el.setAttribute(
            'style',
            style.replace(
              /url\(\s*(['"]?)(?!([a-z]+:|\/\/|#|data:))([^'")]+)\1\s*\)/gi,
              (_, quote, __, path) => `url("${new URL(path, base).href}")`,
            ),
          );
        }
      }
      return clone;
    };

    return nodes.map((node) => {
      const clone = absolutise(document.importNode(node, true));
      for (const sel of strip) clone.querySelectorAll(sel).forEach((el) => el.remove());
      return clone;
    });
  } finally {
    frame.remove();
  }
}

/* Renders cloned specimens into `mount` under a private style scope. */
async function mountClonedSpecimens(mount, { page, css, selector, expect, strip, scope, heading, note }) {
  const holder = document.createElement('div');
  holder.className = 'specimens';
  holder.dataset.specScope = scope;
  holder.innerHTML = `<p class="card__note">Loading the canonical specimens…</p>`;
  mount.appendChild(holder);

  try {
    const [clones] = await Promise.all([
      cloneFromPage(page, selector, { expect, strip }),
      injectScopedCss(new URL(css, document.baseURI).href, `[data-spec-scope="${scope}"]`),
    ]);

    holder.innerHTML = '';
    holder.insertAdjacentHTML(
      'beforebegin',
      `<div class="shead"><h2>${esc(heading)}</h2><p>${esc(
        note ?? `${clones.length} specimens, built by the canonical page`,
      )}</p></div>`,
    );
    for (const clone of clones) holder.appendChild(clone);
    return clones.length;
  } catch (error) {
    holder.innerHTML = `<div class="flag">Could not load the canonical specimens: ${esc(
      error.message,
    )}. The visual page still has them.</div>`;
    return 0;
  }
}

/* ── Visual specimens ────────────────────────────────────────── */

/* Draws the expression at each declared scale band, at its real minimum
 * size, so the bands are something you can see rather than read. Wings are
 * omitted below the marked minimum exactly as the contract requires. */
const scaleBandRow = (bands, shape, markedMinimum = 48) => {
  if (!bands?.length) return '';
  return `
    ${shead('Scale bands, drawn', `${bands.length} bands at their real minimum size`)}
    <div class="stage">
      <div class="stage__bar"><span>Exact static twins · Wings omitted below ${markedMinimum}px, per the contract</span><span class="mono">MZ-G13</span></div>
      <div class="bandrow">
        ${bands
          .map((band) => {
            const size = Math.min(Number(band.minimumPx) || 48, 168);
            const marked = size >= markedMinimum;
            return `
              <figure class="bandfig">
                <span class="core core--${shape}" style="width:${size}px">
                  <img class="core__twin" src="${STATIC_TWIN('MZ-G13')}" alt="">
                  ${marked ? `<img class="wings" src="${WINGS}" alt="">` : ''}
                </span>
                <figcaption>
                  <span class="bandfig__id mono">${esc(band.id)}</span>
                  <span class="bandfig__px mono">${esc(band.minimumPx)}px${band.maximumPx ? `–${esc(band.maximumPx)}` : '+'}</span>
                  <span class="bandfig__role">${esc(band.role ?? '')}</span>
                </figcaption>
              </figure>`;
          })
          .join('')}
      </div>
    </div>`;
};

/* Card specimens are generated against the canonical workbench stylesheet —
 * the real design, with thin markup following its documented class grammar.
 * Only a representative handful; the complete approved set stays on the
 * visual page, which is why every card panel links out to it. */
/* Mirrors faceCard()/productIdentity() in the canonical trading-card
 * controller exactly: a positioned .tc-field carrying the material through
 * the --field custom property, then .tc-identity. Getting this structure
 * wrong is what broke the first attempt — the material must be its own
 * layer, not a background on the card. */
const tcFace = (product, variant) => {
  const identity = (opts = {}) => `
    <div class="tc-identity">
      ${opts.wings === false ? '' : `<img class="tc-wings${opts.large ? ' is-large' : ''}" src="${WINGS}" alt="">`}
      <h4 class="tc-name">${esc(product.publicName)}</h4>
      <span class="tc-function">${esc(product.function ?? '')}</span>
      ${opts.summary && product.summary ? `<p class="tc-summary">${esc(product.summary)}</p>` : ''}
    </div>`;

  const field = `<div class="tc-field" style="--field:url('${STATIC_TWIN_ABS(product.gradientId)}')" data-gradient-id="${esc(product.gradientId)}"></div>`;
  const cornerWings = `<img class="tc-corner-wings" src="${WINGS}" alt="">`;

  const body =
    variant === 'corner'
      ? field + cornerWings + identity({ wings: false, summary: true })
      : field + identity({ large: true });

  return `<article class="tc-card tc-face face--${esc(variant)}">${body}</article>`;
};

const tradingCardSpecimens = (products) => {
  const faces = [
    { variant: 'anchored', title: 'Anchored identity', id: 'TC-F01', index: 0 },
    { variant: 'centred', title: 'Centred identity', id: 'TC-F02', index: 1 },
    { variant: 'corner', title: 'Corner identity', id: 'TC-F05', index: 4 },
  ];
  return `
    ${shead('Card faces, drawn', '3 of the 23 approved specimens · every face, back, deck and placement is on the visual page')}
    <div class="stage" data-card-stage>
      <div class="stage__bar"><span>Canonical trading-card stylesheet and markup · exact static materials</span><span class="mono">TC-F01 · F02 · F05</span></div>
      <div class="cardrow">
        ${faces
          .map(({ variant, title, id, index }) => {
            const product = products[index] ?? products[0];
            return `
              <figure class="cardfig">
                ${tcFace(product, variant)}
                <figcaption>${esc(title)}<span class="mono">${esc(id)} · face--${esc(variant)}</span></figcaption>
              </figure>`;
          })
          .join('')}
      </div>
    </div>`;
};

const productCardSpecimens = (products) => `
  ${shead('Product cards, drawn', 'The calm shelf: white card, one material, name-first hierarchy')}
  <div class="stage">
    <div class="stage__bar"><span>Canonical grammar · one material per card, filled action</span><span class="mono">registry-driven</span></div>
    <div class="pcrow">
      ${products
        .slice(0, 3)
        .map(
          (product) => `
        <article class="pcard">
          <span class="pcard__material" style="background-image:url('${STATIC_TWIN(product.gradientId)}')">
            <img class="wings" src="${WINGS}" alt="">
          </span>
          <div class="pcard__body">
            <h4 class="pcard__name">${esc(product.publicName)}</h4>
            <p class="pcard__fn">${esc(product.function ?? '')}</p>
            <span class="pcard__action">Explore ${esc(product.publicName)}</span>
          </div>
        </article>`,
        )
        .join('')}
    </div>
  </div>`;

let productsPromise = null;
const productRegistry = () =>
  (productsPromise ??= fetch('../registry/products.json')
    .then((r) => r.json())
    .then((d) => d.products ?? [])
    .catch(() => []));

/* ── Generic contract renderers ──────────────────────────────── */

const sentence = (key) =>
  String(key)
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .replace(/^./, (c) => c.toUpperCase());

/* Renders any nested contract object as readable rows: strings inline,
 * arrays as pills, nested objects as an indented sub-list. */
const contractRows = (object) =>
  `<dl class="meta">${Object.entries(object ?? {})
    .map(([key, value]) => {
      if (value === null || value === undefined || value === '') return '';
      let rendered;
      if (Array.isArray(value)) {
        rendered = value.every((v) => typeof v !== 'object')
          ? `<div class="pillrow pillrow--tight">${value.map((v) => `<span class="chip">${esc(v)}</span>`).join('')}</div>`
          : `<div class="pillrow pillrow--tight">${value.map((v) => `<span class="chip">${esc(v.title ?? v.id ?? JSON.stringify(v))}</span>`).join('')}</div>`;
      } else if (typeof value === 'object') {
        rendered = `<div class="subrows">${Object.entries(value)
          .map(
            ([k, v]) =>
              `<div class="subrow"><span class="subrow__k mono">${esc(k)}</span><span>${
                Array.isArray(v) ? esc(v.join(' · ')) : esc(String(v))
              }</span></div>`,
          )
          .join('')}</div>`;
      } else if (typeof value === 'boolean') {
        rendered = value ? 'yes' : 'no';
      } else {
        rendered = esc(String(value));
      }
      return `<dt>${esc(sentence(key))}</dt><dd>${rendered}</dd>`;
    })
    .join('')}</dl>`;

/* A rule list — the allowed/forbidden/prohibited/inherits sets that carry
 * most of the actual law in these contracts. */
const ruleList = (title, items, tone = 'idle') =>
  items?.length
    ? `${shead(title, `${items.length} rules`)}
       <ul class="rules" data-tone="${tone}">
         ${items.map((item) => `<li>${esc(item)}</li>`).join('')}
       </ul>`
    : '';

/* Specimen / scenario tables — the itemised proof lists. */
const specimenTable = (items, families) => {
  const byFamily = {};
  for (const item of items) (byFamily[item.family ?? item.suite ?? 'all'] ??= []).push(item);
  return Object.entries(byFamily)
    .map(([familyId, group]) => {
      const family = (families ?? []).find((f) => f.id === familyId);
      return `
        ${family ? shead(family.title, `${group.length} · ${family.job ?? ''}`) : shead(sentence(familyId), `${group.length} specimens`)}
        <div class="log">
          ${group
            .map(
              (item) => `<div class="log__row log__row--bands">
                <span class="mono">${esc(item.id)}</span>
                <span class="log__title">${esc(item.title)}${
                  item.automatedChecks
                    ? `<span class="log__id">${esc(item.automatedChecks.join(' · '))}</span>`
                    : item.variant
                    ? `<span class="log__id">variant · ${esc(item.variant)}</span>`
                    : item.pattern
                    ? `<span class="log__id">pattern · ${esc(item.pattern)}</span>`
                    : ''
                }</span>
                <span class="mono band-range">${esc(item.fixture ?? item.variant ?? '')}</span>
              </div>`,
            )
            .join('')}
        </div>`;
    })
    .join('');
};

const viewportChips = (viewports) =>
  viewports?.length
    ? `${shead('Test viewports', `${viewports.length} widths certified`)}
       <div class="pillrow">${viewports.map((v) => `<span class="chip mono">${esc(v)}px</span>`).join('')}</div>`
    : '';

/* Dependencies carry integrity hashes — useful, but collapsed by default. */
const dependencyBlock = (dependencies) =>
  dependencies && Object.keys(dependencies).length
    ? `<details class="deps">
         <summary><span>Dependencies &amp; integrity</span><span class="mono">${Object.keys(dependencies).length} pinned</span></summary>
         <div class="log">
           ${Object.entries(dependencies)
             .map(([name, dep]) => {
               const path = typeof dep === 'object' ? dep.path ?? '' : String(dep);
               const sha = typeof dep === 'object' ? dep.sha256 ?? '' : '';
               return `<div class="log__row log__row--bands">
                 <span class="mono">${esc(name)}</span>
                 <span class="log__title mono dep__path">${esc(path)}</span>
                 <span class="mono band-range">${sha ? `${esc(sha.slice(0, 12))}…` : ''}</span>
               </div>`;
             })
             .join('')}
         </div>
       </details>`
    : '';

const section = (title, note, object) =>
  object && Object.keys(object).length ? `${shead(title, note)}${contractRows(object)}` : '';

const allocationBlock = (allocation) =>
  allocation
    ? `${shead('Allocation', 'The one-live law')}
       ${kv([
         ['Static default', allocation.staticDefault ? 'yes — static is the complete expression' : 'no'],
         ['Max live per viewport', esc(allocation.maximumLivePerViewport)],
       ])}
       ${allocation.liveRequirements ? `<p class="card__k pillhead">Live requires</p>${pills(allocation.liveRequirements)}` : ''}
       ${allocation.staticRequired ? `<p class="card__k pillhead">Static required for</p>${pills(allocation.staticRequired)}` : ''}`
    : '';

/* One live core, rest exact static twins — obeying the expression law the
 * panel itself documents. */
const productCoreRow = (shape) => `
  <div class="stage" data-live-stage>
    <div class="stage__bar"><span>Live reference · canonical renderer · one live core, four exact static twins</span><span class="mono" data-stage-mode></span></div>
    <div class="corerow">
      ${PRODUCT_CORES.map(
        ([id, name], index) => `
        <figure class="corefig">
          ${
            index === 0
              ? `<span class="core core--${shape}" data-mz-core="${id}" data-shape="${shape}"><img class="wings" src="${WINGS}" alt=""></span>`
              : `<span class="core core--${shape}"><img class="core__twin" src="${STATIC_TWIN(id)}" alt=""><img class="wings" src="${WINGS}" alt=""></span>`
          }
          <figcaption>${esc(name)}<span class="mono">${id}${index === 0 ? ' · live' : ' · static twin'}</span></figcaption>
        </figure>`,
      ).join('')}
    </div>
  </div>`;

/* ── Foundations ─────────────────────────────────────────────── */

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

function colourPanel(source) {
  const primitives = source.primitives ?? {};
  const resolve = (ref) => primitives[ref] ?? ref;

  const families = {};
  for (const [key, hex] of Object.entries(primitives)) {
    (families[key.split('.')[0]] ??= []).push([key, hex]);
  }

  const swatches = Object.entries(families)
    .map(
      ([family, entries]) => `
        <div class="fam">
          <p class="card__k">${esc(family)}</p>
          <div class="swatches">
            ${entries
              .map(
                ([key, hex]) => `
              <div class="sw">
                <span class="sw__chip" style="background:${esc(hex)}"></span>
                <span class="sw__name">${esc(key.split('.').slice(1).join('.'))}</span>
                <span class="sw__hex mono">${esc(hex)}</span>
              </div>`,
              )
              .join('')}
          </div>
        </div>`,
    )
    .join('');

  const modes = Object.entries(source.modes ?? {})
    .map(([modeId, mode]) => {
      const roles = Object.entries(mode.roles ?? {});
      return `
        <details class="mode"${modeId === 'light' ? ' open' : ''}>
          <summary>
            <span class="mode__name">${esc(modeId)}</span>
            <span class="mode__purpose">${esc(mode.purpose ?? '')}</span>
            <span class="mode__count">${roles.length} roles</span>
          </summary>
          <div class="roles">
            ${roles
              .map(([role, ref]) => {
                const hex = resolve(ref);
                return `<div class="role">
                          <span class="sw__chip sw__chip--sm" style="background:${esc(hex)}"></span>
                          <span class="role__name mono">${esc(role)}</span>
                          <span class="role__ref">${esc(ref)}</span>
                          <span class="sw__hex mono">${esc(hex)}</span>
                        </div>`;
              })
              .join('')}
          </div>
        </details>`;
    })
    .join('');

  const lightRoles = source.modes?.light?.roles ?? {};
  const pairs = (source.contrastPairs ?? []).map((pair) => {
    const fg = resolve(lightRoles[pair.foreground] ?? pair.foreground);
    const bg = resolve(lightRoles[pair.background] ?? pair.background);
    const ratio = contrast(fg, bg);
    return { ...pair, fg, bg, ratio, pass: ratio >= (pair.minimum ?? 0) };
  });
  const failures = pairs.filter((pair) => !pair.pass);

  return `
    ${shead('Primitives', `${Object.keys(primitives).length} values · the only place a raw hex is allowed`)}
    ${swatches}
    ${shead('Modes', `${Object.keys(source.modes ?? {}).length} modes · roles resolve to primitives`)}
    ${modes}
    ${shead('Contrast verification', `${pairs.length} declared pairs, recomputed live`)}
    ${
      failures.length
        ? `<div class="flag"><strong>${failures.length} pair(s) below the declared minimum.</strong></div>`
        : `<p class="plede">All ${pairs.length} pairs meet their declared minimum. Ratios are computed from the source file at load — if a token edit ever broke one, this section would go red.</p>`
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

/* The approved specimen phrases from the canonical typography proof page —
 * the roles must read as the system, not as lorem or usage notes. */
const SPECIMENS = {
  'display.hero': 'AI-native systems.',
  'display.section': 'The work compounds.',
  'display.title': 'Context Engine',
  'heading.section': 'The intelligence is rented. The operating layer is yours.',
  'heading.subsection': 'What changes after installation',
  'body.lead': 'A complete operating system for making AI useful across your company.',
  'body.default':
    'Your context stays legible, your workflows stay consistent and each improvement becomes part of the operating layer.',
  'body.compact': 'Last verified 09:42 AEST by the canonical release validator.',
  'ui.control': 'Explore the AI OS',
  'ui.label': 'Operating principle',
  'numeric.display': '$99',
  'numeric.tabular': '01  03:42  98.6%',
  'editorial.accent': 'The system remembers.',
};

function typographyPanel(source) {
  const families = Object.entries(source.families ?? {})
    .map(
      ([id, family]) => `
      <div class="card">
        <p class="card__title"><span>${esc(family.name)}</span><span class="mono">${esc(id)}</span></p>
        <p class="card__note">${esc(family.role ?? '')}</p>
        ${kv([
          ['CSS family', esc(family.cssFamily), true],
          family.version ? ['Version', esc(family.version), true] : [],
          family.sourceUrl
            ? ['Source', `<a href="${esc(family.sourceUrl)}" target="_blank" rel="noopener">${esc(family.sourceUrl)}</a>`]
            : [],
        ])}
      </div>`,
    )
    .join('');

  const roles = Object.entries(source.roles ?? {})
    .map(([id, role]) => {
      const family = source.families?.[role.family];
      const size = role.size ?? {};
      const clamp =
        size.minPx && size.maxPx
          ? `clamp(${size.minPx}px, ${size.preferredVw}vw, ${size.maxPx}px)`
          : `${size.minPx ?? 16}px`;
      const style = [
        `font-family:"${family?.cssFamily ?? 'inherit'}",${family?.fallback ?? 'sans-serif'}`,
        `font-size:${clamp}`,
        `font-weight:${role.weight ?? 400}`,
        `line-height:${role.lineHeight ?? 1.4}`,
        `letter-spacing:${role.trackingEm ?? 0}em`,
        role.case && role.case !== 'none' ? `text-transform:${role.case}` : '',
        role.maxWidth ? `max-width:${role.maxWidth}` : '',
      ]
        .filter(Boolean)
        .join(';');

      return `
        <div class="spec">
          <div class="spec__head">
            <span class="mono">${esc(id)}</span>
            <span class="spec__meta mono">${esc(role.family)} · ${esc(role.weight)} · ${size.minPx ?? '—'}–${size.maxPx ?? '—'}px · ${esc(role.trackingEm ?? 0)}em</span>
          </div>
          <p class="spec__demo" style="${esc(style)}">${esc(SPECIMENS[id] ?? role.usage ?? 'The quick brown fox')}</p>
          ${role.usage ? `<p class="spec__usage">${esc(role.usage)}</p>` : ''}
        </div>`;
    })
    .join('');

  return `
    ${shead('Families', `${Object.keys(source.families ?? {}).length} licensed families`)}
    <div class="grid" data-cols="2">${families}</div>
    ${shead('Roles', `${Object.keys(source.roles ?? {}).length} roles · rendered at their real values`)}
    ${roles}
  `;
}

function spacePanel(source) {
  const steps = Object.entries(source.space ?? {});
  const widths = Object.entries(source.contentWidths ?? {});
  const maxWidth = Math.max(...widths.map(([, value]) => Number(value) || 0), 1);

  return `
    ${shead('Scale', `Base unit ${esc(source.baseUnit)}px · ${steps.length} steps, drawn at true size`)}
    <div class="scale">
      ${steps
        .map(
          ([step, value]) => `
        <div class="step">
          <span class="step__id mono">${esc(step)}</span>
          <span class="step__bar" style="width:${Number(value)}px"></span>
          <span class="step__px mono">${esc(value)}px</span>
        </div>`,
        )
        .join('')}
    </div>
    ${shead('Content widths', `${widths.length} widths · shown in proportion`)}
    <div class="widths">
      ${widths
        .map(
          ([id, value]) => `
        <div class="wrow">
          <span class="step__id mono">${esc(id)}</span>
          <span class="wrow__bar" style="width:${((Number(value) / maxWidth) * 100).toFixed(1)}%"></span>
          <span class="step__px mono">${esc(value)}px</span>
        </div>`,
        )
        .join('')}
    </div>
  `;
}

function geometryPanel(source) {
  const radii = Object.entries(source.radii ?? {});
  const borders = Object.entries(source.borders ?? {});
  const depth = Object.entries(source.depth ?? {});

  return `
    ${shead('Radii', `${radii.length} named radii, drawn at true value`)}
    <div class="grid" data-cols="4">
      ${radii
        .map(
          ([id, value]) => `
        <div class="geo">
          <span class="geo__box" style="border-radius:${Number(value) > 100 ? '9999px' : `${value}px`}"></span>
          <span class="geo__id">${esc(id)}</span>
          <span class="step__px mono">${esc(value)}px</span>
        </div>`,
        )
        .join('')}
    </div>
    ${shead('Borders', `${borders.length} structural widths`)}
    <div class="grid" data-cols="3">
      ${borders
        .map(
          ([id, value]) => `
        <div class="geo">
          <span class="geo__box" style="border-width:${esc(value)}px;border-radius:12px"></span>
          <span class="geo__id">${esc(id)}</span>
          <span class="step__px mono">${esc(value)}px</span>
        </div>`,
        )
        .join('')}
    </div>
    ${shead('Depth', `${depth.length} levels · the real shadow, not a description`)}
    <div class="grid" data-cols="3">
      ${depth
        .map(
          ([id, value]) => `
        <div class="geo">
          <span class="geo__box geo__box--plain" style="box-shadow:${esc(value)}"></span>
          <span class="geo__id">${esc(id)}</span>
          <span class="step__px mono geo__shadow">${esc(value)}</span>
        </div>`,
        )
        .join('')}
    </div>
  `;
}

/* ── Expressions ─────────────────────────────────────────────── */

function discPanel(source) {
  return `
    ${productCoreRow('disc')}
    ${shead('Geometry', 'The circle is the whole contract')}
    ${contractRows(source.geometry)}
    ${shead('Wings', 'Exact asset, exact ratio')}
    ${contractRows(source.wings)}
    ${scaleBandRow(source.scaleBands, 'disc', source.wings?.minimumMarkedDiscPx ?? 48)}
    ${shead('Scale bands, specified', `${(source.scaleBands ?? []).length} bands · what the disc may do at each size`)}
    ${bandsTable(source.scaleBands ?? [])}
    ${allocationBlock(source.allocation)}
    ${section('Surfaces', 'Where a disc may sit, per mode', source.surfaces)}
    ${section('Channels', `${Object.keys(source.channels ?? {}).length} channel policies`, source.channels)}
    ${section('Accessibility', 'Non-negotiable', source.accessibility)}
    ${
      source.products?.length
        ? `${shead('Products', `${source.products.length} canonical assignments`)}
           <div class="grid" data-cols="3">
             ${source.products
               .map(
                 (product) => `<div class="card">
                   <p class="card__title"><span>${esc(product.publicName)}</span><span class="mono">${esc(product.gradientId)}</span></p>
                   <p class="card__note mono">${esc(product.productId)}</p>
                 </div>`,
               )
               .join('')}
           </div>`
        : ''
    }
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

function spherePanel(source) {
  const finish = source.finish ?? {};
  return `
    <div class="stage" data-live-stage>
      <div class="stage__bar"><span>Live reference · Deep Mineral sphere · canonical renderer</span><span class="mono" data-stage-mode></span></div>
      <div class="corerow">
        <figure class="corefig">
          <span class="core core--sphere core--lg" data-mz-core="MZ-G13" data-shape="sphere"><img class="wings" src="${WINGS}" alt=""></span>
          <figcaption>AI OS<span class="mono">MZ-G13 · live</span></figcaption>
        </figure>
      </div>
    </div>
    ${shead('Relationship to the disc', '')}
    <p class="plede">${esc(source.relationshipToDisc?.policy ?? '')}</p>
    ${shead('Deep Mineral finish', `profile ${esc(finish.profileId ?? '')}`)}
    <div class="grid" data-cols="4">
      ${Object.entries(finish.values ?? {})
        .map(
          ([k, v]) => `<div class="geo"><span class="card__v card__v--sm">${esc(v)}</span><span class="geo__id">${esc(k)}</span></div>`,
        )
        .join('')}
    </div>
    <p class="card__note">${esc(finish.policy ?? '')}</p>
    ${scaleBandRow(source.scaleBands, 'sphere', 48)}
    ${shead('Scale bands, specified', `${(source.scaleBands ?? []).length} bands · crop rules by size`)}
    ${bandsTable(source.scaleBands ?? [])}
    ${section('Allocation', 'The one-live law', source.allocation)}
    ${section('Fallback', 'What replaces the sphere, and when', source.fallback)}
    ${section('Surfaces', 'Placement per surface', source.surfaces)}
    ${section('Wings', 'Exact asset, exact ratio', source.wings)}
    ${section('Accessibility', 'Non-negotiable', source.accessibility)}
    ${section('Proof product', 'The product this contract was proven against', source.proofProduct)}
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

function wingsPanel(source) {
  const roles = source.roles ?? [];
  return `
    ${source.recommendation ? `${shead('Recommendation', 'The whole position in one paragraph')}<p class="plede">${esc(source.recommendation)}</p>` : ''}
    ${shead('Roles', `${roles.length} approved mark roles · each shown on both surfaces`)}
    <div class="grid" data-cols="2">
      ${roles
        .map(
          (role) => `
        <div class="card">
          <div class="wingpair">
            <span class="wingchip" style="background:#F8F8F8"><img src="${WINGS}" alt=""></span>
            <span class="wingchip" style="background:#171715"><img src="${WINGS}" alt="" style="filter:brightness(0) invert(1)"></span>
          </div>
          <p class="card__title"><span>${esc(role.id)}</span>${role.label ? `<span class="mono">${esc(role.label)}</span>` : ''}</p>
          <p class="card__note">${esc(role.use ?? '')}</p>
          ${kv([
            role.colourLight ? ['Light surface', esc(role.colourLight), true] : [],
            role.colourDark ? ['Dark surface', esc(role.colourDark), true] : [],
            role.motion ? ['Motion', esc(role.motion)] : [],
          ])}
        </div>`,
        )
        .join('')}
    </div>
    ${section('Geometry', 'The exact asset', source.geometry)}
    ${section('Lockup', 'Mark plus wordmark', source.lockup)}
    ${section('Space & scale', 'Clear space and minimum sizes', source.spaceAndScale)}
    ${section('Colour', 'No second corporate hue', source.colour)}
    ${shead('Gradient-mask exception', 'Rare by design · one per viewport')}
    ${contractRows({ maximumLivePerViewport: source.gradientMask?.maximumLivePerViewport, fallback: source.gradientMask?.fallback })}
    ${source.gradientMask?.allowed ? `<p class="card__k pillhead">Allowed</p>${pills(source.gradientMask.allowed, 'go')}` : ''}
    ${source.gradientMask?.forbidden ? `<p class="card__k pillhead">Forbidden</p>${pills(source.gradientMask.forbidden, 'alert')}` : ''}
    ${section('Responsive & export', 'Screen, print and export behaviour', source.responsiveAndExport)}
    ${ruleList('Parked treatments', source.parked, 'idle')}
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

async function productCardPanel(source) {
  const arch = source.cardArchitecture ?? {};
  const products = await productRegistry();
  return `
    ${products.length ? productCardSpecimens(products) : ''}
    ${shead('Design thesis', '')}
    <p class="plede">${esc(source.designThesis ?? '')}</p>
    ${shead('Card architecture', esc(arch.name ?? ''))}
    ${kv([
      ['Width range', `${esc((arch.widthRange ?? []).join('–'))}px`],
      ['Ratio', esc(arch.ratio)],
    ])}
    ${arch.fixedSlots ? `<p class="card__k pillhead">Fixed slots</p>${pills(arch.fixedSlots, 'go')}` : ''}
    ${arch.variableMedia ? `<p class="card__k pillhead">Variable media</p>${pills(arch.variableMedia)}` : ''}
    ${shead('Postures', `${(source.postures ?? []).length} approved postures`)}
    <div class="log">
      ${(source.postures ?? [])
        .map(
          (posture) => `<div class="log__row log__row--bands">
            <span class="mono">${esc(posture.id)}</span>
            <span class="log__title">${esc(posture.name)} — ${esc(posture.job ?? '')}<span class="log__id">${esc(posture.rule ?? '')}</span></span>
            <span class="mono band-range">${esc(posture.minimum ?? '')}</span>
          </div>`,
        )
        .join('')}
    </div>
    ${
      source.expressions?.length
        ? `${shead('Expression families', `${source.expressions.length} approved families`)}
           <div class="grid" data-cols="2">
             ${source.expressions
               .map(
                 (expression) => `<div class="card">
                   <p class="card__title"><span>${esc(expression.name)}</span><span class="mono">${esc(expression.id)}</span></p>
                   <p class="card__note"><strong>${esc(expression.role ?? '')}</strong> · ${esc(expression.placement ?? '')}</p>
                   <p class="card__note">${esc(expression.thesis ?? '')}</p>
                 </div>`,
               )
               .join('')}
           </div>`
        : ''
    }
    ${section('Core allocation', 'One live material per viewport', source.coreAllocation)}
    ${section('Surface strategy', 'Where colour is allowed to happen', source.surfaceStrategy)}
    ${section('Territories', 'How products stay distinct inside one chassis', source.territories)}
    ${section('Shared content', 'Everything reads from the registry at runtime', source.sharedContent)}
    ${section('Accessibility', 'Non-negotiable', source.accessibility)}
    ${section('Phase B scope', 'The functional component system', source.phaseBScope)}
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

async function tradingCardPanel(source) {
  const anatomy = source.anatomy ?? {};
  return `
    <div data-clone-specimens></div>
    ${shead('Thesis', '')}
    <p class="plede">${esc(source.thesis ?? '')}</p>
    ${shead('Meaning', 'What each configuration is for')}
    ${kv(Object.entries(source.meaning ?? {}).map(([k, v]) => [k, esc(String(v))]))}
    ${shead('Anatomy', '')}
    ${kv(Object.entries(anatomy).map(([k, v]) => [k, esc(Array.isArray(v) ? v.join(', ') : String(v))]))}
    ${ruleList('Inherits from the product card', source.inherits, 'go')}
    ${specimenTable(source.specimens ?? [], source.families)}
    ${section('Motion', 'One live front field at most', source.motion)}
    ${ruleList('Prohibited', source.prohibited, 'alert')}
    ${section('Round lineage', 'How this revision was reached', source.roundLineage)}
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

function channelMotionPanel(source) {
  return `
    ${shead('Thesis', '')}
    <p class="plede">${esc(source.thesis ?? '')}</p>
    ${section('Decision model', 'How a motion event earns its place', source.decisionModel)}
    ${specimenTable(source.specimens ?? [], source.families)}
    ${section('Reduced motion', 'What happens when motion is refused', source.reducedMotion)}
    ${section('Export contract', 'Motion may never carry sole meaning', source.exportContract)}
    ${section('Scope', 'What this system covers', source.scope)}
    ${ruleList('Prohibited', source.prohibited, 'alert')}
    ${section('Deferral', 'Deliberately left open', source.deferral)}
    ${viewportChips(source.testViewports)}
    ${dependencyBlock(source.dependencies)}
  `;
}

function stressPanel(source) {
  const coverage = source.coverage ?? {};
  return `
    ${shead('Thesis', '')}
    <p class="plede">${esc(source.thesis ?? '')}</p>
    ${shead('Coverage', 'The hostile conditions certified')}
    ${kv(Object.entries(coverage).map(([k, v]) => [k, esc(Array.isArray(v) ? v.join(' · ') : String(v)), true]))}
    ${shead('Suites', `${(source.suites ?? []).length} adversarial suites`)}
    <div class="log">
      ${(source.suites ?? [])
        .map(
          (suite) => `<div class="log__row log__row--bands">
            <span class="mono">${esc(suite.id)}</span>
            <span class="log__title">${esc(suite.title)}<span class="log__id">${esc(suite.passRule ?? '')}</span></span>
            <span class="mono band-range">${esc(suite.count)} fixtures</span>
          </div>`,
        )
        .join('')}
    </div>
    ${specimenTable(source.scenarios ?? [], source.suites)}
    ${section('Acceptance', 'What counts as passing', source.acceptance)}
    ${section('Authority boundary', 'What this proof may and may not certify', source.authorityBoundary)}
    ${dependencyBlock(source.dependencies)}
  `;
}

/* ── Components: live canonical elements ─────────────────────── */

function globalNavigationPanel(source) {
  return `
    <div class="stage stage--nav" data-live-stage>
      <div class="stage__bar"><span>Live component · the real &lt;mez-global-navigation&gt; element</span><span class="mono">canonical module</span></div>
      <div class="navstage">
        <mez-global-navigation selected="aios" home-href="#/item/system/global-navigation"></mez-global-navigation>
      </div>
      <p class="card__note stage__note">Open “Explore systems” to see the Living Registry disclosure — five animated Deep Mineral spheres, the approved bounded exception to the one-live law.</p>
    </div>
    ${shead('Contract', '')}
    ${kv([
      ['Component id', esc(source.componentId), true],
      ['Revision', esc(source.candidateRevision), true],
      ['Task', esc(source.taskId), true],
    ])}
  `;
}

globalNavigationPanel.mount = async () => {
  injectCss('../components/global-navigation/mez-global-navigation.css');
  await import('../components/global-navigation/mez-global-navigation.js');
};

function halftonePanel(source) {
  return `
    <div class="stage" data-live-stage>
      <div class="stage__bar"><span>Live component · the real &lt;mez-halftone-portrait&gt; element</span><span class="mono">canonical module + fixture media</span></div>
      <div class="portraitrow">
        <mez-halftone-portrait src="../components/halftone-portrait/fixtures/media/portrait-a.mp4" label="Halftone portrait, subject A"
          grid-step="4" max-radius="1.8" dot-colour="#212121" background="#ffffff" contrast="1.3" brightness="-0.03"></mez-halftone-portrait>
        <mez-halftone-portrait src="../components/halftone-portrait/fixtures/media/portrait-b.mp4" label="Halftone portrait, subject B"
          grid-step="4" max-radius="1.8" dot-colour="#212121" background="#ffffff" contrast="1.3" brightness="-0.03"></mez-halftone-portrait>
      </div>
      <p class="card__note stage__note">Two portraits shown under the recorded bounded multi-portrait exception; the production default is one.</p>
    </div>
    ${shead('Contract', '')}
    ${kv([
      ['Component id', esc(source.componentId ?? 'mz.systems.component.halftone-portrait'), true],
      ['Revision', esc(source.candidateRevision), true],
    ])}
  `;
}

halftonePanel.mount = async () => {
  injectCss('../components/halftone-portrait/mez-halftone-portrait.css');
  await import('../components/halftone-portrait/mez-halftone-portrait.js');
};

function marqueePanel(source) {
  return `
    <div class="stage" data-live-stage>
      <div class="stage__bar"><span>Live component · the real &lt;mez-testimonial-marquee&gt; element</span><span class="mono">canonical module + frozen fixture</span></div>
      <mez-testimonial-marquee
        src="../components/testimonial-marquee/fixtures/ai-os-testimonials.json"
        label="Operator testimonials for the AI OS"
        presentation="social-caption"></mez-testimonial-marquee>
      <p class="card__note stage__note">Runs from the frozen seven-person fixture with dated follower evidence — the exact policy the approval records.</p>
    </div>
    ${shead('Contract', '')}
    ${kv([
      ['Component id', esc(source.componentId ?? 'mz.systems.component.testimonial-marquee'), true],
      ['Revision', esc(source.candidateRevision), true],
    ])}
  `;
}

marqueePanel.mount = async () => {
  injectCss('../components/testimonial-marquee/mez-testimonial-marquee.css');
  await import('../components/testimonial-marquee/mez-testimonial-marquee.js');
};

/* ── Golden homepage ─────────────────────────────────────────── */

function goldenPanel(source) {
  const sections = source.sections ?? [];
  return `
    ${shead('Regions', `${sections.length} approved regions, in page order`)}
    <div class="log">
      ${sections
        .map(
          (section, index) => `<div class="log__row log__row--bands">
            <span class="mono">${esc(section.id)}</span>
            <span class="log__title">${esc(section.title)}</span>
            <span class="mono band-range">${String(index + 1).padStart(2, '0')}</span>
          </div>`,
        )
        .join('')}
    </div>
    <p class="plede">
      The full page lives at its own address (button above) — it is a complete approved artifact
      with its own motion, and duplicating it here would create a second copy that could drift.
    </p>
  `;
}

/* ── Registry ────────────────────────────────────────────────── */

export const PANELS = {
  colour: { source: '../foundations/colour/colour.source.json', render: colourPanel },
  typography: { source: '../foundations/typography/typography.source.json', render: typographyPanel },
  'space-layout': { source: '../foundations/space-layout/space-layout.source.json', render: spacePanel },
  'geometry-controls': { source: '../foundations/geometry-controls/geometry-controls.source.json', render: geometryPanel },
  disc: { source: '../expressions/disc/disc.source.json', render: discPanel, cores: true },
  sphere: { source: '../expressions/sphere/sphere.source.json', render: spherePanel, cores: true },
  'wings-mark': { source: '../expressions/wings-mark/wings-mark.source.json', render: wingsPanel },
  'product-card': { source: '../expressions/product-card/product-card.source.json', render: productCardPanel },
  'trading-card': {
    source: '../expressions/trading-card/trading-card.source.json',
    render: tradingCardPanel,
    clone: {
      page: '../workbench/expressions/trading-card/',
      css: '../workbench/expressions/trading-card/styles.css',
      selector: '[data-specimen-id]',
      expect: 23,
      scope: 'trading-card',
      heading: 'Every approved specimen',
      note: 'All 23, built by the canonical page itself and adopted here — not redrawn',
      /* The workbench's own review controls belong to its approval flow, not
       * to this console, which has its own. */
      strip: ['[data-verdict]', '.specimen-feedback', '.specimen-verdicts'],
    },
  },
  'channel-motion': { source: '../expressions/channel-motion/channel-motion.source.json', render: channelMotionPanel },
  'stress-proof': { source: '../expressions/stress-proof/expression-stress.source.json', render: stressPanel },
  'global-navigation': { source: '../components/global-navigation/global-navigation.source.json', render: globalNavigationPanel },
  'halftone-portrait': { source: '../components/halftone-portrait/halftone-portrait.source.json', render: halftonePanel },
  'testimonial-marquee': { source: '../components/testimonial-marquee/testimonial-marquee.source.json', render: marqueePanel },
  'golden-homepage': { source: '../golden/homepage/homepage.source.json', render: goldenPanel },
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
  mount.innerHTML = '<p class="card__note">Loading source…</p>';

  /* Canonical stylesheets a panel's specimens depend on, loaded before render
   * so the markup is styled by the real design rather than by the console. */
  for (const href of panel.css ?? []) injectCss(href);

  const source = await loadJson(panel.source);
  if (!source) {
    mount.innerHTML = `<div class="flag">Could not load <code>${esc(panel.source)}</code>.</div>`;
    return;
  }

  /* Some panels load extra canonical data (the product registry) and are async. */
  mount.innerHTML = await panel.render(source);
  mount.insertAdjacentHTML(
    'beforeend',
    `<p class="card__note src">Rendered live from <code>${esc(panel.source.replace(/^\.\.\//, 'brand-kit/'))}</code> —
     the same contract the build and verify scripts read, so this reference cannot drift from the system.</p>`,
  );

  /* Specimens cloned from the canonical page, dropped into the placeholder
   * the panel left for them. */
  if (panel.clone) {
    const slot = mount.querySelector('[data-clone-specimens]');
    if (slot) await mountClonedSpecimens(slot, panel.clone);
  }

  try {
    if (panel.render.mount) await panel.render.mount(mount);
    if (panel.cores || mount.querySelector('[data-mz-core]')) {
      const stage = mount.querySelector('[data-live-stage]') ?? mount;
      await mountCores(stage);
      const modeTag = mount.querySelector('[data-stage-mode]');
      if (modeTag) modeTag.textContent = stage.dataset.coreMode ?? '';
    }
  } catch (error) {
    console.error('[console] panel activation failed', error);
  }
}
