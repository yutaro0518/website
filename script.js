// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');

if (toggle && links) {
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Close mobile menu after clicking a link
  links.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Current year (any .year element)
const yr = new Date().getFullYear();
document.querySelectorAll('.year').forEach((el) => { el.textContent = yr; });

// Landing only: fade the brand into the nav once the hero is scrolled past.
// Sub-pages keep the brand visible (header already has the .scrolled class).
const header = document.querySelector('.site-header');
const hero = document.querySelector('.hero');
if (header && hero) {
  const onScroll = () => {
    if (window.scrollY > window.innerHeight * 0.6) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}
