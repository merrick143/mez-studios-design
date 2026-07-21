const loadingButton = document.querySelector("[data-loading-button]");
const loadingToggle = document.querySelector("[data-toggle-loading]");

loadingToggle?.addEventListener("click", () => {
  const isLoading = loadingButton.classList.toggle("is-loading");
  loadingButton.setAttribute("aria-busy", String(isLoading));
  loadingButton.querySelector(".button-label").textContent = isLoading ? "Installing system" : "Install system";
  loadingToggle.textContent = isLoading ? "Show rest state" : "Show loading state";
});
