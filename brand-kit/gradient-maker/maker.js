import { mountLivingCores } from '../source-pack/design-system-export/mz-core.js';

const $ = (id) => document.getElementById(id);
const params = new URLSearchParams(location.search);
// Per-page QA modes exercise the shared renderer without changing OS settings.
if (params.has('qa-strip')) document.documentElement.classList.add('qa-strip');
if (params.has('qa-reduced')) {
  const originalMatchMedia = window.matchMedia.bind(window);
  window.matchMedia = (query) => {
    const media = originalMatchMedia(query);
    if (query !== '(prefers-reduced-motion: reduce)') return media;
    return new Proxy(media, { get(target, key) {
      if (key === 'matches') return true;
      const value = Reflect.get(target, key, target);
      return typeof value === 'function' ? value.bind(target) : value;
    } });
  };
}
const state = {
  mode: 'compose', recipe: null, selectedPoint: 0, upload: null, presets: null,
  renderer: null, preview: null, revision: 0, renderedRevision: -1,
  timer: null, controller: null, online: false, saving: false,
  requestId: crypto.randomUUID(), parentSlug: null, saved: false,
  candidates: [], comparison: new Set(), reviewSlug: null, shape: 'sphere',
};
const labels = { shortlist: 'Shortlisted', revise: 'Needs changes', reject: 'Rejected' };

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

async function api(action, payload, signal) {
  const response = await fetch(`/api/gradient-maker/${action}`, {
    method: payload === undefined ? 'GET' : 'POST',
    headers: payload === undefined ? {} : { 'Content-Type': 'application/json' },
    body: payload === undefined ? undefined : JSON.stringify(payload),
    cache: 'no-store', signal,
  });
  let result;
  try { result = await response.json(); }
  catch { throw new Error('The local maker is unavailable. Open the setup instructions above to start it.'); }
  if (!response.ok) throw new Error(result.error || 'The operation could not be completed. Try again.');
  return result;
}

function status(message, error = false) {
  $('preview-status').textContent = message;
  $('preview-status').classList.toggle('error', error);
}

function updateSave() {
  $('save').disabled = !state.online || state.saving || state.saved || state.renderedRevision !== state.revision;
  $('save').textContent = state.saving ? 'Saving this version…' : state.saved ? 'Version saved ✓' : state.parentSlug ? 'Save a new version →' : 'Save candidate →';
}

function payload() {
  return state.mode === 'compose'
    ? { mode: 'compose', recipe: structuredClone(state.recipe) }
    : { mode: 'upload', ...state.upload };
}

function changed(delay = 450) {
  state.revision++;
  state.saved = false;
  state.requestId = crypto.randomUUID();
  state.controller?.abort();
  clearTimeout(state.timer);
  $('compare-source').disabled = true;
  $('inspect-source').disabled = true;
  $('download-source').hidden = true;
  updateSave();
  if (!state.online) return;
  if (state.mode === 'upload' && !state.upload) {
    status('Choose an image to build its preview.');
    return;
  }
  status(state.preview ? 'Updating… the previous preview is shown until this version is ready.' : 'Creating the source and extracting its colours…');
  state.timer = setTimeout(refreshPreview, delay);
}

function normaliseCore(raw, staticUrl) {
  const rgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255);
  return {
    id: 'draft', file: staticUrl,
    anchors: raw.anchors.map((a) => ({ colour: rgb(a.hex), pos: a.pos, weight: a.weight })),
    shade: rgb(raw.shade), bloom: rgb(raw.bloom),
    bloomSelect: [0, 1, 2, 3].map((i) => i === raw.bloomAnchor ? 1 : 0),
  };
}

function shapeOptions() {
  return { shape: ['card', 'pill'].includes(state.shape) ? 'rect' : state.shape, radius: state.shape === 'pill' ? 0.5 : state.shape === 'card' ? 0.08 : 0 };
}

async function renderPreview(data, revision) {
  const core = $('live-core');
  if (!state.mountPromise) {
    core.dataset.mzCore = 'draft';
    state.mountPromise = mountLivingCores(document.createDocumentFragment(), {
      catalogue: { cores: { draft: { ...data.core, id: 'draft', staticTwin: data.staticUrl } } },
      staticBaseUrl: location.href,
      wingsUrl: new URL('../source-pack/design-system-export/assets/wings.svg', location.href).href,
      forceStatic: params.has('static'), disableWebGL: params.has('no-webgl'),
    }).then((result) => {
      state.renderer = result.renderer;
      // Opt-in observation only: count the real shared renderer's draw calls.
      if (params.has('qa') && state.renderer.gl) {
        const gl = state.renderer.gl;
        const draw = gl.drawArrays.bind(gl);
        let count = 0;
        gl.drawArrays = (...args) => { core.dataset.drawCalls = String(++count); return draw(...args); };
      }
      const observer = new MutationObserver(() => {
        $('render-mode').textContent = core.dataset.mzCoreMode === 'live' ? 'Live animation' : 'Exact static source';
      });
      observer.observe(core, { attributes: true, attributeFilter: ['data-mz-core-mode'] });
      return state.renderer;
    });
  }
  await state.mountPromise;
  if (revision !== state.revision) return;
  state.renderer.cores.set('draft', normaliseCore(data.core, data.staticUrl));
  const options = shapeOptions();
  if (state.renderer.surfaces.has(core)) {
    state.renderer.setCore(core, 'draft');
    state.renderer.setShape(core, options.shape, options.radius);
  } else state.renderer.mount(core, 'draft', options);
  state.renderer.resize();
  $('render-mode').textContent = core.dataset.mzCoreMode === 'live' ? 'Live animation' : 'Exact static source';
  $('stage-loading').hidden = true;
  $('stage').setAttribute('aria-busy', 'false');
}

async function refreshPreview() {
  const revision = state.revision;
  if (!$('maker-form').checkValidity()) {
    status('Check the highlighted colour, position or name before continuing.', true);
    return;
  }
  const controller = new AbortController();
  state.controller = controller;
  try {
    const data = await api('preview', payload(), controller.signal);
    if (revision !== state.revision) return;
    await renderPreview(data, revision);
    if (revision !== state.revision) return;
    state.preview = data;
    state.renderedRevision = revision;
    $('source-image').src = data.sourceUrl;
    $('source-image').hidden = false;
    $('source-image').alt = state.mode === 'upload' ? 'Normalised uploaded source image' : 'Authored gradient source';
    if (state.sourceObjectUrl) URL.revokeObjectURL(state.sourceObjectUrl);
    const sourceBytes = Uint8Array.from(atob(data.sourceUrl.split(',')[1]), (character) => character.charCodeAt(0));
    state.sourceObjectUrl = URL.createObjectURL(new Blob([sourceBytes], { type: 'image/png' }));
    $('download-source').href = state.sourceObjectUrl;
    $('download-source').hidden = false;
    $('source-info').textContent = `${data.width} × ${data.height}px · ${state.mode === 'compose' ? 'Reproducible colour recipe' : 'Original upload retained on save'}. The animation approximates this source.`;
    $('compare-source').disabled = false;
    $('inspect-source').disabled = false;
    $('source-hash').textContent = `Source SHA-256: ${data.fingerprint}`;
    $('extracted-colours').replaceChildren(...data.core.anchors.map((anchor) => {
      const item = element('span', '', anchor.hex);
      const swatch = element('i'); swatch.style.background = anchor.hex; item.prepend(swatch);
      item.title = `${Math.round(anchor.sourceShare * 100)}% of the source`;
      return item;
    }));
    status('Ready to compare or save. Every preview comes from its source PNG.');
    updateSave();
  } catch (error) {
    if (error.name === 'AbortError' || revision !== state.revision) return;
    status(error.message, true);
    $('stage-loading').hidden = Boolean(state.preview);
    if (!state.preview) $('stage-loading').textContent = 'Adjust the source to continue.';
    updateSave();
  }
}

function selectPoint(index) {
  state.selectedPoint = index;
  document.querySelectorAll('.point-select').forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
  const point = state.recipe.points[index];
  $('point-title').textContent = `Colour ${index + 1} · position & strength`;
  $('point-x').value = Math.round(point.x * 100);
  $('point-y').value = Math.round(point.y * 100);
  $('point-weight').value = point.weight;
  $('weight-value').value = point.weight.toFixed(2);
}

function drawControls() {
  $('colours').replaceChildren(...state.recipe.points.map((point, index) => {
    const row = element('div', 'colour-row');
    const button = element('button', 'point-select', String(index + 1));
    button.type = 'button'; button.setAttribute('aria-label', `Edit colour ${index + 1} position`);
    button.addEventListener('click', () => selectPoint(index));
    const colour = element('input'); colour.type = 'color'; colour.value = point.hex;
    colour.setAttribute('aria-label', `Colour ${index + 1} picker`);
    const hex = element('input'); hex.type = 'text'; hex.value = point.hex; hex.pattern = '#[0-9a-fA-F]{6}'; hex.required = true;
    hex.maxLength = 7; hex.spellcheck = false; hex.setAttribute('aria-label', `Colour ${index + 1} hex`);
    colour.addEventListener('input', () => { point.hex = colour.value.toUpperCase(); hex.value = point.hex; changed(); });
    hex.addEventListener('input', () => {
      if (hex.checkValidity()) { point.hex = hex.value.toUpperCase(); colour.value = point.hex; }
      changed();
    });
    row.append(button, colour, hex); return row;
  }));
  $('softness').value = Math.round(state.recipe.softness * 100);
  $('softness-value').value = `${$('softness').value}%`;
  $('flow').value = Math.round(state.recipe.flow * 100);
  $('flow-value').value = `${$('flow').value}%`;
  $('seed').value = state.recipe.seed;
  selectPoint(Math.min(state.selectedPoint, state.recipe.points.length - 1));
}

function useStarter() {
  const preset = state.presets.presets[Number($('starter').value)];
  state.recipe = { version: state.presets.version, seed: 7, softness: 0.45, flow: 0.35,
    points: preset.colours.map((hex, i) => ({ hex, x: state.presets.positions[i][0], y: state.presets.positions[i][1], weight: 1 })) };
  state.parentSlug = null;
  $('candidate-name').value = `${preset.name} exploration`;
  $('preview-name').textContent = $('candidate-name').value;
  $('save-context').textContent = 'Saves a local version for review. Your approved library stays unchanged.';
  drawControls(); changed();
}

function switchMode(mode) {
  state.mode = mode;
  document.querySelectorAll('[data-mode]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.mode === mode)));
  $('compose-controls').hidden = mode !== 'compose';
  $('upload-controls').hidden = mode !== 'upload';
  // Hidden source inputs must not block the other creation method.
  $('compose-controls').querySelectorAll('input,button,select').forEach((input) => { input.disabled = mode !== 'compose'; });
  $('source-upload').disabled = mode !== 'upload';
  changed(0);
}

async function fileData(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(',')[1]);
    reader.onerror = () => reject(new Error('The file could not be read. Choose it again.'));
    reader.readAsDataURL(file);
  });
}

function figure(url, caption, detail) {
  const item = element('figure'); const img = element('img'); img.src = url; img.alt = caption;
  item.append(img, element('figcaption', '', caption), element('p', '', detail)); return item;
}

function compareSource() {
  if (!state.preview) return;
  const canvas = $('live-core').querySelector('canvas');
  const live = $('live-core').dataset.mzCoreMode === 'live';
  const frame = live && canvas ? canvas.toDataURL('image/png') : state.preview.staticUrl;
  $('compare-title').textContent = 'Source & expression';
  $('compare-content').replaceChildren(
    figure(state.preview.sourceUrl, 'Source PNG', 'The colour authority. The static WebP preserves these pixels losslessly.'),
    figure(frame, live ? 'Living Core · captured frame' : 'Exact static fallback', live ? 'A still from the current animated expression, without the Wings overlay. The composition is a parametric approximation.' : 'Motion is disabled or unavailable. The exact source is used as the fallback.'),
  );
  $('compare-dialog').showModal();
}

function updateComparison() {
  $('compare-saved').textContent = `Compare selected (${state.comparison.size}/2)`;
  $('compare-saved').disabled = state.comparison.size !== 2;
  document.querySelectorAll('.candidate>input').forEach((box) => { box.disabled = state.comparison.size === 2 && !box.checked; });
}

function drawCollection() {
  const filter = $('review-filter').value;
  const rows = state.candidates.filter((row) => filter === 'all' || (row.review?.verdict || 'unreviewed') === filter);
  $('collection').replaceChildren(...rows.map((row) => {
    const item = element('article', 'candidate');
    const checkbox = element('input'); checkbox.type = 'checkbox'; checkbox.checked = state.comparison.has(row.slug);
    checkbox.setAttribute('aria-label', `Compare ${row.name}`);
    checkbox.addEventListener('change', () => { checkbox.checked ? state.comparison.add(row.slug) : state.comparison.delete(row.slug); updateComparison(); });
    const image = element('img'); image.src = row.staticUrl; image.alt = ''; image.loading = 'lazy';
    const info = element('div');
    info.append(element('h3', '', row.name), element('p', 'meta', `${row.candidateId} · ${labels[row.review?.verdict] || 'Unreviewed'} · ${new Date(row.createdAt).toLocaleDateString('en-AU')}`));
    if (row.parentSlug) info.append(element('p', 'meta', 'Refined from a saved candidate'));
    const actions = element('div', 'candidate-actions');
    const load = element('button', 'quiet-button', 'Load version'); load.type = 'button'; load.addEventListener('click', () => loadCandidate(row, load));
    const review = element('button', 'quiet-button', 'Review'); review.type = 'button'; review.addEventListener('click', () => {
      state.reviewSlug = row.slug; $('review-title').textContent = `Review ${row.name}`;
      $('verdict').value = row.review?.verdict || 'shortlist'; $('review-note').value = row.review?.note || '';
      $('review-error').textContent = ''; $('review-dialog').showModal();
    });
    const download = element('a', '', 'Export package ↓'); download.href = row.exportUrl;
    const preview = element('a', '', 'Open preview ↗'); preview.href = row.previewUrl; preview.target = '_blank'; preview.rel = 'noopener';
    actions.append(load, review, download, preview); item.append(checkbox, image, info, actions); return item;
  }));
  if (!rows.length) $('collection').append(element('p', 'empty', state.candidates.length ? 'No candidates match this review filter.' : 'Save your first candidate to start a collection.'));
  updateComparison();
}

async function refreshCollection() {
  try {
    const result = await api('candidates'); state.candidates = result.candidates;
    state.comparison = new Set([...state.comparison].filter((slug) => state.candidates.some((row) => row.slug === slug)));
    drawCollection();
  } catch (error) { $('collection').replaceChildren(element('p', 'empty', error.message)); }
}

async function loadCandidate(row, button) {
  if (state.saving) return;
  button.disabled = true;
  try {
    if (row.recipe) {
      state.recipe = structuredClone(row.recipe); drawControls(); switchMode('compose');
    } else {
      const response = await fetch(row.sourceUrl, { cache: 'no-store' });
      if (!response.ok) throw new Error('This source is unavailable. Refresh the collection and try again.');
      state.upload = { imageBase64: await fileData(await response.blob()), filename: `${row.candidateId}-source.png` };
      $('upload-name').textContent = `Source from ${row.name}. Its original upload remains with the earlier version.`;
      switchMode('upload');
    }
    state.parentSlug = row.slug;
    $('candidate-name').value = row.name;
    $('preview-name').textContent = row.name;
    $('save-context').textContent = `Refining ${row.candidateId}. Saving creates a new version and keeps the original.`;
    $('editor').scrollIntoView({ behavior: 'instant' });
    $('candidate-name').focus({ preventScroll: true });
  } catch (error) { status(error.message, true); }
  finally { button.disabled = false; }
}

$('maker-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if ($('save').disabled || !$('maker-form').reportValidity()) return;
  const revision = state.revision;
  const request = { ...payload(), name: $('candidate-name').value, requestId: state.requestId, parentSlug: state.parentSlug };
  state.saving = true; updateSave();
  try {
    const result = await api('save', request);
    if (revision === state.revision && request.name === $('candidate-name').value) {
      state.saved = true; state.parentSlug = result.candidate.slug;
      $('save-context').textContent = `${result.candidate.candidateId} saved locally. Edit to create another version.`;
    }
    status(`${result.candidate.name} saved as ${result.candidate.candidateId}. It is available in your local collection.`);
    await refreshCollection();
  } catch (error) { status(error.message, true); }
  finally { state.saving = false; updateSave(); }
});

$('candidate-name').addEventListener('input', () => {
  $('preview-name').textContent = $('candidate-name').value || 'Untitled candidate';
  state.saved = false; state.requestId = crypto.randomUUID(); updateSave();
  // A formerly invalid name may have prevented the initial extraction.
  if (state.renderedRevision !== state.revision && $('maker-form').checkValidity()) changed();
});
document.querySelectorAll('[data-mode]').forEach((button) => button.addEventListener('click', () => switchMode(button.dataset.mode)));
$('starter').addEventListener('change', useStarter);
$('reset-palette').addEventListener('click', useStarter);
for (const axis of ['x', 'y']) $('point-' + axis).addEventListener('input', (event) => {
  if (event.target.value !== '' && event.target.checkValidity()) state.recipe.points[state.selectedPoint][axis] = Number(event.target.value) / 100;
  changed();
});
$('point-weight').addEventListener('input', (event) => {
  state.recipe.points[state.selectedPoint].weight = Number(event.target.value);
  $('weight-value').value = Number(event.target.value).toFixed(2); changed();
});
for (const key of ['softness', 'flow']) $(key).addEventListener('input', (event) => {
  state.recipe[key] = Number(event.target.value) / 100; $(key + '-value').value = `${event.target.value}%`; changed();
});
$('seed').addEventListener('input', (event) => { state.recipe.seed = Number(event.target.value); changed(); });
$('remix').addEventListener('click', () => {
  state.recipe.seed = (state.recipe.seed + 1) % 1000000;
  $('seed').value = state.recipe.seed; changed(0);
});
$('source-upload').addEventListener('change', async (event) => {
  const file = event.target.files[0]; if (!file) return;
  state.upload = null; changed();
  const revision = state.revision;
  try {
    if (file.size > 12 * 1024 * 1024 || !['image/png', 'image/jpeg'].includes(file.type)) throw new Error('Choose a PNG or JPEG under 12 MB.');
    const imageBase64 = await fileData(file);
    if (revision !== state.revision) return;
    state.upload = { imageBase64, filename: file.name };
    $('upload-name').textContent = file.name;
    state.parentSlug = null;
    $('save-context').textContent = 'The original upload, source PNG and extracted core are retained in this version.';
    changed(0);
  } catch (error) { status(error.message, true); }
});
document.querySelectorAll('.shape-bar [data-shape]').forEach((button) => button.addEventListener('click', () => {
  state.shape = button.dataset.shape;
  document.querySelectorAll('.shape-bar button').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  $('live-core').dataset.shape = state.shape;
  if (state.renderer) { const options = shapeOptions(); state.renderer.setShape($('live-core'), options.shape, options.radius); state.renderer.resize(); }
}));
$('show-wings').addEventListener('change', (event) => $('live-core').classList.toggle('no-wings', !event.target.checked));
$('surface-toggle').addEventListener('click', () => {
  const dark = $('stage').dataset.mzMode === 'dark';
  $('stage').dataset.mzMode = dark ? 'light' : 'dark';
  $('surface-toggle').textContent = dark ? 'Dark surface' : 'Light surface';
});
$('compare-source').addEventListener('click', compareSource);
$('inspect-source').addEventListener('click', compareSource);
document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => $(button.dataset.close).close()));
$('refresh').addEventListener('click', refreshCollection);
$('review-filter').addEventListener('change', drawCollection);
$('compare-saved').addEventListener('click', () => {
  const rows = state.candidates.filter((row) => state.comparison.has(row.slug));
  if (rows.length !== 2) return;
  $('compare-title').textContent = 'Compare candidates';
  $('compare-content').replaceChildren(...rows.map((row) => figure(row.staticUrl, row.name, `${row.candidateId} · Exact source twin · ${labels[row.review?.verdict] || 'Unreviewed'}`)));
  $('compare-dialog').showModal();
});
$('review-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const button = event.submitter; button.disabled = true;
  try {
    await api('review', { slug: state.reviewSlug, verdict: $('verdict').value, note: $('review-note').value });
    $('review-dialog').close(); await refreshCollection();
  } catch (error) { $('review-error').textContent = error.message; }
  finally { button.disabled = false; }
});

async function start() {
  try {
    const [presets, connection] = await Promise.all([
      fetch('./presets.json').then((response) => { if (!response.ok) throw new Error('Starting palettes could not be loaded. Reload the page.'); return response.json(); }),
      api('status'),
    ]);
    state.presets = presets; state.online = connection.local === true;
    $('starter').replaceChildren(...presets.presets.map((preset, i) => {
      const option = element('option', '', preset.name); option.value = i; return option;
    }));
    $('connection').classList.add('ready'); useStarter(); await refreshCollection();
  } catch (error) {
    $('connection').classList.add('error');
    $('connection').replaceChildren(document.createTextNode('This editor needs the updated local maker server. '));
    const help = element('a', '', 'Open setup instructions'); help.href = './README.md'; $('connection').append(help);
    status(error.message, true); $('stage-loading').textContent = 'Start the local maker to preview a gradient.';
    $('maker-form').querySelectorAll('input,button,select').forEach((input) => { input.disabled = true; });
  }
}
start();
