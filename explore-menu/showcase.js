const menu = document.querySelector("mez-explore-menu");
const controls = [...document.querySelectorAll("[data-menu-variant]")];
const indexNode = document.querySelector("#variant-index");
const nameNode = document.querySelector("#variant-name");
const descriptionNode = document.querySelector("#variant-description");

const directions = {
  registry: {
    index: "Direction 01 / 05",
    name: "Registry",
    description: "A quiet product registry with equal weight and contained depth."
  },
  signal: {
    index: "Direction 02 / 05",
    name: "Signal",
    description: "A stronger typographic identity with numbered system objects."
  },
  aperture: {
    index: "Direction 03 / 05",
    name: "Aperture",
    description: "A compact control that opens into a generous field of cores."
  },
  gallery: {
    index: "Direction 04 / 05",
    name: "Gallery",
    description: "The canonical light canvas, treating each core as a collected object."
  },
  console: {
    index: "Direction 05 / 05",
    name: "Console",
    description: "A technical system index built from hairlines, coordinates and rhythm."
  }
};

function selectVariant(variant) {
  const direction = directions[variant] || directions.registry;
  menu.setAttribute("variant", variant);
  controls.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.menuVariant === variant)));
  indexNode.textContent = direction.index;
  nameNode.textContent = direction.name;
  descriptionNode.textContent = direction.description;
  const url = new URL(location.href);
  url.searchParams.set("variant", variant);
  history.replaceState({}, "", url);
}

controls.forEach(button => button.addEventListener("click", () => selectVariant(button.dataset.menuVariant)));

const initial = new URLSearchParams(location.search).get("variant");
selectVariant(directions[initial] ? initial : "registry");

