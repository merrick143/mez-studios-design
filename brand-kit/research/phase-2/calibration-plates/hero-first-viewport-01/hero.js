import { mountLivingCores } from "../../../../design-system-export/mz-core.js";

const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".desktop-nav");

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    navigation.classList.toggle("is-open", !isOpen);
  });
}

mountLivingCores(document).catch((error) => {
  console.error("[mez-hero-calibration] Living Core mount failed.", error);
});
