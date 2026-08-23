/* Shared canvas runtime: URL params in, artboard out.
   Product → gradient assignments are the locked canonical set from
   brand-kit/releases/production-01/1.0.0-rc.2/identity/products.json
   (DEC-PRODUCT-ARCHITECTURE-001). If that registry changes, change this. */

export const GRADIENT_DIR =
  '../../brand-kit/gradient-library/assets/static/';

export const WINGS =
  '../../brand-kit/source-pack/design-system-export/assets/wings.svg';

export const PRODUCTS = {
  'mez': {
    name: 'Mez Systems', gradient: 'mz-g13', kicker: 'MEZ SYSTEMS',
    fn: 'AI operating systems',
    headline: 'The operating systems AI-native businesses run on.',
    summary: 'Own the context, workflows and decisions that make AI useful.',
  },
  'aios': {
    name: 'AI OS', gradient: 'mz-g13', kicker: 'MEZ SYSTEMS · AI OS',
    fn: 'AI Operating System',
    headline: 'One system your whole business runs on.',
    summary: 'Own the context, workflows and decisions that make AI useful.',
  },
  'context-engine': {
    name: 'Context Engine', gradient: 'mz-g12', kicker: 'MEZ SYSTEMS · CONTEXT ENGINE',
    fn: 'Business context system',
    headline: 'Turns the business into context AI can actually use.',
    summary: 'The layer that gives every model the same picture of the work.',
  },
  'ai-ads-system': {
    name: 'AI Ads System', gradient: 'mz-g06', kicker: 'MEZ SYSTEMS · AI ADS SYSTEM',
    fn: 'Advertising operating system',
    headline: 'Advertising as a repeatable system.',
    summary: 'Build, launch and improve advertising without starting over each time.',
  },
  'claude-code-os': {
    name: 'Claude Code OS', gradient: 'mz-g15', kicker: 'MEZ SYSTEMS · CLAUDE CODE OS',
    fn: 'Software-work operating system',
    headline: 'Repeatable software work, start to ship.',
    summary: 'For people building with Claude Code who want the work to compound.',
  },
  'organic-content-os': {
    name: 'Organic Content OS', gradient: 'mz-g20', kicker: 'MEZ SYSTEMS · ORGANIC CONTENT OS',
    fn: 'Organic content operating system',
    headline: 'Ideas, proof and taste, as an operation.',
    summary: 'Turn what you know into a repeatable content operation.',
  },
};

const ALL_CORES = ['mz-g13', 'mz-g12', 'mz-g06', 'mz-g15', 'mz-g20'];

export function params() {
  const q = new URLSearchParams(location.search);
  const productKey = q.get('product') || 'mez';
  const product = PRODUCTS[productKey] || PRODUCTS['mez'];
  return {
    product,
    productKey,
    // ?g=mz-g34 overrides the product gradient for one-off graphics
    gradient: (q.get('g') || product.gradient).toLowerCase(),
    title: q.get('title'),
    sub: q.get('sub'),
    theme: q.get('theme') === 'light' ? 'light' : 'dark',
  };
}

export function gradientUrl(id) {
  return GRADIENT_DIR + id + '.webp';
}

/* The five locked product cores, in registry order. */
export function allCores() {
  return ALL_CORES.slice();
}

export function applyTheme(canvas, theme) {
  canvas.classList.toggle('canvas--light', theme === 'light');
}
