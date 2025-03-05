const navbar = document.getElementById('navbar');
const navbarBrand = document.querySelector('.navbar-brand');
const navLinks = document.querySelectorAll('.nav-link');
let scrolled = false;

window.addEventListener('scroll', () => {
  if (window.scrollY > 100) {
    if (!scrolled) {
      navbar.style.backgroundColor = 'background-color: rgb(150, 220, 222)'; /* Background color when scrolled */
      navbar.style.height = '90px'; /* Shrink the navbar height */
      navbarBrand.style.transform = 'scale(0.8)'; /* Shrink the brand logo */
      navLinks.forEach(link => {
        link.style.fontSize = '16px'; /* Shrink the font size of links */
      });
      scrolled = true;
    }
  } else {
    if (scrolled) {
      navbar.style.backgroundColor = 'background-color: rgb(150, 220, 222)'; /* Reset background color */
      navbar.style.height = '130px'; /* Reset navbar height */
      navbarBrand.style.transform = 'scale(1)'; /* Reset brand logo size */
      navLinks.forEach(link => {
        link.style.fontSize = '20px'; /* Reset font size of links */
      });
      scrolled = false;
    }
  }
});

  // Initialize ScrollReveal
  ScrollReveal().reveal('.scroll-animation', {
    delay: 100, // Delay before animation starts (in milliseconds)
    distance: '50px', // Distance the element moves when revealed
    origin: 'bottom', // Origin of the animation
    duration: 700, // Duration of the animation (in milliseconds)
    easing: 'ease-out', // Easing function for the animation
    // reset: true // Reset the animation when element is out of view
  });
  ScrollReveal().reveal('.scroll-animation-text', {
    delay: 100, // Delay before animation starts (in milliseconds)
    distance: '50px', // Distance the element moves when revealed
    origin: 'top', // Origin of the animation
    duration: 700, // Duration of the animation (in milliseconds)
    easing: 'ease-out', // Easing function for the animation
  });
