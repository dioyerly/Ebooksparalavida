# SUGA DESDE AQUÍ

Registro persistente de la evolución de la Home unificada.

## Alcance

Este trabajo corresponde exclusivamente a la nueva versión de desarrollo de la plataforma en la rama `feature/multi-brand-evolution` y a la ruta local `/universos`.

El objetivo es convertir la Home en una experiencia editorial y tecnológica para una plataforma que crea productos digitales de tres universos:

- Ebooks para la vida: publicaciones digitales.
- YOYI’R: planners y recursos de organización.
- EstrategIA: herramientas y micro-apps digitales.

## Advertencias permanentes

- No modificar `main`.
- No tocar la tienda real publicada.
- No usar credenciales ni base de datos de producción.
- No modificar Product, Order, checkout, pagos, emails, descargas, access codes ni lógica comercial.
- No hacer deploy de estos cambios sin aprobación explícita.
- Revisar siempre `git branch --show-current` antes de trabajar; debe ser exactamente `feature/multi-brand-evolution`.
- Los cambios visuales quedan para revisión local hasta nueva aprobación.

## Qué se hizo

- Se reemplazó la Home de `/universos` por una composición editorial propia, sin emojis ni stock.
- Se crearon Hero, universos narrativos, transición cromática, kinetic typography, showcase y cierre.
- Se añadieron animaciones con CSS, `IntersectionObserver`, `requestAnimationFrame`, parallax ligero y soporte para `prefers-reduced-motion`.
- Se incorporaron productos visuales reales y assets locales en `frontend/assets/images/home-products/`.
- Se creó el concepto Orbital Digital para el Hero: núcleo tecnológico, productos orbitando, profundidad, luces y movimiento lento.
- Se añadieron cuatro assets generados para la órbita: `orbit-ebook.png`, `orbit-planner.png`, `orbit-estrategia.png` y `orbit-platform.png`.
- La órbita usa un único centro geométrico basado en el núcleo, radios derivados del tamaño real, separación angular y `ResizeObserver`.
- El núcleo queda fijo; los productos cambian posición, escala, opacidad, blur y `z-index` durante una vuelta de 36 segundos.
- La narrativa cromática quedó ordenada como Hero oscuro → EstrategIA → YOYI’R → Ebooks cálido.

## Archivos principales

- `backend/templates/home_unified.html`
- `frontend/assets/css/home-unified.css`
- `frontend/assets/js/home-unified.js`
- `frontend/assets/images/home-products/`

## Qué falta

- Revisar visualmente la última versión con la persona responsable.
- Conectar productos, nombres, previews, precios y enlaces reales cuando se apruebe la dirección visual.
- Determinar si los assets generados deben conservarse, sustituirse o complementarse con material final de marca.
- Hacer una revisión final de rendimiento y accesibilidad antes de cualquier publicación.

## Validación realizada

- Se comprobó la Home en 375, 390, 430, 768, 1024 y 1440 px.
- Se comprobó ausencia de overflow horizontal y errores JavaScript en la vista aislada.
- Se verificó que los assets orbitales responden correctamente.
- Se verificó que el centro del núcleo permaneció constante durante una vuelta completa.

## Estado de publicación

Este archivo se actualiza junto con cada guardado autorizado en GitHub. No representa autorización de producción. La publicación real requiere aprobación explícita posterior.
