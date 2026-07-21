const decisionDefinitions = [
  ["overallDirection", "Overall direction", "Does this finally point toward the Mez website we should keep building?"],
  ["heroComposition", "Hero composition", "Does the open split and oversized product object create the right first impression?"],
  ["typography", "Typography", "Does the simple sans-only hierarchy feel premium and specific enough?"],
  ["controls", "Buttons and controls", "Are the rounded, non-pill controls the right direction?"],
  ["mobileOpening", "Mobile opening", "Does mobile preserve proposition, action and product character?"],
];

const reviewDrawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const decisionRoot = document.querySelector("[data-decisions]");
const progress = document.querySelector("[data-progress]");
const copyState = document.querySelector("[data-copy-state]");

const decisionMarkup = decisionDefinitions.map(([id, title, prompt], index) => `
  <fieldset data-decision="${id}">
    <legend><span>${String(index + 1).padStart(2, "0")}</span>${title}</legend>
    <p>${prompt}</p>
    <div class="decision-options">
      ${["advance", "edit", "reject"].map((option) => `
        <label><input type="radio" name="${id}" value="${option}"><span>${option}</span></label>
      `).join("")}
    </div>
    <label class="decision-note">Note<textarea rows="2" name="${id}Note" placeholder="Optional"></textarea></label>
  </fieldset>
`).join("");

decisionRoot.innerHTML = decisionMarkup;

function setDrawer(open) {
  reviewDrawer.setAttribute("aria-hidden", String(!open));
  document.body.classList.toggle("review-is-open", open);
  if (open) reviewDrawer.querySelector("input")?.focus();
}

function updateProgress() {
  const completed = decisionDefinitions.filter(([id]) => document.querySelector(`input[name="${id}"]:checked`)).length;
  progress.textContent = `${completed}/5`;
}

document.querySelector("[data-open-review]").addEventListener("click", () => setDrawer(true));
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

  decisionDefinitions.forEach(([id]) => {
    const selected = document.querySelector(`input[name="${id}"]:checked`);
    if (!selected) complete = false;
    decisions[id] = {
      decision: selected?.value || "",
      note: document.querySelector(`textarea[name="${id}Note"]`).value.trim(),
    };
  });

  const record = {
    schemaVersion: "1.0.0",
    studyId: "MEZ-HERO-FIRST-VIEWPORT-01",
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
    console.error("[mez-hero-calibration] Could not copy review JSON.", error);
    copyState.textContent = "Clipboard access failed. Select and copy from the browser console export.";
    console.info(JSON.stringify(record, null, 2));
  }
});
