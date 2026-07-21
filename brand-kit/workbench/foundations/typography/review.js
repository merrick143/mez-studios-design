const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const openButtons = document.querySelectorAll("[data-open-review]");
const closeButton = document.querySelector("[data-close-review]");
const fallbackButton = document.querySelector("[data-fallback]");
const expansionButton = document.querySelector("[data-expand-copy]");
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

fallbackButton.addEventListener("click", () => {
  const active = document.body.classList.toggle("fallback-mode");
  fallbackButton.setAttribute("aria-pressed", String(active));
  fallbackButton.textContent = active ? "Fonts active" : "Fallbacks";
});

expansionButton.addEventListener("click", () => {
  const active = expansionButton.getAttribute("aria-pressed") !== "true";
  expansionButton.setAttribute("aria-pressed", String(active));
  expansionButton.textContent = active ? "Original copy" : "130% copy";
  document.querySelectorAll("[data-copy]").forEach((node) => {
    node.textContent = active ? node.dataset.long : node.dataset.short;
  });
});
