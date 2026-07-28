const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const openButtons = document.querySelectorAll("[data-open-review]");
const closeButton = document.querySelector("[data-close-review]");
const grayscaleButton = document.querySelector("[data-grayscale]");
const annotationButton = document.querySelector("[data-annotations]");
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

grayscaleButton.addEventListener("click", () => {
  const active = document.body.classList.toggle("is-grayscale");
  grayscaleButton.setAttribute("aria-pressed", String(active));
  grayscaleButton.textContent = active ? "Show colour" : "Grayscale";
});

annotationButton.addEventListener("click", () => {
  const active = document.body.classList.toggle("hide-annotations");
  annotationButton.setAttribute("aria-pressed", String(!active));
  annotationButton.textContent = active ? "Show labels" : "Hide labels";
});
