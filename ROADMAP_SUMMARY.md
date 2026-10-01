# Roadmap - Plataforma Multi-Marca "Ebooks para la vida"

## 🎯 Visión Estratégica

Evolucionar de una tienda única de ebooks a una plataforma unificada que alberga 3 marcas independientes con identidades visuales propias, manteniendo retrocompatibilidad total y sin romper la tienda actual.

```
Hoy                      Mañana
Ebooks para la vida  →   Ebooks para la vida
                         YOYI'R
                         EstrategIA
                         (Todas en 1 plataforma)
```

---

## ✅ Estado Actual (Oct 1, 2026)

### Infraestructura Git
- ✅ Rama `main` - LIMPIA, lista para producción
- ✅ Rama `feature/multi-brand-evolution` - Creada en GitHub
  - 2 commits con soporte para ZIP y arquitectura
  - Sincronizada y lista para desarrollo paralelo

### Cambios Implementados en Rama de Desarrollo
1. ✅ **Soporte para Productos ZIP Descargables**
   - Modelo: campos `zip_file` (LONGBLOB) y `file_name_zip`
   - Admin: tipo `downloadable_zip` con validación .zip
   - Download: endpoint `/download/<token>/zip` con rate limiting
   - Seguridad: no descomprime, solo descarga autorizada
   - Docs: `ZIP_DOWNLOADABLE_PRODUCTS.md` con guía completa

2. ✅ **Arquitectura Multi-Marca Documentada**
   - Estructura de carpetas con blueprints (modular)
   - Sistema CSS con variables por tema
   - Rutas Flask segregadas por marca
   - Modelo de datos con campo `brand`
   - Timeline de implementación por fases

### Flujo de Trabajo Establecido
- ✅ Sincronización entre 2 computadoras con git pull/push
- ✅ Rama de desarrollo aislada de producción
- ✅ Commits documentados y trazables

---

## 📊 Las 3 Marcas (Futuro)

### 1. Ebooks para la vida (Actual)
```
URL base: /
Paleta: Beige / Teal / Coral
Productos: PDF, EPUB, HTML interactivos, Kits
Público: Personas con TDAH, padres, educadores
```

### 2. YOYI'R (Nuevo)
```
URL base: /yoyir
Paleta: Lavanda / Morado Pastel
Productos: Agendas, Planners, Kits en ZIP
Público: Personas que buscan organización visual
```

### 3. EstrategIA (Futuro)
```
URL base: /estrategia
Paleta: Oscuro / Azul Eléctrico / Magenta Neón
Productos: Micro-apps HTML, Herramientas de datos, Suscripciones
Público: Profesionales, equipos, empresas
```

---

## 🔄 Cronograma de Implementación

### Fase 1: Preparación de Infra (2-3 semanas)
**Estado: PLANIFICADO**
- [ ] Crear estructura de blueprints
- [ ] Implementar sistema CSS modular
- [ ] Configurar estructura de carpetas
- [ ] Tests unitarios

**Rama:** `feature/multi-brand-evolution`
**Riesgo:** BAJO
**Impacto en producción:** NINGUNO

### Fase 2: Migración de Rutas (3-4 semanas)
**Estado: PENDIENTE**
- [ ] Migrar rutas de ebooks a blueprint
- [ ] Crear blueprints de YOYI'R y EstrategIA
- [ ] Tests de integración

### Fase 3: Temas y Estilos (2-3 semanas)
**Estado: PENDIENTE**
- [ ] CSS modular por marca
- [ ] Tema ebooks (refactor)
- [ ] Tema YOYI'R (nuevo)
- [ ] Tema EstrategIA (nuevo)

### Fase 4: Admin Unificado (2-3 semanas)
**Estado: PENDIENTE**
- [ ] Panel con selector de marca
- [ ] Vistas multi-brand
- [ ] Analytics por marca

### Fase 5: Testing y Go-Live (2 semanas)
**Estado: PENDIENTE**
- [ ] Tests E2E en todas las marcas
- [ ] Validación de retrocompatibilidad
- [ ] Merge a release/v1-multi-brand
- [ ] Go-live

**Duración total estimada:** 12-15 semanas

---

## 🔒 Garantías de Seguridad

### Retrocompatibilidad = 100%
```
URLs actuales NO cambian:
GET  / → Ebooks Home (IGUAL)
GET  /shop → Ebooks Shop (IGUAL)
GET  /cart → Carrito (IGUAL)
```

### Datos Actuales NO Se Pierden
```
- Productos existentes = brand='ebooks' automáticamente
- Órdenes = sin cambios
- Clientes = sin cambios
```

### Rama de Desarrollo Aislada
```
main → PRODUCCIÓN (intacta)
feature/multi-brand-evolution → DESARROLLO (cambios seguros)
```

---

## 📁 Estructura Final (Después de todas las fases)

```
ebooks-store/
├── backend/
│   ├── blueprints/
│   │   ├── ebooks/
│   │   ├── yoyir/
│   │   ├── estrategia/
│   │   └── admin/
│   ├── templates/base/
│   ├── app.py (enrutador principal)
│   └── models.py (con campo brand)
│
├── frontend/assets/
│   ├── css/
│   │   ├── variables.css (paletas)
│   │   ├── base.css (compartido)
│   │   └── themes/
│   │       ├── ebooks.css
│   │       ├── yoyir.css
│   │       └── estrategia.css
│   └── js/
│       ├── shared/
│       └── themes/
│
└── DOCUMENTATION/
    ├── ARCHITECTURE_MULTI_BRAND.md
    ├── SETUP_MULTI_BRAND.md
    └── ZIP_DOWNLOADABLE_PRODUCTS.md
```

---

## 🚀 Próximos Pasos Inmediatos

### Para Esta Semana
1. ✅ Revisar documentación de arquitectura
2. ✅ Confirmar estructura de carpetas
3. ✅ Confirmar sistema CSS
4. ⬜ Planificar Fase 1 en detalle

### Para Próxima Sesión (Otra Computadora)
1. `git checkout feature/multi-brand-evolution`
2. `git pull origin`
3. Revisar cambios de ZIP y arquitectura
4. Empezar Fase 1

### NUNCA
- ❌ Hacer push a `main` sin aprobación explícita
- ❌ Borrar rama `feature/multi-brand-evolution`
- ❌ Romper retrocompatibilidad de URLs

---

## 📞 Documentación Clave

| Documento | Propósito |
|-----------|-----------|
| `ARCHITECTURE_MULTI_BRAND.md` | Visión técnica completa |
| `SETUP_MULTI_BRAND.md` | Flujo de trabajo entre máquinas |
| `ZIP_DOWNLOADABLE_PRODUCTS.md` | Guía de productos ZIP |

---

## 💡 Principios Rectores

1. **Incremental:** Un paso a la vez, validación constante
2. **Modular:** Cada marca es independiente pero comparte infraestructura
3. **Retrocompatible:** Nada de lo actual se rompe
4. **Documentado:** Todo está escrito y rastreable en Git
5. **Paralelo:** Dos máquinas pueden trabajar simultáneamente sin conflictos

---

## ✨ Conclusión

El repositorio está estructurado para evolucionar hacia una plataforma multi-marca sin comprometer la tienda actual. Todos los cambios están versionados en GitHub, aislados en una rama de desarrollo, y documentados para que ambas máquinas puedan sincronizarse.

**Estado:** 🟢 LISTO PARA FASE 1

¿Confirmas que entiendes el plan completo?
