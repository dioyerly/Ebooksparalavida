# FASE 4: AUDITORÍA DE MODELO UNIVERSAL DE PRODUCTOS

**Fecha:** 2026-10-01  
**Rama:** `feature/multi-brand-evolution`  
**Responsable:** Auditoría arquitectónica sin modificación de código

---

## 1. ESTADO ACTUAL DEL MODELO PRODUCT

### Estructura de la tabla `product`

| Campo | Tipo | Nullable | Default | Propósito |
|-------|------|----------|---------|-----------|
| `id` | Integer | NO | PK | Identificador único |
| `slug` | String(120) | NO | - | URL única |
| `name` | String(160) | NO | - | Nombre de producto |
| `description` | Text | NO | - | Descripción completa |
| `short_description` | String(280) | SÍ | - | Resumen corto |
| `category` | String(80) | NO | - | Categoría (Vida & Bienestar, etc) |
| `price_ars` | Integer | NO | - | Precio en ARS |
| `cover_class` | String(40) | NO | "coral" | Clase CSS para portada |
| `accent` | String(20) | NO | "#C9756B" | Color secundario |
| `featured` | Boolean | NO | False | Mostrar en portada |
| `file_name` | String(255) | SÍ | - | Nombre de archivo principal (PDF/HTML) |
| `cover_image` | String(255) | SÍ | - | Path de imagen de portada |
| `cover_image_blob` | LargeBinary | SÍ | - | Imagen binaria almacenada |
| `product_type` | String(30) | NO | "pdf" | **TIPO DE PRODUCTO** |
| `source_html_path` | String(255) | SÍ | - | Path HTML original (para futuros usos) |
| `ebook_file` | LargeBinary | SÍ | - | Contenido PDF/HTML binario |
| `file_name_epub` | String(255) | SÍ | - | Nombre del archivo EPUB |
| `ebook_file_epub` | LargeBinary(4GB-1) | SÍ | - | Contenido EPUB binario |
| `instructions_pdf_name` | String(255) | SÍ | - | Nombre instrucciones (HTML only) |
| `instructions_pdf` | LargeBinary(4GB-1) | SÍ | - | PDF instrucciones binario |
| `zip_file` | LargeBinary(4GB-1) | SÍ | - | Archivo ZIP binario |
| `file_name_zip` | String(255) | SÍ | - | Nombre archivo ZIP |
| `is_kit` | Boolean | NO | False | ¿Es un KIT (bundled)? |
| `kit_price_ars` | Integer | SÍ | - | Precio especial si es KIT |
| `kit_description` | Text | SÍ | - | Descripción especial si es KIT |
| `created_at` | DateTime | NO | utcnow | Timestamp creación |
| `updated_at` | DateTime | NO | utcnow | Timestamp última actualización |

### Relaciones

- **bonus_files** (One-to-Many): `ProductBonusFile` cascade delete
  - Archivos extras (PDFs, archivos interactivos) bundled con kits
  - Soportan marcar como `is_interactive` (HTML)

### Valores actuales de `product_type`

```python
"pdf"                  # Default - soporta PDF, EPUB, o ambos
"html_interactive"     # Producto HTML interactivo con acceso personalizado
"downloadable_zip"     # Producto descargable en formato ZIP
```

---

## 2. MODELO ORDER - RELACIÓN CON ENTREGA

### Estructura relevante de `order`

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `id` | Integer | PK |
| `ebook_type` | String(30) | **Derivado dinámicamente**: "html_interactive" si compra contiene HTML, else "pdf" |
| `access_code` | String(8) | Código 8 caracteres único para acceso a HTML interactivo |
| `personalized_html_blob` | LargeBinary(4GB-1) | HTML personalizado con código de acceso incrustado |
| `download_token` | String(120) | Token seguro para descarga (se genera con `secrets.token_urlsafe(32)`) |

### Relaciones

- **OrderItem** (One-to-Many): guarda referencia a `product_id`, `product_name`, `unit_price_ars`
  - El `product_id` es lo único que persiste; si el producto se borra, la orden sigue existiendo

---

## 3. SISTEMA DE ENTREGA - FLUJO COMPLETO

### Endpoints de descarga

```
GET  /download/<token>                  → Selector PDF/EPUB (solo si product_type="pdf")
                                        → Redirige a /download_zip si product_type="downloadable_zip"
                                        → 404 si product_type="html_interactive"

GET  /download/<token>/<fmt>            → Descarga PDF o EPUB (fmt in {pdf, epub})
                                        → Valida que Order.status in {paid_demo, paid}
                                        → Rate limit: 30/min

GET  /download/<token>/bonus/<bonus_id> → Descarga archivo bonus
                                        → Valida que bonus pertenece a product de la orden
                                        → 404 si is_interactive (se accede vía /leer/<code>)

GET  /download/<token>/instrucciones/<product_id>
                                        → Descarga PDF instrucciones (solo HTML interactivo)
                                        → 404 si product_type != "html_interactive"

GET  /download/<token>/zip              → Descarga ZIP
                                        → Solo si product_type="downloadable_zip"

GET  /leer/<access_code>                → Muestra HTML interactivo personalizado
                                        → Busca Order o BonusFileAccess por access_code
                                        → Renderiza HTML desde personalized_html_blob
                                        → Sin rate limit explícito
```

### Generación de acceso a HTML interactivo

1. En **checkout**: si algún producto es `html_interactive`
   - Se genera `access_code` único (8 caracteres)
   - Se genera `personalized_html` (invoca `generate_personalized_html()` con buyer email + código)
   - Se guarda `personalized_html_blob` en Order
   - Se envía email con link `/leer/<access_code>`

2. En **payment success** (POST `/api/webhook/...`):
   - Se regenera HTML personalizado si no existe
   - Se valida que no sea 404 ni esté corrupto

3. Para archivos **bonus interactivos**:
   - Se crea registro `BonusFileAccess` separado
   - Cada bonus tiene su propio `access_code` y `personalized_html_blob`
   - Permite que múltiples compradores del mismo producto no colisionen

---

## 4. SISTEMA DE CREACIÓN DE PRODUCTOS - PANEL ADMIN

### Formulario de creación (`/admin/products/create`)

**Flujo UI:**

1. **Selector de `product_type`:**
   ```html
   <select name="product_type" id="productType" required>
     <option value="pdf">PDF/EPUB</option>
     <option value="html_interactive">HTML Interactivo</option>
     <option value="downloadable_zip">Descargable ZIP</option>
   </select>
   ```

2. **Campos dinámicos basados en `product_type`:**

   - **Si `pdf` (default):**
     - ✅ Input `ebook_file_pdf` (accept=".pdf")
     - ✅ Input `ebook_file_epub` (accept=".epub")
     - ✅ Al menos uno requerido
     - ❌ No JSON, no ZIP, no HTML

   - **Si `html_interactive`:**
     - ✅ Input `ebook_file` (accept=".html") REQUERIDO
     - ✅ Input `instructions_pdf` (accept=".pdf") OPCIONAL
     - ❌ No PDF/EPUB directos

   - **Si `downloadable_zip`:**
     - ✅ Input `zip_file` (accept=".zip") REQUERIDO
     - ✅ Límite 512 MB
     - ❌ No PDF/EPUB/HTML

3. **Campos comunes a todos:**
   - name, slug, category, price_ars
   - cover_class, featured, cover_image
   - description

### Edición de producto (`POST /admin/products/<id>/edit`)

**Comportamiento actual:**
- No se puede cambiar `product_type` (no hay campo en formulario)
- Solo permite actualizar archivos compatibles con tipo actual
- Valida: si intentan subir ZIP a producto "pdf", rechaza con error
- Valida: si intentan subir instrucciones a producto no-HTML, rechaza

### Creación de KIT (`POST /admin/products/<id>/create-kit`)

**Crea un nuevo producto:**
- Hereda `product_type`, `ebook_file`, `ebook_file_epub`, etc. del producto base
- Establece `is_kit=True`
- Añade archivos bonus (vía `ProductBonusFile`)
- Genera slug `kit-<slug-original>`
- Precio 15% más alto por defecto (configurable)

---

## 5. CATÁLOGOS Y FILTRADO POR MARCA

### Estado actual

**Blueprints definidos pero NO funcionales:**
- `ebooks_bp` → `/ebooks/` → renderiza `templates/ebooks/catalog.html`
- `yoyir_bp` → `/yoyir/` → renderiza `templates/yoyir/catalog.html`
- `estrategia_bp` → `/estrategia/` → renderiza `templates/estrategia/catalog.html`

**Templates vacíos:**
```html
<!-- backend/templates/ebooks/catalog.html -->
{% extends "base.html" %}
{% block content %}
<div class="catalog-container">
    <h1>Catálogo - Ebooks para la vida</h1>
    <div class="products-grid">
        <!-- Los productos se cargarán aquí en Fase 5 -->
        <p class="placeholder">Catálogo de Ebooks - Estructura lista</p>
    </div>
</div>
{% endblock %}
```

**Realidad:**
- No hay queries de filtrado por marca
- Todos los blueprints renderean el mismo catálogo (vacío/placeholder)
- `brand` se inyecta en sesión pero NO se usa para filtrar productos
- Sistema de multi-marca es ESTRUCTURA, no FUNCIONALIDAD aún

---

## 6. COMPATIBILIDAD CON PRODUCTOS EXISTENTES

### Productos en producción actuales

Basados en `REAL_PRODUCTS`:
```python
{
    "slug": "primero-tu-mente-despues-tu-hogar",
    "name": "Primero tu mente, después tu hogar",
    "description": "...",
    "category": "VIDA & BIENESTAR",
    "price_ars": 6999,
    "file_name": "primero-tu-mente-despues-tu-hogar.pdf",
    # product_type NO especificado → DEFAULT "pdf"
    # NO tienen brand/universe
    # NO tienen delivery_type explícito
}
```

### Estrategia de compatibilidad para nuevos campos

**Campo `brand` (PROPUESTO):**
- Type: `String(30)` nullable
- Default: NULL
- Migración: SET default NULL para productos existentes
- Compatibilidad: Búsquedas de productos pueden usar `COALESCE(brand, 'legacy')` o filtrar por IS NULL

**Campo `product_type` (YA EXISTE):**
- Ya tiene default "pdf"
- Productos existentes quedan con "pdf" automáticamente
- ✅ NO rompe nada

**Campo `delivery_type` (PROPUESTO ALTERNATIVO A product_type redefinido):**
- Podría ser redundante con product_type
- ⚠️ RIESGO: Dos fuentes de verdad sobre cómo entregar

---

## 7. PROBLEMAS ENCONTRADOS

### 1. **product_type como multi-propósito**
- Combina "¿qué tipo de producto es?" + "¿cómo se entrega?"
- Ejemplo: "pdf" = {puede ser PDF solo, EPUB solo, o ambos}
- Dificulta queries de "dame todos los ZIPs"
- Dificulta future-proofing (ej: "subscription" no encaja bien)

### 2. **Falta de brand/universe en modelo**
- Blueprints existen pero no filtran realmente
- Catálogos están vacíos
- Session `current_brand` se inyecta pero no se usa

### 3. **Sin diferenciación entre product_type y delivery_type**
- HTML interactivo es "product_type" + "delivery_type"
- ZIP descargable es "product_type" + "delivery_type"
- Conceptualmente son niveles diferentes

### 4. **Riesgo en edición de productos**
- No se puede cambiar `product_type` post-creación
- No hay validación que previna "producto sin archivos"
- Si eliminas PDF/EPUB de un producto "pdf", queda inconsistente

### 5. **Campos gigantes en BD**
- `ebook_file_epub` = `LargeBinary(4GB-1)`
- `instructions_pdf` = `LargeBinary(4GB-1)`
- `zip_file` = `LargeBinary(4GB-1)`
- `personalized_html_blob` = `LargeBinary(4GB-1)`
- Almacenar binarios en BD es anti-patrón (mejor: S3 + metadata)
- Pero está funcional y es estado actual

### 6. **Generación de HTML personalizado crítica**
- `generate_personalized_html()` se invoca 3+ veces en checkout
- Si falla, orden no completa
- Si blob queda corrupto, cliente no puede leer
- Sin versionado de HTML templates

---

## 8. CAMPOS REUTILIZABLES

### Ya existen y pueden extenderse:

1. **`product_type`** ✅
   - Reutilizar para distinguir ebook/downloadable/micro_app
   - Considerar renombrar valores a algo más explícito

2. **`category`** ✅
   - Puede distinguir "Vida & Bienestar" (ebooks) vs "Planners" (yoyir) vs "Tools" (estrategia)
   - Pero es insuficiente para filtrado real (sugerencia: usar `brand` + `category`)

3. **`is_kit`** ✅
   - Ya soporta bundled products
   - Puede extenderse a "kit" + "subscription_bundle" si es necesario

4. **`access_code` en Order** ✅
   - Funciona para HTML interactivo
   - Podría extenderse a "micro_app_key" o "subscription_token"

5. **`bonus_files` relationship** ✅
   - Ya soporta múltiples archivos por producto
   - Marcar como `is_interactive` funciona

---

## 9. CAMPOS NUEVOS PROPUESTOS

### A. CAMPO `brand` (CRÍTICO)

**Definición:**
```python
brand = db.Column(db.String(30), nullable=True, default=None)
```

**Valores enumerados:**
- `"ebooks"` → Ebooks para la vida
- `"yoyir"` → YOYI'R (agendas/planners)
- `"estrategia"` → EstrategIA (micro-apps)
- `None` → Producto legacy sin marca (backward compatible)

**Índice:** SÍ (para queries de filtrado)

**Default para productos existentes:** NULL (no retroactivo, decidir en migración)

**Propósito:** Permitir filtrado real `/ebooks/` solo muestre brand="ebooks"

---

### B. CAMPO `delivery_type` (OPCIONAL - CONSIDERAR)

**Alternativa 1: Mantener `product_type` pero redefinirlo**
```
"pdf"              → Ebook entregable como PDF/EPUB
"html"             → Ebook HTML interactivo (acceso web)
"zip"              → Descargable ZIP
"micro_app"        → Micro-app HTML con lógica (futuro)
"subscription"     → Producto con acceso recurrente (futuro)
```

**Alternativa 2: Crear nuevo campo `delivery_type` separado**
```
delivery_type = db.Column(db.String(30), nullable=False, default="file_download")
```

Valores:
- `"file_download"` → Descarga archivo (PDF/EPUB/ZIP)
- `"html_access"` → Acceso web HTML personalizado
- `"app_access"` → Acceso a aplicación/herramienta
- `"subscription"` → Acceso recurrente (futuro)

**RECOMENDACIÓN:** Alternativa 1 (mantener `product_type` pero renombrar valores) es más simple. Alternativa 2 añade complejidad sin beneficio actual.

---

### C. CAMPO `access_type` (FUTURO - NO IMPLEMENTAR TODAVÍA)

```python
access_type = db.Column(db.String(30), nullable=True, default=None)
```

Valores futuros:
- `"lifetime"` → Acceso permanente (actual)
- `"monthly"` → Acceso suscripción mensual
- `"yearly"` → Acceso suscripción anual
- `"subscription"` → Acceso recurrente genérico

**PROPÓSITO:** Preparar arquitectura para suscripciones sin implementar todavía.

**DEFAULT para existentes:** NULL (sin suscripción)

---

## 10. PROPUESTA DE ARQUITECTURA MÍNIMA - FASE 4

### 10.1 Cambios al modelo `Product`

**A HACER (Incremental):**

1. **Añadir `brand` campo** (Nullable, para backward compatibility)
   ```python
   brand = db.Column(db.String(30), nullable=True, default=None)
   db.Index('idx_product_brand', 'brand')  # Índice para queries
   ```

2. **Redefinir valores de `product_type`** (sin cambiar estructura)
   - "pdf" → ebook PDF/EPUB (sin cambios)
   - "html" → renombrar "html_interactive" a "html" (BREAKING CHANGE - ver abajo)
   - "zip" → renombrar "downloadable_zip" a "zip" (BREAKING CHANGE)
   - Futuro: "app", "subscription"

   ⚠️ **PROBLEMA:** Cambiar valores rompe queries existentes.  
   ✅ **SOLUCIÓN:** Mantener valores como están, agregar enum en app.py para documentación.

3. **NO añadir `delivery_type` aún** (es redundante con `product_type`)

4. **Preparar para `access_type`** (campo nullable, sin lógica)
   ```python
   access_type = db.Column(db.String(30), nullable=True, default=None)
   # Valores futuros: "lifetime", "monthly", "yearly"
   ```

**NO HACER (evitar riesgos):**
- ❌ Renombrar valores de `product_type` (rompe queries existentes)
- ❌ Cambiar `nullable=True` a `nullable=False` para campos binarios
- ❌ Eliminar campos no usados (`source_html_path`)
- ❌ Cambiar tipos de datos de campos existentes
- ❌ Reordenar columnas

---

### 10.2 Cambios al Admin Panel

**PROPUESTA de flujo de creación mejorado:**

```
1. Seleccionar Universo:
   - [ ] Ebooks para la vida
   - [ ] YOYI'R
   - [ ] EstrategIA
   - [ ] Sin universo (legacy)

2. Seleccionar Tipo de Producto:
   (dinámico según universo seleccionado)
   
   SI "Ebooks para la vida":
   - [x] Ebook (PDF/EPUB) ← default
   - [ ] Ebook interactivo (HTML)
   
   SI "YOYI'R":
   - [x] Planner/Agenda (ZIP)
   - [ ] Ebook (PDF/EPUB)
   
   SI "EstrategIA":
   - [x] Herramienta/Micro-app (HTML)
   - [ ] Ebook (PDF/EPUB)
   
3. Seleccionar Tipo de Entrega:
   (dinámico según tipo de producto)
   
   SI "Ebook (PDF/EPUB)":
   - PDF: [ ] sí [ ] no
   - EPUB: [ ] sí [ ] no
   (Al menos uno requerido)
   
   SI "Ebook interactivo (HTML)":
   - HTML: [ ] sí
   - Instrucciones PDF: [ ] sí [ ] no
   
   SI "Planner/ZIP":
   - ZIP: [ ] sí
   
4. Campos comunes
   name, slug, category, price_ars, description, cover_image, featured

5. Crear
```

**Cambios implementación:**
- Actualizar `dashboard.html` para mostrar cascada de selectores
- Backend: validar `brand` + `product_type` combo (tabla de validación)
- Admin: mostrar icono/color según universo

---

### 10.3 Catálogos dinámicos

**NO implementado en Fase 4**, pero preparar estructura:

```python
# backend/blueprints/ebooks.py (CAMBIAR FASE 5)
@ebooks_bp.route('/')
def catalog():
    # FASE 5: filtrar por brand="ebooks"
    products = Product.query.filter_by(brand='ebooks').all()
    return render_template('catalog.html', products=products, brand='ebooks')
```

---

### 10.4 Compatibilidad con productos existentes

**Estrategia:**

1. **Productos sin `brand` (NULL)** siguen siendo vendibles
2. **Catálogos** muestran:
   - `/ebooks/` → brand="ebooks" + brand=NULL (legacy)
   - `/yoyir/` → brand="yoyir"
   - `/estrategia/` → brand="estrategia"
3. **Búsquedas internas** usan `COALESCE(brand, 'legacy')` para reportes
4. **Panel admin** permite editar `brand` post-creación

---

### 10.5 Preparación para suscripciones (sin implementar)

1. **Añadir `access_type` nullable**
2. **Actualizar Order model** (si es necesario):
   - Agregar `subscription_ends_at` (DateTime, nullable)
   - NO hacer cambios en checkout todavía
3. **Documentar (en código) cómo funcionaría:**
   ```python
   # Futuro - NO implementar en Fase 4
   # Si access_type="monthly":
   #   - Order.subscription_ends_at = now + 30 días
   #   - Enviar email reminder 5 días antes de expirar
   #   - Bloquear acceso post-expiración
   ```

---

## 11. MAPA COMPLETO: PRODUCT → COMPRA → ENTREGA

```
┌─────────────────────────────────────────┐
│          CREAR PRODUCTO                 │
│  Admin selecciona:                      │
│  - brand (ebooks/yoyir/estrategia/NULL) │
│  - product_type (pdf/html/zip/...)      │
│  - Sube archivos según tipo             │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│     PRODUCTO EN CATÁLOGO                │
│  /ebooks/?filter=brand                  │
│  /yoyir/?filter=brand                   │
│  /estrategia/?filter=brand              │
│  (Fase 5: implementar filtrado)         │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│        AGREGAR A CARRITO                │
│  session['cart'] = [product_id1, ...]   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│          CHECKOUT                       │
│  1. Obtener productos del carrito       │
│  2. Calcular total                      │
│  3. Crear Order + OrderItems            │
│  4. Deriv. ebook_type de products       │
│  5. Si HTML interactivo: generar        │
│     access_code + personalized_html     │
│  6. Crear preferencia de pago (MP/PP)   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         PAYMENT GATEWAY                 │
│  MercadoPago / PayPal                   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│       WEBHOOK / CALLBACK                │
│  Status → "paid" o "paid_demo"          │
│  Si HTML: regenerar + validar HTML      │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│      PÁGINA DE ÉXITO                    │
│  /success/<order_id>                    │
│  Mostrar links de descarga              │
│  Enviar email con download_token        │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────┐
│           ENTREGA (según product_type)              │
│                                                     │
│  PDF/EPUB:                                          │
│  GET /download/<token> → selector PDF/EPUB         │
│  GET /download/<token>/pdf|epub → descarga         │
│  Rate limit: 30/min                                │
│                                                     │
│  ZIP:                                              │
│  GET /download/<token>/zip → descarga ZIP          │
│  Rate limit: 30/min                                │
│                                                     │
│  HTML INTERACTIVO:                                 │
│  GET /leer/<access_code> → renderiza HTML          │
│  HTML personalizado con access_code incrustado    │
│  Acceso sin limit (pero geolocked por IP token)    │
│                                                     │
│  BONUS (cualquier tipo):                           │
│  GET /download/<token>/bonus/<id> → descarga       │
│                                                     │
│  INSTRUCCIONES (HTML only):                        │
│  GET /download/<token>/instrucciones/<id> → PDF   │
└─────────────────────────────────────────────────────┘
```

---

## 12. RIESGOS Y CONSIDERACIONES

### 🔴 RIESGOS ALTOS

1. **Cambiar valores de `product_type`**
   - Causa: Queries hardcodeadas en app.py buscan "html_interactive", "downloadable_zip"
   - Impacto: Productos no se entregan correctamente
   - Mitigación: Crear tabla enum de valores, usar constantes Python

2. **Añadir `brand` nullable pero sin valores por defecto**
   - Causa: Queries que asumen brand no-null fallan
   - Impacto: Catálogos rompen
   - Mitigación: Documentar que brand=NULL = legacy, usar COALESCE en queries

3. **No validar brand + product_type combo**
   - Causa: Admin permite crear producto con brand="estrategia" + product_type="zip"
   - Impacto: Incoherencia de datos
   - Mitigación: Tabla de validación en backend, UI cascada de selectores

### 🟡 RIESGOS MEDIOS

4. **Afectar orden existentes si cambias modelo de entrega**
   - Causa: OrderItem solo guarda product_id, no copia de product_type
   - Impacto: Si borro producto, orden queda orfana (pero funciona, solo falta saber tipo)
   - Mitigación: Copiar product_type a OrderItem (nuevo campo)

5. **Personalized HTML corrupto bloquea acceso**
   - Causa: Si `generate_personalized_html()` falla, blob queda NULL o vacío
   - Impacto: Cliente no puede leer su compra
   - Mitigación: Validar HTML antes de guardar, tener fallback

6. **Cambiar category values rompe filtros**
   - Causa: CATEGORIES = ["VIDA & BIENESTAR", ...] está hardcodeada
   - Impacto: Productos con categoría old no aparecen en filtros
   - Mitigación: Mantener migration de categorías viejas → nuevas (como existe hoy)

### 🟢 RIESGOS BAJOS

7. **Agregar campos nullable no rompe nada**
   - Impacto: Bajo (backward compatible)
   - Ejemplo: `brand=NULL` → queries usan COALESCE

8. **Agregar índices ralentiza inserts levemente**
   - Impacto: Bajo (índices en columnas strings son pequeños)
   - Mitigación: No crear índice si no se usa frecuentemente

---

## 13. PLAN INCREMENTAL RECOMENDADO

### FASE 4A: Preparación (semana 1)
- ✅ Crear este audit (HECHO)
- [ ] Crear tabla de validación brand × product_type (constantes Python)
- [ ] Documentar valores de product_type en código
- [ ] Backup de producción

### FASE 4B: Modelo (semana 2)
- [ ] Migración: ADD COLUMN `brand` VARCHAR(30) NULL
- [ ] Migración: ADD INDEX idx_product_brand
- [ ] Migración: ADD COLUMN `access_type` VARCHAR(30) NULL (preparación para future)
- [ ] Tests: verificar productos existentes NO rompen

### FASE 4C: Admin UI (semana 3)
- [ ] Actualizar formulario de creación con cascada: Universo → Tipo → Entrega
- [ ] Actualizar formulario de edición para mostrar `brand` (no editable para legacy)
- [ ] Validar combo brand × product_type
- [ ] Tests: crear producto en cada combo válido

### FASE 4D: Catálogos (semana 4 - FASE 5)
- [ ] Implementar query filtrado por `brand` en blueprints
- [ ] Renderizar templates ebooks/yoyir/estrategia con productos filtrados
- [ ] Tests: `/ebooks/` solo muestra brand="ebooks"

### FASE 5: Integración completa
- [ ] Crear tabla de análisis: venta por universo/tipo
- [ ] Dashboard admin: métricas por universo
- [ ] Preparar para suscripciones (sin implementar lógica aún)

---

## 14. VALORES/ENUMS PROPUESTOS

### Enum BRAND
```python
class ProductBrand(str, Enum):
    EBOOKS = "ebooks"
    YOYIR = "yoyir"
    ESTRATEGIA = "estrategia"
    # Valores NULL representan productos legacy
```

### Enum PRODUCT_TYPE
```python
class ProductType(str, Enum):
    PDF = "pdf"                          # PDF/EPUB ebook
    HTML = "html_interactive"            # Mantener valor actual
    ZIP = "downloadable_zip"             # Mantener valor actual
    # Futuros: APP = "app", SUBSCRIPTION = "subscription"
```

### Enum ACCESS_TYPE (futuro - no usar todavía)
```python
class AccessType(str, Enum):
    LIFETIME = "lifetime"                # Acceso permanente
    MONTHLY = "monthly"                  # Suscripción mensual
    YEARLY = "yearly"                    # Suscripción anual
```

### Tabla de validación BRAND × PRODUCT_TYPE

| Brand | Product Type | Permitido | Razón |
|-------|--------------|-----------|-------|
| ebooks | pdf | ✅ | Ebooks tradicionales |
| ebooks | html | ✅ | Ebooks interactivos |
| ebooks | zip | ⚠️ | Podría ser recurso descargable |
| yoyir | pdf | ✅ | Planners en PDF |
| yoyir | html | ✅ | Planners interactivos |
| yoyir | zip | ✅ | Archivos ZIP descargables |
| estrategia | pdf | ⚠️ | Menos común |
| estrategia | html | ✅ | Micro-apps HTML |
| estrategia | zip | ✅ | Herramientas descargables |
| NULL | * | ✅ | Productos legacy sin marca |

**Nota:** ⚠️ significa permitido pero no recomendado (validar en admin UI)

---

## 15. RESUMEN EJECUTIVO

### Lo que funciona hoy
- ✅ Sistema de 3 tipos de producto (PDF/EPUB, HTML interactivo, ZIP)
- ✅ Panel admin para crear/editar con validaciones
- ✅ Entrega diferenciada por tipo (descarga vs acceso web)
- ✅ KITs con archivos bonus
- ✅ Órdenes y pagos
- ✅ Acceso a HTML personalizado con código único

### Lo que falta para multi-marca
- ❌ Campo `brand` en modelo Product
- ❌ Filtrado real de productos por marca en catálogos
- ❌ Admin UI para seleccionar marca al crear
- ❌ Queries de analytics por universo

### Riesgos de implementación
- ⚠️ Cambiar valores de product_type rompe queries
- ⚠️ Agregar brand=NULL sin validar combo
- ⚠️ Catálogos siguen mostrando todos los productos (sin filtrado)

### Recomendación
Implementar **FASE 4A + 4B + 4C en orden**, con tests en cada paso. FASE 4D (catálogos) es la Fase 5 en el plan original.

---

**Auditoría completada sin modificación de código.**  
**Listo para revisión arquitectónica antes de autorizar implementación.**
