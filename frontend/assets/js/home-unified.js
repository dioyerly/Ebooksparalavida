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
    scene.innerHTML = `<div class="orbital-glow"></div><div class="orbital-sphere"><span class="sphere-core"></span><span class="sphere-grid"></span><i class="node n1"></i><i class="node n2"></i><i class="node n3"></i><i class="node n4"></i></div><svg class="orbital-lines" viewBox="0 0 760 650" aria-hidden="true"><ellipse cx="390" cy="320" rx="330" ry="112"/><ellipse cx="390" cy="320" rx="290" ry="190" transform="rotate(-33 390 320)"/><ellipse cx="390" cy="320" rx="250" ry="205" transform="rotate(38 390 320)"/><circle cx="390" cy="320" r="3" class="orbit-node cyan"/><circle cx="122" cy="268" r="4" class="orbit-node coral"/><circle cx="637" cy="405" r="4" class="orbit-node lavender"/></svg><div class="orbital-product orbital-product-ebook"><img src="/assets/images/home-products/orbit-ebook.png" alt="Producto editorial de demostración"><span>EBOKS PARA LA VIDA</span></div><div class="orbital-product orbital-product-planner"><img src="/assets/images/home-products/orbit-planner.png" alt="Planner de demostración"><span>YOYI'R</span></div><div class="orbital-product orbital-product-tool"><img src="/assets/images/home-products/orbit-estrategia.png" alt="Herramienta de demostración"><span>ESTRATEGIA</span></div><div class="orbital-product orbital-product-platform"><img src="/assets/images/home-products/orbit-platform.png" alt="Plataforma digital de demostración"><span>PLATAFORMA</span></div>`;
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
// EstrategIA phase navigator (isolated from orbital behavior).
document.addEventListener('DOMContentLoaded', () => {
  const block = document.querySelector('.strategy-system');
  if (!block) return;
  const tabs = [...block.querySelectorAll('[data-phase]')];
  const contents = [...block.querySelectorAll('[data-content]')];
  const mocks = [...block.querySelectorAll('[data-mock]')];
  const progress = block.querySelector('[data-progress]');
  const bar = block.querySelector('[data-progress-bar]');
  let index = 0;
  const show = (next) => {
    index = (next + 4) % 4;
    tabs.forEach((tab, i) => tab.classList.toggle('is-active', i === index));
    contents.forEach((item, i) => { item.hidden = i !== index; });
    mocks.forEach((item, i) => { item.hidden = i !== index; });
    if (progress) progress.textContent = `${String(index + 1).padStart(2, '0')} / 04`;
    if (bar) bar.style.width = `${(index + 1) * 25}%`;
  };
  tabs.forEach((tab, i) => tab.addEventListener('click', () => show(i)));
  block.querySelector('[data-prev]')?.addEventListener('click', () => show(index - 1));
  block.querySelector('[data-next]')?.addEventListener('click', () => show(index + 1));
});

// EstrategIA showcase navigator
(() => {
  const section = document.querySelector('#estrategia-showcase');
  if (!section) return;

  const slides = [
    {
      title: 'Microapps',
      description: 'Aplicaciones web especializadas y ligeras creadas para resolver una función concreta de forma rápida, sin instalaciones complejas.',
      cta: 'Ver microapps',
      image: '/assets/images/home-products/estrategia-planificador-finanzas.jpeg',
      alt: 'Ejemplo de microapp EstrategIA',
      icon: '▦'
    },
    {
      title: 'Automatizar tareas',
      description: 'Herramientas diseñadas para reducir el trabajo manual y acelerar procesos repetitivos en tu día a día.',
      cta: 'Automatizar',
      image: '/assets/images/home-products/estrategia-planificador-finanzas.jpeg',
      alt: 'Herramientas de automatización',
      icon: 'ϟ'
    },
    {
      title: 'Resolver procesos',
      description: 'Soluciones para simplificar los procesos complejos y hacerlos más accesibles para tu equipo.',
      cta: 'Explorar',
      image: '/assets/images/home-products/estrategia-planificador-finanzas.jpeg',
      alt: 'Resolvedor de procesos',
      icon: '⚙'
    },
    {
      title: 'Trabajar con datos',
      description: 'Herramientas para capturar, organizar y transformar datos en decisiones más inteligentes.',
      cta: 'Ver herramientas',
      image: '/assets/images/home-products/estrategia-planificador-finanzas.jpeg',
      alt: 'Herramientas de datos',
      icon: '▥'
    }
  ];

  const tabs = [...section.querySelectorAll('.estrategia-tab')];
  const title = document.getElementById('estrategiaSlideTitle');
  const description = document.getElementById('estrategiaSlideDescription');
  const ctaText = document.getElementById('estrategiaCtaText');
  const current = document.getElementById('estrategiaCurrent');
  const progress = document.getElementById('estrategiaProgressBar');
  const image = document.getElementById('estrategiaProductImage');
  const productWindow = section.querySelector('.estrategia-product-window');
  const floatingIcon = document.getElementById('estrategiaFloatingIcon');
  const copy = document.getElementById('estrategiaSlideCopy');
  const prev = document.getElementById('estrategiaPrev');
  const next = document.getElementById('estrategiaNext');

  let index = 0;

  const renderSlide = (newIndex) => {
    index = (newIndex + 4) % 4;
    const slide = slides[index];

    // Fade out
    copy.classList.add('is-changing');
    productWindow.classList.add('is-changing');
    floatingIcon.style.opacity = '0.5';

    setTimeout(() => {
      // Update content
      title.textContent = slide.title;
      description.textContent = slide.description;
      ctaText.textContent = slide.cta;
      floatingIcon.textContent = slide.icon;
      image.src = slide.image;
      image.alt = slide.alt;

      // Update tabs
      tabs.forEach((tab, i) => {
        tab.classList.toggle('active', i === index);
      });

      // Update progress
      if (current) current.textContent = String(index + 1).padStart(2, '0');
      if (progress) progress.style.width = `${(index + 1) * 25}%`;

      // Fade in
      copy.classList.remove('is-changing');
      productWindow.classList.remove('is-changing');
      floatingIcon.style.opacity = '1';
    }, 140);
  };

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => renderSlide(i));
  });

  prev?.addEventListener('click', () => renderSlide(index - 1));
  next?.addEventListener('click', () => renderSlide(index + 1));

  renderSlide(0);
})();

// YOYI'R — 4 FASES
(() => {

    const slides = [
        {
            title: "Planificar",
            description:
                "Herramientas visuales para convertir pendientes, fechas y objetivos en un plan claro que puedas seguir a tu ritmo.",
            linkText: "Ver planners",
            link: "/yoyir/",
            image: "/assets/images/home-products/yoyir-planificador.jpeg",
            alt: "Planner digital YOYI'R"
        },

        {
            title: "Organizar",
            description:
                "Recursos para ordenar tareas, proyectos, ideas y prioridades y tener lo importante reunido en un mismo lugar.",
            linkText: "Ver recursos",
            link: "/yoyir/",
            image: "/assets/images/home-products/yoyir-planificador.jpeg",
            alt: "Recurso de organización YOYI'R"
        },

        {
            title: "Crear rutinas",
            description:
                "Sistemas sencillos para darle estructura a tus días y construir rutinas que puedas adaptar a tu propio ritmo.",
            linkText: "Ver recursos",
            link: "/yoyir/",
            image: "/assets/images/home-products/yoyir-planificador.jpeg",
            alt: "Recurso para rutinas YOYI'R"
        },

        {
            title: "Recursos a mano",
            description:
                "Plantillas, imprimibles y materiales digitales que puedes guardar, reutilizar y adaptar cuando los necesites.",
            linkText: "Explorar YOYI'R",
            link: "/yoyir/",
            image: "/assets/images/home-products/yoyir-planificador.jpeg",
            alt: "Recursos digitales YOYI'R"
        }
    ];


    const section =
        document.querySelector(".universe-stage--yoyir");

    if (!section) return;


    const tabs =
        [...section.querySelectorAll("[data-yoyir-slide]")];

    const title =
        section.querySelector("#yoyir-slide-title");

    const description =
        section.querySelector("#yoyir-slide-description");

    const link =
        section.querySelector("#yoyir-slide-link");

    const linkText =
        section.querySelector("#yoyir-slide-link-text");

    const image =
        section.querySelector("#yoyir-product-image");

    const current =
        section.querySelector("#yoyir-current");

    const progress =
        section.querySelector("#yoyir-progress-bar");

    const prev =
        section.querySelector("#yoyir-prev");

    const next =
        section.querySelector("#yoyir-next");


    let active = 0;


    function render(index) {

        active =
            (index + slides.length) %
            slides.length;

        const slide = slides[active];


        tabs.forEach((tab, tabIndex) => {

            const selected =
                tabIndex === active;

            tab.classList.toggle(
                "is-active",
                selected
            );

            tab.setAttribute(
                "aria-selected",
                selected ? "true" : "false"
            );
        });


        title.textContent =
            slide.title;

        description.textContent =
            slide.description;

        linkText.textContent =
            slide.linkText;

        link.href =
            slide.link;


        image.style.opacity = "0";
        image.style.transform =
            "translateY(8px) scale(.985)";


        window.setTimeout(() => {

            image.src =
                slide.image;

            image.alt =
                slide.alt;

            image.style.opacity = "1";

            image.style.transform =
                "translateY(0) scale(1)";

        }, 180);


        current.textContent =
            String(active + 1)
                .padStart(2, "0");


        progress.style.width =
            `${((active + 1) / slides.length) * 100}%`;
    }


    tabs.forEach((tab, index) => {

        tab.addEventListener(
            "click",
            () => render(index)
        );
    });


    prev.addEventListener(
        "click",
        () => render(active - 1)
    );


    next.addEventListener(
        "click",
        () => render(active + 1)
    );


    render(0);

})();

// EBOOKS PARA LA VIDA — 4 FASES
(() => {

    const slides = [
        {
            title: "Vida y bienestar",
            description:
                "Guías prácticas para comprenderte mejor, crear hábitos más sostenibles y llevar herramientas útiles a tu vida cotidiana.",
            linkText: "Ver ebooks",
            link: "/ebooks/",
            image: "/assets/images/home-products/ebook-no-te-pierdas-por-amor.jpeg",
            alt: "Ebook de vida y bienestar"
        },

        {
            title: "Aprender y dominar",
            description:
                "Recursos educativos y guías para desarrollar nuevas habilidades, profundizar en temas que te interesan y ampliar tu perspectiva.",
            linkText: "Ver ebooks",
            link: "/ebooks/",
            image: "/assets/images/home-products/ebook-no-te-pierdas-por-amor.jpeg",
            alt: "Ebook de aprendizaje"
        },

        {
            title: "Dinero inteligente",
            description:
                "Guías prácticas para entender finanzas personales, invertir con confianza y construir una relación más saludable con el dinero.",
            linkText: "Ver ebooks",
            link: "/ebooks/",
            image: "/assets/images/home-products/ebook-no-te-pierdas-por-amor.jpeg",
            alt: "Ebook de finanzas"
        },

        {
            title: "Trabajo y carrera",
            description:
                "Recursos para desarrollar tu carrera profesional, mejorar tus habilidades laborales y encontrar más satisfacción en tu trabajo.",
            linkText: "Ver ebooks",
            link: "/ebooks/",
            image: "/assets/images/home-products/ebook-no-te-pierdas-por-amor.jpeg",
            alt: "Ebook de carrera profesional"
        }
    ];


    const section =
        document.querySelector(".universe-stage--ebooks");

    if (!section) return;


    const tabs =
        [...section.querySelectorAll("[data-ebooks-slide]")];

    const title =
        section.querySelector("#ebooks-slide-title");

    const description =
        section.querySelector("#ebooks-slide-description");

    const link =
        section.querySelector("#ebooks-slide-link");

    const linkText =
        section.querySelector("#ebooks-slide-link-text");

    const image =
        section.querySelector("#ebooks-product-image");

    const current =
        section.querySelector("#ebooks-current");

    const progress =
        section.querySelector("#ebooks-progress-bar");

    const prev =
        section.querySelector("#ebooks-prev");

    const next =
        section.querySelector("#ebooks-next");


    let active = 0;


    function render(index) {

        active =
            (index + slides.length) %
            slides.length;

        const slide = slides[active];


        tabs.forEach((tab, tabIndex) => {

            const selected =
                tabIndex === active;

            tab.classList.toggle(
                "is-active",
                selected
            );

            tab.setAttribute(
                "aria-selected",
                selected ? "true" : "false"
            );
        });


        title.textContent =
            slide.title;

        description.textContent =
            slide.description;

        linkText.textContent =
            slide.linkText;

        link.href =
            slide.link;


        image.style.opacity = "0";
        image.style.transform =
            "translateY(8px) scale(.985)";


        window.setTimeout(() => {

            image.src =
                slide.image;

            image.alt =
                slide.alt;

            image.style.opacity = "1";

            image.style.transform =
                "translateY(0) scale(1)";

        }, 180);


        current.textContent =
            String(active + 1)
                .padStart(2, "0");


        progress.style.width =
            `${((active + 1) / slides.length) * 100}%`;
    }


    tabs.forEach((tab, index) => {

        tab.addEventListener(
            "click",
            () => render(index)
        );
    });


    prev.addEventListener(
        "click",
        () => render(active - 1)
    );


    next.addEventListener(
        "click",
        () => render(active + 1)
    );


    render(0);

})();
