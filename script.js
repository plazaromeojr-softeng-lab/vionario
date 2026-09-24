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

    contactForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        formStatus.textContent = "Sending...";

        const formData = new FormData(contactForm);

        const payload = {
            name: formData.get("name"),
            email: formData.get("email"),
            company: formData.get("company") || null,
            phone: formData.get("phone") || null,
            service: formData.get("service"),
            message: formData.get("message")
        };

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/contact",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                }
            );

            if (!response.ok) {
                throw new Error("Request failed");
            }

            const result = await response.json();

            formStatus.textContent = result.message;

            contactForm.reset();

        } catch (error) {

            formStatus.textContent =
                "Something went wrong. Please try again.";

            console.error(error);

        }

    });

}

// Nav hamburger collapse after click
const mobileNavLinks = document.querySelectorAll("#navLinks a");

mobileNavLinks.forEach((link) => {
    link.addEventListener("click", () => {
        navLinks.classList.remove("open");
    });
});
