import { readBrowserDraft, BrowserDrafts } from './browser-drafts.js';
import { mountLivingCores } from '../source-pack/design-system-export/mz-core.js';

const $ = (id) => document.getElementById(id);
try {
  const slug = location.hash.slice(1);
  const row = await readBrowserDraft(slug);
  const url = URL.createObjectURL(new Blob([row.files['source.png']], { type: 'image/png' }));
  const twin = URL.createObjectURL(new Blob([row.files['static.webp']], { type: 'image/webp' }));
  $('draft-name').textContent = row.record.name;
  document.title = `${row.record.name} · Private gradient draft`;
  $('draft-status').textContent = 'The source owns the colour. The Living Core approximates it in motion.';
  $('draft-source').src = url;
  $('draft-download').href = url;
  $('draft-content').hidden = false;
  $('draft-actions').hidden = false;
  const node = $('draft-core'); node.dataset.mzCore = row.record.candidateId;
  node.style.backgroundImage = `url("${twin}")`;
  const params = new URLSearchParams(location.search);
  const result = await mountLivingCores(document, {
    catalogue: { cores: { candidate: { ...row.record.core, staticTwin: twin } } },
    staticBaseUrl: location.href, wingsUrl: new URL('../source-pack/design-system-export/assets/wings.svg', location.href).href,
    forceStatic: params.has('static'), disableWebGL: params.has('no-webgl'),
  });
  const mode = () => { $('draft-mode').textContent = result.renderer.isStaticMode() ? 'Exact static source' : 'Living Core · animated approximation'; };
  mode(); matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', mode);
  $('draft-export').addEventListener('click', async () => {
    $('draft-export').disabled = true;
    try { await new BrowserDrafts().export(slug); }
    catch (error) { $('draft-status').textContent = error.message; }
    finally { $('draft-export').disabled = false; }
  });
} catch (error) {
  $('draft-status').textContent = 'This draft is not available here. Open it in the browser where it was saved, or use its downloaded package.';
}
