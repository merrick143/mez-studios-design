const drawer = document.querySelector("[data-review-drawer]");
const backdrop = document.querySelector("[data-backdrop]");
const openButtons = document.querySelectorAll("[data-open-review]");
const closeButton = document.querySelector("[data-close-review]");
const stateButton = document.querySelector("[data-force-states]");
const fieldDemo = document.querySelector("[data-field-demo]");
const ownerField = fieldDemo.querySelector("[name=owner]");
const ownerMessage = document.querySelector("[data-owner-message]");
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

stateButton.addEventListener("click", () => {
  const active = document.body.classList.toggle("show-forced-states");
  stateButton.setAttribute("aria-pressed", String(active));
  stateButton.textContent = active ? "Hide states" : "Show states";
});

fieldDemo.addEventListener("submit", (event) => {
  event.preventDefault();
  const invalid = !ownerField.value.trim();
  ownerField.setAttribute("aria-invalid", String(invalid));
  ownerMessage.dataset.state = invalid ? "error" : "valid";
  ownerMessage.textContent = invalid ? "Add an approval owner before this system can be published." : "Approval owner recorded.";
  if (invalid) ownerField.focus();
});

fieldDemo.addEventListener("reset", () => {
  window.setTimeout(() => {
    ownerField.removeAttribute("aria-invalid");
    ownerMessage.removeAttribute("data-state");
    ownerMessage.textContent = "Add the person accountable for final approval.";
  }, 0);
});
