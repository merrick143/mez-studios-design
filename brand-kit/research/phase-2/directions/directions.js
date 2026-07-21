const STORAGE_KEY = 'mez-tr6-direction-review-01';
const ROUTES = {
  a: {
    id: 'DIR-A',
    name: 'Kinetic intelligence',
    thesis: 'Energy earned by product behaviour, decisive scale, and visible movement from request to verified work.',
    behaviours: ['expressive scale', 'bounded product colour', 'product as protagonist', 'semantic motion', 'density contrast', 'specialised family proof', 'small-format product cue']
  },
  b: {
    id: 'DIR-B',
    name: 'Evidence architecture',
    thesis: 'Intelligence made visible through evidence rhythm, accountable routes, and exact state transitions.',
    behaviours: ['evidence rhythm', 'routing geometry', 'verification edge', 'bounded dark section', 'inspectable proof', 'precise hierarchy', 'family evidence objects']
  },
  c: {
    id: 'DIR-C',
    name: 'Human systems editorial',
    thesis: 'Software framed through accountable people, decisions, consequences, and literal system evidence.',
    behaviours: ['editorial typography', 'specific human imagery', 'decision narrative', 'marginal evidence', 'human agency', 'publishing identity', 'channel-native storytelling']
  }
};

const state = {
  route: 'a',
  reviews: loadReviews(),
  sessionId: `TR6-${new Date().toISOString().slice(0,10)}-${Math.random().toString(36).slice(2,8).toUpperCase()}`,
  startedAt: new Date().toISOString()
};

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];

function loadReviews() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
  catch { return {}; }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.reviews));
  $('#review-count').textContent = Object.values(state.reviews).filter(review => review.verdict).length;
}

function saveNote() {
  const note = $('#route-note').value.trim();
  if (!note && !state.reviews[state.route]) return;
  state.reviews[state.route] = {...(state.reviews[state.route] || {}), note};
  save();
}

function renderReview() {
  const route = ROUTES[state.route];
  const review = state.reviews[state.route] || {};
  $('#review-route-name').textContent = route.name.toUpperCase();
  $$('[data-verdict]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.verdict === review.verdict)));
  const selected = review.behaviours || [];
  $('#behaviour-tags').innerHTML = route.behaviours.map(behaviour => `
    <button type="button" data-behaviour="${behaviour}" aria-pressed="${selected.includes(behaviour)}" ${selected.length >= 4 && !selected.includes(behaviour) ? 'disabled' : ''}>${behaviour}</button>`).join('');
  $$('[data-behaviour]').forEach(button => button.addEventListener('click', () => toggleBehaviour(button.dataset.behaviour)));
  $('#route-note').value = review.note || '';
}

function showRoute(routeKey) {
  saveNote();
  state.route = routeKey;
  document.body.dataset.route = routeKey;
  $$('[data-route-panel]').forEach(panel => { panel.hidden = panel.dataset.routePanel !== routeKey; });
  $$('[data-route-tab]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.routeTab === routeKey)));
  $('#review-summary').hidden = true;
  $('#direction-content').hidden = false;
  $('#route-review').hidden = false;
  renderReview();
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function chooseVerdict(verdict) {
  const route = ROUTES[state.route];
  const previous = state.reviews[state.route] || {};
  state.reviews[state.route] = {
    ...previous,
    routeId: route.id,
    routeName: route.name,
    verdict,
    decidedAt: new Date().toISOString()
  };
  save();
  renderReview();
}

function toggleBehaviour(behaviour) {
  const previous = state.reviews[state.route] || {};
  const selected = new Set(previous.behaviours || []);
  if (selected.has(behaviour)) selected.delete(behaviour);
  else if (selected.size < 4) selected.add(behaviour);
  state.reviews[state.route] = {...previous, behaviours: [...selected]};
  save();
  renderReview();
}

function records() {
  return Object.entries(ROUTES).map(([key, route], index) => {
    const review = state.reviews[key] || {};
    return {
      sequence: index + 1,
      routeId: route.id,
      routeName: route.name,
      thesis: route.thesis,
      verdict: review.verdict || null,
      behavioursToKeep: review.behaviours || [],
      note: review.note || '',
      decidedAt: review.decidedAt || null,
      productionAuthority: false
    };
  });
}

function buildExport() {
  const directionRecords = records();
  return {
    schemaVersion: '1.0.0',
    studyId: 'MEZ-TR6-DIRECTION-REVIEW-01',
    sessionId: state.sessionId,
    startedAt: state.startedAt,
    exportedAt: new Date().toISOString(),
    complete: directionRecords.every(record => record.verdict),
    productionAuthority: false,
    sourceExpressionApproved: false,
    records: directionRecords
  };
}

function showSummary() {
  saveNote();
  $('#direction-content').hidden = true;
  $('#route-review').hidden = true;
  $('#review-summary').hidden = false;
  $('#summary-routes').innerHTML = records().map(record => `
    <article class="summary-route">
      <small>${record.routeId}</small>
      <h3>${record.routeName}</h3>
      <strong>${record.verdict || 'Not reviewed'}</strong>
      <p>${record.note || 'No note added.'}</p>
      ${record.behavioursToKeep.length ? `<ul>${record.behavioursToKeep.map(item => `<li>${item}</li>`).join('')}</ul>` : '<p>No behaviours selected to keep.</p>'}
    </article>`).join('');
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function exportRecord() {
  const payload = buildExport();
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `mez-tr6-direction-review-${new Date().toISOString().slice(0,10)}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
  $('#export-status').textContent = payload.complete ? 'Complete direction record exported.' : 'Partial record exported. Review all three routes before synthesis.';
}

async function copyRecord() {
  try {
    await navigator.clipboard.writeText(JSON.stringify(buildExport()));
    $('#export-status').textContent = 'Direction record copied as JSON.';
  } catch {
    $('#export-status').textContent = 'Clipboard unavailable. Use Export direction record.';
  }
}

$$('[data-route-tab]').forEach(button => button.addEventListener('click', () => showRoute(button.dataset.routeTab)));
$$('[data-verdict]').forEach(button => button.addEventListener('click', () => chooseVerdict(button.dataset.verdict)));
$('#route-note').addEventListener('change', saveNote);
$('#open-review').addEventListener('click', showSummary);
$('#back-to-directions').addEventListener('click', () => showRoute(state.route));
$('#export-direction-record').addEventListener('click', exportRecord);
$('#copy-direction-record').addEventListener('click', copyRecord);
document.addEventListener('keydown', event => {
  if (event.target.matches('textarea, input')) return;
  if (event.key === '1') showRoute('a');
  if (event.key === '2') showRoute('b');
  if (event.key === '3') showRoute('c');
});

save();
showRoute('a');
