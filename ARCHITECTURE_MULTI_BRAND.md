# Arquitectura Multi-Marca - Estrategia Técnica

## 📊 Estado Actual vs Futuro

### Estado Actual (Producción)
```
Ebooks para la vida (single brand)
├── PDF/EPUB ebooks
├── HTML interactivos
├── Kits (bonus files)
└── Admin panel
```

### Visión Futuro (3 Marcas, 1 Plataforma)
```
Plataforma Unificada
├── Ebooks para la vida (beige/teal/coral)
│   ├── PDF/EPUB ebooks
│   ├── HTML interactivos
│   └── Kits
├── YOYI'R (lavanda/morado pastel)
│   ├── Agendas descargables (.zip)
│   ├── Planners
│   └── Kits de recursos
└── EstrategIA (oscuro/azul eléctrico/magenta)
    ├── Micro-apps HTML
    ├── Herramientas de datos
    └── Suscripciones (futuro)
```

---

## 🌳 Estrategia de Ramas Git

### Estructura de Ramas Recomendada

```
main (producción - NUNCA se toca directamente)
  ↑ (solo merges desde release branches)
  
├─ release/v1-multi-brand (rama de preparación para go-live futuro)
│  ↑ (merges verificados y testeados)
│  
├─ feature/multi-brand-evolution (rama maestra de desarrollo)
│  │
│  ├─ feature/multi-brand-routing (rutas Flask segregadas)
│  ├─ feature/multi-brand-themes (sistema CSS modular)
│  ├─ feature/multi-brand-templates (templates por marca)
│  └─ feature/multi-brand-admin (panel admin unificado)
│
└─ hotfix/* (parches urgentes a producción)
   └─ Siempre se crea desde main
```

### Flujo de Trabajo en 2 Computadoras

**Escenario: Trabajas desde 2 máquinas, quieres sincronizarse sin afectar main**

```
Máquina A (Escritorio)              Máquina B (Laptop)
    │                                    │
    └─ git checkout -b feature/multi-brand-evolution
       git pull origin                   │
       [Trabajo local]              └─ git checkout feature/multi-brand-evolution
       git push origin                   git pull origin
                                        [Trabajo local]
                                        git push origin
    │                                    │
    └─ git pull origin ◄────────────────┘
       [Verifica cambios]
       git push [si hay cambios locales]
```

**Regla Crítica:**
- Ambas máquinas trabajan en la rama `feature/multi-brand-evolution`
- Siempre hacer `git pull origin` antes de empezar a trabajar
- Siempre hacer `git push` después de cada sesión de trabajo
- NUNCA hacer merge a `main` hasta que esté todo testeado y listo

---

## 📁 Estructura de Carpetas Propuesta

### Antes (Actual)
```
ebooks-store/
├── backend/
│   ├── app.py (todo mezclado)
│   ├── models.py
│   ├── services.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── product.html
│       └── admin/
└── frontend/
    └── assets/
        └── css/
            └── style.css (todo mezclado)
```

### Después (Propuesto)
```
ebooks-store/
├── backend/
│   ├── app.py (enrutador principal)
│   ├── models.py (compartido entre marcas)
│   ├── services.py (compartido)
│   ├── config.py (actualizado para multi-brand)
│   │
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── ebooks/ (brand: ebooks-para-la-vida)
│   │   │   ├── __init__.py
│   │   │   ├── routes.py (rutas /ebooks/*)
│   │   │   ├── helpers.py
│   │   │   └── templates/
│   │   │       ├── product.html
│   │   │       ├── home.html
│   │   │       └── checkout.html
│   │   │
│   │   ├── yoyir/ (brand: YOYI'R)
│   │   │   ├── __init__.py
│   │   │   ├── routes.py (rutas /yoyir/*)
│   │   │   ├── helpers.py
│   │   │   └── templates/
│   │   │       ├── product.html
│   │   │       ├── home.html
│   │   │       └── checkout.html
│   │   │
│   │   ├── estrategia/ (brand: EstrategIA)
│   │   │   ├── __init__.py
│   │   │   ├── routes.py (rutas /estrategia/*)
│   │   │   ├── helpers.py
│   │   │   └── templates/
│   │   │       ├── product.html
│   │   │       ├── home.html
│   │   │       └── checkout.html
│   │   │
│   │   └── admin/ (panel unificado)
│   │       ├── __init__.py
│   │       ├── routes.py (rutas /admin/*)
│   │       ├── helpers.py
│   │       └── templates/
│   │           ├── dashboard.html
│   │           ├── products.html
│   │           └── orders.html
│   │
│   └── templates/
│       └── base/ (templates compartidos)
│           ├── base.html (template raíz)
│           ├── navbar.html
│           ├── footer.html
│           └── cart.html
│
├── frontend/
│   └── assets/
│       ├── css/
│       │   ├── index.css (importa todos los demás)
│       │   ├── variables.css (variables CSS customizables)
│       │   ├── base.css (estilos base compartidos)
│       │   │
│       │   └── themes/
│       │       ├── ebooks.css (beige/teal/coral)
│       │       ├── yoyir.css (lavanda/morado)
│       │       └── estrategia.css (oscuro/azul/magenta)
│       │
│       ├── js/
│       │   ├── shared/
│       │   │   ├── cart.js
│       │   │   ├── checkout.js
│       │   │   └── tracking.js
│       │   │
│       │   └── themes/
│       │       ├── ebooks.js
│       │       ├── yoyir.js
│       │       └── estrategia.js
│       │
│       └── images/
│           ├── logos/
│           │   ├── logo-ebooks.svg
│           │   ├── logo-yoyir.svg
│           │   └── logo-estrategia.svg
│           │
│           └── themes/
│               ├── ebooks/
│               ├── yoyir/
│               └── estrategia/
│
└── ARCHITECTURE_MULTI_BRAND.md
```

---

## 🎨 Sistema CSS Modular por Marca

### Paletas de Color

```css
/* variables.css */

/* === Ebooks para la vida === */
:root[data-brand="ebooks"] {
  --primary: #C9756B;      /* Coral */
  --secondary: #3A5F5F;    /* Teal */
  --accent: #D98B7E;       /* Coral más claro */
  --bg-primary: #F5F1EB;   /* Beige */
  --bg-secondary: #FAFAF8; /* Beige muy claro */
  --text-primary: #2D2D2D; /* Gris oscuro */
}

/* === YOYI'R === */
:root[data-brand="yoyir"] {
  --primary: #B599D9;      /* Lavanda */
  --secondary: #E8D5F2;    /* Lavanda pálida */
  --accent: #D8A3E8;       /* Morado pastel */
  --bg-primary: #F9F6FC;   /* Lavanda muy claro */
  --bg-secondary: #FBF8FD; /* Lavanda ultra claro */
  --text-primary: #4A3F5C; /* Morado oscuro */
}

/* === EstrategIA === */
:root[data-brand="estrategia"] {
  --primary: #00D9FF;      /* Azul eléctrico */
  --secondary: #FF00FF;    /* Magenta neón */
  --accent: #00F0FF;       /* Cyan */
  --bg-primary: #0A0E27;   /* Azul muy oscuro */
  --bg-secondary: #111639; /* Azul oscuro */
  --text-primary: #E0E0E0; /* Gris claro */
}
```

### Estructura CSS

```css
/* index.css */
@import url('variables.css');
@import url('base.css');
@import url('themes/ebooks.css');
@import url('themes/yoyir.css');
@import url('themes/estrategia.css');
```

```css
/* base.css - Estilos que funcionan en todas las marcas */
body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'DM Sans', Arial, sans-serif;
}

.btn-primary {
  background: var(--primary);
  color: white;
  /* ... */
}

.navbar {
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--primary);
}

/* Estilos específicos compartidos */
.product-card {
  border: 1px solid var(--primary);
  /* ... */
}
```

```css
/* themes/ebooks.css - Estilos específicos de marca */
[data-brand="ebooks"] .product-card {
  box-shadow: 0 4px 12px rgba(201, 117, 107, 0.15);
  border-radius: 8px;
}

[data-brand="ebooks"] .header-hero {
  background: linear-gradient(135deg, #C9756B 0%, #3A5F5F 100%);
}
```

### Cómo Funciona en Templates

```html
<!-- base.html -->
<html data-brand="{{ request.blueprint | default('ebooks') }}">
  <head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
  </head>
  <body>
    <!-- El atributo data-brand cambia automáticamente -->
    <!-- Los CSS variables.css se aplican según el blueprint actual -->
  </body>
</html>
```

---

## 🚀 Rutas Flask Segregadas

### Arquitectura de Blueprints

**Antes (monolítico):**
```
GET  /                      → home
GET  /shop                  → tienda
POST /cart/add/<id>         → agregar carrito
GET  /download/<token>      → descargar
POST /admin/login           → login admin
```

**Después (modular por marca):**
```
/* Ebooks para la vida - URL base / (retrocompatible) */
GET  /                      → ebooks.home
GET  /shop                  → ebooks.shop
GET  /product/<slug>        → ebooks.product
POST /cart/add/<id>         → shared.add_to_cart
GET  /download/<token>      → ebooks.download
POST /admin/*               → admin.* (unificado)

/* YOYI'R - URL base /yoyir */
GET  /yoyir/                → yoyir.home
GET  /yoyir/shop            → yoyir.shop
GET  /yoyir/product/<slug>  → yoyir.product
POST /yoyir/cart/add/<id>   → shared.add_to_cart
GET  /yoyir/download/<token>→ yoyir.download
POST /yoyir/checkout        → shared.checkout (compartido)

/* EstrategIA - URL base /estrategia */
GET  /estrategia/           → estrategia.home
GET  /estrategia/apps       → estrategia.apps
GET  /estrategia/tools/<id> → estrategia.tool
POST /estrategia/checkout   → shared.checkout (compartido)

/* Admin - URL base /admin (unificado) */
POST /admin/login           → admin.login
GET  /admin/dashboard       → admin.dashboard (multi-brand view)
POST /admin/products        → admin.create_product (con selector de marca)
GET  /admin/orders          → admin.orders (todas las marcas)
```

### Estructura de Blueprints en Python

```python
# backend/blueprints/__init__.py
from flask import Blueprint

def register_blueprints(app):
    from .ebooks import ebooks_bp
    from .yoyir import yoyir_bp
    from .estrategia import estrategia_bp
    from .admin import admin_bp
    
    app.register_blueprint(ebooks_bp, url_prefix='')  # Root
    app.register_blueprint(yoyir_bp, url_prefix='/yoyir')
    app.register_blueprint(estrategia_bp, url_prefix='/estrategia')
    app.register_blueprint(admin_bp, url_prefix='/admin')
```

```python
# backend/blueprints/ebooks/__init__.py
from flask import Blueprint

ebooks_bp = Blueprint(
    'ebooks',
    __name__,
    template_folder='templates'
)

from .routes import *  # Importa todas las rutas
```

```python
# backend/blueprints/ebooks/routes.py
from flask import render_template
from . import ebooks_bp

@ebooks_bp.route('/')
def home():
    return render_template('ebooks/home.html')

@ebooks_bp.route('/shop')
def shop():
    # Filtra productos con brand='ebooks'
    return render_template('ebooks/shop.html')
```

---

## 🗄️ Cambios en el Modelo de Datos

### Actualización de Tablas (sin romper datos actuales)

```python
# backend/models.py

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... campos existentes ...
    
    # NUEVO: campo de marca
    brand = db.Column(
        db.String(30),
        nullable=False,
        default='ebooks',  # Retrocompatible: productos existentes = 'ebooks'
        index=True
    )
    # Valores válidos: 'ebooks', 'yoyir', 'estrategia'
```

**Migration paso a paso:**
1. Agregar columna `brand` con default 'ebooks'
2. Productos existentes quedan automáticamente con brand='ebooks'
3. Nuevos productos pueden tener cualquier brand
4. Rutas Flask filtran por brand automáticamente

---

## 📋 Checklist de Implementación (Fases)

### Fase 1: Preparación de Infra (Esta rama: feature/multi-brand-evolution)
- [ ] Crear estructura de carpetas (blueprints, themes)
- [ ] Implementar sistema de variables CSS
- [ ] Configurar estructura de blueprints Flask
- [ ] Agregar campo `brand` a tabla Product (migration)
- [ ] Tests unitarios para routing

**Duración estimada:** 2-3 semanas
**Riesgo:** BAJO (todo en rama de desarrollo)
**Impacto en producción:** NINGUNO (no se toca main)

### Fase 2: Migración Gradual de Rutas (Después de Fase 1)
- [ ] Migrar ebooks.routes a blueprint ebooks/
- [ ] Crear yoyir blueprint (copia de ebooks con ajustes)
- [ ] Crear estrategia blueprint (copia de ebooks con ajustes)
- [ ] Tests de integración

**Duración estimada:** 3-4 semanas

### Fase 3: Temas y Estilos (Paralelo a Fase 2)
- [ ] Sistema CSS modular con variables
- [ ] Tema ebooks (actual)
- [ ] Tema yoyir (nuevo)
- [ ] Tema estrategia (nuevo)

**Duración estimada:** 2-3 semanas

### Fase 4: Admin Unificado
- [ ] Panel admin con selector de marca
- [ ] Vistas de órdenes multi-brand
- [ ] Analytics por marca

**Duración estimada:** 2-3 semanas

### Fase 5: Testing y Go-Live
- [ ] Tests E2E en todas las marcas
- [ ] Testing de retrocompatibilidad (URLs antiguas)
- [ ] Merge a release/v1-multi-brand
- [ ] Espera y validación en staging
- [ ] Merge a main

**Duración estimada:** 2 semanas

---

## 🔒 Retrocompatibilidad Garantizada

### URLs Antiguas Funcionan Igual

```
Sitio en Producción AHORA:
GET / → Ebooks Home
GET /shop → Ebooks Shop

Sitio en Producción DESPUÉS:
GET / → Ebooks Home (IGUAL)
GET /shop → Ebooks Shop (IGUAL)

Nuevas URLs DESPUÉS:
GET /yoyir/ → YOYI'R Home
GET /estrategia/ → EstrategIA Home
```

### SEO No Se Daña

- Las URLs actuales NO CAMBIAN
- Google sigue indexando lo mismo
- Nuevas marcas = nuevas URLs (no conflicto)
- No hay redirects 301 innecesarios

---

## 💾 Sincronización entre 2 Computadoras

### Día 1: Máquina A

```bash
cd ~/projects/ebooks-store
git checkout main
git pull origin
git checkout -b feature/multi-brand-evolution
git push -u origin feature/multi-brand-evolution

# Haces cambios locales...
git add backend/blueprints/
git commit -m "feat: crear estructura de blueprints"
git push origin
```

### Día 1: Máquina B (después)

```bash
cd ~/projects/ebooks-store
git checkout main
git pull origin
git checkout feature/multi-brand-evolution
git pull origin

# Ves cambios de Máquina A...
# Haces tus propios cambios...
git add frontend/assets/css/
git commit -m "feat: sistema CSS modular"
git push origin
```

### Día 2: Máquina A (próxima sesión)

```bash
git checkout feature/multi-brand-evolution
git pull origin  # Trae cambios de Máquina B

# Resuelves conflictos si los hay
# Continúas tu trabajo...
git push origin
```

---

## 🎯 Resumen Ejecutivo

| Aspecto | Hoy | Futuro |
|--------|-----|--------|
| **Marcas** | 1 (Ebooks) | 3 (Ebooks, YOYI'R, EstrategIA) |
| **URLs base** | / | /, /yoyir, /estrategia |
| **Estructura** | Monolítica | Modular (blueprints) |
| **Estilos** | 1 archivo CSS | Modular por tema |
| **Admin** | Simple | Multi-brand |
| **BD** | Sin campo brand | Con campo brand |
| **Ramas Git** | main | main + feature/multi-brand-evolution |
| **Riesgo** | CERO (desarrollo en rama) | CERO (no toca producción) |

---

## ✅ Próximos Pasos

1. **Confirma que estamos en la misma página:**
   - ¿Te gusta la estructura de carpetas?
   - ¿Te gusta la estrategia de ramas?
   - ¿Te gusta el sistema CSS?

2. **Antes de cualquier código:**
   - Crear rama `feature/multi-brand-evolution` en GitHub
   - Configurar .gitignore para las carpetas nuevas
   - Documentar en CLAUDE.md el flujo de trabajo

3. **Luego (en siguiente sesión):**
   - Empezar Fase 1: Preparación de Infra
   - Crear carpetas de blueprints
   - Implementar sistema CSS modular

---

## 📞 Notas Finales

- **No hay código masivo todavía:** Este documento es arquitectura pura.
- **Todo está en una rama:** `feature/multi-brand-evolution`, separado de `main`.
- **Máquinas sincronizadas:** Con git pull/push, ambas ven los mismos cambios.
- **Retrocompatibilidad:** Las URLs actuales NO cambian, los usuarios de Ebooks no ven nada.
- **Timeline:** Realista, por fases, sin presión.

¿Confirmas que todo esto tiene sentido y quieres que procedamos así?
