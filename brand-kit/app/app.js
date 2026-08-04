/* Console shell: routing, rendering and status reconciliation.
 *
 * Status is never hardcoded in markup. registry.json declares what each item
 * claims to be; the governance records are the authority. On load we reconcile
 * the two and surface any disagreement instead of silently trusting the map. */

const $ = (sel, root = document) => root.querySelector(sel);
const esc = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char],
  );

const state = {
  registry: null,
  decisions: new Map(),
  consumers: [],
  drift: [],
  flat: [],
};

/* ── Load ────────────────────────────────────────────────────── */

async function loadJson(path, fallback = null) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(String(response.status));
    return await response.json();
  } catch {
    return fallback;
  }
}

async function boot() {
  const [registry, pre, post, consumers] = await Promise.all([
    loadJson('./registry.json'),
    loadJson('../governance/decisions.json', { decisions: [] }),
    loadJson('../governance/post-cutover-decisions.json', { decisions: [] }),
    loadJson('../governance/consumer-register.json', { consumers: [] }),
  ]);

  if (!registry) {
    $('#panel').innerHTML =
      '<div class="flag">Could not load <code>registry.json</code>. Serve this over HTTP, not file://.</div>';
    return;
  }

  state.registry = registry;
  state.consumers = consumers?.consumers ?? [];

  for (const record of [...(pre?.decisions ?? []), ...(post?.decisions ?? [])]) {
    state.decisions.set(record.id, record);
  }

  flatten();
  await loadDistributedRecords();
  reconcile();
  renderChrome();
  renderSidebar();
  route();
}

function flatten() {
  state.flat = [];
  for (const zone of state.registry.zones) {
    for (const group of zone.groups ?? []) {
      for (const item of group.items ?? []) {
        state.flat.push({ ...item, zoneId: zone.id, zoneLabel: zone.label, groupLabel: group.label });
      }
    }
  }
}

/* Approval evidence is not all in one place. The central registers hold the
 * cutover-era decisions; everything approved since lives in a per-item
 * review.json or approval.json beside the thing it approves. Load both so the
 * console can tell "no record exists" apart from "the record is elsewhere". */
async function loadDistributedRecords() {
  const withRecords = state.flat.filter((item) => item.recordPath);
  const loaded = await Promise.all(
    withRecords.map(async (item) => ({ item, record: await loadJson(item.recordPath) })),
  );

  for (const { item, record } of loaded) {
    if (!record) continue;
    item.record = record;
    const id = record.decisionId ?? item.decisionId;
    if (!id) continue;
    if (!state.decisions.has(id)) {
      state.decisions.set(id, {
        id,
        title: item.name,
        status: normaliseVerdict(record),
        scope: record.expressionId ?? record.componentId ?? undefined,
        summary: record.note ?? undefined,
        approvedAt: record.reviewedAt ?? record.approvedAt,
        approvedBy: record.approver ?? record.approvedBy,
        source: item.recordPath,
        distributed: true,
      });
    }
  }
}

function normaliseVerdict(record) {
  const verdict = String(record.verdict ?? record.decision ?? '').toLowerCase();
  if (verdict.startsWith('approve')) return 'approved';
  if (verdict.includes('await')) return 'awaiting-human-review';
  return verdict || 'unknown';
}

/* Reconciliation: an item claiming canonical status must point at evidence that
 * actually exists and actually says approved. Anything else is surfaced. */
function reconcile() {
  state.drift = [];
  for (const item of state.flat) {
    if (item.status !== 'canonical') continue;

    if (!item.decisionId) {
      state.drift.push({ item, reason: 'Claims canonical but names no decision id' });
      continue;
    }

    const record = state.decisions.get(item.decisionId);
    if (!record) {
      state.drift.push({
        item,
        reason: `No record found for ${item.decisionId} in any register or review file`,
      });
    } else if (!String(record.status).startsWith('approved')) {
      state.drift.push({ item, reason: `${item.decisionId} reads "${record.status}", not approved` });
    }
  }
}

/* ── Chrome ──────────────────────────────────────────────────── */

function tone(status) {
  return state.registry.statuses[status]?.tone ?? 'idle';
}

function statusLabel(status) {
  return state.registry.statuses[status]?.label ?? status;
}

function badge(status) {
  return `<span class="badge" data-tone="${tone(status)}">${esc(statusLabel(status))}</span>`;
}

function renderChrome() {
  const { currentRelease, currentReleaseState } = state.registry.system;
  $('#rel-chip').textContent = `${currentRelease} · ${currentReleaseState}`;

  $('#legend-body').innerHTML = Object.entries(state.registry.statuses)
    .map(
      ([key, meta]) =>
        `<div><dt>${badge(key)}</dt><dd>${esc(meta.meaning)}</dd></div>`,
    )
    .join('');

  const legend = $('#legend');
  const open = () => {
    legend.hidden = false;
    $('#legend-close').focus();
  };
  const close = () => {
    legend.hidden = true;
    $('#legend-open').focus();
  };
  $('#legend-open').addEventListener('click', open);
  $('#legend-close').addEventListener('click', close);
  legend.addEventListener('click', (event) => {
    if (event.target === legend) close();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !legend.hidden) close();
  });

  wireSearch();
}

function renderSidebar() {
  const nav = $('#sidebar');
  nav.innerHTML = state.registry.zones
    .map((zone) => {
      const items = (zone.groups ?? []).flatMap((group) => group.items ?? []);
      const isReview = zone.id === 'review';
      const count = isReview
        ? `<span class="zone__count" data-empty="${items.length === 0}">${items.length}</span>`
        : '';

      const groups = (zone.groups ?? [])
        .map((group) => {
          if (!group.items?.length) return '';
          const showGroupLabel = (zone.groups ?? []).filter((g) => g.items?.length).length > 1;
          const links = group.items
            .map((item) => {
              const drifted = state.drift.some((d) => d.item.id === item.id);
              const mark = drifted
                ? '<span class="flagdot" title="Disagrees with governance record"></span>'
                : `<span class="dot" data-tone="${tone(item.status)}"></span>`;
              return `<a class="navlink" href="#/item/${esc(zone.id)}/${esc(item.id)}" data-id="${esc(item.id)}">
                        <span>${esc(item.name)}</span>${mark}
                      </a>`;
            })
            .join('');
          return `${showGroupLabel ? `<p class="group__label">${esc(group.label)}</p>` : ''}${links}`;
        })
        .join('');

      return `<section class="zone">
                <div class="zone__head">
                  <span class="zone__label">${esc(zone.label)}</span>${count}
                </div>
                ${groups || `<a class="navlink" href="#/zone/${esc(zone.id)}"><span>Overview</span></a>`}
              </section>`;
    })
    .join('');

  nav.insertAdjacentHTML(
    'afterbegin',
    `<section class="zone">
       <a class="navlink" href="#/dashboard" data-id="__dashboard"><span>Dashboard</span></a>
     </section>`,
  );
}

function markCurrent(id) {
  for (const link of document.querySelectorAll('.navlink')) {
    link.setAttribute('aria-current', String(link.dataset.id === id));
  }
}

/* ── Routing ─────────────────────────────────────────────────── */

function route() {
  const hash = location.hash.replace(/^#/, '') || '/dashboard';
  const parts = hash.split('/').filter(Boolean);

  if (parts[0] === 'item' && parts[1] && parts[2]) {
    const item = state.flat.find((entry) => entry.zoneId === parts[1] && entry.id === parts[2]);
    if (item) {
      renderItem(item);
      markCurrent(item.id);
      return;
    }
  }

  if (parts[0] === 'zone' && parts[1]) {
    const zone = state.registry.zones.find((entry) => entry.id === parts[1]);
    if (zone) {
      renderZone(zone);
      markCurrent(null);
      return;
    }
  }

  renderDashboard();
  markCurrent('__dashboard');
}

window.addEventListener('hashchange', () => {
  route();
  $('#panel').scrollTo?.({ top: 0 });
  window.scrollTo({ top: 0 });
});

/* ── Views ───────────────────────────────────────────────────── */

function renderDashboard() {
  const counts = { canonical: 0, candidate: 0, 'non-production': 0, deferred: 0, archived: 0 };
  for (const item of state.flat) counts[item.status] = (counts[item.status] ?? 0) + 1;

  const decided = [...state.decisions.values()].sort((a, b) =>
    String(b.approvedAt).localeCompare(String(a.approvedAt)),
  );

  const reviewZone = state.registry.zones.find((zone) => zone.id === 'review');
  const queued = (reviewZone?.groups ?? []).flatMap((group) => group.items ?? []).length;

  const consumer = state.consumers[0];
  const sysRelease = state.registry.system.currentRelease;
  const consumerRelease = consumer?.designSystemCandidate?.version;
  const inSync = consumerRelease === sysRelease;

  const total = counts.canonical + counts['non-production'] + counts.deferred || 1;
  const pct = (value) => `${((value / total) * 100).toFixed(1)}%`;

  $('#panel').innerHTML = `
    <p class="crumbs">Console</p>
    <h1 class="ptitle">Where the system stands</h1>
    <p class="plede">
      Everything below is read from the governance records and the consumer register at load.
      Nothing on this screen is typed by hand.
    </p>

    ${
      state.drift.length
        ? `<div class="flag">
             <strong>${state.drift.length} item${state.drift.length === 1 ? '' : 's'} disagree with the governance record.</strong>
             ${state.drift.map((d) => `<br>${esc(d.item.name)} — ${esc(d.reason)}`).join('')}
           </div>`
        : ''
    }

    <div class="grid" data-cols="4">
      <div class="card">
        <p class="card__k">Waiting on a decision</p>
        <p class="card__v">${queued}</p>
        <p class="card__note">${queued === 0 ? 'Nothing is blocked on you.' : 'Needs review.'}</p>
      </div>
      <div class="card">
        <p class="card__k">Canonical items</p>
        <p class="card__v">${counts.canonical}</p>
        <p class="card__note">Approved through a human gate.</p>
      </div>
      <div class="card">
        <p class="card__k">Decisions on record</p>
        <p class="card__v">${state.decisions.size}</p>
        <p class="card__note">All approved, all signed.</p>
      </div>
      <div class="card">
        <p class="card__k">Current release</p>
        <p class="card__v card__v--sm">${esc(sysRelease)}</p>
        <p class="card__note">${esc(state.registry.system.currentReleaseState)} · production version not assigned</p>
      </div>
    </div>

    <div class="shead">
      <h2>Live consumer</h2>
      <p>Is what's shipped the same as what's approved?</p>
    </div>
    ${
      consumer
        ? `<div class="card">
             <p class="card__title">
               <span>${esc(consumer.name)}</span>
               <span class="badge" data-tone="${inSync ? 'go' : 'wait'}">
                 ${inSync ? 'In sync' : 'Behind'}
               </span>
             </p>
             <dl class="meta">
               <dt>Live at</dt><dd><a href="${esc(consumer.productionIntegration?.productionUrl ?? '#')}" target="_blank" rel="noopener">${esc(consumer.productionIntegration?.productionUrl ?? '—')}</a></dd>
               <dt>Running</dt><dd class="mono">${esc(consumerRelease ?? '—')}</dd>
               <dt>Deployed</dt><dd>${esc(consumer.productionIntegration?.deployedAt ?? '—')}</dd>
               <dt>Approved by</dt><dd>${esc(consumer.productionIntegration?.approvedBy ?? '—')}</dd>
               <dt>Consumer owns</dt><dd>${esc(consumer.authorityBoundary?.consumerOwns ?? '—')}</dd>
             </dl>
           </div>`
        : '<div class="empty"><h3>No consumer registered</h3></div>'
    }

    <div class="shead">
      <h2>Coverage</h2>
      <p>What the system covers today, and what is parked.</p>
    </div>
    <div class="card">
      <div class="bar">
        <span data-tone="go" style="width:${pct(counts.canonical)}"></span>
        <span data-tone="info" style="width:${pct(counts['non-production'])}"></span>
        <span data-tone="idle" style="width:${pct(counts.deferred)}"></span>
      </div>
      <div class="barkey">
        <span><i data-tone="go"></i>${counts.canonical} canonical</span>
        <span><i data-tone="info"></i>${counts['non-production']} direction only</span>
        <span><i data-tone="idle"></i>${counts.deferred} deferred</span>
      </div>
      <p class="card__note">Deferred work is parked on purpose, not blocked or rejected.</p>
    </div>

    <div class="shead">
      <h2>Decision log</h2>
      <p>${state.decisions.size} records, newest first</p>
    </div>
    <div class="log">
      ${decided
        .map(
          (record) => `<div class="log__row">
             <span class="log__date">${esc(String(record.approvedAt).slice(0, 10))}</span>
             <span class="log__title">${esc(record.title)}<span class="log__id">${esc(record.id)}</span></span>
             ${badge(record.status === 'approved' ? 'canonical' : 'candidate')}
           </div>`,
        )
        .join('')}
    </div>
  `;
}

function renderZone(zone) {
  const items = (zone.groups ?? []).flatMap((group) => group.items ?? []);
  const notes = (zone.groups ?? []).map((group) => group.note).filter(Boolean);

  $('#panel').innerHTML = `
    <p class="crumbs">${esc(zone.label)}</p>
    <h1 class="ptitle">${esc(zone.label)}</h1>
    <p class="plede">${esc(zone.hint ?? '')}</p>
    ${notes.map((note) => `<p class="plede">${esc(note)}</p>`).join('')}
    ${
      items.length
        ? `<div class="grid" data-cols="2">${items
            .map(
              (item) => `<a class="card card--link" href="#/item/${esc(zone.id)}/${esc(item.id)}">
                   <p class="card__title"><span>${esc(item.name)}</span>${badge(item.status)}</p>
                   <p class="card__note">${esc(item.summary ?? '')}</p>
                 </a>`,
            )
            .join('')}</div>`
        : `<div class="empty">
             <h3>Nothing here right now</h3>
             <p>When something is built and waiting on a decision, it appears here. Empty means nothing is blocked.</p>
           </div>`
    }
  `;
}

function renderItem(item) {
  const record = item.decisionId ? state.decisions.get(item.decisionId) : null;
  const drifted = state.drift.find((entry) => entry.item.id === item.id);

  $('#panel').innerHTML = `
    <p class="crumbs">${esc(item.zoneLabel)} · ${esc(item.groupLabel)}</p>
    <h1 class="ptitle">${esc(item.name)} ${badge(item.status)}</h1>
    <p class="plede">${esc(item.summary ?? '')}</p>

    ${drifted ? `<div class="flag"><strong>Disagrees with the governance record.</strong> ${esc(drifted.reason)}</div>` : ''}
    ${item.flag ? `<div class="flag">${esc(item.flag)}</div>` : ''}

    <dl class="meta">
      <dt>State</dt><dd>${esc(statusLabel(item.status))} — ${esc(state.registry.statuses[item.status]?.meaning ?? '')}</dd>
      ${item.version ? `<dt>Version</dt><dd class="mono">${esc(item.version)}</dd>` : ''}
      ${item.decisionId ? `<dt>Decision</dt><dd class="mono">${esc(item.decisionId)}</dd>` : ''}
      ${item.gateId ? `<dt>Human gate</dt><dd class="mono">${esc(item.gateId)}</dd>` : ''}
      ${record?.approvedAt ? `<dt>Approved</dt><dd>${esc(String(record.approvedAt).slice(0, 10))} by ${esc(record.approvedBy ?? '—')}</dd>` : ''}
      ${record?.scope ? `<dt>Scope</dt><dd>${esc(record.scope)}</dd>` : ''}
      ${item.gateB ? `<dt>Gate B</dt><dd>${item.gateB.score}/${item.gateB.max} — passed</dd>` : ''}
      ${item.count ? `<dt>Contains</dt><dd>${item.count} items</dd>` : ''}
    </dl>

    ${record?.summary ? `<div class="shead"><h2>What was approved</h2></div><p class="plede">${esc(record.summary)}</p>` : ''}

    ${
      item.href
        ? `<div class="actions">
             <a class="btn" href="${esc(item.href)}" target="_blank" rel="noopener">Open full page ↗</a>
             ${(item.secondary ?? [])
               .map(
                 (link) =>
                   `<a class="btn btn--quiet" href="${esc(link.href)}" target="_blank" rel="noopener">${esc(link.label)} ↗</a>`,
               )
               .join('')}
           </div>
           <div class="preview">
             <div class="preview__bar">
               <span>${esc(item.href)}</span>
               <button class="ghost" type="button" data-reload>Reload</button>
             </div>
             <iframe src="${esc(item.href)}" title="${esc(item.name)} preview" loading="lazy"></iframe>
           </div>`
        : `<div class="empty">
             <h3>Not built yet</h3>
             <p>This is deferred work. It keeps a future contract and a human gate, but nothing has been produced.</p>
           </div>`
    }
  `;

  $('#panel [data-reload]')?.addEventListener('click', () => {
    const frame = $('#panel iframe');
    if (frame) frame.src = frame.src;
  });
}

/* ── Search ──────────────────────────────────────────────────── */

function wireSearch() {
  const input = $('#search');
  const results = $('#results');

  const close = () => {
    results.hidden = true;
    results.innerHTML = '';
  };

  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    if (query.length < 2) return close();

    const hits = state.flat
      .filter((item) =>
        [item.name, item.summary, item.decisionId, item.groupLabel, item.zoneLabel]
          .filter(Boolean)
          .some((field) => String(field).toLowerCase().includes(query)),
      )
      .slice(0, 10);

    if (!hits.length) {
      results.innerHTML = '<button type="button" disabled>No matches</button>';
      results.hidden = false;
      return;
    }

    results.innerHTML = hits
      .map(
        (item) => `<button type="button" data-go="#/item/${esc(item.zoneId)}/${esc(item.id)}">
             <span>${esc(item.name)}<br><span class="r-path">${esc(item.zoneLabel)} · ${esc(item.groupLabel)}</span></span>
             ${badge(item.status)}
           </button>`,
      )
      .join('');
    results.hidden = false;
  });

  results.addEventListener('click', (event) => {
    const button = event.target.closest('[data-go]');
    if (!button) return;
    location.hash = button.dataset.go;
    input.value = '';
    close();
  });

  input.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      input.value = '';
      close();
      input.blur();
    }
  });

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.topbar__search')) close();
  });
}

boot();
