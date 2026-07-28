/** Mez Systems · Product Card 02 · Round 10 hierarchy-lock matrix. */
export const STATIC_FIELD_BASE = "../../../gradient-library/assets/static/";
export const WINGS_URL = "../../../source-pack/design-system-export/assets/wings.svg";

export function h(tag, className = "", text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function productViewModel(products) {
  return products.map(product => ({
    ...product,
    role: product.function,
    job: product.summary,
    field: `${STATIC_FIELD_BASE}${product.gradientId.toLowerCase()}.webp`,
    action: product.availability === "live" ? "Explore AI OS" : "Join waitlist",
    availabilityLabel: product.availability === "live" ? "Available now" : "Coming soon"
  }));
}

function wings(className = "wings") {
  const image = h("img", className);
  image.src = WINGS_URL;
  image.alt = "";
  return image;
}

function material(product, className = "material", live = false) {
  const node = h("div", className);
  node.style.setProperty("--field", `url("${product.field}")`);
  node.dataset.gradientId = product.gradientId;
  if (live) node.dataset.autoLive = "";
  return node;
}

function action(label, treatment = "solid") {
  const node = h("button", `action action--${treatment}`, label);
  node.type = "button";
  if (treatment === "text") node.append(h("span", "action-arrow", "↗"));
  return node;
}

function productCopy(product, spec = {}) {
  const copy = h("div", "product-copy");
  copy.append(h("h4", "", product.publicName));
  copy.append(h("span", "product-extended", product.role));
  if (!spec.minimal) copy.append(h("p", "", product.job));
  copy.append(action(product.action, spec.button || "solid"));
  return copy;
}

function pair(build, product, products) {
  const wrap = h("div", "state-pair");
  [["Static", false], ["Animated", true]].forEach(([label, live]) => {
    const pane = h("div", `state-pane state-pane--${live ? "motion" : "still"}`);
    pane.append(h("span", "state-label", label), build(product, products, live));
    wrap.append(pane);
  });
  return wrap;
}

function verdicts(id) {
  const controls = h("div", "study-controls");
  [["keep", "Keep"], ["revise", "Revise"], ["kill", "Kill"]].forEach(([verdict, label]) => {
    const button = h("button", "", label);
    button.type = "button";
    button.dataset.verdict = verdict;
    button.setAttribute("aria-label", `${label} ${id}`);
    controls.append(button);
  });
  return controls;
}

function reviewable(spec, products, build) {
  const product = products[spec.product % products.length];
  const item = h("article", `study study--${spec.family} study--${spec.scale || "standard"}`);
  item.dataset.specimenId = spec.id;
  item.dataset.specimenTitle = spec.title;
  item.dataset.specimenFamily = spec.family;
  const head = h("header", "study-head");
  const identity = h("div", "study-identity");
  identity.append(h("span", "study-id", spec.id), h("h3", "", spec.title), h("p", "", spec.note));
  head.append(identity, verdicts(spec.id));
  const canvas = h("div", "study-canvas");
  canvas.append(pair(build, product, products));
  const feedback = h("label", "study-feedback");
  feedback.append(h("span", "study-feedback-label", `Feedback on ${spec.id}`));
  const note = h("textarea", "study-feedback-input");
  note.dataset.specimenNote = spec.id;
  note.rows = 1;
  note.placeholder = `What should change, stay, or be explored in ${spec.title}?`;
  feedback.append(note);
  item.append(head, canvas, feedback);
  return item;
}

function landing(spec) {
  return (product, products, live) => {
    const card = h("section", `landing-card landing-card--${spec.layout} mark--${spec.mark} ratio--${spec.ratio || "wide"}${spec.dark ? " is-dark" : ""}${spec.reverse ? " is-reverse" : ""}${spec.largeMark ? " mark--large" : ""}`);
    const field = material(product, "material landing-field", live);
    const copy = productCopy(product, {...spec, button: spec.dark ? "light" : "solid"});
    if (spec.mark === "above") copy.prepend(wings("wings wings--copy"));
    else field.append(wings());
    if (["quiet", "immersive", "frame"].includes(spec.layout)) field.append(copy);
    else card.append(copy);
    card.append(field);
    return card;
  };
}

function productCard(spec) {
  return (product, products, live) => {
    const card = h("article", `product-card product-card--${spec.layout} mark--${spec.mark}${spec.darkFooter ? " footer--dark" : ""}${spec.allDark ? " card--all-dark" : ""}${spec.largeMark ? " mark--large" : ""}`);
    const field = material(product, "material product-field", live);
    field.append(wings());
    const copy = h("div", "card-copy");
    copy.append(h("h4", "", product.publicName), h("span", "product-extended", product.role), h("p", "", product.job));
    const footer = h("footer", "product-footer");
    footer.append(h("span", "status", product.availabilityLabel), action(product.action, spec.darkFooter || spec.allDark ? "light" : "solid"));
    card.append(field, copy, footer);
    return card;
  };
}

function bundle(spec) {
  return (product, products, live) => {
    const pack = h("section", `bundle bundle--${spec.layout} mark--${spec.mark}${spec.dark ? " is-dark" : ""}${spec.darkFooter ? " footer--dark" : ""}${spec.flush ? " media--flush" : ""}${spec.noStroke ? " no-stroke" : ""}`);
    const deck = h("div", "bundle-deck");
    const items = products.slice(0, spec.layout === "single" ? 1 : 5);
    const leadIndex = ["stack", "fan", "boxed"].includes(spec.layout) ? items.length - 1 : 0;
    items.forEach((item, index) => {
      const isLead = index === leadIndex;
      const card = h("article", `bundle-card${isLead ? " is-lead" : ""}`);
      card.style.setProperty("--index", index);
      const field = material(item, "material bundle-field", live && isLead);
      if (isLead) field.append(wings());
      const footer = h("div", "bundle-card-footer");
      footer.append(h("strong", "", item.publicName));
      if (isLead && spec.moreCopy) footer.append(h("small", "", item.summary));
      card.append(field, footer);
      deck.append(card);
    });
    const copy = h("div", "bundle-copy");
    copy.append(h("span", "eyebrow", "THE MEZ SYSTEMS SUITE"), h("h4", "", spec.headline || "Build the operating layer your company needs."), h("p", "", spec.copy || "Five specialised products. One shared visual and operating language."), action("Explore the suite", spec.button || "solid"));
    pack.append(deck, copy);
    return pack;
  };
}

function section(spec) {
  return (product, products, live) => {
    const shell = h("section", `site-section site-section--${spec.layout} mark--${spec.mark}${spec.dark ? " is-dark" : ""}${spec.reverse ? " is-reverse" : ""}${spec.largeMark ? " mark--large" : ""}`);
    if (spec.layout === "hero") {
      const copy = productCopy(product, {...spec, button:"solid"});
      const field = material(product, "material site-hero-field", live);
      field.append(wings());
      shell.append(copy, field);
    }
    if (spec.layout === "shelf") {
      const head = h("header", "site-heading");
      head.append(h("span", "eyebrow", "MEZ SYSTEMS PRODUCTS"), h("h4", "", "Systems for the work between strategy and execution."));
      const rail = h("div", "site-rail");
      products.slice(0, 4).forEach((item, index) => {
        const card = h("article", "site-rail-card");
        const field = material(item, "material site-rail-field", live && index === 0);
        field.append(wings());
        card.append(field, h("span", "eyebrow", item.function), h("strong", "", item.publicName), h("p", "", item.summary));
        rail.append(card);
      });
      shell.append(head, rail);
    }
    if (spec.layout === "explainer") {
      const field = material(product, "material explainer-field", live);
      field.append(wings());
      const copy = h("div", "explainer-copy");
      copy.append(h("span", "eyebrow", "HOW IT WORKS"), h("h4", "", product.publicName), h("p", "", product.job));
      const sequence = h("ol", "explainer-sequence");
      ["Connect business context", "Turn decisions into runs", "Keep proof attached"].forEach(item => sequence.append(h("li", "", item)));
      copy.append(sequence);
      shell.append(field, copy);
    }
    if (spec.layout === "offer") {
      const field = material(product, "material offer-field", live);
      field.append(wings());
      const copy = h("div", "offer-copy");
      copy.append(h("span", "eyebrow", spec.label || "THE COMPLETE SYSTEM"), h("h4", "", spec.title), h("p", "", spec.copy), action(spec.buttonLabel || "See everything included", spec.button || "solid"));
      shell.append(field, copy);
    }
    return shell;
  };
}

const specs = [
  {id:"QC01",title:"Quiet · hierarchy locked",family:"landing",layout:"quiet",mark:"corner",largeMark:true,note:"R09 revise · larger Wings · public name first · filled action",product:0,scale:"wide"},
  {id:"QC02",title:"Quiet · mark above locked",family:"landing",layout:"quiet",mark:"above",largeMark:true,note:"R09 revise · larger Wings · public name first · filled action",product:0,scale:"wide"},
  {id:"QC03",title:"Quiet · centred hierarchy",family:"landing",layout:"quiet",mark:"center",minimal:true,note:"R09 revise · public name first · filled action",product:0,scale:"wide"},
  {id:"QC04",title:"Quiet · portrait locked",family:"landing",layout:"quiet",mark:"corner",largeMark:true,ratio:"portrait",note:"R09 revise · larger Wings · public name first · filled action",product:0},
  {id:"ES02",title:"Split · centred field",family:"landing",layout:"split",mark:"center",note:"R09 keep · family filled-action rule applied",product:1,scale:"wide"},
  {id:"ES04",title:"Split · vertical",family:"landing",layout:"split",mark:"center",ratio:"portrait",note:"R09 keep · family filled-action rule applied",product:1},
  {id:"IC01",title:"Immersive · corner locked",family:"landing",layout:"immersive",mark:"corner",largeMark:true,note:"R09 revise · larger Wings · canonical AI Ads hierarchy",product:2,scale:"wide"},
  {id:"IC02",title:"Immersive · mark above locked",family:"landing",layout:"immersive",mark:"above",largeMark:true,note:"R09 revise · larger Wings · canonical AI Ads hierarchy",product:2,scale:"wide"},
  {id:"IC03",title:"Immersive · centred hierarchy",family:"landing",layout:"immersive",mark:"center",minimal:true,note:"R09 revise · canonical AI Ads hierarchy · filled action",product:2,scale:"wide"},
  {id:"HL01",title:"Launch · corner hierarchy",family:"landing",layout:"launch",mark:"corner",dark:true,note:"R09 revise · Organic Content OS first · extended name second",product:4,scale:"wide"},
  {id:"HL02",title:"Launch · centred hierarchy",family:"landing",layout:"launch",mark:"center",dark:true,note:"R09 revise · Organic Content OS first · filled action",product:4,scale:"wide"},
  {id:"HL04",title:"Launch · portrait",family:"landing",layout:"launch",mark:"center",dark:true,ratio:"portrait",note:"R09 keep · family hierarchy and filled-action rules applied",product:4},
  {id:"QF01",title:"Frame · hierarchy locked",family:"landing",layout:"frame",mark:"corner",note:"R09 revise · Claude Code OS first · extended name second",product:3,scale:"wide"},
  {id:"QF03",title:"Frame · portrait simplified",family:"landing",layout:"frame",mark:"above",largeMark:true,ratio:"portrait",note:"R09 keep · family hierarchy and filled-action rules applied",product:3},

  {id:"FC01",title:"Full field · hierarchy locked",family:"cards",layout:"footer",mark:"center",largeMark:true,note:"R09 revise · larger Wings · public name first · filled action",product:0},
  {id:"FC02",title:"Full field · continuous dark locked",family:"cards",layout:"footer",mark:"center",largeMark:true,darkFooter:true,allDark:true,note:"R09 revise · larger Wings · public name first · filled action",product:0},
  {id:"PO01",title:"Portrait · corner hierarchy",family:"cards",layout:"portrait",mark:"corner",largeMark:true,note:"R09 revise · larger Wings · public name first · filled action",product:1},
  {id:"PO02",title:"Portrait · centred hierarchy",family:"cards",layout:"portrait",mark:"center",largeMark:true,note:"R09 revise · larger Wings · public name first · filled action",product:1},

  {id:"ST01",title:"Stack · flat media join",family:"bundles",layout:"stack",mark:"corner",flush:true,note:"R08 revise · flat material-to-footer line",product:0,scale:"wide"},
  {id:"ST02",title:"Stack · clean dark footer",family:"bundles",layout:"stack",mark:"center",darkFooter:true,flush:true,noStroke:true,moreCopy:true,note:"R08 revise · no white stroke · centred identity",product:0,scale:"wide"},
  {id:"SG01",title:"Single · light integrated card",family:"bundles",layout:"single",mark:"center",flush:true,noStroke:true,moreCopy:true,note:"New from ST02 · one light card instead of a stack",product:0,scale:"wide"},
  {id:"FN01",title:"Fan · measured spread",family:"bundles",layout:"fan",mark:"corner",flush:true,noStroke:true,note:"R09 revise · smaller cards · even separation · no copy collision",product:1,scale:"wide"},
  {id:"BX01",title:"Boxed suite · light refined",family:"bundles",layout:"boxed",mark:"corner",flush:true,noStroke:true,moreCopy:true,note:"R08 revise · cleaner contained suite",product:2,scale:"wide"},
  {id:"BX02",title:"Boxed suite · dark refined",family:"bundles",layout:"boxed",mark:"center",dark:true,darkFooter:true,flush:true,noStroke:true,note:"R08 revise · dark contained suite · centred identity",product:2,scale:"wide"},

  {id:"SH01",title:"Hero · corner hierarchy",family:"sections",layout:"hero",mark:"corner",largeMark:true,note:"R09 revise · larger Wings · AI OS first · filled action",product:0,scale:"full"},
  {id:"SH02",title:"Hero · centred field left locked",family:"sections",layout:"hero",mark:"center",largeMark:true,reverse:true,note:"R09 revise · larger Wings · AI OS first · filled action",product:0,scale:"full"},
  {id:"SH03",title:"Hero · centred field right locked",family:"sections",layout:"hero",mark:"center",largeMark:true,note:"R09 revise · larger Wings · AI OS first · filled action",product:0,scale:"full"},
  {id:"FS01",title:"Family shelf · light refined",family:"sections",layout:"shelf",mark:"center",note:"R08 revise · aligned light family",product:1,scale:"full"},
  {id:"FS02",title:"Family shelf · charcoal",family:"sections",layout:"shelf",mark:"center",dark:true,note:"R08 keep · contained dark family",product:1,scale:"full"},
  {id:"EX02",title:"Explainer · centred Wings",family:"sections",layout:"explainer",mark:"center",reverse:true,note:"R08 keep · centred identity on material",product:2,scale:"full"},
  {id:"BO01",title:"Start with one. Build the whole operating layer.",family:"sections",layout:"offer",mark:"center",dark:true,label:"THE COMPLETE SYSTEM",copy:"A coherent suite that grows with the company.",buttonLabel:"See everything included",button:"light",note:"R08 keep · section champion",product:3,scale:"full"},
  {id:"BO02",title:"Five systems. One operating layer.",family:"sections",layout:"offer",mark:"center",label:"MEZ SYSTEMS SUITE",copy:"Choose the product that removes today's constraint, then grow into the complete suite.",buttonLabel:"Explore the suite",button:"outline",note:"R08 revise · centred Wings",product:3,scale:"full"}
];

const builders = {landing, cards: productCard, bundles: bundle, sections: section};

export function buildLibrary(products) {
  return specs.map(spec => reviewable(spec, products, builders[spec.family](spec)));
}

export const specimenCount = specs.length;
export const specimenIds = specs.map(spec => spec.id);
