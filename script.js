// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');

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

// Current year (footer + hero)
const yr = new Date().getFullYear();
document.getElementById('year').textContent = yr;
document.querySelectorAll('.year').forEach((el) => { el.textContent = yr; });

// Fade the brand into the nav once the hero is scrolled past
const header = document.querySelector('.site-header');
const onScroll = () => {
  if (window.scrollY > window.innerHeight * 0.6) header.classList.add('scrolled');
  else header.classList.remove('scrolled');
};
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });
