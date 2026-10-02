# Estructura de Blueprints - Plataforma Multi-Marca

## Visión General
La aplicación Flask actual será modularizada en blueprints independientes por marca, manteniendo un carrito y sistema de pagos unificado.

---

## Blueprints por Marca

### 1. **ebooks_bp** (Ebooks para la vida)
**Ruta base:** `/ebooks`

**Responsabilidades:**
- Catálogo de ebooks (PDF/EPUB)
- Página de producto individual
- Filtros por categoría (Bienestar, TDAH, etc.)
- Búsqueda
- Reseñas/calificaciones

**Templates:**
- `templates/ebooks/catalog.html` - Catálogo
- `templates/ebooks/product.html` - Detalle producto
- `templates/ebooks/category.html` - Categorías

**Modelos de datos:**
- `Product` con `marca='ebooks'` y `tipo='pdf'` o `'epub'`

**Estética:**
- Colores: Beige, Teal, Coral
- CSS: `static/css/theme-ebooks.css`

---

### 2. **yoyir_bp** (YOYI'R - Agendas y Planners)
**Ruta base:** `/yoyir`

**Responsabilidades:**
- Catálogo de agendas/planners (ZIP descargables)
- Página de producto individual
- Filtros por tipo (Agenda anual, Planner mensual, etc.)
- Búsqueda

**Templates:**
- `templates/yoyir/catalog.html` - Catálogo
- `templates/yoyir/product.html` - Detalle producto

**Modelos de datos:**
- `Product` con `marca='yoyir'` y `tipo='zip'`

**Estética:**
- Colores: Lavanda, Morado Pastel
- CSS: `static/css/theme-yoyir.css`

---

### 3. **estrategia_bp** (EstrategIA - Micro-apps e Herramientas)
**Ruta base:** `/estrategia`

**Responsabilidades:**
- Catálogo de herramientas interactivas (HTML)
- Página de producto individual
- Acceso a micro-apps
- Gestión de suscripciones (futuro)

**Templates:**
- `templates/estrategia/catalog.html` - Catálogo
- `templates/estrategia/product.html` - Detalle producto
- `templates/estrategia/app.html` - Visor de app HTML

**Modelos de datos:**
- `Product` con `marca='estrategia'` y `tipo='html_interactive'`

**Estética:**
- Colores: Oscuro con Azul Neón, Magenta Neón
- CSS: `static/css/theme-estrategia.css`

---

## Blueprints Compartidos (Agnósticos de Marca)

### 4. **cart_bp**
**Ruta base:** `/cart`

**Responsabilidades:**
- Ver carrito (items de cualquier marca)
- Agregar/remover productos
- Cálculo de total
- Persistencia en `session['cart']`

**Nota:** El carrito NO se personaliza por marca. Funciona igual para cualquier producto.

---

### 5. **checkout_bp**
**Ruta base:** `/checkout`

**Responsabilidades:**
- Procesar pagos (Mercado Pago / PayPal)
- Crear órdenes en BD
- Gestionar webhooks
- Envío de emails de confirmación

**Nota:** Unificado para todas las marcas. No cambia por marca.

---

### 6. **admin_bp** (Panel Admin Unificado)
**Ruta base:** `/admin`

**Responsabilidades:**
- Dashboard con ventas totales
- Gestión de productos (crear, editar, eliminar)
- Seleccionar marca al crear producto
- Subida de archivos (PDF, ZIP, HTML)
- Gestión de órdenes
- Analytics por marca

**Nota:** Un solo admin para gestionar las 3 marcas.

---

## Estructura de Archivos (Resultado esperado)

```
backend/
├── blueprints/
│   ├── __init__.py (importar todos los blueprints)
│   ├── ebooks.py
│   ├── yoyir.py
│   ├── estrategia.py
│   ├── cart.py
│   ├── checkout.py
│   └── admin.py
├── templates/
│   ├── base.html (template base común)
│   ├── home.html (home narrativa)
│   ├── ebooks/
│   │   ├── catalog.html
│   │   ├── product.html
│   │   └── category.html
│   ├── yoyir/
│   │   ├── catalog.html
│   │   └── product.html
│   └── estrategia/
│       ├── catalog.html
│       ├── product.html
│       └── app.html
├── static/
│   ├── css/
│   │   ├── global.css (común a todas)
│   │   ├── theme-ebooks.css
│   │   ├── theme-yoyir.css
│   │   └── theme-estrategia.css
│   └── js/
│       ├── brands/
│       │   ├── ebooks.js
│       │   ├── yoyir.js
│       │   └── estrategia.js
│       └── cart.js (agnóstico)
├── app.py (orquestador, registra blueprints)
├── config.py (igual que hoy)
├── models.py (igual que hoy, + columna marca)
└── services.py (servicios compartidos)
```

---

## Registro de Blueprints en app.py

En `app.py`, se registrarán así:

```python
# Pseudo-código (no real todavía)
from blueprints.ebooks import ebooks_bp
from blueprints.yoyir import yoyir_bp
from blueprints.estrategia import estrategia_bp
from blueprints.cart import cart_bp
from blueprints.checkout import checkout_bp
from blueprints.admin import admin_bp

app.register_blueprint(ebooks_bp, url_prefix='/ebooks')
app.register_blueprint(yoyir_bp, url_prefix='/yoyir')
app.register_blueprint(estrategia_bp, url_prefix='/estrategia')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(checkout_bp, url_prefix='/checkout')
app.register_blueprint(admin_bp, url_prefix='/admin')
```

---

## Notas Importantes

- Cada blueprint puede importar servicios comunes (`models.py`, `config.py`).
- El contexto de marca se pasa vía variable en plantillas: `{{ brand }}`.
- El carrito y checkout NO cambian de código por marca, son agnósticos.
- Cada blueprint renderiza sus propios templates con su propia estética CSS.
