const decisionDefinitions = [
  {
    id: "publicRoster",
    title: "Public product roster",
    prompt: "Which product family should the website research advance? Core assignments remain separate.",
    options: [["homepage-five", "Homepage five-product roster"], ["legacy-four", "Legacy four-product roster"], ["edit", "Needs editing"]],
  },
  {
    id: "familyChassis",
    title: "Family chassis",
    prompt: "How should multiple products appear together without becoming staggered or generic?",
    options: [["aligned-catalogue", "Aligned operating catalogue"], ["bordered-cards", "Independent bordered cards"], ["edit", "Needs editing"]],
  },
  {
    id: "territoryMethod",
    title: "Product distinction",
    prompt: "What should make each system feel different inside the shared family?",
    options: [["job-native-proof", "Job-native proof objects"], ["gradient-and-copy", "Gradient and copy only"], ["edit", "Needs editing"]],
  },
  {
    id: "expressionMode",
    title: "Product expression",
    prompt: "What belongs inside repeated product and commerce contexts?",
    options: [["static-core-plus-proof", "Static core plus proof object"], ["static-core-only", "Static core only"], ["proof-only", "Proof object only"], ["edit", "Needs editing"]],
  },
  {
    id: "availabilityHierarchy",
    title: "Availability hierarchy",
    prompt: "How strongly should AI OS lead while the rest of the family is coming soon?",
    options: [["one-live-future-quiet", "One live product, future kept quiet"], ["equal-family", "All products get equal weight"], ["edit", "Needs editing"]],
  },
  {
    id: "commerceSequence",
    title: "Commerce sequence",
    prompt: "When should bundle composition enter the public purchase journey?",
    options: [["live-first-bundle-later", "Sell AI OS now, bundle later"], ["bundle-first", "Lead with the future bundle"], ["edit", "Needs editing"]],
  },
  {
    id: "mobileBehaviour",
    title: "Mobile behavior",
    prompt: "How should the product family and purchase action compress on mobile?",
    options: [["vertical-catalogue-sticky-summary", "Vertical catalogue and purchase summary"], ["swipe-carousel", "Swipeable product carousel"], ["edit", "Needs editing"]],
  },
];

const reviewDrawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const decisionRoot = document.querySelector("[data-decisions]");
const progressNodes = [...document.querySelectorAll("[data-progress]")];
const copyState = document.querySelector("[data-copy-state]");

decisionRoot.innerHTML = decisionDefinitions.map((definition) => `
  <fieldset data-decision="${definition.id}">
    <legend>${definition.title}</legend>
    <p>${definition.prompt}</p>
    <div class="decision-options">
      ${definition.options.map(([value, label]) => `<label><input type="radio" name="${definition.id}" value="${value}"><span>${label}</span></label>`).join("")}
    </div>
    <label class="decision-note">Note<textarea rows="2" name="${definition.id}Note" placeholder="Optional"></textarea></label>
  </fieldset>
`).join("");

function setDrawer(open) {
  reviewDrawer.setAttribute("aria-hidden", String(!open));
  document.body.classList.toggle("review-is-open", open);
  if (open) reviewDrawer.querySelector("input")?.focus();
}

function updateProgress() {
  const completed = decisionDefinitions.filter(({id}) => document.querySelector(`input[name="${id}"]:checked`)).length;
  progressNodes.forEach((node) => { node.textContent = `${completed}/7`; });
}

document.querySelectorAll("[data-open-review]").forEach((button) => button.addEventListener("click", () => setDrawer(true)));
document.querySelector("[data-close-review]").addEventListener("click", () => setDrawer(false));
backdrop.addEventListener("click", () => setDrawer(false));
document.addEventListener("keydown", (event) => { if (event.key === "Escape") setDrawer(false); });
document.querySelectorAll("input[type=radio]").forEach((input) => input.addEventListener("change", updateProgress));

document.querySelector("[data-review-form]").addEventListener("submit", async (event) => {
  event.preventDefault();
  const decisions = {};
  let complete = true;
  decisionDefinitions.forEach(({id}) => {
    const selected = document.querySelector(`input[name="${id}"]:checked`);
    if (!selected) complete = false;
    decisions[id] = {decision: selected?.value || "", note: document.querySelector(`textarea[name="${id}Note"]`).value.trim()};
  });
  const record = {
    schemaVersion: "1.0.0",
    studyId: "MEZ-PRODUCT-FAMILY-COMMERCE-01",
    exportedAt: new Date().toISOString(),
    complete,
    productionAuthority: false,
    sourceExpressionApproved: false,
    decisions,
    overallNote: document.querySelector("textarea[name=overallNote]").value.trim(),
  };
  try {
    await navigator.clipboard.writeText(JSON.stringify(record, null, 2));
    copyState.textContent = complete ? "Copied. Paste this JSON into Codex." : "Copied, but some decisions are still empty.";
  } catch (error) {
    console.error("[mez-family-calibration] Could not copy review JSON.", error);
    copyState.textContent = "Clipboard access failed. The export is in the browser console.";
    console.info(JSON.stringify(record, null, 2));
  }
});
