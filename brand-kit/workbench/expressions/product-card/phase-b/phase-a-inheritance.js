/**
 * Product Card 02 · Phase B · approved Phase A expression bridge.
 *
 * This module consumes the canonical Round 10 builders without editing them.
 * Each approved expression is presented as a Phase B application candidate with
 * its original static/automatic twin and a declared functional website job.
 */
import { buildLibrary as buildApprovedPhaseALibrary } from "../card-components.js";

// The inherited cards consume this value through Phase A's ../styles.css, so
// CSS resolves the URL from the parent product-card directory rather than from
// the Phase B document. Keep the canonical Phase A-relative path here.
const STATIC_FIELD_BASE = "../../../gradient-library/assets/static/";
const WINGS_URL = "../../../../source-pack/design-system-export/assets/wings.svg";

const FAMILY_MAP = Object.freeze({
  landing: "phase-a-landing",
  cards: "phase-a-cards",
  bundles: "phase-a-bundles",
  sections: "phase-a-sections",
});

const BRIDGE_META = Object.freeze({
  QC01: { job: "Primary product launch hero", placement: "Product landing · first viewport", behavior: "Filled launch action · corner identity", description: "Use the quiet plate when the product proposition and one conversion action need to lead." },
  QC02: { job: "Identity-led product hero", placement: "Product landing · brand-first opening", behavior: "Large mark above · filled launch action", description: "Use the mark-above composition when the Wings should introduce the product before the headline." },
  QC03: { job: "Centred conversion plate", placement: "Campaign landing · focused decision", behavior: "Centred identity · minimal copy · filled action", description: "A reduced, centred opening for one product and one unambiguous next step." },
  QC04: { job: "Portrait product placement", placement: "Mobile hero · editorial side rail", behavior: "Portrait receiver · corner identity", description: "The quiet family adapted to a narrow receiver without losing the product-first hierarchy." },
  ES02: { job: "Featured product split", placement: "Homepage feature · product introduction", behavior: "Copy and material split · centred Wings", description: "A balanced editorial split for explaining one system beside its focal product material." },
  ES04: { job: "Vertical feature story", placement: "Mobile feature · narrow explainer", behavior: "Vertical split · centred identity", description: "The split family linearised for compact receivers and long-form product storytelling." },
  IC01: { job: "Immersive campaign hero", placement: "Campaign landing · launch moment", behavior: "Edge crop · corner identity · filled action", description: "A high-energy product opening where the material owns most of the viewport." },
  IC02: { job: "Immersive identity feature", placement: "Product page · signature section", behavior: "Large mark above · material field", description: "An immersive field with a stronger branded introduction and restrained supporting copy." },
  IC03: { job: "Immersive centred conversion", placement: "Launch page · singular action", behavior: "Centred identity · minimal hierarchy", description: "A cinematic but disciplined product moment for a single launch proposition." },
  HL01: { job: "Dark availability launch", placement: "Coming-soon page · waitlist hero", behavior: "Contained dark · corner identity", description: "A dark launch treatment for availability, release or waitlist communication." },
  HL02: { job: "Dark centred launch", placement: "Release campaign · conversion hero", behavior: "Contained dark · centred Wings · filled action", description: "The launch family with the product identity held centrally inside the dark room." },
  HL04: { job: "Mobile dark launch", placement: "Mobile campaign · sticky conversion entry", behavior: "Portrait dark receiver · centred identity", description: "A narrow dark launch expression that keeps the primary action and hierarchy intact." },
  QF01: { job: "Framed proof introduction", placement: "Case study · proof-led feature", behavior: "Quiet frame · corner identity", description: "A bounded product frame that can introduce proof without turning into a generic screenshot card." },
  QF03: { job: "Compact framed feature", placement: "Integration page · supporting placement", behavior: "Portrait frame · mark above", description: "A framed narrow placement for integrations, feature rails and supporting product stories." },

  FC01: { job: "Standard product discovery card", placement: "Product shelf · navigation · pricing lead-in", behavior: "Full field · integrated light footer", description: "The primary repeatable product-card anatomy for discovery and commercial entry points." },
  FC02: { job: "Selected dark product card", placement: "Featured plan · selected product · dark shelf", behavior: "Continuous charcoal chassis · light action", description: "A higher-contrast product card for a selected or featured decision without decorative glow." },
  PO01: { job: "Portrait feature card", placement: "Feature rail · checkout add-on", behavior: "Portrait field · corner identity", description: "A narrower product card for feature discovery, related products and optional additions." },
  PO02: { job: "Centred portrait selector", placement: "Product picker · plan selector", behavior: "Portrait field · centred Wings", description: "A selectable portrait card whose centred identity remains legible in a repeated family." },

  ST01: { job: "Bundle contents preview", placement: "Suite offer · bundle introduction", behavior: "Measured stack · flat media join", description: "A stacked relationship that shows several products belong to one offer without hiding their identity." },
  ST02: { job: "Dark fixed-suite offer", placement: "Bundle pricing · checkout package", behavior: "Stack · clean dark footer · lead cover", description: "A contained fixed bundle with one focal cover and static supporting products." },
  SG01: { job: "Single flagship offer", placement: "Pricing feature · checkout summary", behavior: "Integrated light card · no stack", description: "The stack anatomy reduced to one product for a flagship offer or purchase summary." },
  FN01: { job: "Configurable bundle preview", placement: "Bundle builder · product selection", behavior: "Measured fan · legible separation", description: "A fan used only when the buyer is choosing a relationship between several visible products." },
  BX01: { job: "Light complete-suite package", placement: "Bundle comparison · purchase package", behavior: "Contained light box · visible contents", description: "A bounded suite package for comparing a complete system against smaller offers." },
  BX02: { job: "Dark enterprise package", placement: "Enterprise offer · premium bundle", behavior: "Contained dark box · centred identity", description: "A dark suite package for a high-consideration offer with calm, explicit contents." },

  SH01: { job: "Product hero · corner field", placement: "Product page · desktop first viewport", behavior: "Copy left · material right · filled action", description: "A complete website hero using the approved corner-identity field and public-name-first hierarchy." },
  SH02: { job: "Product hero · reversed field", placement: "Product page · alternate chapter", behavior: "Material left · copy right · centred Wings", description: "The hero relationship reversed to create page rhythm without inventing a new design world." },
  SH03: { job: "Product hero · centred field", placement: "Product page · primary champion", behavior: "Copy left · centred Wings · filled action", description: "The strongest general product hero bridge for functional Phase B pages." },
  FS01: { job: "Light product-family catalogue", placement: "Homepage · product discovery", behavior: "Equal static siblings · light room", description: "A complete family shelf with equal geometry and registry-driven product count." },
  FS02: { job: "Contained-dark family shelf", placement: "Homepage · dark product chapter", behavior: "Equal static siblings · charcoal room", description: "The approved dark family system for a high-contrast discovery chapter." },
  EX02: { job: "Mechanism explainer section", placement: "Product page · how it works", behavior: "Centred material · ordered explanation", description: "A product explainer that pairs the focal material with an explicit operating sequence." },
  BO01: { job: "Complete-system bundle offer", placement: "Product page · final conversion", behavior: "Contained dark · section champion", description: "The Phase A champion for closing a page with one coherent suite proposition." },
  BO02: { job: "Product-family conversion offer", placement: "Homepage · suite transition", behavior: "Light room · centred Wings", description: "A family-level offer that helps someone move from one product into the complete operating layer." },
});

export const phaseASpecimenIds = Object.freeze(Object.keys(BRIDGE_META).map((id) => `B-A-${id}`));
export const phaseASpecimenCount = phaseASpecimenIds.length;

function element(tag, className = "", text = "") {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function normalizeProducts(products) {
  return products.map((product) => ({
    ...product,
    function: product.extendedName,
    role: product.extendedName,
    job: product.summary,
    field: `${STATIC_FIELD_BASE}${product.gradientId.toLowerCase()}.webp`,
    action: product.availability === "live" ? "Explore the product" : "Join waitlist",
    availabilityLabel: product.availability === "live" ? "Available now" : "Coming soon",
  }));
}

function functionalContext(sourceId, meta) {
  const context = element("aside", "phase-a-bridge-context");
  const intro = element("div", "phase-a-bridge-context__intro");
  intro.append(
    element("span", "phase-a-bridge-context__kicker", `APPROVED PHASE A · ${sourceId}`),
    element("strong", "phase-a-bridge-context__job", meta.job),
    element("p", "phase-a-bridge-context__description", meta.description),
  );
  const facts = element("dl", "phase-a-bridge-context__facts");
  [["Placement", meta.placement], ["Behaviour", meta.behavior]].forEach(([label, value]) => {
    const row = element("div");
    row.append(element("dt", "", label), element("dd", "", value));
    facts.append(row);
  });
  const state = element("span", "phase-a-bridge-context__state", "Fixture state · ready");
  state.setAttribute("aria-live", "polite");
  context.append(intro, facts, state);
  return context;
}

function adaptStudy(node) {
  const sourceId = node.dataset.specimenId;
  const sourceFamily = node.dataset.specimenFamily;
  const meta = BRIDGE_META[sourceId];
  if (!meta || !FAMILY_MAP[sourceFamily]) throw new Error(`Unknown approved Phase A bridge ${sourceId}`);

  const bridgeId = `B-A-${sourceId}`;
  node.classList.add("phase-a-bridge-study");
  node.dataset.phaseASource = sourceId;
  node.dataset.phaseARefs = sourceId;
  node.dataset.functionalJob = meta.job;
  node.dataset.specimenId = bridgeId;
  node.dataset.specimenFamily = FAMILY_MAP[sourceFamily];
  node.dataset.specimenTitle = `${node.dataset.specimenTitle} · ${meta.job}`;

  const identity = node.querySelector(".study-identity");
  identity.querySelector(".study-id").textContent = bridgeId;
  identity.querySelector("p").textContent = `Inherited ${sourceId} · ${meta.job} · ${meta.placement}`;

  node.querySelectorAll("[data-verdict]").forEach((button) => {
    const label = button.textContent.trim();
    button.setAttribute("aria-label", `${label} ${bridgeId}`);
  });

  const note = node.querySelector("[data-specimen-note]");
  note.dataset.specimenNote = bridgeId;
  note.placeholder = `What should stay, change or be explored in this ${meta.job.toLowerCase()}?`;
  node.querySelector(".study-feedback-label").textContent = `Feedback on ${bridgeId}`;

  node.querySelectorAll("img.wings").forEach((image) => { image.src = WINGS_URL; });

  if (["FS01", "FS02"].includes(sourceId)) {
    node.querySelectorAll("[data-auto-live]").forEach((field) => field.removeAttribute("data-auto-live"));
    node.querySelector(".state-pane--motion .state-label").textContent = "Static family · motion intentionally withheld";
  }

  const context = functionalContext(sourceId, meta);
  node.insertBefore(context, node.querySelector(".study-canvas"));

  node.querySelectorAll("button.action").forEach((action) => {
    action.dataset.bridgeAction = bridgeId;
    action.setAttribute("aria-pressed", "false");
    action.addEventListener("click", () => {
      const active = action.getAttribute("aria-pressed") !== "true";
      action.setAttribute("aria-pressed", String(active));
      action.closest(".state-pane")?.classList.toggle("is-actioned", active);
      context.querySelector(".phase-a-bridge-context__state").textContent = active
        ? `Fixture state · ${meta.job} action selected`
        : "Fixture state · ready";
    });
  });

  return node;
}

export function buildPhaseAInheritance(products) {
  const source = Array.isArray(products) ? products : products?.products;
  if (!Array.isArray(source) || source.length === 0) throw new TypeError("Phase A inheritance requires canonical products.");
  const nodes = buildApprovedPhaseALibrary(normalizeProducts(source)).map(adaptStudy);
  if (nodes.length !== phaseASpecimenCount) throw new Error(`Expected ${phaseASpecimenCount} approved Phase A bridges, received ${nodes.length}`);
  return nodes;
}
