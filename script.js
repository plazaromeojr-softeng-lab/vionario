// Navbar
const navbar = document.querySelector("#navbar");
const hero = document.querySelector("#home");

function updateNavbar() {
  if (!hero) {
    navbar.classList.add("visible");
    return;
  }

  const heroHeight = hero.offsetHeight;

  if (window.scrollY >= heroHeight - 80) {
    navbar.classList.add("visible");
  } else {
    navbar.classList.remove("visible");
  }
}

window.addEventListener("scroll", updateNavbar);

updateNavbar();

const menuToggle = document.querySelector("#menuToggle");
const navLinks = document.querySelector("#navLinks");

menuToggle.addEventListener("click", () => {
  navLinks.classList.toggle("open");
});

// Contact
const contactForm = document.querySelector("#contactForm");
const formStatus = document.querySelector("#formStatus");

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    formStatus.textContent = "Form received. Backend connection coming next.";
  });
}
