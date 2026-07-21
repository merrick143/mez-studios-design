const decisions = [
  ["overallDirection", "Overall direction", "Does this feel like a stronger and more distinctive Mez Systems homepage opening?"],
  ["messageHierarchy", "Message hierarchy", "Do the centred proposition, support and actions still have the right scale and order?"],
  ["cardStackComposition", "Card stack", "Does the five-card fan feel intentional, premium and legible rather than cluttered?"],
  ["animationUse", "Living texture", "Does animation make the product family feel alive without overpowering the message?"],
  ["productFamilyRead", "Product family", "Do five equal-size cards read as one house with distinct products?"],
  ["mobileOpening", "Mobile opening", "Does the compact deck keep the idea clear and usable on mobile?"],
];

const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const progress = document.querySelector("[data-progress]");
const decisionRoot = document.querySelector("[data-decisions]");
const copyState = document.querySelector("[data-copy-state]");

decisionRoot.innerHTML = decisions.map(([id, title, prompt]) => {
  const options = ["approve", "edit", "reject"].map((option) =>
    '<label><input type="radio" name="' + id + '" value="' + option + '"><span>' + option + '</span></label>'
  ).join("");
  return '<fieldset data-decision="' + id + '"><legend>' + title + '</legend><p>' + prompt + '</p><div class="decision-options">' + options + '</div><label class="decision-note">Optional note<textarea rows="2" name="' + id + 'Note" placeholder="What is causing the reaction?"></textarea></label></fieldset>';
}).join("");

function setDrawer(open) {
  drawer.setAttribute("aria-hidden", String(!open));
  document.body.classList.toggle("review-is-open", open);
  if (open) drawer.querySelector("input")?.focus();
}

function updateProgress() {
  const count = decisions.filter(([id]) => document.querySelector('input[name="' + id + '"]:checked')).length;
  progress.textContent = count + "/6";
}

document.querySelectorAll("[data-open-review]").forEach((button) => button.addEventListener("click", () => setDrawer(true)));
document.querySelector("[data-close-review]").addEventListener("click", () => setDrawer(false));
backdrop.addEventListener("click", () => setDrawer(false));
document.addEventListener("keydown", (event) => { if (event.key === "Escape") setDrawer(false); });
document.querySelectorAll('input[type="radio"]').forEach((input) => input.addEventListener("change", updateProgress));

document.querySelector("[data-review-form]").addEventListener("submit", async (event) => {
  event.preventDefault();
  let complete = true;
  const output = {};

  decisions.forEach(([id]) => {
    const selected = document.querySelector('input[name="' + id + '"]:checked');
    if (!selected) complete = false;
    output[id] = {
      decision: selected?.value || "",
      note: document.querySelector('textarea[name="' + id + 'Note"]').value.trim(),
    };
  });

  const record = {
    schemaVersion: "1.0.0",
    studyId: "MEZ-HERO-FIRST-VIEWPORT-03",
    exportedAt: new Date().toISOString(),
    complete,
    productionAuthority: false,
    sourceExpressionApproved: false,
    decisions: output,
    overallNote: document.querySelector('textarea[name="overallNote"]').value.trim(),
  };

  try {
    await navigator.clipboard.writeText(JSON.stringify(record, null, 2));
    copyState.textContent = complete ? "Copied. Paste the JSON into Codex." : "Copied, but some decisions are still empty.";
  } catch (error) {
    console.error("[mez-hero-03] Clipboard export failed.", error);
    copyState.textContent = "Clipboard access failed. The export is in the browser console.";
    console.info(JSON.stringify(record, null, 2));
  }
});
