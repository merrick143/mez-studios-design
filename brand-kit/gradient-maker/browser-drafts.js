/* Public drafts belong to this browser. The generator has no collection API. */
import { zipBlob } from './zip.js';

const encode = (value) => new TextEncoder().encode(value);
const json = (value) => encode(JSON.stringify(value, null, 2) + '\n');
const escapeHTML = (text) => String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const bytes = (dataURL) => Uint8Array.from(atob(dataURL.split(',')[1]), (c) => c.charCodeAt(0));
const sha256 = async (data) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', data)), (n) => n.toString(16).padStart(2, '0')).join('');
let dbPromise;
let assetsPromise;

function database() {
  if (!dbPromise) dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open('mez-gradient-drafts', 1);
    request.onupgradeneeded = () => request.result.createObjectStore('drafts', { keyPath: 'slug' });
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(new Error('Browser storage is unavailable. Allow site storage to save drafts; you can still download the source PNG.'));
    request.onblocked = () => reject(new Error('Close other Gradient maker tabs and try again.'));
  }).catch((error) => { dbPromise = null; throw error; });
  return dbPromise;
}

async function transaction(mode, operation) {
  const db = await database();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('drafts', mode);
    let result;
    const request = operation(tx.objectStore('drafts'));
    request.onsuccess = () => { result = request.result; };
    tx.oncomplete = () => resolve(result);
    tx.onabort = () => reject(new Error(tx.error?.name === 'QuotaExceededError'
      ? 'This browser has run out of storage. Download your source PNG, free some site storage, then try saving again.'
      : 'This draft could not be saved in your browser. Your existing drafts are unchanged.'));
    tx.onerror = () => {}; // The abort handler reports the durable transaction result.
  });
}

async function required(slug) {
  const row = await transaction('readonly', (store) => store.get(slug));
  if (!row) throw new Error('This draft is no longer in this browser.');
  return row;
}

export async function readBrowserDraft(slug) {
  return required(slug);
}

async function assets() {
  if (!assetsPromise) assetsPromise = Promise.all([
    new URL('./preview-template.html', import.meta.url),
    new URL('../source-pack/design-system-export/mz-core.js', import.meta.url),
    new URL('../source-pack/design-system-export/assets/wings.svg', import.meta.url),
  ].map(async (url) => {
    const response = await fetch(url);
    if (!response.ok) throw new Error('The export assets could not be loaded. Try saving again.');
    return new Uint8Array(await response.arrayBuffer());
  })).catch((error) => { assetsPromise = null; throw error; });
  return assetsPromise;
}

export class BrowserDrafts {
  urls = new Map();
  async list() {
    const rows = await transaction('readonly', (store) => store.getAll());
    return rows.sort((a, b) => b.record.createdAt.localeCompare(a.record.createdAt)).map((row) => ({
      ...this.summary(row), previewUrl: new URL('./draft-preview.html#' + row.slug, import.meta.url).href,
    }));
  }

  summary(row) {
    if (!this.urls.has(row.slug)) {
      this.urls.set(row.slug, {
        sourceUrl: URL.createObjectURL(new Blob([row.files['source.png']], { type: 'image/png' })),
        staticUrl: URL.createObjectURL(new Blob([row.files['static.webp']], { type: 'image/webp' })),
      });
    }
    return { ...row.record, ...this.urls.get(row.slug), slug: row.slug, review: row.review, browserDraft: true };
  }

  async save(request, preview) {
    const slug = 'draft-' + request.requestId.replaceAll('-', '');
    const existing = await transaction('readonly', (store) => store.get(slug));
    if (existing) return this.summary(existing);
    if (!preview) throw new Error('Wait for the preview to finish before saving.');
    if (request.parentSlug) await required(request.parentSlug);
    const name = request.name.trim();
    if (name.length < 2 || name.length > 80) throw new Error('Give this draft a name between 2 and 80 characters.');
    const source = bytes(preview.sourceUrl);
    if (await sha256(source) !== preview.fingerprint) throw new Error('The source could not be verified. Refresh the preview and try again.');
    const [staticResponse, [template, renderer, wings]] = await Promise.all([
      fetch('/api/gradient-maker?action=static', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: 'upload', imageBase64: preview.sourceUrl.split(',')[1], filename: 'source.png' }), cache: 'no-store' }),
      assets(),
    ]);
    if (!staticResponse.ok || !staticResponse.headers.get('content-type')?.startsWith('image/webp')) {
      const failure = await staticResponse.json().catch(() => ({}));
      throw new Error(failure.error || 'The static export could not be created. Try saving again.');
    }
    const candidateId = 'DRAFT-' + request.requestId.slice(0, 8).toUpperCase();
    const core = { ...preview.core, id: candidateId };
    const record = {
      schemaVersion: '1.0.0', candidateId, name, createdAt: new Date().toISOString(),
      status: 'research-only', productionAuthority: false, parentSlug: request.parentSlug || null,
      mode: request.mode, recipe: preview.recipe,
      source: { file: 'source.png', sha256: preview.fingerprint, width: preview.width, height: preview.height, ...preview.origin },
      core, extraction: preview.extraction, environment: preview.environment,
      storage: 'private-browser', promotion: { status: 'not-promoted', requires: ['Separate human review and approved library import', 'Separate product assignment and release when applicable'] },
    };
    const html = new TextDecoder().decode(template).replaceAll('{{NAME}}', escapeHTML(name))
      .replaceAll('{{ID}}', candidateId).replace('{{CORE}}', JSON.stringify(core).replaceAll('<', '\\u003c'));
    const files = {
      'source.png': source, 'static.webp': new Uint8Array(await staticResponse.arrayBuffer()),
      'candidate.json': json(record), 'mz-core.js': renderer, 'wings.svg': wings, 'preview.html': encode(html),
      'README.md': encode(`# ${name}\n\nPrivate research draft ${candidateId}. Not approved or assigned to a product.\n\nServe this folder over local HTTP and open preview.html. source.png owns colour; static.webp preserves its RGB pixels losslessly. The animated Living Core approximates the source.\n\nDrafts are stored in the browser where they were saved. Keep this ZIP as your portable backup. The recipe and recorded NumPy/Pillow versions reproduce composed sources using mesh-source-1. The original upload is retained when supplied.\n\nImport into the canonical library requires a separate human decision.\n`),
    };
    if (record.recipe) files['recipe.json'] = json(record.recipe);
    if (request.mode === 'upload') {
      files['original-upload.bin'] = bytes('data:application/octet-stream;base64,' + request.imageBase64);
      if (await sha256(files['original-upload.bin']) !== preview.origin.originalSha256) throw new Error('The original upload changed. Refresh its preview before saving.');
    }
    const hashes = Object.fromEntries(await Promise.all(Object.entries(files).map(async ([file, data]) => [file, await sha256(data)])));
    files['manifest.json'] = json({ schemaVersion: '1.0.0', productionAuthority: false, files: hashes });
    const row = { slug, record, files, review: null, reviewHistory: [] };
    await transaction('readwrite', (store) => store.add(row));
    return this.summary(row);
  }

  async review({ slug, verdict, note }) {
    if (!['shortlist', 'revise', 'reject'].includes(verdict) || typeof note !== 'string' || note.length > 2000) throw new Error('Choose a review and keep your note under 2000 characters.');
    const db = await database();
    return new Promise((resolve, reject) => {
      // Read and write in one transaction so reviews in another tab cannot be lost.
      const tx = db.transaction('drafts', 'readwrite');
      const store = tx.objectStore('drafts');
      let review;
      const request = store.get(slug);
      request.onsuccess = () => {
        const row = request.result;
        if (!row) { tx.abort(); return; }
        review = { verdict, note: note.trim(), reviewedAt: new Date().toISOString(), productionAuthority: false, promotesCandidate: false };
        row.review = review; row.reviewHistory.push(review); store.put(row);
      };
      tx.oncomplete = () => resolve(review);
      tx.onabort = () => reject(new Error('The review was not saved. Refresh the collection and try again.'));
      tx.onerror = () => {};
    });
  }

  async export(slug) {
    const row = await required(slug);
    const files = { ...row.files };
    if (row.review) {
      files['review.json'] = json(row.review);
      files['review-history.jsonl'] = encode(row.reviewHistory.map((review) => JSON.stringify(review)).join('\n') + '\n');
    }
    const url = URL.createObjectURL(zipBlob(files));
    const link = document.createElement('a'); link.href = url;
    link.download = `${row.record.candidateId.toLowerCase()}.zip`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 60_000);
  }

}
