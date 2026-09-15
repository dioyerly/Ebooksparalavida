# 🔍 AUDITORÍA TÉCNICA COMPLETA
## Ebooksparalavida - Aplicación Flask

**Fecha:** 14 Septiembre 2026 | **Total de Problemas:** 49 (13 Críticos, 21 Altos, 15 Medios)

---

## 📊 RESUMEN POR CATEGORÍA

| Categoría | Críticos | Altos | Medios | Total |
|-----------|----------|-------|--------|-------|
| Esquema de BD | 3 | 0 | 0 | 3 |
| Features KIT | 1 | 4 | 0 | 5 |
| Endpoints API | 4 | 0 | 0 | 4 |
| Almacenamiento Archivos | 0 | 3 | 0 | 3 |
| Configuración | 2 | 0 | 2 | 4 |
| Migraciones | 3 | 0 | 0 | 3 |
| JavaScript | 0 | 3 | 0 | 3 |
| Manejo de Errores | 0 | 5 | 0 | 5 |
| Validaciones | 0 | 4 | 0 | 4 |
| Templates | 0 | 0 | 3 | 3 |
| Seguridad | 0 | 1 | 2 | 3 |
| Consistencia BD | 0 | 0 | 3 | 3 |
| Pagos | 0 | 1 | 1 | 2 |
| Analytics | 0 | 0 | 2 | 2 |
| Features Faltantes | 0 | 0 | 2 | 2 |
| **TOTAL** | **13** | **21** | **15** | **49** |

---

## 🚨 PROBLEMAS CRÍTICOS QUE BLOQUEAN (13)

### 1. Migración de Columnas Usa Sintaxis MySQL en SQLite ⚠️
- **Archivo:** `backend/app.py:217-258`
- **Problema:** Usa `INFORMATION_SCHEMA.COLUMNS` y `DATABASE()` (MySQL only), pero app usa SQLite localmente
- **Resultado:** ❌ Migración FALLA. Las columnas NO se crean en desarrollo
- **Solución:** Usar API de Flask-SQLAlchemy que funciona con cualquier BD

### 2. Acceso a Array Sin Validación en Descarga 💥
- **Archivo:** `backend/app.py:494-495`
- **Código:** `order.items[0]` sin verificar si la lista está vacía
- **Resultado:** ❌ IndexError si orden no tiene items
- **Solución:** Validar `if not order.items: abort(400)`

### 3. Comparación Inconsistente de is_kit ❌
- **Archivo:** `backend/app.py:634` vs `677`
- **Problema:** 
  - Línea 634: `== "True"` (INCORRECTO - nunca cumple)
  - Línea 677: `== "on"` (CORRECTO - lo que envía checkbox HTML)
- **Resultado:** ❌ **KIT NUNCA se guarda** porque comparación siempre es False
- **ESTO EXPLICA POR QUÉ NO FUNCIONA EL KIT**

### 4. Credenciales Admin Débiles y Expuestas
- **Archivo:** `backend/config.py:23-24`
- **Problema:** `ADMIN_PASSWORD = "admin123"` por defecto en código
- **Resultado:** ❌ Cualquiera puede hacer login como admin
- **Solución:** Lanzar excepción si no está configurada en env vars

### 5. Secreto y Tokens en .env (Versionado)
- **Archivo:** `.env`
- **Problema:** Contiene `SECRET_KEY`, `MP_ACCESS_TOKEN`, `PAYPAL_CLIENT_SECRET` reales
- **Resultado:** ❌ Credenciales públicas en GitHub
- **Solución:** Nunca commitear .env. Usar .env.example + .gitignore

### 6. Falta Llave Foránea en OrderItem
- **Archivo:** `backend/models.py:50`
- **Problema:** `product_id` sin FK constraint
- **Resultado:** ❌ Se puede crear OrderItem con producto_id inexistente
- **Solución:** Agregar `db.ForeignKey("product.id")`

### 7. Schema.sql Desactualizado
- **Archivo:** `/database/schema.sql`
- **Problema:** Falta columnas: `ebook_file`, `is_kit`, `kit_bonus_ids`, `kit_price_ars`, `kit_description`
- **Resultado:** ❌ Si se usa schema.sql para crear BD, falta todo el sistema KIT
- **Solución:** Actualizar schema.sql o usar SQLAlchemy para crear tablas

### 8. ALTER TABLE Sin IF NOT EXISTS
- **Archivo:** `backend/app.py:239-242`
- **Problema:** Ejecuta `ALTER TABLE ADD COLUMN` sin verificar existencia
- **Resultado:** ❌ Si se ejecuta dos veces → "column already exists error"
- **Solución:** Agregar `IF NOT EXISTS` o verificar primero

### 9. Tipos de Datos Inconsistentes (SQLite vs MySQL)
- **Archivo:** `backend/app.py:233`
- **Problema:** Define `BOOLEAN` pero SQLite usa `INTEGER` (0/1)
- **Resultado:** ❌ Inconsistencia esquema local vs producción
- **Solución:** Detectar tipo de BD y usar sintaxis correcta

### 10. No Valida Conexión a BD al Iniciar
- **Archivo:** `backend/config.py:13-15`
- **Problema:** No verifica que DATABASE_URL sea válido
- **Resultado:** ❌ Errores solo aparecen en runtime, no en startup
- **Solución:** Agregar test de conexión en `app.before_first_request`

### 11. No Maneja Archivos Inexistentes
- **Archivo:** `backend/app.py:445-451, 487-492`
- **Problema:** Asume que archivos existen sin verificar
- **Resultado:** ❌ Crash 500 si archivo falta, no fallback
- **Solución:** Verificar existencia con `Path.exists()` antes de usar

### 12. Falta Validación en int() Conversions
- **Archivo:** `backend/app.py:675, 758, 655`
- **Problema:** `int(request.form.get(...))` sin try-except
- **Resultado:** ❌ ValueError si valor no es numérico
- **Solución:** Wrap en try-except o validar formato primero

### 13. Vulnerability: Timing Attack en Login
- **Archivo:** `backend/app.py:584`
- **Problema:** Usa `==` para comparar password (vulnerable a timing attacks)
- **Resultado:** ❌ Attacker puede adivinar password midiendo tiempos
- **Solución:** Usar `secrets.compare_digest()`

---

## ⚠️ PROBLEMAS ALTOS (21)

### KIT System Issues (4)

**2.1 Kit Description Falta en Kit Dictionary**
- `backend/app.py:324-339`: Kit object no incluye `kit_description`
- `backend/templates/product.html:58`: Hardcoded description, no dinámico

**2.2 Kit Bonus Files No Linked Correctamente**
- `backend/app.py:635-651`: Guarda archivos a disk pero no vincula con productos

**2.3 kit_bonus_ids Nunca Poblado**
- `backend/app.py:705-706`: Cuando se crea KIT vía admin, kit_bonus_ids no se guarda

**2.4 No Valida que Kit Bonus IDs Existan**
- Puede referenciar productos inexistentes como bonuses

### API Endpoints (0 additional critical issues identified at High level)

### File Storage Issues (3)

**4.1 No Valida Permisos de Escritura en Storage**
- `backend/app.py:620-727`: Crea directorios pero no verifica permisos

**4.2 Personalized HTML Puede No Existir**
- `backend/app.py:487-492`: No fallback si archivo falta

**4.3 No Valida Tipo de Archivo en Uploads**
- Solo verifica extensión, no MIME type ni contenido
- Riesgo: Archivos maliciosos con extensión `.pdf` falsa

### Error Handling (5)

**8.1 generate_personalized_html() Sin Error Handling**
- `backend/services.py:19-124`: No try-catch en file operations

**8.2 Regex Sin Validación**
- `backend/services.py:30-41`: Si HTML cambio de formato, regex falla

**8.3 SMTP Errors Sin Catch**
- `backend/services.py:365-368`: No try-except en conexión SMTP
- Resultado: Email failures causan crash

**8.4 Producto Puede Tener Nombre/Descripción Vacío**
- `backend/app.py:673-674`: Solo hace `.strip()` sin validar vacío

**8.5 Conversión int() Sin Try-Except**
- `backend/app.py:675, 758, 655`: ValueError no controlado

### Validation Issues (4)

**9.1 Email Validation Muy Permisiva**
- `backend/app.py:385`: Solo verifica si contiene `@`, acepta "test@"

**9.2 Slug No Validado por Uniqueness**
- `backend/app.py:702, 754`: No verifica si slug ya existe

**9.3 Category No Validada**
- Usuario puede submitir cualquier categoría, no debe estar en lista predefinida

**9.4 Kit Bonus IDs No Validados**
- Puede referenciar productos inexistentes

### Otros Altos (5 additional)

**7.1 Broken Delete Button en Bonus Files**
- `dashboard.html:567`: `arguments[0]` undefined en onclick handler

**7.2 Kit Bonus Select No Valida**
- Format mismatch entre kit_bonus_ids y option values

**7.3 Missing Validation para Kit Setup**
- No considera archivos existentes en validación

**13.1 Exchange Rate Rounding Issues**
- Pequeñas discrepancias ARS ↔ USD

**13.2 No Valida Exchange Rates**
- Aceptaría 0 o negativo (división por cero)

---

## 🔧 PROBLEMAS MEDIANOS (15)

### Templates (3)
- Price formatting puede fallar si precio es None
- Product descriptions no escapadas (XSS risk aunque Jinja2 escapa por default)

### Security (2)
- Session data no validada (posible integer overflow)
- Download token no tiene rate limiting

### Database Consistency (3)
- Cascade delete no limpia archivos
- Product deletion deja archivos huérfanos
- Unique constraint en download_token pero no retry

### Payment (1)
- Demo mode conversion pierde precisión

### Analytics (2)
- Click tracking poco preciso
- Sin deduplicación por sesión

### Missing Features (2)
- **NO HAY WEBHOOK HANDLER para Mercado Pago**
- NO HAY ORDER CONFIRMATION verificación de payment status

---

## 🚀 TOP 10 FIXES PRIORITARIOS

**DEBE HACER PRIMERO (Bloquea todo):**

1. ✅ **FIX: Inconsistencia is_kit en línea 634**
   ```python
   # CAMBIAR:
   product.is_kit = request.form.get("is_kit") == "True"
   # A:
   product.is_kit = request.form.get("is_kit") == "on"
   ```
   **⏱️ 1 minuto - ESTO ARREGLA EL KIT**

2. ✅ **FIX: Migración de Columnas para SQLite**
   - Usar `from flask_sqlalchemy import inspect` en lugar de INFORMATION_SCHEMA
   - **⏱️ 15 minutos**

3. ✅ **FIX: Null Check en order.items[0]**
   ```python
   if not order.items:
       abort(400, "Orden sin items")
   ```
   - **⏱️ 2 minutos**

4. ✅ **FIX: Kit Description en Template**
   - `backend/templates/product.html:58` usar `{{ kit.description }}`
   - `backend/app.py:324` agregar `"description": product.kit_description` a dict
   - **⏱️ 3 minutos**

5. ✅ **FIX: Schema.sql Actualizado**
   - Agregar todas las columnas del modelo
   - **⏱️ 5 minutos**

6. ✅ **FIX: Credenciales Admin**
   - Quitar defaults, lanzar excepción si no están en env
   - **⏱️ 3 minutos**

7. ✅ **FIX: .env en .gitignore**
   - Crear .env.example
   - **⏱️ 2 minutos**

8. ✅ **FIX: Try-Except en int() Conversions**
   - `backend/app.py:675, 758, 655`
   - **⏱️ 10 minutos**

9. ✅ **FIX: File Existence Checks**
   - `backend/app.py:445-451, 487-492`
   - **⏱️ 10 minutos**

10. ✅ **FIX: Llave Foránea OrderItem**
    - `backend/models.py:50`
    - **⏱️ 2 minutos**

---

## 📋 CHECKLIST POR FECHA

### HOY (Antes de Mañana)
- [ ] FIX #1: is_kit comparison (1 min) → ARREGLA KIT
- [ ] FIX #3: order.items null check (2 min)
- [ ] FIX #4: Kit description en template (3 min)
- [ ] FIX #6: Admin credentials (3 min)
- [ ] FIX #7: .env to .gitignore (2 min)
- [ ] Test completo del flujo KIT

**Total: ~15 minutos**

### MAÑANA (Antes de Producción)
- [ ] FIX #2: Migración SQLite (15 min)
- [ ] FIX #5: Schema.sql (5 min)
- [ ] FIX #8: int() validations (10 min)
- [ ] FIX #9: File existence checks (10 min)
- [ ] FIX #10: FK constraint (2 min)
- [ ] Mercado Pago webhook handler (30 min)
- [ ] SMTP error handling (10 min)

**Total: ~1.5 horas**

---

## 📍 ESTADO DEL SISTEMA KIT

### ❌ POR QUÉ NO FUNCIONA:
1. **is_kit nunca se guarda** → Línea 634 compara con "True" en lugar de "on"
2. **kit_description no se renderiza** → No incluida en template
3. **migrate_product_columns() crashea en SQLite** → INFORMATION_SCHEMA no existe

### ✅ QUÉ ESTÁ BIEN:
- Columnas en BD están creadas (en prod MySQL)
- Formulario admin recibe datos
- Archivo JS intenta guardar
- Template tiene sección KIT

### 🔄 ESTADO ACTUAL:
- **Desarrollo:** Funciona parcialmente en MySQL (Render)
- **Producción:** A prueba en Render con MySQL
- **Local SQLite:** Fallará en migración

---

## 📊 IMPACT BY AREA

```
┌─────────────────┬──────────┬───────┬────────┐
│ Area            │ Critical │ High  │ Medium │
├─────────────────┼──────────┼───────┼────────┤
│ KIT System      │    1     │   4   │   0    │  ← BLOQUEA FEATURE
│ Database        │    6     │   0   │   3    │  ← INTEGRIDAD DATOS
│ API Endpoints   │    4     │   0   │   0    │  ← CRASHES
│ Security        │    2     │   1   │   2    │  ← RIESGO
│ File Storage    │    0     │   3   │   0    │  ← CONFIABILIDAD
│ Config          │    2     │   0   │   2    │  ← DEPLOYMENT
│ Error Handling  │    0     │   5   │   0    │  ← USER EXPERIENCE
│ Validation      │    0     │   4   │   0    │  ← DATA QUALITY
└─────────────────┴──────────┴───────┴────────┘
```

---

## ✅ RECOMENDACIONES

### Corto Plazo (Esta Semana)
1. Arreglar is_kit comparison → URGENTE
2. Arreglar migración para SQLite
3. Agregar validaciones básicas en endpoints
4. Mover credenciales a env vars

### Mediano Plazo (Este Mes)
1. Implementar webhook Mercado Pago
2. Agregar SMTP error handling
3. Limpiar archivos huérfanos
4. Audit de seguridad completo

### Largo Plazo (Próximos 2-3 Meses)
1. Agregar tests unitarios (no hay tests actuales)
2. Refactorizar services.py (líneas muy largas)
3. Implementar logging estructurado
4. Agregar monitoring en producción

---

## 📌 NOTAS IMPORTANTES

⚠️ **El sistema KIT está casi completo pero bloqueado por 1 bug: la comparación de is_kit en línea 634**

⚠️ **La BD está lista pero la migración crashea en SQLite**

⚠️ **No hay webhook para Mercado Pago - solo funciona demo mode**

⚠️ **Las credenciales están expuestas en .env versionado**

---

*Reportado por: Claude Code AI*
*Fecha: 14 Septiembre 2026*
*Versión: 1.0*
