const decisionDefinitions = [
  {
    id: "primaryFamily",
    title: "Primary system",
    prompt: "Which family should define Mez across marketing, product names, commerce and everyday UI?",
    options: [
      ["inter-tuned", "Tuned Inter"],
      ["instrument-sans", "Instrument Sans"],
      ["geist", "Geist"],
      ["none", "None are right"],
    ],
  },
  {
    id: "displayFamily",
    title: "Display voice",
    prompt: "Which family makes the large homepage proposition feel most intentional and recognisable?",
    options: [
      ["inter-tuned", "Tuned Inter"],
      ["instrument-sans", "Instrument Sans"],
      ["geist", "Geist"],
      ["none", "None are right"],
    ],
  },
  {
    id: "bodyFamily",
    title: "Reading voice",
    prompt: "Which family is calmest and clearest in explanations, product copy and longer reading?",
    options: [
      ["inter-tuned", "Tuned Inter"],
      ["instrument-sans", "Instrument Sans"],
      ["geist", "Geist"],
      ["none", "None are right"],
    ],
  },
  {
    id: "serifPolicy",
    title: "Serif policy",
    prompt: "Should the old Instrument Serif moment disappear, become contextual, or remain a once-per-page rule?",
    options: [
      ["remove-default", "Remove by default"],
      ["contextual-only", "Contextual only"],
      ["once-per-page", "Keep once per page"],
    ],
  },
  {
    id: "monoPolicy",
    title: "Mono and data",
    prompt: "How should codes, versions, provenance and compact system data behave?",
    options: [
      ["keep-ibm-plex", "Keep IBM Plex Mono"],
      ["primary-numerals", "Use primary numerals"],
      ["study-separately", "Study mono separately"],
    ],
  },
  {
    id: "mobileType",
    title: "Mobile type system",
    prompt: "Do the proposed mobile sizes, wraps and hierarchy deserve to move forward?",
    options: [
      ["advance", "Advance"],
      ["edit", "Edit"],
      ["reject", "Reject"],
    ],
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
  progressNodes.forEach((node) => { node.textContent = `${completed}/6`; });
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
    studyId: "MEZ-TYPOGRAPHY-SYSTEM-01",
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
    console.error("[mez-typography-calibration] Could not copy review JSON.", error);
    copyState.textContent = "Clipboard access failed. The export is in the browser console.";
    console.info(JSON.stringify(record, null, 2));
  }
});
