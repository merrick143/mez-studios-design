const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const openButtons = document.querySelectorAll("[data-open-review]");
const closeButton = document.querySelector("[data-close-review]");
const gridButton = document.querySelector("[data-grid]");
const stressButton = document.querySelector("[data-stress]");
let returnFocus = null;

function setDrawer(open) {
  drawer.classList.toggle("is-open", open);
  backdrop.classList.toggle("is-open", open);
  drawer.setAttribute("aria-hidden", String(!open));
  document.body.style.overflow = open ? "hidden" : "";
  if (open) {
    returnFocus = document.activeElement;
    closeButton.focus();
  } else if (returnFocus) {
    returnFocus.focus();
  }
}

openButtons.forEach((button) => button.addEventListener("click", () => setDrawer(true)));
closeButton.addEventListener("click", () => setDrawer(false));
backdrop.addEventListener("click", () => setDrawer(false));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false);
});

gridButton.addEventListener("click", () => {
  const active = document.body.classList.toggle("show-grid");
  gridButton.setAttribute("aria-pressed", String(active));
  gridButton.textContent = active ? "Hide grid" : "Show grid";
});

stressButton.addEventListener("click", () => {
  const active = stressButton.getAttribute("aria-pressed") !== "true";
  stressButton.setAttribute("aria-pressed", String(active));
  stressButton.textContent = active ? "Original copy" : "Stress copy";
  document.querySelectorAll("[data-copy]").forEach((node) => {
    node.textContent = active ? node.dataset.long : node.dataset.short;
  });
});
