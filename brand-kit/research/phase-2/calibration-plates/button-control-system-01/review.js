const decisionDefinitions = [
  {
    id: "shape",
    title: "Control shape",
    prompt: "Which radius feels rounded and premium without turning every action into a capsule?",
    options: [["moderate-12", "12px moderate"], ["soft-14", "14px soft"], ["pill", "Full pill"], ["none", "None are right"]],
  },
  {
    id: "hierarchy",
    title: "Action hierarchy",
    prompt: "Which primary, secondary and tertiary relationship should govern marketing and commerce?",
    options: [["solid-outline-text", "Solid, outline, text"], ["solid-soft-text", "Solid, soft fill, text"], ["edit", "Needs editing"]],
  },
  {
    id: "depth",
    title: "Interaction depth",
    prompt: "How much physical response should a pointer action create?",
    options: [["micro-lift", "One-pixel micro lift"], ["press-only", "Press response only"], ["flat", "Always flat"], ["edit", "Needs editing"]],
  },
  {
    id: "scale",
    title: "Control scale",
    prompt: "Which default size feels premium and remains reliable for a mobile-heavy audience?",
    options: [["48-default", "48px default"], ["44-default", "44px default"], ["edit", "Needs editing"]],
  },
  {
    id: "iconPolicy",
    title: "Icon policy",
    prompt: "When should arrows and utility icons appear?",
    options: [["selective-directional", "Selective and directional"], ["always", "On every action"], ["none", "No button icons"]],
  },
  {
    id: "darkSurface",
    title: "Dark-section hierarchy",
    prompt: "How should action hierarchy invert on a near-black bundle or final section?",
    options: [["white-primary-outline-secondary", "White primary, light outline"], ["ink-primary-white-secondary", "Ink primary on white panel"], ["edit", "Needs editing"]],
  },
  {
    id: "mobileBehaviour",
    title: "Mobile behaviour",
    prompt: "How should paired hero actions compress on a narrow viewport?",
    options: [["primary-full-secondary-link", "Full primary, text secondary"], ["paired-full-width", "Two full-width buttons"], ["edit", "Needs editing"]],
  },
];

const reviewDrawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const decisionRoot = document.querySelector("[data-decisions]");
const progressNodes = [...document.querySelectorAll("[data-progress]")];
const copyState = document.querySelector("[data-copy-state]");

decisionRoot.innerHTML = decisionDefinitions.map((definition, index) => `
  <fieldset data-decision="${definition.id}">
    <legend><span>${String(index + 1).padStart(2, "0")}</span>${definition.title}</legend>
    <p>${definition.prompt}</p>
    <div class="decision-options">
      ${definition.options.map(([value, label]) => `
        <label><input type="radio" name="${definition.id}" value="${value}"><span>${label}</span></label>
      `).join("")}
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
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setDrawer(false);
});
document.querySelectorAll("input[type=radio]").forEach((input) => input.addEventListener("change", updateProgress));

document.querySelector("[data-review-form]").addEventListener("submit", async (event) => {
  event.preventDefault();
  const decisions = {};
  let complete = true;

  decisionDefinitions.forEach(({id}) => {
    const selected = document.querySelector(`input[name="${id}"]:checked`);
    if (!selected) complete = false;
    decisions[id] = {
      decision: selected?.value || "",
      note: document.querySelector(`textarea[name="${id}Note"]`).value.trim(),
    };
  });

  const record = {
    schemaVersion: "1.0.0",
    studyId: "MEZ-BUTTON-CONTROL-SYSTEM-01",
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
    console.error("[mez-control-calibration] Could not copy review JSON.", error);
    copyState.textContent = "Clipboard access failed. The export is in the browser console.";
    console.info(JSON.stringify(record, null, 2));
  }
});
