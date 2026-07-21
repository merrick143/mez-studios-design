const SPEC_FILES = [
  'specs/pairs-01-04.json',
  'specs/pairs-05-08.json',
  'specs/pairs-09-12.json'
];
const STORAGE_KEY = 'mez-tr5-calibration-round-01';
const DIMENSIONS = {
  'TD-001': 'Recognition resilience',
  'TD-002': 'Restraint to expressiveness',
  'TD-003': 'Editorial to operational density',
  'TD-004': 'Proof literalness',
  'TD-005': 'Family coherence to product distinction',
  'TD-006': 'Motion semantics',
  'TD-007': 'Human control visibility',
  'TD-008': 'Machine portability'
};

const state = {
  pairs: [],
  current: 0,
  decisions: loadDecisions(),
  sessionId: `TR5-${new Date().toISOString().slice(0, 10)}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
  startedAt: new Date().toISOString()
};

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];

function loadDecisions() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
  catch { return {}; }
}

function saveDecisions() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.decisions));
  $('#save-state').textContent = 'SAVED LOCALLY';
  window.setTimeout(() => { $('#save-state').textContent = 'LOCAL SAVE ACTIVE'; }, 900);
}

function escapeHTML(value = '') {
  return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
}

function firstValue(object, keys, fallback = '') {
  for (const key of keys) if (typeof object?.[key] === 'string') return object[key];
  return fallback;
}

function collectRows(content) {
  const arrayEntry = Object.entries(content).find(([, value]) => Array.isArray(value) && value.length);
  if (arrayEntry) {
    return arrayEntry[1].slice(0, 4).map((item, index) => {
      if (typeof item === 'string') return {lead: `${index + 1}`.padStart(2, '0'), detail: item};
      const strings = Object.values(item).filter(value => typeof value === 'string');
      return {lead: strings[0] || `${index + 1}`.padStart(2, '0'), detail: strings.slice(1).join(' · ') || 'Recorded'};
    });
  }
  const objectEntry = Object.entries(content).find(([, value]) => value && typeof value === 'object' && !Array.isArray(value));
  if (objectEntry) {
    return Object.entries(objectEntry[1]).slice(0, 4).map(([key, value]) => ({
      lead: key.replace(/([A-Z])/g, ' $1').replace(/^./, letter => letter.toUpperCase()),
      detail: typeof value === 'string' ? value : JSON.stringify(value)
    }));
  }
  const ignored = new Set(['contentStatus', 'contentId', 'surface', 'eyebrow', 'headline', 'title', 'body', 'supportingText', 'summary', 'action', 'primaryAction', 'secondaryAction']);
  return Object.entries(content)
    .filter(([key, value]) => !ignored.has(key) && typeof value === 'string')
    .slice(0, 4)
    .map(([key, value]) => ({lead: key.replace(/([A-Z])/g, ' $1'), detail: value}));
}

function renderDemo(pair, option) {
  const content = option.copy || pair.constantContent;
  const eyebrow = firstValue(content, ['eyebrow', 'surface', 'contentStatus'], 'MEZ SYSTEMS / CONTROLLED SPECIMEN');
  const headline = firstValue(content, ['headline', 'title', 'currentState', 'recommendation'], pair.title);
  const body = firstValue(content, ['body', 'supportingText', 'summary', 'recommendation', 'nextStep']);
  const action = firstValue(content, ['primaryAction', 'action', 'secondaryAction'], 'Review the evidence');
  const rows = collectRows(content);
  const pairClass = pair.id.toLowerCase();
  const variantClass = option === pair.optionA ? 'variant-a' : 'variant-b';
  const motion = pair.id === 'PAIR-06' ? '<div class="motion-orbit" aria-hidden="true"></div>' : '';
  const machine = pair.id === 'PAIR-08'
    ? `<div class="machine-object"><span>type</span><span>decision.record</span><span>state</span><span>awaiting-review</span><span>owner</span><span>human</span></div>`
    : '';
  const lockup = pair.id === 'PAIR-09'
    ? `<div class="compact-lockup"><span class="parent">MEZ SYSTEMS</span><span class="product">AI OS</span></div>`
    : '';
  const rowMarkup = rows.map(row => `<div class="demo-row"><strong>${escapeHTML(row.lead)}</strong><span>${escapeHTML(row.detail)}</span></div>`).join('');
  return `
    <div class="demo ${pairClass} ${variantClass}">
      <div>
        <p class="demo-eyebrow">${escapeHTML(eyebrow)}</p>
        ${lockup}
        <h3>${escapeHTML(headline)}</h3>
        ${body ? `<p class="demo-body">${escapeHTML(body)}</p>` : ''}
        ${motion}${machine}
        ${rows.length ? `<div class="demo-grid">${rowMarkup}</div>` : ''}
      </div>
      <span class="demo-action">${escapeHTML(action)}</span>
    </div>`;
}

function oneVariableLabel(oneVariable) {
  if (typeof oneVariable === 'string') return oneVariable.replace(/([A-Z])/g, ' $1').replace(/^./, c => c.toUpperCase());
  if (!oneVariable) return 'One controlled visual variable';
  return `${oneVariable.name}: ${oneVariable.optionAValue} compared with ${oneVariable.optionBValue}`;
}

function renderIndex() {
  $('#pair-index').innerHTML = state.pairs.map((pair, index) => {
    const classes = [index === state.current ? 'current' : '', state.decisions[pair.id]?.choice ? 'complete' : ''].filter(Boolean).join(' ');
    return `<li><button type="button" class="${classes}" data-index="${index}" aria-label="Open pair ${index + 1}" ${index === state.current ? 'aria-current="step"' : ''}>${String(index + 1).padStart(2, '0')}</button></li>`;
  }).join('');
  $$('#pair-index button').forEach(button => button.addEventListener('click', () => showPair(Number(button.dataset.index))));
}

function renderDecision() {
  const pair = state.pairs[state.current];
  const decision = state.decisions[pair.id] || {};
  $$('[data-choice]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.choice === decision.choice)));
  $$('.specimen').forEach(specimen => specimen.classList.toggle('is-selected', specimen.dataset.option === decision.choice));
  $$('[data-confidence]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.confidence === decision.confidence)));
  $('#decision-note').value = decision.note || '';
  $('#completion-hint').textContent = decision.choice
    ? `${decision.choice === 'neither' ? 'Neither selected' : `Option ${decision.choice} selected`}${decision.confidence ? ` · ${decision.confidence} confidence` : ' · add confidence if useful'}`
    : 'Choose A, B, or neither to continue.';
}

function showPair(index) {
  state.current = Math.max(0, Math.min(index, state.pairs.length - 1));
  const pair = state.pairs[state.current];
  $('#summary-view').hidden = true;
  $('#pair-view').hidden = false;
  $('#pair-number').textContent = String(state.current + 1).padStart(2, '0');
  $('#dimension-label').textContent = `${pair.dimensionId} / ${DIMENSIONS[pair.dimensionId] || 'Controlled dimension'}`;
  $('#pair-title').textContent = pair.title;
  $('#pair-question').textContent = pair.question;
  $('#stage-a').innerHTML = renderDemo(pair, pair.optionA);
  $('#stage-b').innerHTML = renderDemo(pair, pair.optionB);
  $('#variable-copy').textContent = oneVariableLabel(pair.oneVariable);
  $('#intent-a').textContent = pair.optionA.intent;
  $('#intent-b').textContent = pair.optionB.intent;
  $('#evaluation-copy').textContent = pair.evaluationPrompt;
  $('#research-notes').open = false;
  $('#previous-pair').disabled = state.current === 0;
  $('#next-pair').textContent = state.current === state.pairs.length - 1 ? 'Review →' : 'Next →';
  $('#progress-bar').style.width = `${(Object.values(state.decisions).filter(d => d.choice).length / state.pairs.length) * 100}%`;
  renderIndex();
  renderDecision();
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function choose(choice) {
  const pair = state.pairs[state.current];
  state.decisions[pair.id] = {
    ...state.decisions[pair.id],
    pairId: pair.id,
    dimensionId: pair.dimensionId,
    choice,
    decidedAt: new Date().toISOString()
  };
  saveDecisions();
  renderDecision();
  renderIndex();
  $('#progress-bar').style.width = `${(Object.values(state.decisions).filter(d => d.choice).length / state.pairs.length) * 100}%`;
}

function setConfidence(confidence) {
  const pair = state.pairs[state.current];
  state.decisions[pair.id] = {...state.decisions[pair.id], pairId: pair.id, dimensionId: pair.dimensionId, confidence};
  saveDecisions();
  renderDecision();
}

function recordNote() {
  const pair = state.pairs[state.current];
  state.decisions[pair.id] = {...state.decisions[pair.id], pairId: pair.id, dimensionId: pair.dimensionId, note: $('#decision-note').value.trim()};
  saveDecisions();
}

function buildRecord() {
  return state.pairs.map((pair, index) => ({
    schemaVersion: '1.0.0',
    studyId: 'MEZ-TR5-ROUND-01',
    sessionId: state.sessionId,
    pairId: pair.id,
    sequence: index + 1,
    dimensionId: pair.dimensionId,
    oneVariable: pair.oneVariable,
    choice: state.decisions[pair.id]?.choice || null,
    confidence: state.decisions[pair.id]?.confidence || null,
    comment: state.decisions[pair.id]?.note || '',
    contradictionFlag: state.decisions[pair.id]?.choice === 'neither' || state.decisions[pair.id]?.confidence === 'low',
    decidedAt: state.decisions[pair.id]?.decidedAt || null,
    decisionStatus: 'human-observation-unapproved-for-production'
  }));
}

function renderSummary() {
  recordNote();
  $('#pair-view').hidden = true;
  $('#summary-view').hidden = false;
  const records = buildRecord();
  const decided = records.filter(item => item.choice).length;
  const low = records.filter(item => item.confidence === 'low').length;
  const neither = records.filter(item => item.choice === 'neither').length;
  const notes = records.filter(item => item.comment).length;
  $('#summary-stats').innerHTML = [
    [decided, 'DECISIONS / 12'], [low, 'LOW CONFIDENCE'], [neither, 'NEITHER'], [notes, 'NOTES ADDED']
  ].map(([value, label]) => `<div class="summary-stat"><strong>${value}</strong><span>${label}</span></div>`).join('');
  $('#summary-list').innerHTML = records.map((record, index) => `
    <div class="summary-item">
      <span>${String(index + 1).padStart(2, '0')}</span>
      <button type="button" data-review-index="${index}">${escapeHTML(state.pairs[index].title)}</button>
      <span class="summary-choice">${record.choice ? escapeHTML(record.choice.toUpperCase()) : 'MISSING'}</span>
      <span class="summary-confidence">${escapeHTML(record.confidence || 'No confidence')}</span>
    </div>`).join('');
  $$('[data-review-index]').forEach(button => button.addEventListener('click', () => showPair(Number(button.dataset.reviewIndex))));
  $('#progress-bar').style.width = `${(decided / state.pairs.length) * 100}%`;
  window.scrollTo({top: 0, behavior: 'smooth'});
}

function downloadRecord() {
  const payload = {
    schemaVersion: '1.0.0',
    studyId: 'MEZ-TR5-ROUND-01',
    sessionId: state.sessionId,
    startedAt: state.startedAt,
    exportedAt: new Date().toISOString(),
    productionAuthority: false,
    records: buildRecord()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `mez-tr5-preference-record-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
  $('#export-status').textContent = 'Record exported. Send the JSON file back for synthesis.';
}

async function copyJSONL() {
  const jsonl = buildRecord().map(record => JSON.stringify(record)).join('\n');
  try {
    await navigator.clipboard.writeText(jsonl);
    $('#export-status').textContent = 'JSONL copied to clipboard.';
  } catch {
    $('#export-status').textContent = 'Clipboard was unavailable. Use Export record instead.';
  }
}

async function initialise() {
  try {
    const groups = await Promise.all(SPEC_FILES.map(async file => {
      const response = await fetch(file);
      if (!response.ok) throw new Error(`${file}: ${response.status}`);
      return response.json();
    }));
    state.pairs = groups.flat().sort((a, b) => a.id.localeCompare(b.id));
    if (state.pairs.length !== 12) throw new Error(`Expected 12 pairs, found ${state.pairs.length}`);
    $('#loading').hidden = true;
    showPair(0);
  } catch (error) {
    $('#loading').innerHTML = `<strong>Calibration could not load.</strong><span>${escapeHTML(error.message)}</span><span>Run this folder through a local web server, as described in README.md.</span>`;
  }
}

$$('[data-choice]').forEach(button => button.addEventListener('click', () => choose(button.dataset.choice)));
$$('[data-confidence]').forEach(button => button.addEventListener('click', () => setConfidence(button.dataset.confidence)));
$('#decision-note').addEventListener('change', recordNote);
$('#previous-pair').addEventListener('click', () => { recordNote(); showPair(state.current - 1); });
$('#next-pair').addEventListener('click', () => { recordNote(); state.current === state.pairs.length - 1 ? renderSummary() : showPair(state.current + 1); });
$('#return-to-pairs').addEventListener('click', () => showPair(state.current));
$('#export-json').addEventListener('click', downloadRecord);
$('#copy-jsonl').addEventListener('click', copyJSONL);
document.addEventListener('keydown', event => {
  if (event.target.matches('textarea, input')) return;
  if (event.key.toLowerCase() === 'a') choose('A');
  if (event.key.toLowerCase() === 'b') choose('B');
  if (event.key.toLowerCase() === 'n') choose('neither');
  if (event.key === 'ArrowLeft' && state.current > 0) showPair(state.current - 1);
  if (event.key === 'ArrowRight' && state.current < state.pairs.length - 1) showPair(state.current + 1);
});

initialise();
