const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const closeButton = document.querySelector("[data-close-review]");
const modeButton = document.querySelector("[data-mode]");
const densityButton = document.querySelector("[data-density]");
const profile = document.querySelector("[data-profile]");
const viewport = document.querySelector("[data-viewport]");
let returnFocus = null;

function setDrawer(open) {
  drawer.classList.toggle("is-open", open);
  backdrop.classList.toggle("is-open", open);
  drawer.setAttribute("aria-hidden", String(!open));
  document.body.style.overflow = open ? "hidden" : "";
  if (open) {
    returnFocus = document.activeElement;
    closeButton.focus();
  } else if (returnFocus) returnFocus.focus();
}

document.querySelectorAll("[data-open-review]").forEach((button) => button.addEventListener("click", () => setDrawer(true)));
closeButton.addEventListener("click", () => setDrawer(false));
backdrop.addEventListener("click", () => setDrawer(false));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false);
});

modeButton.addEventListener("click", () => {
  const dark = document.body.dataset.mzMode !== "dark";
  document.body.dataset.mzMode = dark ? "dark" : "light";
  modeButton.setAttribute("aria-pressed", String(dark));
  modeButton.textContent = dark ? "Light mode" : "Dark mode";
});

densityButton.addEventListener("click", () => {
  const operational = document.body.dataset.mzDensity !== "operational";
  document.body.dataset.mzDensity = operational ? "operational" : "standard";
  densityButton.setAttribute("aria-pressed", String(operational));
  densityButton.textContent = operational ? "Standard density" : "Operational density";
});

function updateViewport() {
  const width = window.innerWidth;
  viewport.textContent = String(width);
  profile.textContent = width < 600 ? "COMPACT" : width < 920 ? "MEDIUM" : width < 1280 ? "EXPANDED" : "WIDE";
}
window.addEventListener("resize", updateViewport);
updateViewport();

document.querySelector("[data-copy-import]").addEventListener("click", async (event) => {
  await navigator.clipboard.writeText('@import "./mez-foundations/index.css";');
  event.currentTarget.textContent = "Copied";
  window.setTimeout(() => { event.currentTarget.textContent = "Copy"; }, 1400);
});

document.querySelector("[data-release-form]").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = event.currentTarget.elements.path;
  const message = document.querySelector("[data-path-message]");
  const invalid = !input.value.trim();
  input.setAttribute("aria-invalid", String(invalid));
  message.dataset.state = invalid ? "error" : "valid";
  message.textContent = invalid ? "Name a consumer path before creating a migration handoff." : "Named consumer is ready for its own comparison and receipt.";
  if (invalid) input.focus();
});
