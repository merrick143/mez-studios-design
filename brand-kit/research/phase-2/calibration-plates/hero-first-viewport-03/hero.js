import { mountLivingCores } from "../../../../design-system-export/mz-core.js";

const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".site-nav");

if (menuButton && navigation) {
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!open));
    menuButton.setAttribute("aria-label", open ? "Open navigation" : "Close navigation");
    navigation.classList.toggle("is-open", !open);
  });

  navigation.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
    navigation.classList.remove("is-open");
  });
}

mountLivingCores(document).catch((error) => {
  console.error("[mez-hero-03] Living Core mounting failed. Static twins remain active.", error);
});
