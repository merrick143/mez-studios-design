import { mountLivingCores } from "../../source-pack/design-system-export/mz-core.js";

/* PC2-B-C04 · Product Feature Bento
 *
 * A bento is a layout contract, not a style. The component owns geometry,
 * surface allocation and the motion budget. The fixture owns content. Product
 * identity is never hardcoded: it resolves from the canonical registry, so a
 * product added or removed reflows the bento with no code change (LAY-09).
 *
 * The rules below are enforced rather than documented. A fixture that asks for
 * two material cells does not render a slightly worse bento; it renders the
 * reason it was rejected. That is deliberate: the pantry rule that multiple live
 * gradient cells fail validation is the same rule the reference study arrived at
 * independently, and the whole premium read depends on it holding.
 */

const PRODUCTS_URL = new URL("../../registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../gradient-library/assets/static/", import.meta.url);
const WINGS_URL = new URL("../../source-pack/design-system-export/assets/wings.svg", import.meta.url);

const JOBS = ["product", "proof", "workflow", "metric", "media", "integration", "quote", "action"];
const SURFACES = ["paper", "muted", "tint", "outline", "recessed", "raised", "dark", "material"];
const MATERIAL_JOBS = ["product", "metric"];

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reduced || query.has("static") || query.has("no-webgl");

const esc = value => String(value).replace(/[&<>'"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[c]);
const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const scaleFor = span => (span >= 6 ? "xl" : span >= 5 ? "l" : span <= 3 ? "s" : "m");

/* One live core across every bento on the page, handed to whichever is most
   visible. Shared at module scope because MOT-01 is a page budget, not a
   per-instance one. */
const shared = { renderer: null, catalogue: null, anchor: null, observer: null, ratios: new Map() };

async function ensureRenderer(host) {
  if (shared.renderer || forceStatic) return;
  const response = await fetch(CATALOGUE_URL);
  if (!response.ok) throw new Error("Living Core catalogue unavailable");
  shared.catalogue = await response.json();
  const mounted = await mountLivingCores(host.ownerDocument, {
    catalogue: shared.catalogue,
    selector: "[data-mz-bento-never]",
    staticBaseUrl: STATIC_BASE
  });
  shared.renderer = mounted.renderer;
}

function unmount(anchor) {
  if (!anchor) return;
  shared.renderer?.surfaces?.delete(anchor);
  anchor.querySelector("canvas[data-mz-core-canvas]")?.remove();
  anchor.removeAttribute("data-mz-core");
}

/* mz-core renders every surface through one shared offscreen framebuffer that it
   caps at 2048 device pixels, with devicePixelRatio clamped to 2. A surface wider
   than 1024 CSS pixels therefore asks drawImage for more source than exists, and
   the remainder arrives as a stretched vertical band with a hard seam where the
   source ran out. Rather than render that, the cell keeps its exact static twin,
   which is the same image without the motion. */
const FRAMEBUFFER_CAP = 2048;
const maxLiveWidth = () => FRAMEBUFFER_CAP / Math.min(devicePixelRatio || 1, 2);

function mount(anchor) {
  if (!shared.renderer || forceStatic || !anchor || shared.anchor === anchor) return;
  const width = anchor.getBoundingClientRect().width;
  if (width > maxLiveWidth()) {
    anchor.dataset.coreSkipped = `surface is ${Math.round(width)}px wide; the renderer framebuffer tops out at ${Math.round(maxLiveWidth())}px`;
    return;
  }
  delete anchor.dataset.coreSkipped;
  unmount(shared.anchor);
  try {
    shared.renderer.mount(anchor, anchor.dataset.gradientId, { shape: "rect", radius: 0.055, profile: "deep" });
    anchor.dataset.mzCore = anchor.dataset.gradientId;
    shared.anchor = anchor;
  } catch (error) {
    anchor.closest("mez-product-feature-bento").dataset.coreFailure = error?.message || "unknown";
  }
}

function observe(anchor) {
  if (forceStatic) return;
  if (!shared.observer) {
    shared.observer = new IntersectionObserver(entries => {
      entries.forEach(entry => shared.ratios.set(entry.target, entry.intersectionRatio));
      const [best] = [...shared.ratios.entries()].sort((a, b) => b[1] - a[1]);
      if (best && best[1] > 0.2) mount(best[0]);
    }, { threshold: [0, 0.2, 0.4, 0.6, 0.8, 1] });
  }
  shared.observer.observe(anchor);
}

/* --- the contract ---------------------------------------------------------
   Returns the list of violations. Empty means the fixture may render. */
export function validate(fixture, cells) {
  const problems = [];
  const columns = fixture.columns ?? 12;

  if (!cells.length) problems.push("a bento must have at least one cell");

  cells.forEach((cell, index) => {
    const at = `cell ${index + 1}`;
    if (!JOBS.includes(cell.job)) problems.push(`${at}: job "${cell.job}" is not one of ${JOBS.join(", ")}`);
    if (cell.surface && !SURFACES.includes(cell.surface)) problems.push(`${at}: surface "${cell.surface}" is not a declared surface`);
    if (!cell.label && !cell.productSlug && cell.figure === undefined) {
      problems.push(`${at}: resolves to no content, which makes it filler`);
    }
    const span = cell.span ?? 3;
    if (span < 1 || span > columns) problems.push(`${at}: span ${span} does not fit ${columns} columns`);
  });

  /* The rule is one colour event, not one material cell. A single continuous band
     running behind every cell and showing through an aperture in each is one
     object seen through many windows, so it spends the same single event that a
     material cell does. Declaring both is the violation, because then there are
     two things competing to be the thing you look at first. */
  const material = cells.filter(cell => cell.surface === "material");
  const events = material.length + (fixture.layer ? 1 : 0);
  if (events > 1) {
    problems.push(
      fixture.layer
        ? `a layer and ${material.length} material cell${material.length === 1 ? "" : "s"}: a bento carries exactly one colour event`
        : `${material.length} material cells: a bento carries exactly one colour event`
    );
  }
  material.forEach(cell => {
    if (!MATERIAL_JOBS.includes(cell.job)) {
      problems.push(`a material cell must be a ${MATERIAL_JOBS.join(" or ")} cell, not ${cell.job}`);
    }
  });
  if (fixture.layer && !fixture.layer.productSlug) {
    problems.push("a layer must name the product whose material it carries");
  }

  if (cells.filter(cell => cell.focal).length > 1) problems.push("a bento may declare at most one focal cell");

  /* LAY-01: three or more identical spans as the shape of the whole bento. Three
     equal cells inside a genuinely uneven grid is fine; three equal cells that
     are the entire grid is the default feature row wearing bento clothing. */
  const spans = cells.map(cell => cell.span ?? 3);
  if (spans.length >= 3 && new Set(spans).size === 1) {
    problems.push(`every cell spans ${spans[0]}: an even grid is not a bento (LAY-01)`);
  }

  return problems;
}

class MezProductFeatureBento extends HTMLElement {
  static observedAttributes = ["fixture"];

  async connectedCallback() {
    this.dataset.ready = "false";
    try {
      const fixtureHref = this.getAttribute("fixture");
      if (!fixtureHref) throw new Error("no fixture attribute");
      const [fixtureResponse, productsResponse] = await Promise.all([
        fetch(new URL(fixtureHref, document.baseURI)),
        fetch(PRODUCTS_URL)
      ]);
      if (!fixtureResponse.ok) throw new Error("bento fixture unavailable");
      if (!productsResponse.ok) throw new Error("canonical product registry unavailable");
      this.fixture = await fixtureResponse.json();
      this.products = (await productsResponse.json()).products;
      this.cells = this.resolveCells();

      const problems = validate(this.fixture, this.cells);
      if (problems.length) return this.renderContractFailure(problems);

      this.render();
      this.bind();
      this.dataset.ready = "true";
      this.dataset.variant = this.fixture.variant || "";
      this.dispatchEvent(new CustomEvent("mez-bento-ready", {
        bubbles: true,
        detail: { variant: this.fixture.variant, cells: this.cells.length }
      }));

      const anchor = this.querySelector("[data-gradient-id]");
      if (anchor && !forceStatic) {
        await ensureRenderer(this).catch(error => { this.dataset.coreFailure = error.message; });
        observe(anchor);
      }
    } catch (error) {
      this.renderFailure(error.message);
    }
  }

  disconnectedCallback() {
    this.querySelectorAll("[data-gradient-id]").forEach(anchor => {
      shared.observer?.unobserve(anchor);
      shared.ratios.delete(anchor);
      if (shared.anchor === anchor) { unmount(anchor); shared.anchor = null; }
    });
  }

  /* Any cell may name a registry slug, not only a product cell. A product cell
     is the product; another job that names a slug is a part of the business that
     a system already serves, and it takes an identity disc rather than the
     bento's one colour event.

     Which default it takes matters. A product cell is titled by the product and
     subtitled by its function. A block cell keeps its own title, which is the
     part of the business, and is subtitled by the system that serves it. Getting
     that the wrong way round prints the block name twice. */
  resolveCells() {
    const source = this.fixture.source === "registry" ? this.registryCells() : this.fixture.cells || [];
    return source.map(cell => {
      if (!cell.productSlug) return cell;
      const product = this.products.find(item => item.slug === cell.productSlug);
      if (!product) throw new Error(`product "${cell.productSlug}" is not in the registry`);
      const isProductCell = cell.job === "product";
      return {
        ...cell,
        label: cell.label ?? product.publicName,
        detail: cell.detail ?? (isProductCell ? product.function : undefined),
        tag: isProductCell ? cell.tag : (cell.tag ?? product.publicName),
        gradientId: product.gradientId,
        availability: isProductCell ? product.availability : cell.availability
      };
    });
  }

  /* Nothing here counts to five. Availability sets the treatment, so the layout
     survives the registry returning a different number of products (LAY-09). */
  registryCells() {
    const template = this.fixture.registryTemplate || {};
    const ordered = [...this.products].sort(
      (a, b) => (a.availability === "live" ? -1 : 0) - (b.availability === "live" ? -1 : 0)
    );
    return ordered.map(product => ({
      job: "product",
      productSlug: product.slug,
      ...(product.availability === "live" ? template.live : template.coming)
    }));
  }

  cellMarkup(cell, index) {
    const span = cell.span ?? 3;
    const surface = cell.surface || "paper";
    const tag = cell.href ? "a" : cell.interactive ? "button" : "article";
    const style = [
      `--span:${span}`,
      cell.rows ? `--rows:${cell.rows}` : "",
      cell.col ? `--col-start:${cell.col}` : "",
      cell.row ? `--row-start:${cell.row}` : "",
      cell.gradientId ? `--material:url('${twin(cell.gradientId)}')` : "",
      cell.materialPosition ? `--material-position:${cell.materialPosition}` : ""
    ].filter(Boolean).join(";");

    const parts = [];
    if (cell.gradientId && surface !== "material" && cell.tokenShape === "bar") {
      parts.push(`<i class="mz-bento__bar" aria-hidden="true"></i>`);
    }
    if (cell.kicker) parts.push(`<p class="mz-bento__kicker">${esc(cell.kicker)}</p>`);

    const body = [];
    /* Wings mark identity where it is the focal event, and are omitted on small
       cells where material already fills the field (ICO-05). */
    if (surface === "material" && span >= 4) body.push(`<img class="mz-bento__wings" src="${WINGS_URL.href}" alt="" />`);
    if (cell.figure !== undefined) body.push(`<span class="mz-bento__figure">${esc(cell.figure)}</span>`);
    /* Disc and label share one line. The disc identifies the material; sitting it
       above the title made it read as a separate ornament rather than as part of
       naming the thing. */
    if (cell.label) {
      const token = cell.gradientId && surface !== "material" && cell.tokenShape !== "bar"
        ? `<i class="mz-bento__disc" aria-hidden="true"></i>` : "";
      body.push(`<p class="mz-bento__title">${token}<span>${esc(cell.label)}</span></p>`);
    }
    if (cell.detail) body.push(`<p class="mz-bento__detail">${esc(cell.detail)}</p>`);
    if (cell.tag) body.push(`<p class="mz-bento__tag"><i aria-hidden="true"></i>${esc(cell.tag)}</p>`);
    /* A cell may hold a list of parts rather than being one part. Rows and chips
       are the same data at two densities: both are plain text and neither is a
       bordered card, so a cell holding them still satisfies LAY-12. */
    if (cell.entries?.length) body.push(this.entriesMarkup(cell));
    parts.push(`<div class="mz-bento__body">${body.join("")}</div>`);
    if (cell.availability === "coming-soon") parts.push(`<span class="mz-bento__availability">In development</span>`);

    const attributes = [
      `class="mz-bento__cell"`,
      `style="${style}"`,
      `data-job="${esc(cell.job)}"`,
      `data-surface="${esc(surface)}"`,
      `data-scale="${cell.scale || scaleFor(span)}"`,
      cell.focal ? `data-focal="true"` : "",
      cell.align ? `data-align="${esc(cell.align)}"` : "",
      cell.presentation ? `data-presentation="${esc(cell.presentation)}"` : "",
      cell.tokenSize ? `data-token="${esc(cell.tokenSize)}"` : "",
      cell.tokenBleed ? `data-token-bleed="true"` : "",
      tag !== "article" ? `data-interactive="true" data-cell-index="${index}"` : "",
      tag === "a" ? `href="${esc(cell.href)}"` : "",
      tag === "button" ? `type="button"` : "",
      surface === "material" && cell.gradientId ? `data-gradient-id="${esc(cell.gradientId)}"` : ""
    ].filter(Boolean).join(" ");

    return `<${tag} ${attributes}>${parts.join("")}</${tag}>`;
  }

  entriesMarkup(cell) {
    const display = cell.entriesDisplay === "chips" ? "chips" : "rows";
    const items = cell.entries.map(entry => {
      const product = entry.productSlug ? this.products.find(item => item.slug === entry.productSlug) : null;
      const covered = product ? `<span class="mz-bento__entry-system">${esc(product.publicName)}</span>` : "";
      return `<li class="mz-bento__entry"${product ? ' data-covered="true"' : ""}><span>${esc(entry.label)}</span>${covered}</li>`;
    });
    return `<ul class="mz-bento__entries" data-display="${display}">${items.join("")}</ul>`;
  }

  render() {
    const columns = this.fixture.columns ?? 12;
    const label = this.fixture.label ? ` aria-label="${esc(this.fixture.label)}"` : "";
    /* The layer is one material object behind every cell. Each cell reveals it
       through an aperture along its base, and because the cells share one
       background image the strips line up into a single continuous band. */
    const layer = this.fixture.layer
      ? this.products.find(item => item.slug === this.fixture.layer.productSlug)
      : null;
    const layerAttributes = layer
      ? ` data-layer="true" data-gradient-id="${esc(layer.gradientId)}" style="--bento-columns:${columns};--material:url('${twin(layer.gradientId)}')"`
      : ` style="--bento-columns:${columns}"`;
    const frame = this.fixture.frame === "none" ? ' data-frame="none"' : "";
    this.innerHTML = `<div class="mz-bento"${frame}><div class="mz-bento__grid"${layerAttributes}${label}>${
      this.cells.map((cell, index) => this.cellMarkup(cell, index)).join("")
    }</div></div>`;
  }

  bind() {
    this.querySelectorAll("[data-cell-index]").forEach(node => {
      node.addEventListener("click", () => {
        const cell = this.cells[Number(node.dataset.cellIndex)];
        this.dispatchEvent(new CustomEvent("mez-bento-cell-activate", {
          bubbles: true,
          detail: { job: cell.job, label: cell.label, productSlug: cell.productSlug ?? null }
        }));
      });
    });
  }

  renderContractFailure(problems) {
    this.dataset.contractFailure = problems.join(" | ");
    this.innerHTML = `<div class="mz-bento"><div class="mz-bento__failure"><strong>This bento does not satisfy the layout contract.</strong>${
      problems.map(problem => `<span>${esc(problem)}</span>`).join("<br />")
    }</div></div>`;
    this.dispatchEvent(new CustomEvent("mez-bento-contract-failure", { bubbles: true, detail: { problems } }));
  }

  renderFailure(message) {
    this.dataset.failure = message;
    this.innerHTML = `<div class="mz-bento"><div class="mz-bento__failure"><strong>Bento unavailable.</strong><span>${esc(message)}</span></div></div>`;
  }
}

if (!customElements.get("mez-product-feature-bento")) {
  customElements.define("mez-product-feature-bento", MezProductFeatureBento);
}

export { MezProductFeatureBento, JOBS, SURFACES };
