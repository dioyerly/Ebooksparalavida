(() => {
  const filterButtons = [
    ...document.querySelectorAll("[data-yoyir-filter]")
  ];

  const productCards = [
    ...document.querySelectorAll("[data-yoyir-product]")
  ];

  const jumpButtons = [
    ...document.querySelectorAll("[data-yoyir-jump]")
  ];

  const productsSection = document.querySelector("#productos");

  const normalize = (value = "") =>
    value
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();

  const matchesFilter = (category, filter) => {
    if (filter === "all") return true;

    const categoryText = normalize(category);
    const filterText = normalize(filter);

    const aliases = {
      agenda: ["agenda", "anual"],
      planificacion: [
        "planificacion",
        "planificador",
        "mensual",
        "semanal",
        "diaria",
        "diario"
      ],
      habitos: [
        "habito",
        "habitos",
        "bienestar",
        "rutina",
        "rutinas"
      ],
      finanzas: [
        "finanza",
        "finanzas",
        "dinero",
        "presupuesto"
      ],
      proposito: [
        "proposito",
        "objetivo",
        "objetivos",
        "metas"
      ]
    };

    const terms = aliases[filterText] || [filterText];

    return terms.some(term =>
      categoryText.includes(normalize(term))
    );
  };

  const applyFilter = (filter) => {
    filterButtons.forEach(button => {
      const active =
        button.dataset.yoyirFilter === filter;

      button.classList.toggle("active", active);
      button.setAttribute(
        "aria-pressed",
        active ? "true" : "false"
      );
    });

    productCards.forEach(card => {
      const category =
        card.dataset.yoyirCategory || "";

      const visible =
        matchesFilter(category, filter);

      card.hidden = !visible;
    });
  };

  filterButtons.forEach(button => {
    button.addEventListener("click", () => {
      applyFilter(button.dataset.yoyirFilter);
    });
  });

  jumpButtons.forEach(button => {
    button.addEventListener("click", () => {
      const requested =
        button.dataset.yoyirJump;

      let target = requested;

      const filterExists =
        filterButtons.some(
          item =>
            item.dataset.yoyirFilter === requested
        );

      if (!filterExists) {
        target = "all";
      }

      applyFilter(target);

      productsSection?.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    });
  });

  applyFilter("all");
})();
