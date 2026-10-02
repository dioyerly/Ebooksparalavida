# Ebooks para la vida — Plataforma Multi-Marca
## Documento Maestro de Proyecto

**Versión:** 1.0  
**Rama de desarrollo:** `feature/multi-brand-evolution`  
**Estado:** En arquitectura y documentación  
**Último actualizado:** 2026-10-02  

---

## 1. VISIÓN DEL PROYECTO

### ¿Qué es?
Evolución de la tienda actual `Ebooksparalavida` hacia una **plataforma unificada** que fusiona tres universos digitales bajo un motor técnico único, pero con identidades visuales y propósitos propios.

### ¿A quién le sirve?
- Creadores de contenido digital que entienden que los productos digitales tienen naturaleza diferente
- Usuarios que buscan: conocimiento (ebooks), organización (planners), y herramientas interactivas (datos/tech)

### ¿Cómo es la experiencia?
NO es un típico "elige tu aventura" con botones fríos. Es una **página web unificada** que cuenta una historia:
- **Home:** Portal inmersivo que presenta la fusión de 3 creadores
- **Navegación:** Al entrar a cada marca, la interfaz adopta su propia paleta visual
- **Carrito:** Agnóstico de marca — acepta items de cualquier universo
- **Checkout:** Pagos unificados (Mercado Pago/PayPal)

---

## 2. LAS TRES MARCAS

| Marca | Estética | Productos | Colores | Vibe |
|-------|----------|-----------|---------|------|
| **Ebooks para la vida** | Calidez, bienestar | PDF/EPUB (conocimiento) | Beige, Teal, Coral | Spa, naturales, empoderante |
| **YOYI'R** | Minimalista, creativo | ZIP (agendas, planners) | Lavanda, Morado | Sofisticado, inspirador |
| **EstrategIA** | Tecnológica, futurista | HTML interactivo + suscripciones | Oscuro, Azul Neón, Magenta | Edgy, moderno, avanzado |

---

## 3. ARQUITECTURA TÉCNICA (Alto Nivel)

### Backend (Flask)

```
app.py (orquestador)
  ├── blueprints/
  │   ├── ebooks.py (rutas: /ebooks/*)
  │   ├── yoyir.py (rutas: /yoyir/*)
  │   ├── estrategia.py (rutas: /estrategia/*)
  │   ├── cart.py (rutas: /cart/*, agnóstico)
  │   ├── checkout.py (rutas: /checkout/*, agnóstico)
  │   └── admin.py (rutas: /admin/*, compartido)
  ├── models.py (con columna marca en products)
  ├── config.py
  └── services.py (compartidos)
```

### Frontend (Templates + CSS)

```
templates/
  ├── base.html (shell común)
  ├── home.html (home narrativa)
  ├── ebooks/, yoyir/, estrategia/ (templates por marca)

static/css/
  ├── global.css (común)
  ├── theme-ebooks.css (variables CSS por marca)
  ├── theme-yoyir.css
  └── theme-estrategia.css

static/js/
  ├── brands/ (lógica opcional por marca)
  └── cart.js (agnóstico)
```

### Base de Datos

```
Cambio mínimo: Agregar columna marca a tabla products
  → marca: ENUM('ebooks', 'yoyir', 'estrategia')
  
Resto de tablas: SIN CAMBIOS
  → orders, order_items, users funcionan igual
  → Carrito (session['cart']) agnóstico de marca
```

---

## 4. REGLA DE ORO: PROHIBICIONES

✋ **ESTO NO SE HACE TODAVÍA:**

1. ❌ NO escribir código masivo de implementación
2. ❌ NO modificar la tienda actual (`main`) que está en producción
3. ❌ NO cambiar rutas existentes (ej: `/products`)
4. ❌ NO alterar modelos sin documentar cambios
5. ❌ NO tocar el checkout/pagos de producción

✅ **LO QUE SÍ HACEMOS:**

- ✅ Documentar arquitectura conceptual
- ✅ Organizar estructura de carpetas
- ✅ Validar cambios localmente en `localhost:5000`
- ✅ Trabajar **SIEMPRE** en rama `feature/multi-brand-evolution`
- ✅ Hacer commits descriptivos con contexto

---

## 5. FASES DE IMPLEMENTACIÓN (Roadmap)

### Fase 1: Arquitectura y Documentación ✅ (ACTUAL)
- [x] Crear estructura de carpetas
- [x] Documentar blueprints
- [x] Documentar rutas
- [x] Definir schema de BD
- [x] Crear paletas de color
- [x] Documentar home narrativa
- [ ] Commit inicial a rama

### Fase 2: Blueprints Vacíos
- [ ] Crear `blueprints/ebooks.py` (sin lógica)
- [ ] Crear `blueprints/yoyir.py`
- [ ] Crear `blueprints/estrategia.py`
- [ ] Crear `blueprints/cart.py`
- [ ] Crear `blueprints/checkout.py`
- [ ] Crear `blueprints/admin.py`
- [ ] Registrar en `app.py`

### Fase 3: Templates Base
- [ ] `templates/base.html` (shell común)
- [ ] `templates/home.html` (home narrativa)
- [ ] Templates por marca (sin contenido visual)

### Fase 4: Sistema de Temas CSS
- [ ] `static/css/global.css`
- [ ] `static/css/theme-ebooks.css`
- [ ] `static/css/theme-yoyir.css`
- [ ] `static/css/theme-estrategia.css`
- [ ] Pruebas de transición entre temas

### Fase 5: Lógica de Blueprints
- [ ] Rutas en `ebooks.py`, `yoyir.py`, `estrategia.py`
- [ ] Filtros, búsqueda
- [ ] Integración con modelos

### Fase 6: Home Narrativa (Video + Interacciones)
- [ ] Obtener/generar video de IA
- [ ] Implementar hero inmersivo
- [ ] Scroll-driven animations
- [ ] Micro-interacciones

### Fase 7: Testing en Localhost
- [ ] `flask run`
- [ ] Navegar entre marcas
- [ ] Verificar cambio de tema CSS
- [ ] Probar carrito unificado
- [ ] Testing en móvil (responsive)

### Fase 8: Merge a Main (Cuando esté Listo)
- [ ] Code review
- [ ] Testing final en producción
- [ ] Rollback plan documentado

---

## 6. CÓMO TRABAJAR LOCALMENTE

### Setup Inicial

```bash
# Traer la rama de desarrollo
git checkout feature/multi-brand-evolution
git pull origin feature/multi-brand-evolution

# Instalar dependencias (si hay nuevas)
pip install -r requirements.txt

# Levantar servidor en localhost
flask run

# Abrir en navegador
# http://localhost:5000/
```

### Flujo de Trabajo

1. Crea rama local: `git checkout -b feature/multi-brand-evolution-mi-cambio`
2. Haz cambios en la estructura o documentación
3. Commit descriptivo: `git commit -m "feat: agregar blueprint de YOYI'R estructura"`
4. Push a remoto: `git push origin feature/multi-brand-evolution-mi-cambio`
5. Abre PR en GitHub (para revisión)

### Validación en Localhost

```bash
# Ver que la app corre sin errores
flask run

# Verificar templates
# Ir a http://localhost:5000/ebooks
# Ir a http://localhost:5000/yoyir
# Ir a http://localhost:5000/estrategia

# Ver en consola del navegador (F12) que CSS se carga correctamente
# Verificar que body tiene clase correcta: class="theme-ebooks", etc.
```

---

## 7. DOCUMENTACIÓN GENERADA

En `/docs/`:

| Archivo | Propósito |
|---------|-----------|
| `architecture/blueprint-structure.md` | Cómo se organizan los blueprints Flask |
| `architecture/routes-map.md` | Todas las rutas públicas y privadas |
| `architecture/database-schema-updates.md` | Cambios en la BD (mínimos) |
| `design/color-palettes.md` | Paletas de color por marca + CSS vars |
| `design/home-narrative.md` | Estructura visual y narrativa del home |
| `PROJECT-MASTER.md` | Este archivo |

**Cómo usar:**
1. Lee `PROJECT-MASTER.md` (contexto global)
2. Lee `architecture/blueprint-structure.md` (cómo organizar código)
3. Lee `architecture/routes-map.md` (qué rutas crear)
4. Lee `design/color-palettes.md` (paletas CSS)
5. Lee `design/home-narrative.md` (cómo ver se el home)

---

## 8. CONTACTO Y PREGUNTAS

**¿Dudas sobre la arquitectura?**
→ Revisa `blueprint-structure.md` y `routes-map.md`

**¿No sabes qué color usar?**
→ Revisa `color-palettes.md`

**¿Cómo debe verse el home?**
→ Revisa `home-narrative.md`

**¿Cambié algo y no funciona?**
→ Consulta `database-schema-updates.md` para verificar si necesita migración

---

## 9. CHECKLIST PREVIO A MERGE (Futura)

- [ ] Todas las documentaciones revisadas
- [ ] Estructura de carpetas en lugar
- [ ] Blueprints vacíos compilables
- [ ] Templates base sin errores
- [ ] CSS variables funcionando
- [ ] Pruebas en localhost exitosas
- [ ] Responsive verificado (desktop, tablet, mobile)
- [ ] No hay conflictos con `main`
- [ ] Commits bien documentados
- [ ] Code review aprobado

---

## 10. NOTAS IMPORTANTES

1. **Seguridad:** NO cambiar autenticación ni pagos hasta que esté 100% listo
2. **Performance:** Optimizar videos, lazy-load imágenes
3. **SEO:** Meta tags en home por marca
4. **Analytics:** Trackear clicks en CTA por marca
5. **Fallback:** Si algo falla, siempre podemos hacer rollback a `main`

---

## Historial de Cambios

| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2026-10-02 | Creación de documento maestro | Claude |
| | Documentación de arquitectura | Claude |
| | Definición de paletas de color | Claude |
| | Narrativa del home | Claude |

---

**Estado:** ✅ Documentación conceptual completa  
**Próximo paso:** Crear estructura de carpetas y blueprints vacíos
