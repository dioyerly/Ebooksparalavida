(() => {
  'use strict';
  const hero = document.querySelector('.universe-hero');
  const journey = document.querySelector('.universe-journey');
  if (journey) {
    ['.software-section', '.planner-section', '.editorial-section'].forEach(selector => {
      const section = journey.querySelector(selector);
      if (section) journey.appendChild(section);
    });
  }
  if (hero) {
    const title = hero.querySelector('#hero-title');
    if (title) title.innerHTML = 'Productos<br><span>digitales</span><br><em>que hacen más.</em>';
    const scene = document.createElement('div');
    scene.className = 'orbital-scene';
    scene.setAttribute('aria-label', 'Ecosistema digital con productos de demostración');
    scene.innerHTML = `<div class="orbital-glow"></div><div class="orbital-sphere"><span class="sphere-core"></span><span class="sphere-grid"></span><i class="node n1"></i><i class="node n2"></i><i class="node n3"></i><i class="node n4"></i></div><svg class="orbital-lines" viewBox="0 0 760 650" aria-hidden="true"><ellipse cx="390" cy="320" rx="330" ry="112"/><ellipse cx="390" cy="320" rx="290" ry="190" transform="rotate(-33 390 320)"/><ellipse cx="390" cy="320" rx="250" ry="205" transform="rotate(38 390 320)"/><circle cx="390" cy="320" r="3" class="orbit-node cyan"/><circle cx="122" cy="268" r="4" class="orbit-node coral"/><circle cx="637" cy="405" r="4" class="orbit-node lavender"/></svg><div class="orbital-product orbital-product-ebook"><img src="/static/images/home-products/orbit-ebook.png" alt="Producto editorial de demostración"><span>EBOKS PARA LA VIDA</span></div><div class="orbital-product orbital-product-planner"><img src="/static/images/home-products/orbit-planner.png" alt="Planner de demostración"><span>YOYI'R</span></div><div class="orbital-product orbital-product-tool"><img src="/static/images/home-products/orbit-estrategia.png" alt="Herramienta de demostración"><span>ESTRATEGIA</span></div><div class="orbital-product orbital-product-platform"><img src="/static/images/home-products/orbit-platform.png" alt="Plataforma digital de demostración"><span>PLATAFORMA</span></div>`;
    hero.appendChild(scene);
    hero.querySelector('.hero-book')?.remove();
    hero.querySelector('.hero-planner')?.remove();
    hero.querySelector('.hero-software')?.remove();
    const orbitProducts = [...scene.querySelectorAll('.orbital-product')];
    const orbitPhases = [0, Math.PI / 2, Math.PI, (Math.PI * 3) / 2];
    let orbitPaused = false;
    let orbitStart = performance.now();
    const core = scene.querySelector('.orbital-sphere');
    let geometry = { centerX: 0, centerY: 0, radiusX: 0, radiusY: 0 };
    const measureOrbit = () => {
      if (!core) return;
      const sceneRect = scene.getBoundingClientRect();
      const coreRect = core.getBoundingClientRect();
      geometry.centerX = coreRect.left - sceneRect.left + coreRect.width / 2;
      geometry.centerY = coreRect.top - sceneRect.top + coreRect.height / 2;
      const coreRadius = coreRect.width / 2;
      geometry.radiusX = coreRadius * 1.08;
      geometry.radiusY = coreRadius * .62;
    };
    measureOrbit();
    if ('ResizeObserver' in window) new ResizeObserver(measureOrbit).observe(scene);
    window.addEventListener('resize', measureOrbit, { passive: true });
    const orbitFrame = now => {
      if (!document.hidden && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && !orbitPaused) {
        const elapsed = (now - orbitStart) / 1000;
        const angle = elapsed * (Math.PI * 2 / 36);
        orbitProducts.forEach((product, index) => {
          const a = angle + orbitPhases[index];
          const depth = Math.sin(a);
          const x = Math.cos(a) * geometry.radiusX;
          const y = Math.sin(a) * geometry.radiusY;
          const near = (depth + 1) / 2;
          const scale = .68 + near * .32;
          product.style.left = `${geometry.centerX - product.offsetWidth / 2}px`;
          product.style.top = `${geometry.centerY - product.offsetHeight / 2}px`;
          product.style.transform = `translate3d(${x}px,${y}px,0) scale(${scale})`;
          product.style.opacity = String(.42 + near * .58);
          product.style.filter = `blur(${(1 - near) * 1.6}px) brightness(${.72 + near * .28})`;
          product.style.zIndex = depth > 0 ? '6' : '2';
        });
      }
      requestAnimationFrame(orbitFrame);
    };
    orbitProducts.forEach(product => {
      product.addEventListener('mouseenter', () => { orbitPaused = true; });
      product.addEventListener('mouseleave', () => { orbitPaused = false; });
    });
    requestAnimationFrame(orbitFrame);
  }
  document.body.classList.add('js-ready');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#platform-nav');
  const closeMenu = () => { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
  });
  nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); } });
  document.addEventListener('click', e => { if (!e.target.closest('.platform-header')) closeMenu(); });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const objects = document.querySelector('.hero-objects');
  let heroVisible = true;
  let queued = false;
  const updateParallax = () => {
    queued = false;
    if (reduce.matches || !heroVisible) return;
    const y = Math.min(window.scrollY, hero.offsetHeight);
    objects.style.transform = `translate3d(0,${y * (window.innerWidth < 768 ? .035 : .085)}px,0)`;
  };
  if ('IntersectionObserver' in window) {
    if (!reduce.matches) document.body.classList.add('motion-enabled');
    const reveals = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); reveals.unobserve(entry.target); }
      });
    }, { threshold: .08 });
    document.querySelectorAll('.reveal').forEach(el => reveals.observe(el));
    const activity = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        entry.target.classList.toggle('offscreen', !entry.isIntersecting);
        if (entry.target === hero) { heroVisible = entry.isIntersecting; if (heroVisible) updateParallax(); }
      });
    }, { rootMargin: '100px' });
    document.querySelectorAll('.universe-hero, .chapter, .creation-section, .showcase-item').forEach(el => activity.observe(el));
  }
  window.addEventListener('scroll', () => {
    if (!queued && !reduce.matches && heroVisible) { queued = true; requestAnimationFrame(updateParallax); }
  }, { passive: true });
  reduce.addEventListener('change', () => {
    document.body.classList.toggle('motion-enabled', !reduce.matches);
    if (reduce.matches) objects.style.transform = '';
    else updateParallax();
  });
  // Same-origin visit tracking retained from the shared shell; no demo purchase events.
  fetch('/api/track-visit', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page_path: window.location.pathname })
  }).catch(() => {});
})();
