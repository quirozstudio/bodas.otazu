const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-toggle");
const mainMenu = document.querySelector(".main-menu");
const menuLinks = document.querySelectorAll(".main-menu a");
const galleryItems = document.querySelectorAll(".gallery-item");
const lightbox = document.querySelector("#lightbox");
const lightboxImage = lightbox.querySelector("img");
const lightboxClose = lightbox.querySelector(".lightbox-close");
const memoryForm = document.querySelector("#memory-form");
const formNote = document.querySelector("#form-note");
const revealItems = document.querySelectorAll(".reveal");

function setHeaderState() {
  header.classList.toggle("scrolled", window.scrollY > 20);
}

function closeMenu() {
  document.body.classList.remove("menu-open");
  header.classList.remove("menu-active");
  mainMenu.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}

function toggleMenu() {
  const isOpen = document.body.classList.toggle("menu-open");
  header.classList.toggle("menu-active", isOpen);
  mainMenu.classList.toggle("is-open", isOpen);
  menuButton.setAttribute("aria-expanded", String(isOpen));
}

function openLightbox(imageUrl, imageAlt) {
  lightboxImage.src = imageUrl;
  lightboxImage.alt = imageAlt || "Foto ampliada de la boda";
  lightbox.classList.add("is-open");
  lightbox.setAttribute("aria-hidden", "false");
  document.body.classList.add("lightbox-open");
}

function closeLightbox() {
  lightbox.classList.remove("is-open");
  lightbox.setAttribute("aria-hidden", "true");
  document.body.classList.remove("lightbox-open");
  lightboxImage.src = "";
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

revealItems.forEach((item) => revealObserver.observe(item));

window.addEventListener("scroll", setHeaderState);
menuButton.addEventListener("click", toggleMenu);
menuLinks.forEach((link) => link.addEventListener("click", closeMenu));

galleryItems.forEach((item) => {
  item.addEventListener("click", () => {
    const image = item.querySelector("img");
    openLightbox(item.dataset.full, image.alt);
  });
});

lightboxClose.addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) {
    closeLightbox();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeMenu();
    closeLightbox();
  }
});

memoryForm.addEventListener("submit", (event) => {
  event.preventDefault();
  formNote.textContent = "Recuerdo enviado. Gracias por formar parte de este día.";
  memoryForm.reset();
});

setHeaderState();
