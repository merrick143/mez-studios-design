/**
 * Mez Systems · Product Card 02 · Phase B · PB2 Round 04 convergence.
 *
 * The commercial values in this file are review fixtures. They are deliberately
 * local, illustrative and disconnected from payments, tax, inventory or network
 * services. Canonical product identity continues to come from products.json.
 */
import { phaseALineageFor } from "./phase-a-lineage.js";

const STATIC_FIELD_BASE = "../../../../gradient-library/assets/static/";
const WINGS_URL = "../../../../source-pack/design-system-export/assets/wings.svg";

// Real review assets already held by the canonical repository. The integration
// specimen consumes image data; it never redraws or approximates third-party marks.
const INTEGRATION_ASSETS = Object.freeze([
  { id: "notion", name: "Notion", role: "Knowledge", src: "./assets/integrations/notion.svg" },
  { id: "slack", name: "Slack", role: "Signals", src: "./assets/integrations/slack.svg" },
  { id: "stripe", name: "Stripe", role: "Commerce", src: "./assets/integrations/stripe.svg" },
  { id: "openai", name: "OpenAI", role: "Models", src: "./assets/integrations/openai.svg" },
  { id: "github", name: "GitHub", role: "Delivery", src: "./assets/integrations/github.svg" },
  { id: "claude", name: "Claude", role: "Reasoning", src: "./assets/integrations/claude.svg" },
]);

// REVIEW FIXTURES ONLY — these values are not pricing authority.
const FIXTURE_OFFERS = Object.freeze({
  aios: { oneTime: 299, monthly: 79, annual: 63, setup: 0 },
  "context-engine": { oneTime: 189, monthly: 49, annual: 39, setup: 0 },
  "ai-ads-system": { oneTime: 249, monthly: 69, annual: 55, setup: 0 },
  "claude-code-os": { oneTime: 149, monthly: 39, annual: 31, setup: 0 },
  "organic-content-os": { oneTime: 199, monthly: 59, annual: 47, setup: 0 },
});

const FORMAT_CURRENCY = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function h(tag, className = "", text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}

function setAttributes(node, attributes = {}) {
  Object.entries(attributes).forEach(([name, value]) => {
    if (value === undefined || value === null || value === false) return;
    if (name === "checked") node.checked = Boolean(value);
    else if (name === "disabled") node.disabled = Boolean(value);
    else node.setAttribute(name, String(value));
  });
  return node;
}

function button(label, className = "pb-button pb-button--solid", attributes = {}) {
  const node = h("button", className, label);
  node.type = "button";
  return setAttributes(node, attributes);
}

function linkAction(label, className = "pb-button pb-button--solid") {
  return setAttributes(h("a", className, label), { href: "#top" });
}

function fixtureNotice(copy = "Illustrative pricing") {
  return h("small", "pb-fixture-note", copy);
}

function normalizedGradientId(value) {
  const candidate = String(value || "").toUpperCase();
  return /^MZ-G\d{2}$/.test(candidate) ? candidate : "MZ-G13";
}

function offerFor(product) {
  return FIXTURE_OFFERS[product.slug] || FIXTURE_OFFERS.aios;
}

export function productViewModel(products) {
  const source = Array.isArray(products) ? products : products?.products;
  if (!Array.isArray(source) || source.length === 0) {
    throw new TypeError("Phase B requires at least one canonical product.");
  }

  return source.map((product) => {
    const gradientId = normalizedGradientId(product.gradientId);
    const fixtureOffer = FIXTURE_OFFERS[product.slug] || FIXTURE_OFFERS.aios;
    return {
      productId: String(product.productId || product.slug || product.publicName),
      slug: String(product.slug || "aios"),
      publicName: String(product.publicName || "AI OS"),
      extendedName: String(product.function || product.extendedName || "AI Operating System"),
      summary: String(product.summary || "One system your whole business runs on."),
      availability: String(product.availability || "coming-soon"),
      availabilityLabel: product.availability === "live" ? "Available now" : "Coming soon",
      gradientId,
      staticField: `${STATIC_FIELD_BASE}${gradientId.toLowerCase()}.webp`,
      fixtureOffer: { ...fixtureOffer },
    };
  });
}

function wings(className = "pb-wings") {
  const image = h("img", className);
  image.src = WINGS_URL;
  image.alt = "";
  image.setAttribute("aria-hidden", "true");
  return image;
}

function integrationLogo(asset) {
  const image = h("img", "pb-integration-logo");
  image.src = asset.src;
  image.alt = `${asset.name} logo`;
  image.loading = "lazy";
  image.decoding = "async";
  return image;
}

function coreField(product, { live = false, compact = false, label, mark = "center", largeMark = false, showMark = true } = {}) {
  const field = h("div", `pb-core-field core-field pb-core-field--mark-${mark}${compact ? " pb-core-field--compact" : ""}${largeMark ? " pb-core-field--large-mark" : ""}`);
  field.dataset.gradientId = product.gradientId;
  if (live) field.dataset.autoLive = "";
  if (label) field.setAttribute("aria-label", label);
  else field.setAttribute("aria-hidden", "true");
  const source = h("img", "pb-core-field__source");
  source.src = product.staticField;
  source.alt = "";
  field.append(source);
  if (showMark) field.append(wings());
  return field;
}

function identity(product, { compact = false, eyebrow = "" } = {}) {
  const copy = h("div", `pb-product-identity${compact ? " pb-product-identity--compact" : ""}`);
  if (eyebrow) copy.append(h("span", "pb-eyebrow", eyebrow));
  copy.append(
    h(compact ? "h4" : "h3", "pb-product-name", product.publicName),
    h("p", "pb-product-extended", product.extendedName),
    h("p", "pb-product-summary", product.summary),
  );
  return copy;
}

function availability(product) {
  const state = product.availability === "live" ? "live" : "soon";
  return h("span", `pb-status pb-status--${state}`, product.availabilityLabel);
}

function featureList(items, className = "pb-feature-list") {
  const list = h("ul", className);
  items.forEach((item) => {
    const row = h("li", "pb-feature-list__item");
    row.append(h("span", "pb-feature-list__check", "✓"), h("span", "", item));
    list.append(row);
  });
  return list;
}

function priceBlock(amount, cadence = "one time", className = "pb-price") {
  const wrap = h("div", className);
  wrap.append(h("strong", "pb-price__amount", FORMAT_CURRENCY.format(amount)), h("span", "pb-price__cadence", cadence));
  return wrap;
}

function reviewControls(spec) {
  const controls = h("div", "pb-review-controls");
  controls.setAttribute("aria-label", `Review ${spec.id}`);
  [["keep", "Keep"], ["revise", "Revise"], ["kill", "Kill"]].forEach(([verdict, label]) => {
    controls.append(button(label, "pb-review-control", {
      "data-verdict": verdict,
      "aria-pressed": "false",
      "aria-label": `${label} ${spec.id}`,
    }));
  });
  return controls;
}

function reviewable(spec, canvasNode) {
  const article = h("article", `pb-specimen pb-specimen--${spec.family}`);
  const phaseARefs = phaseALineageFor(spec.id);
  article.dataset.specimenId = spec.id;
  article.dataset.specimenFamily = spec.family;
  article.dataset.specimenTitle = spec.title;
  article.dataset.phaseARefs = phaseARefs.join(" ");
  article.dataset.phaseAPrimary = phaseARefs[0] || "";
  if (phaseARefs.length) article.classList.add("pb-specimen--phase-a-linked");

  const header = h("header", "pb-specimen__header");
  const title = h("div", "pb-specimen__identity");
  title.append(h("span", "pb-specimen__id", spec.id), h("h2", "pb-specimen__title", spec.title), h("p", "pb-specimen__note", spec.note));
  if (phaseARefs.length) {
    const lineage = h("div", "pb-specimen__lineage");
    lineage.append(h("span", "pb-specimen__lineage-label", "PHASE A LINEAGE"));
    phaseARefs.forEach((reference) => lineage.append(h("span", "pb-specimen__lineage-chip", reference)));
    title.append(lineage);
  }
  header.append(title, reviewControls(spec));

  const canvas = h("div", "specimen-canvas pb-specimen__canvas");
  canvas.append(canvasNode);

  const feedback = h("label", "pb-specimen__feedback");
  feedback.append(h("span", "pb-specimen__feedback-label", `Feedback on ${spec.id}`));
  const textarea = h("textarea", "pb-specimen__feedback-input");
  textarea.dataset.specimenNote = spec.id;
  textarea.rows = 2;
  textarea.placeholder = `What should stay, change or be explored in ${spec.title}?`;
  feedback.append(textarea);
  article.append(header, canvas, feedback);
  return article;
}

function productTile(product, { selected = false, compact = false } = {}) {
  const tile = h("article", `pb-product-tile${selected ? " is-selected" : ""}${compact ? " pb-product-tile--compact" : ""}`);
  tile.append(coreField(product, { compact }), identity(product, { compact }), availability(product));
  if (selected) tile.append(h("span", "pb-selection-label", "Selected"));
  return tile;
}

function familyRail(products, { selectedIndex = -1, compact = false } = {}) {
  const rail = h("div", `pb-family-rail${compact ? " pb-family-rail--compact" : ""}`);
  products.forEach((product, index) => rail.append(productTile(product, { selected: index === selectedIndex, compact })));
  return rail;
}

function phaseAFullFieldCard(product, {
  live = false,
  dark = false,
  actionLabel = `Explore ${product.publicName}`,
  eyebrow = "COMPLETE SYSTEM",
} = {}) {
  const card = h("article", `pb-phase-a-card${dark ? " pb-phase-a-card--dark" : ""}`);
  card.append(coreField(product, {
    live,
    label: live ? `${product.publicName} product-card material` : undefined,
    mark: "center",
    largeMark: true,
  }));
  const body = h("div", "pb-phase-a-card__body");
  body.append(identity(product, { eyebrow }));
  const footer = h("footer", "pb-phase-a-card__footer");
  footer.append(availability(product), linkAction(actionLabel, dark ? "pb-button pb-button--light" : "pb-button pb-button--solid"));
  card.append(body, footer);
  return card;
}

function discoveryCanvas(spec, product, products) {
  if (spec.variant === "mega-menu") {
    const menu = h("nav", "pb-mega-menu pb-mega-menu--r04 pb-surface", "");
    menu.setAttribute("aria-label", "Products");
    const intro = h("div", "pb-mega-menu__intro");
    intro.append(
      h("span", "pb-eyebrow", "MEZ SYSTEMS"),
      h("h3", "", "The operating layer, in focused systems."),
      h("p", "", "Start with the job that matters now. Add the rest when the company needs them."),
    );
    const directory = h("div", "pb-mega-menu__directory");
    const directoryHead = h("div", "pb-mega-menu__directory-head");
    directoryHead.append(h("span", "pb-eyebrow", "ALL SYSTEMS"), h("span", "", "Choose by the operating job."));
    directory.append(directoryHead);
    products.forEach((item, index) => {
      const link = setAttributes(h("a", `pb-menu-product${index === 0 ? " is-current" : ""}`), { href: "#top" });
      link.append(identity(item, { compact: true }), availability(item));
      directory.append(link);
    });
    const feature = h("article", "pb-mega-menu__feature");
    feature.append(coreField(product, { mark: "center", largeMark: true }));
    const featureCopy = h("div", "pb-mega-menu__feature-copy");
    featureCopy.append(identity(product, { compact: true, eyebrow: "FEATURED SYSTEM" }), linkAction(`Explore ${product.publicName}`, "pb-button pb-button--solid"));
    feature.append(featureCopy);
    menu.append(intro, directory, feature);
    return menu;
  }

  if (spec.variant === "product-hero") {
    const hero = h("section", "pb-product-hero pb-product-hero--phase-a pb-surface pb-surface--light");
    const copy = h("div", "pb-product-hero__copy");
    copy.append(identity(product), availability(product));
    const actions = h("div", "pb-action-row");
    actions.append(linkAction(`Explore ${product.publicName}`), linkAction("See how it works", "pb-text-link"));
    copy.append(actions);
    hero.append(copy, coreField(product, { live: true, label: `${product.publicName} product material`, mark: "center", largeMark: true }));
    return hero;
  }

  if (spec.variant === "family-hero") {
    const hero = h("section", "pb-family-hero pb-family-hero--phase-a pb-surface pb-surface--dark");
    const head = h("header", "pb-family-hero__header");
    head.append(h("span", "pb-eyebrow", "MEZ SYSTEMS PRODUCTS"), h("h3", "", "One operating layer. Five focused systems."), h("p", "", "Begin with the system that removes today’s constraint. Each one connects through the same parent operating language."));
    const showcase = h("div", "pb-family-showcase");
    const lead = h("article", "pb-family-showcase__lead");
    lead.append(coreField(product, { mark: "center", largeMark: true }));
    const leadCopy = h("div", "pb-family-showcase__lead-copy");
    leadCopy.append(identity(product, { eyebrow: "START HERE" }), linkAction(`Explore ${product.publicName}`, "pb-button pb-button--light"));
    lead.append(leadCopy);
    const directory = h("div", "pb-family-showcase__directory");
    products.slice(1).forEach((item) => {
      const link = setAttributes(h("a", "pb-family-showcase__row"), { href: "#top" });
      link.append(identity(item, { compact: true }), availability(item), h("span", "pb-family-showcase__arrow", "↗"));
      directory.append(link);
    });
    showcase.append(lead, directory);
    hero.append(head, showcase);
    return hero;
  }

  if (spec.variant === "featured-split") {
    const section = h("section", "pb-featured-product pb-featured-product--phase-a pb-surface");
    const visual = h("div", "pb-featured-product__visual");
    visual.append(coreField(product, { live: true, label: `${product.publicName} featured material`, mark: "center", largeMark: true }));
    const copy = h("div", "pb-featured-product__copy");
    copy.append(identity(product), h("p", "pb-featured-product__statement", "Give every AI workflow the company context it needs before the work begins."), featureList(["One governed context layer", "Sources remain attached", "Ready for every operating run"]), linkAction("See the complete system"));
    section.append(visual, copy);
    return section;
  }

  if (spec.variant === "shelf") {
    const section = h("section", "pb-product-shelf pb-product-shelf--phase-a pb-product-shelf--equal pb-surface");
    const head = h("header", "pb-section-heading");
    head.append(h("div", "", "Built for the work between strategy and execution."), h("p", "", "Five focused systems. One equal family."));
    const cards = h("div", "pb-shelf-cards");
    products.forEach((item) => {
      const card = setAttributes(h("a", "pb-shelf-card"), { href: "#top" });
      card.append(coreField(item, { mark: "center" }));
      const footer = h("div", "pb-shelf-card__footer");
      footer.append(identity(item, { compact: true }), availability(item), h("span", "pb-shelf-card__arrow", "↗"));
      card.append(footer);
      cards.append(card);
    });
    section.append(head, cards, linkAction("Compare all systems", "pb-button pb-button--solid pb-shelf-cta"));
    return section;
  }

  if (spec.variant === "matrix") {
    const section = h("section", "pb-starting-points pb-starting-points--cards pb-surface");
    const intro = h("header", "pb-starting-points__intro");
    intro.append(h("span", "pb-eyebrow", "FIND YOUR STARTING POINT"), h("h3", "", "Start with the work that needs to become a system."), h("p", "", "Each product owns a distinct operating job. Choose by the change you need, not a feature checklist."));
    const points = h("div", "pb-starting-points__cards");
    const outcomes = ["Run the company from shared decisions", "Make company context usable by AI", "Turn demand into a repeatable growth system"];
    products.slice(0, 3).forEach((item, index) => {
      const card = h("article", "pb-starting-card");
      card.append(coreField(item, { mark: "center" }));
      const body = h("div", "pb-starting-card__body");
      body.append(h("span", "pb-eyebrow", "START HERE"), h("h4", "", outcomes[index]), identity(item, { compact: true }), h("p", "", item.summary), linkAction(item.availability === "live" ? `Explore ${item.publicName}` : "Join the waitlist", "pb-text-link"));
      card.append(body);
      points.append(card);
    });
    const footer = h("div", "pb-starting-points__footer");
    footer.append(h("p", "", "Need the complete picture? Compare every system by job, availability and operating model."), linkAction("Compare all five systems", "pb-button pb-button--solid"));
    section.append(intro, points, footer);
    return section;
  }

  if (spec.variant === "related-rail") {
    const section = h("section", "pb-related-products pb-related-products--equal pb-surface pb-surface--recessed");
    const intro = h("div", "pb-compact-discovery__intro");
    intro.append(h("span", "pb-eyebrow", "CONTINUE THE OPERATING LAYER"), h("h3", "", `Systems that work naturally with ${product.publicName}.`), h("p", "", "Continue into the next operating job without replacing the system you already chose."));
    const rail = h("div", "pb-related-products__rail");
    products.filter((item) => item.slug !== product.slug).slice(0, 3).forEach((item) => {
      const action = setAttributes(h("a", "pb-related-product"), { href: "#top" });
      action.append(coreField(item, { mark: "center" }), identity(item, { compact: true }), h("span", "pb-related-product__arrow", "↗"));
      rail.append(action);
    });
    section.append(intro, rail);
    return section;
  }

  if (spec.variant === "footer") {
    const footer = h("footer", "pb-product-footer pb-product-footer--refined pb-surface pb-surface--dark");
    const conversion = h("div", "pb-product-footer__conversion");
    conversion.append(coreField(product, { live: true, label: `${product.publicName} complete-system material`, mark: "center", largeMark: true }));
    const copy = h("div", "pb-product-footer__copy");
    copy.append(h("span", "pb-eyebrow", "BUILD THE OPERATING LAYER"), h("h3", "", `${product.publicName} first. The whole operating layer when you need it.`), h("p", "", "Every product stands alone, then connects through one parent operating language."));
    conversion.append(copy, linkAction(`Explore ${product.publicName}`, "pb-button pb-button--solid"));
    const directory = h("div", "pb-product-footer__directory");
    const parent = h("div", "pb-product-footer__parent");
    parent.append(wings(), h("strong", "", "MEZ SYSTEMS"), h("p", "", "Product operating systems for the work between strategy and execution."));
    const productLinks = h("div", "pb-product-footer__products");
    products.forEach((item) => {
      const link = setAttributes(h("a", "pb-product-footer__product"), { href: "#top" });
      link.append(identity(item, { compact: true }), availability(item), h("span", "pb-product-footer__arrow", "↗"));
      productLinks.append(link);
    });
    directory.append(parent, productLinks);
    const legal = h("div", "pb-product-footer__legal");
    legal.append(h("span", "", "© 2026 Mez Systems"), h("span", "", "Privacy · Terms · Support"));
    footer.append(conversion, directory, legal);
    return footer;
  }

  const finder = h("section", "pb-product-finder pb-surface pb-surface--dark");
  const copy = h("div", "pb-product-finder__copy");
  copy.append(h("span", "pb-eyebrow", "PRODUCT FINDER"), h("h3", "", "Start with the bottleneck."), h("p", "", "Choose the work you need to make repeatable. We’ll show the system built for it."));
  const choices = h("div", "pb-product-finder__choices");
  ["Run the whole business", "Make AI context usable", "Build repeatable growth", "Ship software reliably"].forEach((label, index) => choices.append(button(label, "pb-choice-button", { "data-local-select": `finder-${index}`, "aria-pressed": index === 0 ? "true" : "false" })));
  const result = h("article", "pb-product-finder__result");
  result.append(coreField(product, { compact: true }), identity(product), linkAction("Explore this system", "pb-button pb-button--light"));
  finder.append(copy, choices, result);
  return finder;
}

function proofRecord(title, claim, detail, result) {
  const card = h("article", "pb-proof-record");
  card.append(h("span", "pb-eyebrow", title), h("h4", "", claim), h("p", "", detail));
  const resultNode = h("div", "pb-proof-record__result");
  resultNode.append(h("strong", "", result), h("span", "", "Illustrative proof fixture"));
  card.append(resultNode);
  return card;
}

function featureCanvas(spec, product, products) {
  if (spec.variant === "split") {
    const section = h("section", "pb-context-story pb-context-story--r04 pb-surface");
    const copy = h("div", "pb-context-story__copy");
    copy.append(identity(product, { eyebrow: "CONTEXT, BEFORE AUTOMATION" }), h("h4", "", "The business becomes legible before the AI starts working."), h("p", "", "Plans, decisions and source material stay connected as one operating context, ready before the first workflow begins."));
    const sources = h("div", "pb-context-story__sources");
    [["Sources", "Company truth"], ["Decisions", "Active direction"], ["Evidence", "Proof attached"]].forEach(([role, label]) => {
      const row = h("div", "pb-context-story__source");
      row.append(h("span", "", role), h("strong", "", label));
      sources.append(row);
    });
    copy.append(sources, linkAction("See how context is governed", "pb-button pb-button--solid"));
    const visual = h("div", "pb-context-story__visual");
    visual.append(coreField(product, { live: true, label: `${product.publicName} context material`, mark: "center", largeMark: true }));
    const caption = h("div", "pb-context-story__caption");
    caption.append(h("span", "pb-eyebrow", "ONE SHARED CONTEXT LAYER"), h("p", "", "The same company truth follows every decision, workflow and verified result."));
    visual.append(caption);
    section.append(copy, visual);
    return section;
  }

  if (spec.variant === "split-reverse") {
    const section = h("section", "pb-run-story pb-run-story--r04 pb-surface pb-surface--dark");
    const field = h("div", "pb-run-story__field");
    field.append(coreField(product, { live: true, label: `${product.publicName} operating-run material`, mark: "center", largeMark: true }));
    const body = h("div", "pb-run-story__body");
    const copy = h("div", "pb-run-story__copy");
    copy.append(identity(product, { eyebrow: "FROM DECISION TO OPERATING RUN" }), h("h4", "", "Build the run once. Keep the work attached to why it exists."), h("p", "", "A named sequence turns an approved decision into owned work, then carries the proof back to the operating layer."), linkAction("Explore the operating model", "pb-button pb-button--light"));
    const sequence = h("ol", "pb-run-story__sequence");
    [["START", "Decision", "Intent is explicit."], ["OPERATE", "Run", "Work has an owner."], ["VERIFY", "Proof", "The result stays attached."]].forEach(([index, title, detail]) => {
      const step = h("li", "pb-run-story__step");
      step.append(h("span", "", index), h("strong", "", title), h("p", "", detail));
      sequence.append(step);
    });
    body.append(copy, sequence);
    section.append(field, body);
    return section;
  }

  if (spec.variant === "mechanism-bento") {
    const section = h("section", "pb-card-bento pb-surface");
    const head = h("header", "pb-card-bento__head");
    head.append(h("span", "pb-eyebrow", "ONE SYSTEM · FOUR USEFUL VIEWS"), h("h3", "", "See the operating layer from decision to proof."), h("p", "", "A conventional bento made from complete marketing cards—each card owns one job, one hierarchy and one action."));

    const grid = h("div", "pb-card-bento__grid");
    const lead = phaseAFullFieldCard(product, {
      live: true,
      dark: true,
      eyebrow: "FEATURED SYSTEM",
      actionLabel: `Explore ${product.publicName}`,
    });
    lead.classList.add("pb-card-bento__lead");

    const capability = h("article", "pb-card-bento-card pb-card-bento-card--capability");
    capability.append(h("span", "pb-eyebrow", "CAPABILITY"), h("h4", "", "Context enters once."), h("p", "", "Company truth, active decisions and source evidence stay connected before the work begins."), featureList(["Governed sources", "Named decisions", "Reusable operating context"]), linkAction("See the context layer", "pb-button pb-button--solid"));

    const workflow = h("article", "pb-card-bento-card pb-card-bento-card--workflow");
    workflow.append(h("span", "pb-eyebrow", "WORKFLOW"), h("h4", "", "Decision to run to proof."));
    const stages = h("ol", "pb-card-bento__stages");
    ["Approve the direction", "Run the owned work", "Attach the verified result"].forEach((label) => stages.append(h("li", "", label)));
    workflow.append(stages, linkAction("How operating runs work", "pb-text-link"));

    const proof = h("article", "pb-card-bento-card pb-card-bento-card--proof");
    proof.append(h("span", "pb-eyebrow", "PROOF"), h("strong", "pb-card-bento__metric", "1"), h("h4", "", "traceable operating outcome"), h("p", "", "Every result keeps its source, owner and human verification attached."), h("small", "pb-fixture-note", "Illustrative proof fixture"));

    grid.append(lead, capability, workflow, proof);
    section.append(head, grid);
    return section;
  }

  if (spec.variant === "proof") {
    const section = h("section", "pb-proof-section pb-proof-section--r04 pb-surface pb-surface--dark");
    const copy = h("div", "pb-proof-section__copy");
    const identityCard = h("div", "pb-proof-section__identity-card");
    identityCard.append(coreField(product, { mark: "center", largeMark: true }), identity(product, { eyebrow: "VISIBLE OPERATING PROOF" }));
    copy.append(identityCard, h("h4", "", "Show what changed, not a fake dashboard."), h("p", "", "Each record names its source, mechanism, result and limitation."), linkAction("Read the proof standard", "pb-button pb-button--light"));
    const records = h("div", "pb-proof-section__records");
    records.append(proofRecord("MECHANISM", "One decision became an assigned run", "Source: strategy review · Owner: Operations", "4 linked steps"), proofRecord("OUTCOME", "The run reached a verified output", "Verification: human review · Limitation: staged fixture", "1 approved output"));
    section.append(copy, records);
    return section;
  }

  if (spec.variant === "integrations") {
    const section = h("section", "pb-integrations-section pb-integrations-section--assets pb-surface");
    const intro = h("div", "pb-integrations-section__intro");
    intro.append(identity(product, { eyebrow: "WORKS WITH THE TOOLS ALREADY IN MOTION" }), h("h4", "", "Connect the sources. Keep the operating system in charge."), h("p", "", "Real brand assets are shown as restrained review fixtures. No live connections are made here."), linkAction("See integration principles", "pb-button pb-button--solid"));
    const list = h("div", "pb-integration-wordmarks");
    INTEGRATION_ASSETS.forEach((asset) => {
      const item = h("article", "pb-integration-wordmark");
      const brand = h("div", "pb-integration-wordmark__brand");
      brand.append(integrationLogo(asset), h("strong", "", asset.name));
      item.append(brand, h("span", "", asset.role));
      list.append(item);
    });
    section.append(intro, list);
    return section;
  }

  if (spec.variant === "before-after") {
    const section = h("section", "pb-before-after pb-before-after--phase-a pb-before-after--r04 pb-surface");
    const plate = phaseAFullFieldCard(product, { live: true, dark: true, eyebrow: "THE OPERATING SHIFT", actionLabel: `Explore ${product.publicName}` });
    plate.classList.add("pb-before-after__product-card");
    const comparison = h("div", "pb-before-after__grid");
    const before = h("article", "pb-change-card pb-change-card--before");
    before.append(h("span", "pb-eyebrow", "BEFORE"), h("h4", "", "Work starts from scratch"), featureList(["Context split across tools", "Decisions disappear in chat", "Outputs have no proof trail"]));
    const after = h("article", "pb-change-card pb-change-card--after");
    after.append(h("span", "pb-eyebrow", "WITH THE SYSTEM"), h("h4", "", "Work compounds as a system"), featureList(["Shared operating context", "Named repeatable runs", "Evidence attached to outcomes"]));
    comparison.append(before, after);
    section.append(plate, comparison);
    return section;
  }

  if (spec.variant === "accordion") {
    const section = h("section", "pb-feature-accordion pb-feature-accordion--r04 pb-surface");
    const intro = h("div", "pb-feature-accordion__intro");
    intro.append(identity(product, { eyebrow: "EXPLORE THE LAYERS" }), coreField(product, { live: true, label: `${product.publicName} feature material` }));
    const list = h("div", "pb-accordion");
    [["Context", "Give every workflow the business truth it needs."], ["Operating runs", "Turn decisions into repeatable sequences with owners."], ["Human gates", "Put judgement at the exact points where it belongs."], ["Proof", "Keep the inputs, outputs and verification connected."]].forEach(([title, copy], index) => {
      const item = h("article", "pb-accordion__item");
      const trigger = button(title, "pb-accordion__trigger", { "data-accordion-trigger": "", "aria-expanded": index === 0 ? "true" : "false" });
      trigger.append(h("span", "", index === 0 ? "−" : "+"));
      const panel = h("div", "pb-accordion__panel");
      panel.hidden = index !== 0;
      panel.append(h("p", "", copy), linkAction("Read the detail", "pb-text-link"));
      item.append(trigger, panel);
      list.append(item);
    });
    list.append(linkAction("Explore every capability", "pb-button pb-button--solid pb-accordion__action"));
    section.append(intro, list);
    return section;
  }

  if (spec.variant === "feature-grid") {
    const section = h("section", "pb-feature-grid-section pb-surface");
    section.append(identity(product, { eyebrow: "CAPABILITIES" }));
    const grid = h("div", "pb-feature-grid");
    [["Shared context", "One source for product, company and customer truth."], ["Named workflows", "Repeatable runs with clear ownership."], ["Human gates", "Explicit review where judgement matters."], ["Proof records", "Evidence attached to the changed state."]].forEach(([title, copy], index) => {
      const card = h("article", "pb-feature-card");
      card.append(h("span", "pb-feature-card__index", String(index + 1).padStart(2, "0")), h("h4", "", title), h("p", "", copy));
      grid.append(card);
    });
    section.append(grid);
    return section;
  }

  const explainer = h("section", "pb-explainer-section pb-explainer-section--phase-a pb-explainer-section--r04 pb-surface pb-surface--dark");
  const focal = h("div", "pb-explainer-section__focal");
  focal.append(coreField(product, { live: true, label: `${product.publicName} material`, mark: "center", largeMark: true }), identity(product));
  const sequence = h("div", "pb-explainer-sequence");
  [["01", "Know the business"], ["02", "Run the workflow"], ["03", "Verify the result"]].forEach(([index, title]) => {
    const row = h("article", "pb-explainer-sequence__row");
    row.append(h("span", "", index), h("h4", "", title), h("p", "", "A bounded system step with a named input, owner and output."));
    sequence.append(row);
  });
  sequence.append(linkAction(`Explore ${product.publicName}`, "pb-button pb-button--light"));
  explainer.append(focal, sequence);
  return explainer;
}

function pricingCard(product, {
  mode = "one-time",
  tier = "Core",
  recommended = false,
  amount,
  features = [],
  material = false,
  materialLive = false,
  mark = "center",
  dark = false,
} = {}) {
  const offer = offerFor(product);
  const card = h("article", `pb-pricing-card${recommended ? " is-recommended" : ""}${material ? " pb-pricing-card--material" : ""}${dark ? " pb-pricing-card--dark" : ""}`);
  if (material) card.append(coreField(product, { live: materialLive, label: materialLive ? `${product.publicName} pricing material` : undefined, mark, largeMark: true }));
  if (recommended) card.append(h("span", "pb-recommendation", "Recommended"));
  card.append(identity(product, { compact: true }), h("span", "pb-pricing-card__tier", tier));
  if (mode === "waitlist") card.append(h("div", "pb-waitlist-price", "Join before launch"));
  else if (mode === "enterprise") card.append(h("div", "pb-enterprise-price", "Custom"), h("p", "pb-pricing-card__disclosure", "Annual agreement · implementation scoped separately"));
  else card.append(priceBlock(amount ?? (mode === "subscription" ? offer.monthly : offer.oneTime), mode === "subscription" ? "per month" : "one time"));
  card.append(featureList(features.length ? features : ["Complete product access", "Updates included", "Guided setup"]));
  const label = mode === "waitlist" ? "Join the waitlist" : mode === "enterprise" ? "Talk to Mez" : mode === "subscription" ? "Start subscription" : "Buy access";
  const actionClass = dark ? "pb-button pb-button--light" : "pb-button pb-button--solid";
  card.append(button(label, actionClass, { "data-commerce-action": mode }));
  return card;
}

function cadenceControl(monthly = true) {
  const control = h("div", "pb-cadence-toggle");
  control.dataset.cadenceControl = "";
  control.append(button("Monthly", "pb-cadence-toggle__option", { "data-cadence": "monthly", "aria-pressed": monthly ? "true" : "false" }), button("Annual · save 20%", "pb-cadence-toggle__option", { "data-cadence": "annual", "aria-pressed": monthly ? "false" : "true" }));
  return control;
}

function pricingCanvas(spec, product, products) {
  if (spec.variant === "one-time") {
    const section = h("section", "pb-pricing-single pb-surface");
    const intro = h("div", "pb-pricing-intro");
    intro.append(h("span", "pb-eyebrow", "ONE-TIME DIGITAL PRODUCT"), h("h3", "", "Own the complete operating system."), h("p", "", "A single purchase for the system, implementation guide and future product updates."), fixtureNotice());
    section.append(intro, pricingCard(product, { mode: "one-time", tier: "Complete system", material: true, materialLive: true, mark: "center", primary: true, features: ["Complete operating system", "Implementation playbook", "Future version updates"] }));
    return section;
  }

  if (spec.variant === "one-time-multi") {
    const section = h("section", "pb-pricing-grid-section pb-surface pb-surface--recessed");
    const head = h("header", "pb-section-heading");
    head.append(h("div", "", "Choose the system you need now."), fixtureNotice("Illustrative one-time prices"));
    const grid = h("div", "pb-pricing-grid");
    products.slice(0, 3).forEach((item, index) => grid.append(pricingCard(item, { mode: "one-time", tier: index === 0 ? "Complete" : "Standalone", recommended: index === 0, material: true, mark: index === 1 ? "corner" : "center", features: ["Complete system", "Setup guide", "Updates included"] })));
    section.append(head, grid);
    return section;
  }

  if (spec.variant === "saas-single") {
    const section = h("section", "pb-pricing-single pb-pricing-single--saas pb-surface pb-surface--dark");
    const intro = h("div", "pb-pricing-intro");
    intro.append(identity(product, { eyebrow: "SAAS OFFER FIXTURE" }), h("h4", "", "One plan for the whole operating team."), h("p", "", "Includes 10 seats, shared workspaces and operating support."), fixtureNotice());
    section.append(intro, pricingCard(product, { mode: "subscription", tier: "Team", recommended: true, material: true, materialLive: true, mark: "center", dark: true, features: ["10 team seats", "Unlimited operating runs", "Priority support"] }));
    return section;
  }

  if (spec.variant === "three-tier") {
    const section = h("section", "pb-tier-section pb-surface");
    const head = h("header", "pb-tier-section__header");
    head.append(h("div", "", "Plans that grow with the operating layer."), cadenceControl());
    const grid = h("div", "pb-pricing-grid pb-pricing-grid--three");
    const monthly = offerFor(product).monthly;
    [["Starter", monthly - 30, ["3 seats", "5 operating runs", "Community support"]], ["Team", monthly, ["10 seats", "Unlimited runs", "Priority support"]], ["Scale", monthly + 80, ["30 seats", "Advanced controls", "Operating review"]]].forEach(([tier, amount, features], index) => {
      const card = pricingCard(product, { mode: "subscription", tier, amount, recommended: index === 1, material: true, mark: index === 1 ? "center" : "corner", features });
      const amountNode = card.querySelector(".pb-price__amount");
      amountNode.dataset.monthly = amount;
      amountNode.dataset.annual = Math.round(amount * 0.8);
      grid.append(card);
    });
    section.append(head, grid, fixtureNotice());
    return section;
  }

  if (spec.variant === "cadence") {
    const section = h("section", "pb-cadence-section pb-surface pb-surface--recessed");
    const head = h("header", "pb-section-heading");
    head.append(h("div", "", "Pay monthly or commit for a year."), cadenceControl());
    const offer = offerFor(product);
    const card = h("article", "pb-cadence-offer");
    card.append(coreField(product, { compact: true }), identity(product));
    const amount = h("strong", "pb-cadence-offer__amount", FORMAT_CURRENCY.format(offer.monthly));
    amount.dataset.monthly = offer.monthly;
    amount.dataset.annual = offer.annual;
    const cadence = h("span", "pb-cadence-offer__cadence", "/ month");
    cadence.dataset.cadenceLabel = "";
    const price = h("div", "pb-cadence-offer__price");
    price.append(amount, cadence);
    card.append(price, h("p", "", "10 seats · Unlimited runs · Cancel at the end of the billing period"), button("Choose this plan", "pb-button pb-button--solid"));
    section.append(head, card, fixtureNotice());
    return section;
  }

  if (spec.variant === "usage") {
    const section = h("section", "pb-usage-pricing pb-surface");
    const copy = h("div", "pb-usage-pricing__copy");
    copy.append(coreField(product, { mark: "corner" }), identity(product, { eyebrow: "USAGE-BASED FIXTURE" }), h("h4", "", "Scale operating runs with the team."), h("p", "", "$29 platform access plus $6 per active operator each month."), fixtureNotice());
    const calculator = h("div", "pb-usage-calculator");
    const label = setAttributes(h("label", "pb-usage-calculator__label", "Active operators"), { for: `usage-${spec.id}` });
    const output = h("output", "pb-usage-calculator__count", "10 operators");
    output.dataset.usageCount = "";
    const range = setAttributes(h("input", "pb-usage-calculator__range"), { id: `usage-${spec.id}`, type: "range", min: "1", max: "50", value: "10", step: "1", "data-usage-slider": "", "data-base": "29", "data-unit": "6" });
    const total = h("strong", "pb-usage-calculator__total", "$89 / month");
    total.dataset.usageTotal = "";
    calculator.append(label, output, range, total, h("small", "", "No charge is made in this review fixture."), button("Start with 10 operators", "pb-button pb-button--solid"));
    section.append(copy, calculator);
    return section;
  }

  if (spec.variant === "comparison") {
    const section = h("section", "pb-plan-comparison pb-surface");
    const head = h("header", "pb-section-heading");
    const heading = h("div", "pb-plan-comparison__heading");
    heading.append(identity(product, { compact: true }), h("h3", "", "Compare the operating plans."));
    head.append(heading, fixtureNotice());
    const table = h("div", "pb-comparison-table");
    table.setAttribute("role", "table");
    [["Capability", "Starter", "Team", "Scale"], ["Seats", "3", "10", "30"], ["Operating runs", "5 / month", "Unlimited", "Unlimited"], ["Human review gates", "Basic", "Complete", "Custom"], ["Support", "Community", "Priority", "Operating review"]].forEach((cells, rowIndex) => {
      const row = h("div", `pb-comparison-row${rowIndex === 0 ? " pb-comparison-row--head" : ""}`);
      row.setAttribute("role", "row");
      cells.forEach((cell, index) => row.append(setAttributes(h(index === 0 ? "strong" : "span", "", cell), { role: rowIndex === 0 ? "columnheader" : index === 0 ? "rowheader" : "cell" })));
      table.append(row);
    });
    section.append(head, table, button("Choose Team", "pb-button pb-button--solid"));
    return section;
  }

  if (spec.variant === "enterprise") {
    const section = h("section", "pb-enterprise-offer pb-enterprise-offer--phase-a pb-surface pb-surface--dark");
    section.append(coreField(product, { live: true, label: `${product.publicName} enterprise material`, showMark: false }));
    const copy = h("div", "pb-enterprise-offer__copy");
    copy.append(h("span", "pb-eyebrow", "MEZ SYSTEMS FOR SCALE"), h("h3", "", `${product.publicName}, built around your company.`), h("p", "", "Custom product mix, governance, implementation and operating support for larger teams."), featureList(["Custom product and seat scope", "Implementation planning", "Governance and support"]), fixtureNotice("Illustrative enterprise offer"));
    section.append(copy, pricingCard(product, { mode: "enterprise", tier: "Enterprise", dark: true, features: ["Scoped implementation", "Named operating partner", "Custom controls"] }));
    return section;
  }

  if (spec.variant === "waitlist") {
    const section = h("section", "pb-waitlist-offer pb-surface");
    const field = coreField(product, { live: true, label: `${product.publicName} preview material`, mark: "center", largeMark: true });
    const copy = h("div", "pb-waitlist-offer__copy");
    copy.append(availability(product), identity(product, { eyebrow: "EARLY ACCESS" }), h("h4", "", "Be first into the system when access opens."));
    const form = h("form", "pb-waitlist-form");
    form.addEventListener("submit", (event) => event.preventDefault());
    const label = setAttributes(h("label", "pb-sr-only", "Work email"), { for: `waitlist-${spec.id}` });
    const input = setAttributes(h("input", "pb-input"), { id: `waitlist-${spec.id}`, type: "email", placeholder: "you@company.com", autocomplete: "email" });
    form.append(label, input, button("Join the waitlist", "pb-button pb-button--solid", { type: "submit", "data-local-state": "waitlist" }));
    copy.append(form, h("small", "", "No email is submitted from this review fixture."));
    section.append(field, copy);
    return section;
  }

  const section = h("section", "pb-mixed-pricing pb-surface pb-surface--recessed");
  const head = h("header", "pb-section-heading");
  head.append(h("div", "", "Buy the system, subscribe to the service, or talk to us."), fixtureNotice("Illustrative offer models"));
  const grid = h("div", "pb-pricing-grid pb-pricing-grid--three");
  grid.append(
    pricingCard(product, { mode: "one-time", tier: "Digital system", material: true, mark: "corner", features: ["One-time access", "Implementation guide", "Version updates"] }),
    pricingCard(product, { mode: "subscription", tier: "Operating service", recommended: true, material: true, mark: "center", dark: true, features: ["Live workspace", "10 seats", "Priority support"] }),
    pricingCard(product, { mode: "enterprise", tier: "Company layer", material: true, mark: "corner", features: ["Custom scope", "Implementation", "Governance"] }),
  );
  section.append(head, grid);
  return section;
}

function orderRows(rows) {
  const list = h("dl", "pb-order-rows");
  rows.forEach(([label, value, strong = false]) => {
    const term = h("dt", strong ? "is-total" : "", label);
    const amount = h("dd", strong ? "is-total" : "", value);
    list.append(term, amount);
  });
  return list;
}

function field(label, id, options = {}) {
  const wrap = h("label", `pb-field${options.wide ? " pb-field--wide" : ""}`);
  wrap.append(h("span", "pb-field__label", label));
  const input = setAttributes(h("input", "pb-input"), { id, name: id, type: options.type || "text", placeholder: options.placeholder || "", autocomplete: options.autocomplete || "off" });
  wrap.append(input);
  return wrap;
}

function checkoutIdentity(product, label = "YOUR ORDER") {
  const wrap = h("div", "pb-checkout-product");
  wrap.append(coreField(product, { compact: true }), identity(product, { compact: true, eyebrow: label }));
  return wrap;
}

function checkoutCanvas(spec, product) {
  const offer = offerFor(product);
  if (spec.variant === "digital" || spec.variant === "saas") {
    const checkout = h("section", `pb-checkout pb-surface${spec.variant === "saas" ? " pb-checkout--saas" : ""}`);
    const form = h("form", "pb-checkout__form");
    form.addEventListener("submit", (event) => event.preventDefault());
    const legend = h("div", "pb-checkout__legend");
    legend.append(h("span", "pb-eyebrow", spec.variant === "saas" ? "START TEAM PLAN" : "SECURE CHECKOUT"), h("h3", "", spec.variant === "saas" ? "Create the team workspace." : "Complete your purchase."), h("p", "", spec.variant === "saas" ? "Choose an owner and billing contact. Seats can be invited after checkout." : "Your download and setup guide arrive after confirmation."));
    const fields = h("div", "pb-form-grid");
    fields.append(field("Name", `${spec.id}-name`, { autocomplete: "name" }), field("Work email", `${spec.id}-email`, { type: "email", autocomplete: "email" }), field(spec.variant === "saas" ? "Workspace name" : "Company", `${spec.id}-company`, { wide: true, autocomplete: "organization" }), field("Card information", `${spec.id}-card`, { wide: true, placeholder: "Payment field placeholder" }));
    form.append(legend, fields, h("p", "pb-checkout-disclosure", "Static payment UI for design review. No card data is accepted or transmitted."));
    const summary = h("aside", `pb-order-summary pb-order-summary--phase-a${spec.variant === "saas" ? " pb-order-summary--dark" : ""}`);
    summary.append(coreField(product, { mark: spec.variant === "saas" ? "center" : "corner", largeMark: true }), checkoutIdentity(product), priceBlock(spec.variant === "saas" ? offer.monthly : offer.oneTime, spec.variant === "saas" ? "per month" : "one time"), orderRows([[spec.variant === "saas" ? "Team plan" : "Complete system", FORMAT_CURRENCY.format(spec.variant === "saas" ? offer.monthly : offer.oneTime)], ["Tax", "Calculated later"], ["Due today", FORMAT_CURRENCY.format(spec.variant === "saas" ? offer.monthly : offer.oneTime), true]]), button(spec.variant === "saas" ? "Start Team plan" : "Complete purchase", spec.variant === "saas" ? "pb-button pb-button--light" : "pb-button pb-button--solid", { "data-local-state": "processing" }));
    checkout.append(form, summary);
    return checkout;
  }

  if (spec.variant === "express") {
    const checkout = h("section", "pb-express-checkout pb-express-checkout--phase-a pb-surface pb-surface--recessed");
    checkout.append(coreField(product, { mark: "center", largeMark: true }));
    const head = h("div", "pb-express-checkout__head");
    head.append(checkoutIdentity(product, "EXPRESS CHECKOUT"), priceBlock(offer.oneTime), h("p", "", "One-time access · setup guide · future version updates"));
    checkout.append(head);
    const express = h("div", "pb-express-actions");
    express.append(button("Pay with wallet", "pb-button pb-button--dark", { "data-local-state": "processing" }), button("Use saved checkout", "pb-button pb-button--outline", { "data-local-state": "processing" }));
    checkout.append(express, h("div", "pb-checkout-divider", "or pay by card"), field("Work email", `${spec.id}-email`, { type: "email", autocomplete: "email", wide: true }), button("Continue to payment", "pb-button pb-button--solid"), h("small", "", "Interaction fixture only; no payment provider is connected."));
    return checkout;
  }

  if (spec.variant === "summary") {
    const summary = h("aside", "pb-order-summary pb-order-summary--expanded pb-order-summary--phase-a pb-surface");
    summary.append(coreField(product, { mark: "center", largeMark: true }), h("span", "pb-eyebrow", "ORDER SUMMARY"), checkoutIdentity(product), orderRows([["Complete system", FORMAT_CURRENCY.format(offer.oneTime)], ["Launch discount", "−$30"], ["Subtotal", FORMAT_CURRENCY.format(offer.oneTime - 30)], ["Tax", "Calculated at payment"], ["Total due", FORMAT_CURRENCY.format(offer.oneTime - 30), true]]));
    const disclosure = h("div", "pb-order-summary__disclosure");
    disclosure.append(h("strong", "", "Included with purchase"), h("p", "", "Implementation guide, future updates and 30-day setup support."));
    summary.append(disclosure, button("Complete purchase", "pb-button pb-button--solid"), fixtureNotice());
    return summary;
  }

  if (spec.variant === "processing" || spec.variant === "error") {
    const state = h("section", `pb-checkout-state pb-checkout-state--${spec.variant} pb-surface`);
    const mark = h("div", "pb-checkout-state__mark", spec.variant === "processing" ? "…" : "!");
    const copy = h("div", "pb-checkout-state__copy");
    copy.append(h("span", "pb-eyebrow", spec.variant === "processing" ? "PAYMENT IN PROGRESS" : "PAYMENT NOT COMPLETED"), h("h3", "", spec.variant === "processing" ? "Confirming your access." : "Your card was not charged."), h("p", "", spec.variant === "processing" ? "Keep this page open. We’re waiting for the local review state to resolve." : "Review the card details or choose another payment method. Your order is still saved."), checkoutIdentity(product));
    const actions = h("div", "pb-action-row");
    if (spec.variant === "processing") actions.append(button("Processing…", "pb-button pb-button--solid", { disabled: true }), button("Cancel", "pb-button pb-button--quiet", { "data-local-state": "cancelled" }));
    else actions.append(button("Try again", "pb-button pb-button--solid", { "data-local-state": "processing" }), button("Use another method", "pb-button pb-button--outline"));
    copy.append(actions, h("p", "pb-local-status", spec.variant === "processing" ? "Review state: processing" : "Review state: recoverable error"));
    copy.querySelector(".pb-local-status").dataset.localStatus = "";
    state.append(mark, copy);
    return state;
  }

  const confirmation = h("section", `pb-confirmation pb-confirmation--r04 pb-confirmation--${spec.variant} pb-surface${spec.variant === "confirmation-saas" ? " pb-surface--dark" : ""}`);
  const hero = h("div", "pb-confirmation__hero");
  hero.append(coreField(product, { mark: "center", largeMark: true }));
  const copy = h("div", "pb-confirmation__copy");
  copy.append(h("span", "pb-confirmation__mark", "✓"), identity(product, { eyebrow: spec.variant === "confirmation-saas" ? "WORKSPACE READY" : "PURCHASE COMPLETE" }), h("h3", "", spec.variant === "confirmation-saas" ? "The operating workspace is ready." : "Your system is ready to use."), h("p", "", spec.variant === "confirmation-saas" ? "Invite the team, connect the first source and choose the first operating run." : "Open the system, follow the setup path and make the first operating decision."));
  hero.append(copy);
  const nextActions = h("div", "pb-confirmation__next");
  const next = h("ol", "pb-confirmation__steps");
  const steps = spec.variant === "confirmation-saas" ? ["Invite your operators", "Connect company context", "Launch the first run"] : ["Open the complete system", "Follow the setup guide", "Create the first run"];
  steps.forEach((step, index) => {
    const item = h("li", "");
    item.append(h("span", "", String(index + 1).padStart(2, "0")), h("strong", "", step));
    next.append(item);
  });
  nextActions.append(h("span", "pb-eyebrow", "YOUR FIRST THREE STEPS"), next, linkAction(spec.variant === "confirmation-saas" ? "Open workspace" : "Open your system", spec.variant === "confirmation-saas" ? "pb-button pb-button--light" : "pb-button pb-button--solid"));
  confirmation.append(hero, nextActions);
  return confirmation;
}

function bundlePack(products, { layout = "stack", liveLead = false, sequenced = false } = {}) {
  const pack = h("div", `pb-bundle-pack pb-bundle-pack--${layout}${sequenced ? " pb-bundle-pack--sequenced" : ""}`);
  const visibleProducts = products.slice(0, layout === "mini" ? 4 : 5);
  pack.style.setProperty("--pb-pack-center", String((visibleProducts.length - 1) / 2));
  visibleProducts.forEach((product, index) => {
    const isLead = index === visibleProducts.length - 1;
    const card = h("article", `pb-bundle-pack__card${isLead ? " is-lead" : ""}`);
    card.style.setProperty("--pb-pack-index", String(index));
    card.append(coreField(product, { live: liveLead && isLead, label: liveLead && isLead ? `${product.publicName} bundle material` : undefined, mark: layout === "fan" ? "corner" : "center", largeMark: isLead, showMark: isLead }), identity(product, { compact: true }));
    pack.append(card);
  });
  return pack;
}

function bundleCanvas(spec, product, products) {
  if (spec.variant === "fixed") {
    const section = h("section", "pb-fixed-bundle pb-fixed-bundle--r04 pb-surface pb-surface--dark");
    const copy = h("div", "pb-fixed-bundle__copy");
    copy.append(h("span", "pb-eyebrow", "THE OPERATING SUITE"), h("h3", "", "Five systems. One operating layer."), h("p", "", "A fixed package for teams ready to connect strategy, growth, content and software work."), featureList(["Every Mez Systems product", "One connected setup path", "Future family updates"]), priceBlock(799, "one-time fixture"), fixtureNotice(), button("Choose the complete suite", "pb-button pb-button--light"));
    section.append(bundlePack(products, { layout: "stack" }), copy);
    return section;
  }

  if (spec.variant === "builder") {
    const section = h("section", "pb-bundle-builder pb-surface");
    const options = h("fieldset", "pb-bundle-builder__options");
    options.append(h("legend", "", "Build your operating layer"), h("p", "", "Choose at least two systems. AI OS is included as the foundation."));
    products.forEach((item, index) => {
      const row = h("label", "pb-bundle-option");
      const input = setAttributes(h("input", ""), { type: "checkbox", value: item.slug, "data-bundle-option": "", "data-price": offerFor(item).oneTime, checked: index < 2, disabled: index === 0 });
      row.append(input, coreField(item, { compact: true }), identity(item, { compact: true }), h("strong", "", FORMAT_CURRENCY.format(offerFor(item).oneTime)));
      options.append(row);
    });
    const summary = h("aside", "pb-bundle-builder__summary");
    summary.append(bundlePack(products.slice(0, 2), { layout: "mini" }));
    summary.append(h("span", "pb-eyebrow", "YOUR BUNDLE"), h("strong", "pb-bundle-total", "$488"), h("span", "", "Illustrative total"), h("p", "pb-bundle-count", "2 systems selected"), button("Continue with bundle", "pb-button pb-button--solid"), fixtureNotice());
    summary.querySelector(".pb-bundle-total").dataset.bundleTotal = "";
    summary.querySelector(".pb-bundle-count").dataset.bundleCount = "";
    section.append(options, summary);
    return section;
  }

  if (spec.variant === "stack") {
    const section = h("section", "pb-bundle-stack-section pb-bundle-stack-section--phase-a pb-surface pb-surface--recessed");
    const copy = h("div", "pb-bundle-stack-section__copy");
    copy.append(h("span", "pb-eyebrow", "START WITH A STACK"), h("h3", "", "The core company operating layer."), h("p", "", "AI OS, Context Engine and AI Ads System packaged around one shared operating model."), featureList(["Three complete systems", "One setup path", "Connected context model"]), button("See the stack", "pb-button pb-button--solid"));
    section.append(copy, bundlePack(products.slice(0, 3), { layout: "stack", liveLead: true, sequenced: true }));
    return section;
  }

  if (spec.variant === "comparison") {
    const section = h("section", "pb-bundle-comparison pb-surface");
    const head = h("header", "pb-section-heading");
    head.append(h("div", "", "Choose a focused stack or the complete suite."), fixtureNotice());
    const grid = h("div", "pb-bundle-comparison__grid");
    [["Growth stack", products.slice(2, 5), "$499", "Advertising, content and software"], ["Complete suite", products, "$799", "Every operating system" ]].forEach(([title, items, amount, copy], index) => {
      const card = h("article", `pb-bundle-comparison-card${index === 1 ? " is-recommended" : ""}`);
      card.append(h("span", "pb-eyebrow", index === 1 ? "RECOMMENDED" : "FOCUSED"), h("h3", "", title), h("p", "", copy), bundlePack(items, { layout: "mini" }), h("strong", "pb-bundle-comparison-card__price", amount), featureList(items.map((item) => item.publicName)), button("Choose bundle", index === 1 ? "pb-button pb-button--light" : "pb-button pb-button--solid"));
      grid.append(card);
    });
    section.append(head, grid);
    return section;
  }

  if (spec.variant === "order-bump") {
    const row = h("section", "pb-order-bump pb-surface");
    const input = setAttributes(h("input", ""), { type: "checkbox", id: `bump-${spec.id}`, "data-upsell-toggle": "", "data-price": "49" });
    const label = setAttributes(h("label", "pb-order-bump__content"), { for: `bump-${spec.id}` });
    label.append(coreField(product, { compact: true }), identity(product, { compact: true }), h("div", "pb-order-bump__price", "+$49 one time"));
    const total = h("div", "pb-order-bump__total", "Order total · $299");
    total.dataset.upsellTotal = "";
    total.dataset.base = "299";
    row.append(input, label, total, h("small", "", "Optional and unchecked by default · illustrative pricing"));
    return row;
  }

  if (spec.variant === "cart-upsell") {
    const section = h("section", "pb-cart-upsell pb-cart-upsell--r04 pb-surface pb-surface--recessed");
    const intro = h("div", "pb-cart-upsell__intro");
    intro.append(h("span", "pb-eyebrow", "ADD TO YOUR OPERATING LAYER"), h("h3", "", "Complete the context loop."), h("p", "", "Context Engine makes the business legible to every AI workflow you run."));
    const item = h("article", "pb-cart-upsell__item");
    item.append(coreField(product, { mark: "center", largeMark: true }));
    const body = h("div", "pb-cart-upsell__body");
    body.append(identity(product), featureList(["Shared company context", "Connected operating runs"]), priceBlock(offerFor(product).oneTime), button("Add to order", "pb-button pb-button--solid", { "data-local-toggle": "add", "aria-pressed": "false" }), button("Continue without it", "pb-button pb-button--quiet"));
    item.append(body);
    section.append(intro, item, fixtureNotice());
    return section;
  }

  if (spec.variant === "upgrade") {
    const section = h("section", "pb-upgrade-offer pb-upgrade-offer--r04 pb-surface pb-surface--dark");
    const current = h("article", "pb-upgrade-current");
    current.append(coreField(products[0], { mark: "center", largeMark: true }), identity(products[0], { eyebrow: "CURRENT ORDER" }), h("p", "", "$299 one time · complete operating system"), featureList(["AI operating system", "Implementation guide"]));
    const next = h("article", "pb-upgrade-next");
    next.append(h("span", "pb-eyebrow", "UPGRADE THE ORDER"), h("h3", "", "AI OS + Context Engine"), h("p", "", "Add the shared context layer and save $40 on the pair."), bundlePack(products.slice(0, 2), { layout: "mini" }), h("strong", "", "+$149 today"), button("Upgrade my order", "pb-button pb-button--light", { "data-local-toggle": "upgrade", "aria-pressed": "false" }), button("Keep AI OS only", "pb-button pb-button--quiet"));
    section.append(current, h("span", "pb-upgrade-arrow", "→"), next, fixtureNotice());
    return section;
  }

  const section = h("section", "pb-post-purchase pb-post-purchase--phase-a pb-post-purchase--r04 pb-surface");
  const head = h("div", "pb-post-purchase__head");
  head.append(h("span", "pb-confirmation__mark", "✓"), h("span", "pb-eyebrow", "PURCHASE COMPLETE"), h("h3", "", "Add one more system before you enter."), h("p", "", "This optional addition is separate from the purchase you already completed."));
  const offer = h("article", "pb-post-purchase__offer");
  offer.append(coreField(product, { mark: "center", largeMark: true }), identity(product), featureList(["Immediate access", "One connected setup path"]), priceBlock(129, "one-time add-on fixture"), button("Add with one confirmation", "pb-button pb-button--solid", { "data-local-toggle": "post-purchase", "aria-pressed": "false" }), button("Continue without it", "pb-button pb-button--quiet"));
  section.append(head, offer, fixtureNotice());
  return section;
}

function phoneFrame(title, content) {
  const phone = h("section", "pb-phone");
  const bar = h("div", "pb-phone__bar");
  bar.append(h("span", "", "9:41"), h("strong", "", title), h("span", "", "•••"));
  const body = h("div", "pb-phone__body");
  body.append(content);
  phone.append(bar, body);
  return phone;
}

function mobileCanvas(spec, product, products) {
  if (spec.variant === "discovery") {
    const page = h("div", "pb-mobile-page pb-mobile-page--discovery");
    const plate = h("div", "pb-mobile-landing-plate");
    plate.append(coreField(product, { live: true, label: `${product.publicName} mobile product material`, mark: "center", largeMark: true }), identity(product, { eyebrow: "FEATURED SYSTEM" }));
    const head = h("header", "pb-mobile-page__head");
    head.append(h("span", "pb-eyebrow", "MEZ SYSTEMS"), h("h3", "", "Start with one. Add the next system when it earns its place."), h("p", "", "Every system can stand alone, then connect through the same operating layer."));
    const related = h("div", "pb-mobile-related-list");
    products.slice(1, 3).forEach((item) => {
      const row = setAttributes(h("a", "pb-mobile-related"), { href: "#top" });
      row.append(coreField(item, { compact: true, mark: "center" }), identity(item, { compact: true }), availability(item));
      related.append(row);
    });
    page.append(plate, head, related);
    const sticky = h("div", "pb-mobile-sticky");
    sticky.append(coreField(product, { compact: true }), identity(product, { compact: true }), button(`Explore ${product.publicName}`, "pb-button pb-button--solid"));
    page.append(sticky);
    return phoneFrame("Products", page);
  }

  if (spec.variant === "pricing") {
    const page = h("div", "pb-mobile-page pb-mobile-page--pricing");
    page.append(identity(product, { eyebrow: "CHOOSE A PLAN" }), cadenceControl(), pricingCard(product, { mode: "subscription", tier: "Team", recommended: true, material: true, mark: "center", features: ["10 seats", "Unlimited runs", "Priority support"] }));
    const sticky = h("div", "pb-mobile-sticky pb-mobile-sticky--price");
    sticky.append(h("div", "", "Team plan"), priceBlock(offerFor(product).monthly, "/ month"), button("Choose plan", "pb-button pb-button--solid"));
    page.append(sticky, fixtureNotice());
    return phoneFrame("Plans", page);
  }

  if (spec.variant === "checkout") {
    const page = h("div", "pb-mobile-page pb-mobile-page--checkout");
    page.append(coreField(product, { mark: "center", largeMark: true }), checkoutIdentity(product), field("Work email", `${spec.id}-email`, { type: "email", autocomplete: "email", wide: true }), field("Card information", `${spec.id}-card`, { placeholder: "Payment field placeholder", wide: true }), h("p", "pb-checkout-disclosure", "Review fixture only. No payment data is accepted."));
    const disclosure = h("div", "pb-mobile-order-disclosure");
    const trigger = button("Order summary · $299", "pb-mobile-order-disclosure__trigger", { "data-accordion-trigger": "", "aria-expanded": "false" });
    trigger.append(h("span", "", "+"));
    const panel = h("div", "pb-mobile-order-disclosure__panel");
    panel.hidden = true;
    panel.append(orderRows([["Complete system", "$299"], ["Tax", "Calculated later"], ["Total", "$299", true]]));
    disclosure.append(trigger, panel);
    const sticky = h("div", "pb-mobile-sticky pb-mobile-sticky--checkout");
    sticky.append(h("strong", "", "$299 due today"), button("Complete purchase", "pb-button pb-button--solid", { "data-local-state": "processing" }));
    page.append(disclosure, sticky);
    return phoneFrame("Checkout", page);
  }

  const page = h("div", "pb-mobile-page pb-mobile-page--confirmation");
  const confirm = h("div", "pb-mobile-confirmation");
  confirm.append(coreField(product, { mark: "center", largeMark: true }), h("span", "pb-confirmation__mark", "✓"), h("span", "pb-eyebrow", "ACCESS READY"), h("h3", "", "Your system is ready."), identity(product, { compact: true }), featureList(["Open the complete system", "Follow the setup guide", "Create the first operating run"]));
  const upsell = h("article", "pb-mobile-upsell");
  const related = products[1] || product;
  upsell.append(h("span", "pb-eyebrow", "OPTIONAL NEXT SYSTEM"), coreField(related, { compact: true }), identity(related, { compact: true }), h("strong", "", "+$129 one time"), button("Add to access", "pb-button pb-button--solid", { "data-local-toggle": "mobile-upsell", "aria-pressed": "false" }), button("Continue", "pb-button pb-button--quiet"));
  page.append(confirm, upsell, fixtureNotice());
  return phoneFrame("Complete", page);
}

const SPECS = Object.freeze([
  { id: "B-DS01", family: "discovery", title: "Product mega-menu", note: "A real navigation surface for the five-product family.", variant: "mega-menu", product: 0 },
  { id: "B-DS02", family: "discovery", title: "Single product hero", note: "Name-first hero with one focal live product field.", variant: "product-hero", product: 0 },
  { id: "B-DS03", family: "discovery", title: "Product family hero", note: "Contained-dark family opening with equal static product objects.", variant: "family-hero", product: 0 },
  { id: "B-DS04", family: "discovery", title: "Featured product split", note: "A product-specific discovery placement with proof and capability detail.", variant: "featured-split", product: 1 },
  { id: "B-DS05", family: "discovery", title: "Product family shelf", note: "Five equal Phase A-derived cards preserve one family geometry.", variant: "shelf", product: 0 },
  { id: "B-DS06", family: "discovery", title: "Editorial starting points", note: "Three complete marketing cards organise the family by the change a buyer needs.", variant: "matrix", product: 0 },
  { id: "B-DS07", family: "discovery", title: "Related systems rail", note: "A contextual end-of-story rail that earns its place through product relationships.", variant: "related-rail", product: 2 },
  { id: "B-DS08", family: "discovery", title: "Product-aware footer", note: "A complete product footer with one bounded conversion moment and the full family directory.", variant: "footer", product: 0 },

  { id: "B-FT01", family: "features", title: "Context operating story", note: "An authored product narrative with one focal material field and no simulated UI overlay.", variant: "split", product: 0 },
  { id: "B-FT02", family: "features", title: "Operating-run story", note: "A contained-dark marketing sequence that explains how a decision becomes proof.", variant: "split-reverse", product: 3 },
  { id: "B-FT03", family: "features", title: "Product card bento", note: "Four complete marketing cards form a conventional premium bento with one live focal core.", variant: "mechanism-bento", product: 1 },
  { id: "B-FT05", family: "features", title: "Proof record section", note: "Mechanism and outcome proof stay explicitly typed.", variant: "proof", product: 0 },
  { id: "B-FT07", family: "features", title: "Integration wordmark field", note: "Real repository-held logo assets form a restrained connected-tools section.", variant: "integrations", product: 0 },
  { id: "B-FT08", family: "features", title: "Before and after shift", note: "An approved Phase A full-field card anchors a concrete operating change.", variant: "before-after", product: 4 },
  { id: "B-FT09", family: "features", title: "Feature accordion", note: "A progressive disclosure component with usable local interaction.", variant: "accordion", product: 3 },
  { id: "B-FT10", family: "features", title: "Dark product explainer", note: "A complete explainer section with focal material and still sequence.", variant: "explainer", product: 2 },

  { id: "B-PR01", family: "pricing", title: "One-time digital offer", note: "Digital-product language, inclusions and one clear commitment.", variant: "one-time", product: 0 },
  { id: "B-PR02", family: "pricing", title: "Multi-product digital pricing", note: "Three equal one-time offers with one bounded recommendation.", variant: "one-time-multi", product: 0 },
  { id: "B-PR03", family: "pricing", title: "Single SaaS plan", note: "Subscription language and team inclusions remain explicit.", variant: "saas-single", product: 0 },
  { id: "B-PR04", family: "pricing", title: "Three SaaS tiers", note: "Starter, Team and Scale with equal comparison geometry.", variant: "three-tier", product: 0 },
  { id: "B-PR05", family: "pricing", title: "Billing cadence selector", note: "Monthly and annual values update locally with no price authority claim.", variant: "cadence", product: 1 },
  { id: "B-PR06", family: "pricing", title: "Usage-based calculator", note: "A local operator slider demonstrates transparent usage pricing.", variant: "usage", product: 1 },
  { id: "B-PR07", family: "pricing", title: "Plan comparison table", note: "Essential differences stay visible and semantically related.", variant: "comparison", product: 0 },
  { id: "B-PR08", family: "pricing", title: "Enterprise offer", note: "Custom scope is explained without inventing a production amount.", variant: "enterprise", product: 0 },
  { id: "B-PR09", family: "pricing", title: "Coming-soon waitlist", note: "One automatically live focal core makes availability feel active without fake purchase UI.", variant: "waitlist", product: 2 },
  { id: "B-PR10", family: "pricing", title: "Mixed commercial models", note: "One-time, subscription and enterprise keep equal decision geometry while explaining different jobs.", variant: "mixed", product: 0 },

  { id: "B-CK01", family: "checkout", title: "Digital product checkout", note: "A realistic one-time checkout with static provider placeholders.", variant: "digital", product: 0 },
  { id: "B-CK02", family: "checkout", title: "SaaS workspace checkout", note: "Subscription checkout adds workspace ownership without changing identity.", variant: "saas", product: 0 },
  { id: "B-CK03", family: "checkout", title: "Express checkout", note: "A compact alternative-payment route with explicit fixture limits.", variant: "express", product: 0 },
  { id: "B-CK04", family: "checkout", title: "Expanded order summary", note: "Line items, discount, tax status and commitment stay visible.", variant: "summary", product: 0 },
  { id: "B-CK05", family: "checkout", title: "Processing state", note: "The commitment is locked while the local state is processing.", variant: "processing", product: 0 },
  { id: "B-CK06", family: "checkout", title: "Recoverable payment error", note: "Failure explains what happened and preserves a clear recovery path.", variant: "error", product: 0 },
  { id: "B-CK07", family: "checkout", title: "Digital access confirmation", note: "Confirmation sends the buyer into the first useful setup action.", variant: "confirmation-digital", product: 0 },
  { id: "B-CK08", family: "checkout", title: "SaaS workspace confirmation", note: "The subscription state continues into team and workspace setup.", variant: "confirmation-saas", product: 0 },

  { id: "B-BU01", family: "bundles", title: "Fixed complete suite", note: "A bounded product stack is sold as one clear fixed offer.", variant: "fixed", product: 0 },
  { id: "B-BU02", family: "bundles", title: "Configurable bundle builder", note: "Native controls update a transparent illustrative total.", variant: "builder", product: 0 },
  { id: "B-BU03", family: "bundles", title: "Focused product stack", note: "A three-product relationship with measured, legible overlap.", variant: "stack", product: 0 },
  { id: "B-BU04", family: "bundles", title: "Bundle comparison", note: "Focused stack and complete suite retain equal decision geometry.", variant: "comparison", product: 0 },
  { id: "B-BU05", family: "bundles", title: "Checkout order bump", note: "An optional addition starts unchecked and states its exact delta.", variant: "order-bump", product: 3 },
  { id: "B-BU06", family: "bundles", title: "Cart cross-sell", note: "A relevant adjacent system with equally clear accept and decline.", variant: "cart-upsell", product: 1 },
  { id: "B-BU07", family: "bundles", title: "Order upgrade", note: "The buyer can compare the current order with a two-system upgrade.", variant: "upgrade", product: 1 },
  { id: "B-BU08", family: "bundles", title: "Post-purchase addition", note: "The completed order is never held hostage by the optional offer.", variant: "post-purchase", product: 4 },

  { id: "B-MB01", family: "mobile", title: "Mobile product discovery", note: "A phone-sized product browse flow with intent-triggered summary.", variant: "discovery", product: 0 },
  { id: "B-MB02", family: "mobile", title: "Mobile plan selection", note: "Cadence, plan and sticky action preserve the current decision.", variant: "pricing", product: 0 },
  { id: "B-MB03", family: "mobile", title: "Mobile checkout summary", note: "An expandable order summary and safe-area action stay accessible.", variant: "checkout", product: 0 },
  { id: "B-MB04", family: "mobile", title: "Mobile confirmation and upsell", note: "Access confirmation leads; the optional addition remains secondary.", variant: "confirmation", product: 0 },
]);

const FAMILY_BUILDERS = Object.freeze({
  discovery: discoveryCanvas,
  features: featureCanvas,
  pricing: pricingCanvas,
  checkout: checkoutCanvas,
  bundles: bundleCanvas,
  mobile: mobileCanvas,
});

export const specimenCount = SPECS.length;
export const specimenIds = SPECS.map((spec) => spec.id);

export function buildRound(products) {
  const source = Array.isArray(products) ? products : products?.products;
  const alreadyNormalized = Array.isArray(source)
    && source.length > 0
    && source.every((product) => product.extendedName && product.staticField && product.fixtureOffer);
  const viewModels = alreadyNormalized ? source : productViewModel(source);
  return SPECS.map((spec) => {
    const product = viewModels[spec.product % viewModels.length];
    const canvas = FAMILY_BUILDERS[spec.family](spec, product, viewModels);
    return reviewable(spec, canvas);
  });
}

const boundRoots = new WeakSet();

function setExclusivePressed(container, target, selector) {
  container.querySelectorAll(selector).forEach((item) => item.setAttribute("aria-pressed", String(item === target)));
}

function updateCadence(control, cadence) {
  const scope = control.closest(".pb-specimen__canvas") || control.parentElement;
  control.dataset.cadenceValue = cadence;
  setExclusivePressed(control, control.querySelector(`[data-cadence="${cadence}"]`), "[data-cadence]");
  scope.querySelectorAll("[data-monthly][data-annual]").forEach((amount) => {
    const value = Number(amount.dataset[cadence]);
    if (Number.isFinite(value)) amount.textContent = FORMAT_CURRENCY.format(value);
  });
  scope.querySelectorAll("[data-cadence-label]").forEach((label) => {
    label.textContent = cadence === "annual" ? "/ month · billed annually" : "/ month";
  });
}

function updateUsage(range) {
  const scope = range.closest(".pb-usage-calculator");
  const count = Number(range.value);
  const base = Number(range.dataset.base);
  const unit = Number(range.dataset.unit);
  scope.querySelector("[data-usage-count]").textContent = `${count} ${count === 1 ? "operator" : "operators"}`;
  scope.querySelector("[data-usage-total]").textContent = `${FORMAT_CURRENCY.format(base + count * unit)} / month`;
  const action = scope.querySelector(".pb-button--solid");
  if (action) action.textContent = `Start with ${count} ${count === 1 ? "operator" : "operators"}`;
}

function updateBundle(input) {
  const scope = input.closest(".pb-bundle-builder");
  const selected = [...scope.querySelectorAll("[data-bundle-option]:checked")];
  const total = selected.reduce((sum, item) => sum + Number(item.dataset.price || 0), 0);
  scope.querySelector("[data-bundle-total]").textContent = FORMAT_CURRENCY.format(total);
  scope.querySelector("[data-bundle-count]").textContent = `${selected.length} systems selected`;
  const action = scope.querySelector(".pb-bundle-builder__summary .pb-button");
  action.disabled = selected.length < 2;
}

function toggleAccordion(trigger) {
  const panel = trigger.nextElementSibling;
  const expanded = trigger.getAttribute("aria-expanded") === "true";
  trigger.setAttribute("aria-expanded", String(!expanded));
  if (panel) panel.hidden = expanded;
  const marker = trigger.querySelector("span:last-child");
  if (marker) marker.textContent = expanded ? "+" : "−";
}

export function bindSpecimenInteractions(root) {
  if (!root || boundRoots.has(root)) return;
  boundRoots.add(root);

  root.addEventListener("click", (event) => {
    const verdict = event.target.closest("[data-verdict]");
    if (verdict && root.contains(verdict)) {
      const article = verdict.closest("[data-specimen-id]");
      article.dataset.verdict = verdict.dataset.verdict;
      setExclusivePressed(verdict.parentElement, verdict, "[data-verdict]");
      article.dispatchEvent(new CustomEvent("pb:verdict", { bubbles: true, detail: { id: article.dataset.specimenId, verdict: verdict.dataset.verdict } }));
      return;
    }

    const cadence = event.target.closest("[data-cadence]");
    if (cadence && root.contains(cadence)) {
      updateCadence(cadence.closest("[data-cadence-control]"), cadence.dataset.cadence);
      return;
    }

    const accordion = event.target.closest("[data-accordion-trigger]");
    if (accordion && root.contains(accordion)) {
      toggleAccordion(accordion);
      return;
    }

    const selectable = event.target.closest("[data-local-select]");
    if (selectable && root.contains(selectable)) {
      setExclusivePressed(selectable.parentElement, selectable, "[data-local-select]");
      return;
    }

    const toggle = event.target.closest("[data-local-toggle]");
    if (toggle && root.contains(toggle)) {
      const selected = toggle.getAttribute("aria-pressed") !== "true";
      toggle.setAttribute("aria-pressed", String(selected));
      toggle.textContent = selected ? "Added" : toggle.dataset.localToggle === "upgrade" ? "Upgrade my order" : "Add to order";
      return;
    }

    const localState = event.target.closest("[data-local-state]");
    if (localState && root.contains(localState)) {
      const scope = localState.closest(".pb-specimen__canvas");
      const status = scope.querySelector("[data-local-status]");
      if (status) status.textContent = `Review state: ${localState.dataset.localState}`;
      localState.setAttribute("aria-busy", localState.dataset.localState === "processing" ? "true" : "false");
    }
  });

  root.addEventListener("input", (event) => {
    const range = event.target.closest("[data-usage-slider]");
    if (range && root.contains(range)) updateUsage(range);
  });

  root.addEventListener("change", (event) => {
    const bundle = event.target.closest("[data-bundle-option]");
    if (bundle && root.contains(bundle)) updateBundle(bundle);

    const upsell = event.target.closest("[data-upsell-toggle]");
    if (upsell && root.contains(upsell)) {
      const scope = upsell.closest(".pb-order-bump");
      const base = Number(scope.querySelector("[data-upsell-total]").dataset.base);
      const delta = upsell.checked ? Number(upsell.dataset.price) : 0;
      scope.querySelector("[data-upsell-total]").textContent = `Order total · ${FORMAT_CURRENCY.format(base + delta)}`;
    }
  });

  root.addEventListener("input", (event) => {
    const note = event.target.closest("[data-specimen-note]");
    if (!note || !root.contains(note)) return;
    const article = note.closest("[data-specimen-id]");
    article.dispatchEvent(new CustomEvent("pb:note", { bubbles: true, detail: { id: article.dataset.specimenId, note: note.value } }));
  });
}
