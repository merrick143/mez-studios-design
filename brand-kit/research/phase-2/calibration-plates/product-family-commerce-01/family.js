const bundleOptions = [...document.querySelectorAll("[data-product]")];
const summaryProducts = document.querySelector("[data-summary-products]");
const summaryCount = document.querySelector("[data-summary-count]");

function updateBundleSummary() {
  const selected = bundleOptions.filter((option) => option.getAttribute("aria-pressed") === "true");
  summaryProducts.innerHTML = selected.map((option) => `<span>${option.dataset.product}</span>`).join("");
  summaryCount.textContent = `${selected.length} ${selected.length === 1 ? "system" : "systems"} selected`;
}

bundleOptions.forEach((option) => {
  option.addEventListener("click", () => {
    const selected = option.getAttribute("aria-pressed") === "true";
    option.setAttribute("aria-pressed", String(!selected));
    option.classList.toggle("is-selected", !selected);
    option.querySelector("em").textContent = selected ? "Include" : "Included";
    updateBundleSummary();
  });
});

updateBundleSummary();
