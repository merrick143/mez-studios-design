/* Native foundation panels.
 *
 * These render straight from the same *.source.json that build_*.py compiles
 * into dist/. That is the whole point of converting them: the panel and the
 * tokens cannot disagree, because they are the same file. Nothing here
 * restates a value by hand. */

const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char],
  );

/* ── Colour ──────────────────────────────────────────────────── */

const hexToRgb = (hex) => {
  const clean = String(hex).replace('#', '');
  const full =
    clean.length === 3
      ? clean
          .split('')
          .map((char) => char + char)
          .join('')
      : clean;
  return [0, 2, 4].map((offset) => parseInt(full.slice(offset, offset + 2), 16));
};

/* WCAG 2.1 relative luminance + contrast ratio. Used to actually verify the
 * declared contrast pairs rather than trusting the recorded minimum. */
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
    const family = key.split('.')[0];
    (families[family] ??= []).push([key, hex]);
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

  /* Verify every declared pair against the light-mode resolution. */
  const lightRoles = source.modes?.light?.roles ?? {};
  const pairs = (source.contrastPairs ?? []).map((pair) => {
    const fg = resolve(lightRoles[pair.foreground] ?? pair.foreground);
    const bg = resolve(lightRoles[pair.background] ?? pair.background);
    const ratio = contrast(fg, bg);
    return { ...pair, fg, bg, ratio, pass: ratio >= (pair.minimum ?? 0) };
  });
  const failures = pairs.filter((pair) => !pair.pass);

  return `
    <div class="shead">
      <h2>Contrast verification</h2>
      <p>${pairs.length} declared pairs, recomputed live</p>
    </div>
    ${
      failures.length
        ? `<div class="flag"><strong>${failures.length} pair(s) below the declared minimum.</strong></div>`
        : `<p class="plede">All ${pairs.length} pairs meet their declared minimum. Ratios below are computed
           from the source file at load, not copied from the record.</p>`
    }
    <div class="pairs">
      ${pairs
        .map(
          (pair) => `
        <div class="pair">
          <span class="pair__demo" style="background:${esc(pair.bg)};color:${esc(pair.fg)}">Aa</span>
          <span class="pair__id mono">${esc(pair.id)}</span>
          <span class="pair__ratio mono">${pair.ratio.toFixed(2)}:1</span>
          <span class="badge" data-tone="${pair.pass ? 'go' : 'alert'}">
            ${pair.pass ? 'pass' : 'fail'} · min ${esc(pair.minimum)}
          </span>
        </div>`,
        )
        .join('')}
    </div>

    <div class="shead">
      <h2>Primitives</h2>
      <p>${Object.keys(primitives).length} values · the only place a raw hex is allowed</p>
    </div>
    ${swatches}

    <div class="shead">
      <h2>Modes</h2>
      <p>${Object.keys(source.modes ?? {}).length} modes · roles resolve to primitives</p>
    </div>
    ${modes}
  `;
}

/* ── Typography ──────────────────────────────────────────────── */

function typographyPanel(source) {
  const families = Object.entries(source.families ?? {})
    .map(
      ([id, family]) => `
      <div class="card">
        <p class="card__title"><span>${esc(family.name)}</span><span class="mono">${esc(id)}</span></p>
        <p class="card__note">${esc(family.role ?? '')}</p>
        <dl class="meta">
          <dt>CSS family</dt><dd class="mono">${esc(family.cssFamily)}</dd>
          ${family.version ? `<dt>Version</dt><dd class="mono">${esc(family.version)}</dd>` : ''}
          ${family.sourceUrl ? `<dt>Source</dt><dd><a href="${esc(family.sourceUrl)}" target="_blank" rel="noopener">${esc(family.sourceUrl)}</a></dd>` : ''}
        </dl>
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
          <p class="spec__demo" style="${esc(style)}">${esc(role.usage ?? 'The quick brown fox')}</p>
        </div>`;
    })
    .join('');

  return `
    <div class="shead">
      <h2>Families</h2>
      <p>${Object.keys(source.families ?? {}).length} licensed families</p>
    </div>
    <div class="grid" data-cols="2">${families}</div>

    <div class="shead">
      <h2>Roles</h2>
      <p>${Object.keys(source.roles ?? {}).length} roles · rendered at their real values</p>
    </div>
    ${roles}
  `;
}

/* ── Space & layout ──────────────────────────────────────────── */

function spacePanel(source) {
  const steps = Object.entries(source.space ?? {});
  const widths = Object.entries(source.contentWidths ?? {});
  const maxWidth = Math.max(...widths.map(([, value]) => Number(value) || 0), 1);

  return `
    <div class="shead">
      <h2>Scale</h2>
      <p>Base unit ${esc(source.baseUnit)}px · ${steps.length} steps, drawn at true size</p>
    </div>
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

    <div class="shead">
      <h2>Content widths</h2>
      <p>${widths.length} widths · shown in proportion</p>
    </div>
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

/* ── Geometry & controls ─────────────────────────────────────── */

function geometryPanel(source) {
  const radii = Object.entries(source.radii ?? {});
  const borders = Object.entries(source.borders ?? {});
  const depth = Object.entries(source.depth ?? {});

  return `
    <div class="shead">
      <h2>Radii</h2>
      <p>${radii.length} named radii, drawn at true value</p>
    </div>
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

    <div class="shead">
      <h2>Borders</h2>
      <p>${borders.length} structural widths</p>
    </div>
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

    <div class="shead">
      <h2>Depth</h2>
      <p>${depth.length} levels · the real shadow, not a description</p>
    </div>
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

/* ── Registry ────────────────────────────────────────────────── */

export const PANELS = {
  colour: { source: '../foundations/colour/colour.source.json', render: colourPanel },
  typography: { source: '../foundations/typography/typography.source.json', render: typographyPanel },
  'space-layout': { source: '../foundations/space-layout/space-layout.source.json', render: spacePanel },
  'geometry-controls': {
    source: '../foundations/geometry-controls/geometry-controls.source.json',
    render: geometryPanel,
  },
};
