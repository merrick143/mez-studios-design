import { mountLivingCores } from "../brand-kit/source-pack/design-system-export/mz-core.js";

const PRODUCTS_URL = new URL("../brand-kit/registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../brand-kit/gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE_URL = new URL("../brand-kit/gradient-library/assets/static/", import.meta.url);
const WINGS_URL = new URL("../brand-kit/source-pack/design-system-export/assets/wings.svg", import.meta.url);

const query = new URLSearchParams(location.search);
const forceStatic = query.has("static") || matchMedia("(prefers-reduced-motion: reduce)").matches;
const disableWebGL = query.has("no-webgl");
const VARIANTS = new Set(["registry", "signal", "aperture", "gallery", "console"]);

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

function statusLabel(value) {
  return value === "live" ? "Available now" : "In development";
}

function staticTwin(gradientId) {
  return new URL(`${gradientId.toLowerCase()}.webp`, STATIC_BASE_URL).href;
}

function wingsMarkup(className = "") {
  return `<img class="${className}" src="${WINGS_URL.href}" alt="">`;
}

function arrowIcon() {
  return `<svg viewBox="0 0 20 20" aria-hidden="true" data-directional><path d="M4 10h11m-4-4 4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

function closeIcon() {
  return `<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>`;
}

class MezExploreMenu extends HTMLElement {
  static get observedAttributes() {
    return ["variant"];
  }

  constructor() {
    super();
    this.expanded = false;
    this.activeIndex = 0;
    this.products = [];
    this.renderer = null;
    this.lastFocused = null;
    this.onKeydown = this.onKeydown.bind(this);
  }

  async connectedCallback() {
    this.applyVariant(this.getAttribute("variant") || query.get("variant") || "registry");
    this.setAttribute("data-ready", "false");
    try {
      const [productsResponse, catalogueResponse] = await Promise.all([
        fetch(PRODUCTS_URL),
        fetch(CATALOGUE_URL)
      ]);
      if (!productsResponse.ok) throw new Error(`Product registry failed: ${productsResponse.status}`);
      if (!catalogueResponse.ok) throw new Error(`Living Core catalogue failed: ${catalogueResponse.status}`);

      const registry = await productsResponse.json();
      const catalogue = await catalogueResponse.json();
      this.products = registry.products;
      const selected = this.getAttribute("selected") || "aios";
      this.activeIndex = Math.max(0, this.products.findIndex(product => product.slug === selected));

      this.render();
      this.bindEvents();
      await this.mountCores(catalogue);
      this.setAttribute("data-ready", "true");
    } catch (error) {
      this.renderFailure();
      console.error("[mez-explore-menu] Component initialisation failed.", error);
    }
  }

  disconnectedCallback() {
    document.removeEventListener("keydown", this.onKeydown);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name !== "variant" || oldValue === newValue) return;
    this.applyVariant(newValue);
  }

  applyVariant(value) {
    const variant = VARIANTS.has(value) ? value : "registry";
    this.dataset.variant = variant;
    if (this.shell) {
      this.shell.dataset.mzMode = variant === "gallery" ? "light" : "dark";
      requestAnimationFrame(() => {
        this.renderer?.resize();
        if (this.expanded) this.syncExpandedHeight();
      });
      if (this.expanded) {
        setTimeout(() => {
          this.renderer?.resize();
          this.syncExpandedHeight();
        }, 760);
      }
    }
  }

  render() {
    const familyPips = this.products.map(product => `<i style="--pip-material:url('${staticTwin(product.gradientId)}')"></i>`).join("");
    const systems = this.products.map((product, index) => `
      <button class="system-orb${index === this.activeIndex ? " is-active" : ""}" type="button"
        data-product-index="${index}" data-system="${String(index + 1).padStart(2, "0")}" aria-pressed="${index === this.activeIndex}">
        <span class="system-orb__disc" data-mz-core="${escapeHtml(product.gradientId)}" data-shape="disc">
          ${wingsMarkup("system-orb__wings")}
        </span>
        <span class="system-orb__meta">
          <small>System ${String(index + 1).padStart(2, "0")} · ${statusLabel(product.availability)}</small>
          <strong>${escapeHtml(product.publicName)}</strong>
        </span>
      </button>`).join("");

    this.innerHTML = `
      <button class="menu-scrim" type="button" tabindex="-1" aria-label="Close Explore menu"></button>
      <nav class="explore-shell" data-expanded="false" data-mz-mode="${this.dataset.variant === "gallery" ? "light" : "dark"}" aria-label="Mez Systems product navigation">
        <header class="explore-bar">
          <a class="explore-brand" href="../" aria-label="Mez Systems design home">
            ${wingsMarkup("explore-brand__mark")}
            <span class="explore-brand__name">Mez<br>Systems</span>
          </a>
          <span class="family-ribbon" aria-label="Five Mez Systems products">
            <span class="family-ribbon__pips" aria-hidden="true">${familyPips}</span>
            <span class="family-ribbon__copy"><small>Product family</small><strong>Five operating systems</strong></span>
          </span>
          <div class="explore-actions">
            <button class="mz-control explore-trigger" data-variant="secondary" data-size="compact" type="button" aria-expanded="false">
              <span>Explore</span><b aria-hidden="true">05</b>${arrowIcon()}
            </button>
          </div>
          <button class="mz-control mz-icon-control explore-close" data-variant="primary" type="button" aria-label="Close Explore menu">${closeIcon()}</button>
        </header>

        <div class="explore-body" aria-hidden="true" inert>
          <div class="systems-gallery" aria-label="Five Mez Systems products">${systems}</div>
        </div>
      </nav>`;
  }

  renderFailure() {
    this.innerHTML = `
      <nav class="explore-shell explore-shell--failed" data-mz-mode="dark" aria-label="Mez Systems product navigation">
        <header class="explore-bar">
          <a class="explore-brand" href="../">${wingsMarkup("explore-brand__mark")}<span class="explore-brand__name">Mez<br>Systems</span></a>
          <p>Explore menu unavailable</p>
          <a class="mz-control" data-variant="primary" data-size="compact" href="../brand-kit/product-architecture/">View systems</a>
        </header>
      </nav>`;
  }

  bindEvents() {
    this.shell = this.querySelector(".explore-shell");
    this.body = this.querySelector(".explore-body");
    this.openButton = this.querySelector(".explore-trigger");
    this.closeButton = this.querySelector(".explore-close");
    this.scrim = this.querySelector(".menu-scrim");

    this.openButton.addEventListener("click", () => this.setExpanded(true));
    this.closeButton.addEventListener("click", () => this.setExpanded(false));
    this.scrim.addEventListener("click", () => this.setExpanded(false));
    this.querySelectorAll("[data-product-index]").forEach(button => {
      button.addEventListener("click", () => this.selectProduct(Number(button.dataset.productIndex)));
      button.addEventListener("keydown", event => this.onGalleryKeydown(event));
    });
    document.addEventListener("keydown", this.onKeydown);
  }

  async mountCores(catalogue) {
    const result = await mountLivingCores(this, {
      catalogue,
      selector: ".system-orb__disc[data-mz-core]",
      staticBaseUrl: STATIC_BASE_URL,
      wingsUrl: WINGS_URL,
      forceStatic,
      disableWebGL
    });
    this.renderer = result.renderer;
    this.dataset.coreMode = result.mode;
    this.dataset.coreCount = String(result.count);
    requestAnimationFrame(() => this.renderer.resize());
    document.fonts?.ready.then(() => this.renderer?.resize());
  }

  setExpanded(next) {
    if (this.expanded === next) return;
    this.expanded = next;
    this.lastFocused = next ? document.activeElement : this.lastFocused;
    const startHeight = this.shell.getBoundingClientRect().height;
    this.shell.style.height = `${startHeight}px`;
    this.shell.dataset.expanded = String(next);
    this.openButton.setAttribute("aria-expanded", String(next));
    this.body.setAttribute("aria-hidden", String(!next));
    this.body.inert = !next;
    this.scrim.classList.toggle("is-visible", next);
    document.documentElement.classList.toggle("explore-menu-open", next);

    requestAnimationFrame(() => {
      this.renderer?.resize();
      if (next) this.syncExpandedHeight();
      else this.shell.style.height = `${this.querySelector(".explore-bar").offsetHeight}px`;
    });

    if (next) {
      setTimeout(() => this.closeButton.focus({ preventScroll: true }), 260);
      setTimeout(() => {
        this.renderer?.resize();
        this.syncExpandedHeight();
      }, 760);
    } else {
      setTimeout(() => {
        this.shell.style.height = "";
        (this.lastFocused || this.openButton).focus({ preventScroll: true });
      }, 620);
    }
  }

  selectProduct(index) {
    if (!this.products[index]) return;
    this.activeIndex = index;
    const product = this.products[index];
    this.setAttribute("selected", product.slug);

    this.querySelectorAll("[data-product-index]").forEach((button, buttonIndex) => {
      const isActive = buttonIndex === index;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  syncExpandedHeight() {
    if (!this.expanded) return;
    const targetHeight = Math.min(this.querySelector(".explore-bar").offsetHeight + this.body.scrollHeight, innerHeight - 32);
    this.shell.style.height = `${targetHeight}px`;
  }

  onGalleryKeydown(event) {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    let next = this.activeIndex;
    if (event.key === "ArrowLeft") next = (next - 1 + this.products.length) % this.products.length;
    if (event.key === "ArrowRight") next = (next + 1) % this.products.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = this.products.length - 1;
    this.selectProduct(next);
    this.querySelector(`[data-product-index="${next}"]`).focus();
  }

  onKeydown(event) {
    if (!this.expanded) return;
    if (event.key === "Escape") {
      event.preventDefault();
      this.setExpanded(false);
      return;
    }
    if (event.key !== "Tab") return;
    const focusable = [...this.shell.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')]
      .filter(element => !element.closest("[inert]"));
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
}

if (!customElements.get("mez-explore-menu")) customElements.define("mez-explore-menu", MezExploreMenu);

export { MezExploreMenu };
