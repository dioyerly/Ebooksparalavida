document.addEventListener("DOMContentLoaded", () => {
  const normalize = (value = "") =>
    value
      .toString()
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");

  const aliases = {
    administracion: ["administracion"],
    "creador-de-apps": [
      "creador-de-apps",
      "creadores-de-apps",
      "creadores",
      "creador"
    ],
    marketing: ["marketing"],
    negocio: ["negocio", "negocios"],
    "vida-diaria": ["vida-diaria"]
  };

  const filters = [...document.querySelectorAll(".ea-filter")];
  const products = [...document.querySelectorAll(".ea-product")];
  const noResults = document.querySelector(".ea-no-results");

  function applyFilter(filter) {
    let visible = 0;

    products.forEach(product => {
      const category = normalize(product.dataset.category);

      const show =
        filter === "todas" ||
        (aliases[filter] || [filter]).includes(category);

      product.hidden = !show;

      if (show) visible++;
    });

    filters.forEach(button => {
      const active = button.dataset.filter === filter;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });

    if (noResults) {
      noResults.hidden = visible !== 0;
    }
  }

  filters.forEach(button => {
    button.addEventListener("click", () => {
      applyFilter(button.dataset.filter);
    });
  });

  document.querySelectorAll("[data-jump-filter]").forEach(card => {
    card.addEventListener("click", () => {
      applyFilter(card.dataset.jumpFilter);

      document.querySelector("#productos")?.scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth"
      });
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", event => {
      const selector = link.getAttribute("href");

      if (!selector || selector === "#") return;

      const target = document.querySelector(selector);
      if (!target) return;

      event.preventDefault();

      target.scrollIntoView({
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth"
      });
    });
  });

  const menu = document.querySelector(".ea-menu");
  const mobileNav = document.querySelector(".ea-mobile-nav");

  menu?.addEventListener("click", () => {
    const open = mobileNav.classList.toggle("is-open");
    menu.setAttribute("aria-expanded", open ? "true" : "false");
  });

  mobileNav?.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("is-open");
      menu?.setAttribute("aria-expanded", "false");
    });
  });

  applyFilter("todas");
});
