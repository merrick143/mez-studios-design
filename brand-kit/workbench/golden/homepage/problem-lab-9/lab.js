(() => {
  const focusId = new URLSearchParams(window.location.search).get('focus');
  const focusedConcept = focusId ? document.getElementById(focusId) : null;

  if (focusedConcept?.classList.contains('lab-item')) {
    document.body.classList.add('is-focus-mode');
    focusedConcept.classList.add('is-focused');
  }

  const links = new Map(
    [...document.querySelectorAll('.lab-bar nav a')].map((link) => [link.getAttribute('href').slice(1), link])
  );
  const concepts = [...document.querySelectorAll('.lab-item[id]')];

  if (!('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    links.forEach((link) => link.classList.remove('is-current'));
    links.get(visible.target.id)?.classList.add('is-current');
  }, { rootMargin: '-20% 0px -65% 0px', threshold: [0, .2, .5] });

  concepts.forEach((concept) => observer.observe(concept));
})();
