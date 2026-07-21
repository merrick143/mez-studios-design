import "./play-button.js";

const STORAGE_KEY = "mezIdentityProductObject01";
const STUDY_ID = "MEZ-IDENTITY-PRODUCT-OBJECT-01";
const state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"decisions":{},"overallNote":""}');

const panel = document.querySelector("#review-panel");
const scrim = document.querySelector("[data-scrim]");
const count = document.querySelector("[data-count]");
const status = document.querySelector("#review-status");

function setPanel(open) {
  panel.classList.toggle("open", open);
  scrim.classList.toggle("open", open);
  panel.setAttribute("aria-hidden", String(!open));
  document.querySelector(".review-open").setAttribute("aria-expanded", String(open));
  if (open) panel.querySelector(".review-close").focus();
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  const complete = Object.values(state.decisions).filter(item => item.decision).length;
  count.textContent = `${complete}/3`;
  status.textContent = complete === 3 ? "Ready to export" : `${complete} of 3 decisions complete`;
}

function hydrate() {
  document.querySelectorAll(".decision").forEach(group => {
    const key = group.dataset.key;
    const record = state.decisions[key] || {};
    group.querySelectorAll("[data-value]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.value === record.decision));
    });
    group.querySelector("[data-note]").value = record.note || "";
  });
  document.querySelector("[data-overall-note]").value = state.overallNote || "";
  save();
}

function exportRecord() {
  return {
    schemaVersion: "1.0.0",
    studyId: STUDY_ID,
    exportedAt: new Date().toISOString(),
    productionAuthority: false,
    sourceExpressionApproved: false,
    sourceGradient: "MZ-G13",
    sourceGradientSha256: "7932fb83949329ad562a13010221d2c0e6cad9f24312993acf781935547a946e",
    record: {
      decisions: state.decisions,
      overallNote: state.overallNote || "",
      productionAuthority: false
    }
  };
}

document.addEventListener("click", event => {
  const valueButton = event.target.closest("[data-value]");
  if (valueButton) {
    const group = valueButton.closest(".decision");
    const key = group.dataset.key;
    state.decisions[key] = state.decisions[key] || { decision: "", note: "" };
    state.decisions[key].decision = valueButton.dataset.value;
    group.querySelectorAll("[data-value]").forEach(button => button.setAttribute("aria-pressed", String(button === valueButton)));
    save();
    return;
  }

  if (event.target.closest(".review-open") || event.target.closest("[data-open-review]")) setPanel(true);
  if (event.target.closest(".review-close") || event.target.closest("[data-scrim]")) setPanel(false);
});

document.addEventListener("input", event => {
  const note = event.target.closest("[data-note]");
  if (note) {
    const key = note.closest(".decision").dataset.key;
    state.decisions[key] = state.decisions[key] || { decision: "", note: "" };
    state.decisions[key].note = note.value;
    save();
  }
  if (event.target.matches("[data-overall-note]")) {
    state.overallNote = event.target.value;
    save();
  }
});

document.addEventListener("keydown", event => {
  if (event.key === "Escape" && panel.classList.contains("open")) setPanel(false);
});

document.querySelector("#copy-review").addEventListener("click", async () => {
  await navigator.clipboard.writeText(JSON.stringify(exportRecord(), null, 2));
  status.textContent = "Review JSON copied";
});

document.querySelector("#download-review").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(exportRecord(), null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "mez-identity-product-object-01-review.json";
  link.click();
  URL.revokeObjectURL(link.href);
});

hydrate();
