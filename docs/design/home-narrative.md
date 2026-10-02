# Home Page - Narrativa Visual e Interactiva

## Objetivo

Crear una página de inicio de vanguardia que no sea un "menú aburrido", sino un **portal inmersivo** que cuenta la historia de cómo tres creadores/universos (Bienestar, Agendas estéticas, y Tecnología/Datos) se unieron para entregar productos digitales de calidad.

---

## Estructura Visual (Sin código)

### Sección 1: Hero Inmersivo
**Altura:** Full viewport (100vh)

**Componentes:**
- **Fondo dinámico:** Video generado por IA o loop visual sofisticado
  - Muestra la fusión de 3 elementos: ondas suaves (bienestar), patrones geométricos (planners), código/datos (tech)
  - Duración: 8-12 segundos en loop
  - Resolución: 1920x1080 mínimo
  - Formato: MP4 WebM (optimizado para web)

- **Overlay Narrativo:** Texto en capas
  - Línea 1 (arriba): "Tres universos. Un motor digital."
  - Línea 2 (centro): Animación de entrada (fade-in + slide)
  - Línea 3 (abajo): "Productos pensados para ti. En cada forma."

- **CTA Sutil:** "Descubre los universos" (botón con efecto hover)
  - Posición: Abajo, centrado
  - Animación: Pulse infinito (parpadeo suave)

**Estética:**
- Colores neutros (blanco, gris oscuro)
- Tipografía grande y bold (72px+)
- Sombras suaves, sin agresividad

---

### Sección 2: Presentación de los 3 Creadores
**Altura:** Auto (contenido fluido)
**Padding:** 80px horizontal, 60px vertical

**Layout:** 3 columnas (responsive: 1 columna en mobile)

**Por cada columna:**

#### Columna 1: Ebooks para la vida
- **Icono/Avatar:** Ilustración minimalista (hoja, bienestar, calidez)
- **Nombre:** "Ebooks para la vida"
- **Descripción (40-60 caracteres):**
  > "Conocimiento transformador sobre bienestar, TDAH y autodescubrimiento en formato PDF y EPUB."
- **Tono de voz:** Cálido, accesible, empoderante
- **Colores destacados:** Beige, Teal, Coral

#### Columna 2: YOYI'R
- **Icono/Avatar:** Ilustración de agenda, planner, creatividad visual
- **Nombre:** "YOYI'R"
- **Descripción (40-60 caracteres):**
  > "Agendas y planners diseñados con estetismo. Organiza tu vida, beautify your days."
- **Tono de voz:** Minimalista, inspirador, sofisticado
- **Colores destacados:** Lavanda, Morado

#### Columna 3: EstrategIA
- **Icono/Avatar:** Ilustración de gráficos, código, datos, neón
- **Nombre:** "EstrategIA"
- **Descripción (40-60 caracteres):**
  > "Micro-apps interactivas y herramientas de datos. Tecnología para decisiones inteligentes."
- **Tono de voz:** Futurista, técnico pero accesible
- **Colores destacados:** Azul Neón, Magenta

**Interacción:**
- Hover en columna: Elevación (box-shadow), escala suave (1.05x)
- Transición: 0.3s ease-out

---

### Sección 3: Portal de Entrada a Cada Universo
**Altura:** Auto (3 bloques grandes)
**Padding:** 60px

**Layout:** 3 cards visuales (grid 3 columnas, responsive 1 columna)

**Card 1: Ebooks para la vida**
- **Fondo:** Gradiente beige → teal (135deg)
- **Icono:** Libro abierto (SVG animado)
- **Headline:** "Explora Ebooks"
- **Subheadline:** "Desde $5.99"
- **CTA Button:** "Entrar a Ebooks" → enlace a `/ebooks`
- **Animación:** Al scroll, aparecer con slide-up + fade-in

**Card 2: YOYI'R**
- **Fondo:** Gradiente lavanda → morado (135deg)
- **Icono:** Agenda/Planner (SVG animado)
- **Headline:** "Descubre Planners"
- **Subheadline:** "Desde $9.99"
- **CTA Button:** "Entrar a YOYI'R" → enlace a `/yoyir`
- **Animación:** Delay 0.2s vs Card 1

**Card 3: EstrategIA**
- **Fondo:** Gradiente oscuro → azul neón (135deg)
- **Icono:** Gráfico/Datos (SVG animado con glow)
- **Headline:** "Accede a Herramientas"
- **Subheadline:** "Desde $14.99"
- **CTA Button:** "Entrar a EstrategIA" → enlace a `/estrategia`
- **Animación:** Delay 0.4s vs Card 1

**Hover efecto global:**
- Box-shadow con color de tema
- Transformación: translateY(-8px)
- Duración: 0.4s

---

### Sección 4: Footer de Home
**Altura:** Auto
**Padding:** 40px

**Contenido:**
- Línea 1: "¿No sabes dónde empezar?"
- Línea 2: "Pequeño cuestionario" (link opcional, futuro)
- Línea 3: Separador visual
- Línea 4: Links de navegación (Sobre Nosotros, FAQ, Contacto)
- Línea 5: Redes sociales (iconos SVG)

---

## Animaciones y Micro-interacciones

### Scroll-Driven Animations

```
1. Hero → Fade-out del video mientras baja
2. Sección Creadores → Cards animan entrada al llegar a viewport
3. Cards Portal → Elevation efecto al pasar mouse
4. Button CTA → Pulse continuo (parpadeo suave)
```

### Transiciones

- Entrada a página: 0.5s fade-in global
- Hover en cards: 0.3-0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)
- Navegación entre rutas: 0.5s fade-out + fade-in

### Interactividad

- Click en card → Destello de luz (radial gradient flash)
- Hover en botón CTA → Glow efecto (box-shadow expandible)
- Navbar aparece al scroll down 100px (sticky, con fade-in)

---

## Tecnologías Recomendadas

- **Video:** Generador de IA (Synthesia, Runway) o video estático MP4
- **Animaciones:** CSS transitions + GSAP (si se requiere complejidad)
- **Scroll:** Intersection Observer API (vanilla JS) o Lenis.js (smooth scroll)
- **Iconos:** SVG inline con CSS animations
- **Tipografía:** Google Fonts (serif, sans-serif, monospace)

---

## Responsive Breakpoints

| Dispositivo | Ancho | Ajustes |
|-------------|-------|---------|
| Desktop | 1920px+ | 3 columnas/cards, font 72px hero |
| Tablet | 768px - 1024px | 2 columnas, font 48px hero |
| Mobile | 320px - 767px | 1 columna stacked, font 32px hero |

---

## Accesibilidad

- Texto alternativo en imágenes/videos (alt tags, aria-labels)
- Ratios de contraste AA mínimo (4.5:1)
- Navegación por teclado (Tab, Enter)
- Focus states visibles en botones
- Subtítulos en video (SI-SE-USA VIDEO)

---

## Ejemplos de Inspiración Visual

- Stripe.com (hero fluido, narrativa clara)
- Framer.com (animaciones suaves, enfoque en creatividad)
- Vercel.com (transiciones cinemáticas, design moderno)
- Mailchimp.com (humor, colores vibrantes)

---

## Notas de Desarrollo

1. **Performance:** Optimizar video (WebP, compresión), lazy-load de imágenes
2. **SEO:** Meta tags, Open Graph (og:image, og:description)
3. **Analytics:** Tracking de clicks en CTA por marca
4. **A/B Testing:** Versión sin video vs. con video para comparar engagement

---

## Checklist Pre-Implementación

- [ ] Video/Loop generado o descargado (1920x1080, <30MB)
- [ ] Paletas de color definidas en CSS variables
- [ ] SVG icons creados/descargados (optimizados)
- [ ] Tipografías desde Google Fonts importadas
- [ ] Breakpoints responsive testeados en Figma
- [ ] Copy final validado (sin typos)
- [ ] Accessibility audit (WAVE, Axe)
