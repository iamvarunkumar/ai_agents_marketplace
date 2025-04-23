// static/js/script.js

// Add any site-wide JavaScript functionality here.
// For example, enhancing navbar behavior, animations, etc.

document.addEventListener("DOMContentLoaded", () => {
  console.log("Main script loaded.");

  // Example: Add a class to navbar on scroll (optional)
  const navbar = document.querySelector(".navbar.glass-navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        navbar.classList.add("scrolled"); // You might define .scrolled styles in CSS
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }
});
