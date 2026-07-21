const MODULE_LABELS = {
  hero: 'Hero and product opening',
  problem: 'Market problem',
  principle: 'Mez Systems principle',
  proof: 'Built-on-ourselves proof',
  'ai-os': 'AI OS product and purchase story',
  systems: 'Product family',
  bundle: 'Future bundle',
  final: 'Final route'
};

const REACTIONS = ['keep', 'change', 'too much', 'too plain', 'not Mez'];
const OVERALL = ['refine this system', 'useful details only', 'rebuild'];
const STORAGE_KEY = 'mezHomepageSynthesisReview01';
const state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"overall":"","note":"","annotations":{}}');
let activeModule = null;

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[character]));

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  updateCount();
}

function buttons(values, selected, attribute) {
  return values.map(value => `<button type="button" ${attribute}="${value}" aria-pressed="${selected === value}">${value}</button>`).join('');
}

function updateCount() {
  const count = (state.overall ? 1 : 0) + (state.note ? 1 : 0) + Object.keys(state.annotations || {}).length;
  $('#feedback-count').textContent = count;
}

function renderOverall() {
  $('[data-overall]').innerHTML = buttons(OVERALL, state.overall, 'data-overall-choice');
}

function renderAnnotations() {
  const entries = Object.entries(state.annotations || {});
  $('#annotation-list').innerHTML = entries.length
    ? entries.map(([module, response]) => `<article><header><small>${MODULE_LABELS[module]}</small><b>${response.reaction}</b></header><p>${escapeHtml(response.note || 'No note')}</p></article>`).join('')
    : '<p class="review-help">No section feedback yet.</p>';
}

function openPanel() {
  $('.review-panel').classList.add('open');
  $('.review-panel').setAttribute('aria-hidden', 'false');
  $('.review-open').setAttribute('aria-expanded', 'true');
}

function closePanel() {
  $('.review-panel').classList.remove('open');
  $('.review-panel').setAttribute('aria-hidden', 'true');
  $('.review-open').setAttribute('aria-expanded', 'false');
}

function openFeedback(module) {
  activeModule = module;
  const response = state.annotations[module] || {};
  $('#feedback-title').textContent = MODULE_LABELS[module];
  $('#dialog-choices').innerHTML = buttons(REACTIONS, response.reaction || '', 'data-reaction');
  $('#feedback-note').value = response.note || '';
  $('#feedback-dialog').showModal();
}

function exportRecord() {
  return {
    schemaVersion: '1.0.0',
    studyId: 'MEZ-HOMEPAGE-SYNTHESIS-01',
    exportedAt: new Date().toISOString(),
    productionAuthority: false,
    sourceExpressionApproved: false,
    sourceReview: 'MEZ-HOMEPAGE-FOUNDATION-STUDIO-01',
    record: {
      overall: state.overall,
      note: state.note,
      annotations: state.annotations,
      productionAuthority: false
    }
  };
}

renderOverall();
renderAnnotations();
$('#review-note').value = state.note || '';
updateCount();

document.addEventListener('click', event => {
  const feedback = event.target.closest('[data-feedback]');
  if (feedback) openFeedback(feedback.dataset.feedback);

  const overall = event.target.closest('[data-overall-choice]');
  if (overall) {
    state.overall = overall.dataset.overallChoice;
    saveState();
    renderOverall();
  }

  const reaction = event.target.closest('[data-reaction]');
  if (reaction) {
    $$('[data-reaction]').forEach(button => button.setAttribute('aria-pressed', String(button === reaction)));
  }

  if (event.target.closest('.review-open')) openPanel();
  if (event.target.closest('.review-close')) closePanel();

  const menu = event.target.closest('.menu-button');
  if (menu) {
    const open = $('.site-nav').classList.toggle('menu-open');
    menu.setAttribute('aria-expanded', String(open));
  }
});

$('#review-note').addEventListener('input', event => {
  state.note = event.target.value;
  saveState();
});

$('#save-feedback').addEventListener('click', event => {
  const selected = $('[data-reaction][aria-pressed="true"]');
  if (!selected) {
    event.preventDefault();
    return;
  }
  state.annotations[activeModule] = {
    reaction: selected.dataset.reaction,
    note: $('#feedback-note').value.trim()
  };
  saveState();
  renderAnnotations();
});

$('#copy-review').addEventListener('click', async () => {
  await navigator.clipboard.writeText(JSON.stringify(exportRecord(), null, 2));
  $('#review-status').textContent = 'Synthesis review JSON copied.';
});

$('#download-review').addEventListener('click', () => {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([JSON.stringify(exportRecord(), null, 2)], {type: 'application/json'}));
  link.download = 'mez-homepage-synthesis-review.json';
  link.click();
  URL.revokeObjectURL(link.href);
  $('#review-status').textContent = 'Synthesis review JSON downloaded.';
});
