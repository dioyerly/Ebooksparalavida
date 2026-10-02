# Ebooksparalavida — Rama de Desarrollo: Plataforma Unificada

🚀 **Rama Activa:** `develop/multi-brand-platform`

Esta rama contiene el desarrollo visual y funcional de la **plataforma unificada de tres universos**: EstrategIA (herramientas), YOYI'R (organización) y Ebooks para la vida (contenidos educativos).

---

## ⚠️ IMPORTANTE

✋ **Esta rama NO modifica producción** (`main`)

- ✅ Desarrollo visual en `/universos` (landing unificada)
- ✅ Tres universos completamente implementados y funcionales
- ✅ Testing en `localhost:5000`
- ✅ Página comercial `/` aislada e intacta
- ❌ NO se publica a Fly.io hasta autorización explícita
- ❌ NO se modifica ni se reemplaza `/` hasta que se ordene la integración

---

## 📁 Estructura de Carpetas (Nueva)

```
backend/
├── blueprints/              ← Blueprints por marca (vacíos por ahora)
│   ├── ebooks.py
│   ├── yoyir.py
│   ├── estrategia.py
│   ├── cart.py
│   ├── checkout.py
│   └── admin.py
│
├── templates/
│   ├── ebooks/              ← Templates de Ebooks
│   ├── yoyir/               ← Templates de YOYI'R
│   ├── estrategia/          ← Templates de EstrategIA
│   ├── base.html
│   └── home.html            ← Home narrativa (nueva)
│
└── static/css/
    ├── theme-ebooks.css     ← Paleta Ebooks
    ├── theme-yoyir.css      ← Paleta YOYI'R
    └── theme-estrategia.css ← Paleta EstrategIA

docs/
├── PROJECT-MASTER.md        ← Lee esto primero
├── architecture/
│   ├── blueprint-structure.md
│   ├── routes-map.md
│   └── database-schema-updates.md
└── design/
    ├── color-palettes.md
    └── home-narrative.md
```

---

## 🚀 Cómo Empezar (Continuación)

### 1. Traer la rama de desarrollo

```bash
git checkout develop/multi-brand-platform
git pull origin develop/multi-brand-platform
```

### 2. Instalar dependencias (si cambiaron)

```bash
pip install -r requirements.txt
```

### 3. Levantar el servidor

```bash
flask run
# Abre http://localhost:5000/universos
```

### 4. Verificar la plataforma unificada

- **`/universos`** — Landing unificada con tres universos (NUEVA, IMPLEMENTADA)
  - EstrategIA: herramientas interactivas, microapps
  - YOYI'R: planners, agendas, recursos de organización
  - Ebooks para la vida: ebooks, guías, contenidos educativos
- **`/`** — Página comercial original (intacta, sin cambios)
- **`/ebooks`, `/yoyir`, `/estrategia`** — Catálogos por marca (funcionales)

---

## 📋 Estado del Desarrollo Visual

### ✅ COMPLETADO: `/universos` (Landing Unificada)

#### Hero y Núcleo
- [x] Hero con título "PRODUCTOS DIGITALES QUE HACEN MÁS"
- [x] Núcleo luminoso orbital con productos animados
- [x] Banda móvil "¿QUÉ ESTÁS BUSCANDO?" con destellos
- [x] Header minimalista con navegación (Explorar | EstrategIA | YOYI'R | Ebooks)
- [x] Línea degradada fina (lavanda → rosa → peach) bajo header

#### 01 / ESTRATEGIA — Herramientas Interactivas
- [x] Sección con 4 fases (Microapps | Automatizar | Resolver | Datos)
- [x] Navegación dinámica con tabs funcionales
- [x] Tema frío: violeta/lavanda con gradientes
- [x] Órbitas, destellos y halos luminosos
- [x] Imagen del mockup cargando correctamente
- [x] CTA y contador de fases

#### 02 / YOYI'R — Organización y Planificación
- [x] Sección con 4 fases (Planificar | Organizar | Rutinas | Recursos)
- [x] Navegación dinámica con tabs funcionales
- [x] Tema cálido: rosa empolvado/malva con gradientes
- [x] Órbitas, destellos y halos luminosos
- [x] Imagen del mockup cargando correctamente
- [x] CTA y contador de fases

#### 03 / EBOOKS — Contenidos Educativos
- [x] Sección con 4 fases (Vida y bienestar | Aprender | Dinero | Carrera)
- [x] Navegación dinámica con tabs funcionales
- [x] Tema editorial: crema/peach/coral empolvado con gradientes
- [x] Órbitas, destellos y halos luminosos
- [x] Imagen del mockup cargando correctamente
- [x] CTA y contador de fases

#### Cierre y Footer
- [x] Sección de cierre con tres CTAs discretas (Resolver | Organizar | Aprender)
- [x] Footer minimalista con 4 columnas (Marca | Explorar | Ayuda | Legal)
- [x] Línea fina separadora
- [x] Información en parte inferior (Copyright | Tagline | Claim)

#### Limpieza
- [x] Eliminados bloques visuales antiguos duplicados
- [x] Sin residuos de versión anterior

---

## 🎨 Los Tres Universos

| Universo | URL | Tema Visual | Contenido |
|----------|-----|-------------|----------|
| **EstrategIA** | `/estrategia` | Violeta/Lavanda (frío, tecnológico) | Microapps, herramientas interactivas |
| **YOYI'R** | `/yoyir` | Rosa empolvado/Malva (cálido, creativo) | Planners, agendas, recursos |
| **Ebooks para la vida** | `/ebooks` | Crema/Peach (editorial, tranquilo) | Ebooks, guías, contenidos |

### Paletas de Color

- **EstrategIA:** Fondo #FBF9FF, primario #7655D9, secundario #A88AF0
- **YOYI'R:** Fondo #FFF9FB, primario #C6539A, secundario #E38BBE
- **Ebooks:** Fondo #FFFCF8, primario #C97768, secundario #E7A897

## 📁 Archivos Modificados en Este Commit

```
backend/app.py                          (+11 líneas)
backend/templates/home_unified.html     (+570 líneas)
frontend/assets/css/home-unified.css    (+2568 líneas)
frontend/assets/js/home-unified.js      (+485 líneas)
```

### Cambios Principales

**backend/app.py**
- Rutas para /universos actualizado
- Manejo de menú toggle para mobile

**backend/templates/home_unified.html**
- Nueva sección hero optimizada
- Tres secciones de universos (EstrategIA, YOYI'R, Ebooks)
- Header con navegación unificada
- Línea degradada divisor bajo header
- Sección de cierre con tres CTAs
- Footer minimalista con 4 columnas
- Eliminados bloques visuales duplicados

**frontend/assets/css/home-unified.css**
- CSS para header divider (línea degradada)
- CSS para estrategia-showcase (tema violeta)
- CSS para universe-stage--yoyir (tema rosa)
- CSS para universe-stage--ebooks (tema peach)
- CSS para cierre y footer minimalista
- Responsive media queries para mobile/tablet
- Animaciones de órbitas, destellos, halos

**frontend/assets/js/home-unified.js**
- Navegación de fases EstrategIA (4 tabs dinámicos)
- Navegación de fases YOYI'R (4 tabs dinámicos)
- Navegación de fases Ebooks (4 tabs dinámicos)
- Transiciones suaves entre fases
- Actualización de contadores y barras de progreso

---

## 🛠️ Comandos Útiles

```bash
# Ver ramas locales
git branch

# Ver rama actual
git branch -a

# Cambiar a la rama de desarrollo
git checkout feature/multi-brand-evolution

# Traer últimos cambios
git pull origin feature/multi-brand-evolution

# Crear rama local para tu trabajo
git checkout -b feature/multi-brand-evolution-tu-tarea

# Hacer commit
git commit -m "feat: descripción de lo que cambió"

# Pushear cambios
git push origin feature/multi-brand-evolution-tu-tarea

# Levantar servidor local
flask run

# Ver archivos modificados
git status

# Ver cambios en un archivo
git diff archivo.py
```

---

## 📝 Reglas de Commits

**Formato:**
```
<tipo>: <descripción breve>

<descripción detallada (opcional)>
```

**Tipos:**
- `feat:` → Nueva funcionalidad
- `fix:` → Arreglar bug
- `docs:` → Documentación
- `refactor:` → Reescribir código
- `test:` → Tests

**Ejemplos:**
```bash
git commit -m "feat: agregar blueprint de YOYI'R"
git commit -m "docs: actualizar color palettes"
git commit -m "refactor: reorganizar templates base"
```

---

## 🚫 Reglas Operacionales

❌ **PROHIBIDO:**

1. NO merges a `main` sin autorización explícita
2. NO modificar, eliminar ni reemplazar `/` (página comercial) sin orden
3. NO tocar checkout, pagos, carrito ni transacciones
4. NO modificar base de datos de producción
5. NO incluir `.env`, credenciales ni archivos temporales en commits
6. NO borrar, reemplazar, simplificar ni reconstruir funcionalidades existentes
7. NO hacer despliegues a producción sin autorización

✅ **PERMITIDO:**

- Desarrollo visual en `/universos` (landing unificada)
- Cambios incrementales con revisión previa
- Testing en `localhost:5000`
- Commits descriptivos con `feat:`, `fix:`, `refactor:`, `docs:`
- Usar rama `develop/multi-brand-platform` para todo

## 📝 Metodología de Trabajo

### Desarrollo Visual
1. Cambios locales en `/universos` únicamente
2. Revisar en `http://localhost:5000/universos`
3. Aprobar visualmente antes de commit
4. Documentar cambios en commit message

### Seguridad
- Entorno de desarrollo aislado
- NO modificar producción (`main`)
- NO incluir credenciales en Git
- Usar variables de entorno para secretos

### Continuidad
- Este punto de guardado permite continuar desde otra computadora
- Rama `recovery/multi-brand-20261002` disponible como backup
- Todos los cambios documentados en este README

---

## 🧪 Testing en Localhost

### Verificar que todo funciona

```bash
# 1. Levantar servidor
flask run

# 2. Abrir navegador
# http://localhost:5000/

# 3. Probar navegación
# http://localhost:5000/ebooks
# http://localhost:5000/yoyir
# http://localhost:5000/estrategia

# 4. Abrir DevTools (F12) y verificar:
# - Body tiene clase: class="theme-ebooks", "theme-yoyir", etc.
# - CSS se carga sin errores
# - No hay 404s en Network

# 5. Responsive
# Presiona F12 → Toggle device toolbar (Ctrl+Shift+M)
# Prueba en: iPhone SE, iPad, Desktop
```

---

## 🔗 Links Importantes

- **Documentación:** `docs/`
- **Roadmap:** `docs/PROJECT-MASTER.md`
- **Arquitectura:** `docs/architecture/`
- **Diseño:** `docs/design/`
- **GitHub:** https://github.com/dioyerly/Ebooksparalavida
- **Producción:** https://estrategia.site

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo hacer cambios en `main` mientras trabajo en esta rama?**
R: NO. Trabaja siempre en `feature/multi-brand-evolution`.

**P: ¿Cuándo se publica a producción?**
R: Cuando todas las fases estén completas y testeadas. Se notificará explícitamente.

**P: ¿Qué pasa si rompo algo en la rama?**
R: No hay problema. Es una rama aislada. Solo avisa y hacemos revert si es necesario.

**P: ¿Cómo veo qué cambios hay desde main?**
R: `git diff main feature/multi-brand-evolution`

**P: ¿Necesito crear base de datos nueva?**
R: NO. La BD actual sirve. Solo se agrega 1 columna cuando sea momento.

---

## 📞 Contacto y Dudas

Si tienes dudas:
1. Revisa primero `docs/PROJECT-MASTER.md`
2. Revisa el documento específico de tu tarea
3. Si aún tienes dudas, pregunta en los commits o comentarios

---

## ✅ Checklist para Empezar

- [ ] He leído `PROJECT-MASTER.md`
- [ ] He traído la rama: `git checkout feature/multi-brand-evolution`
- [ ] He levantado el servidor: `flask run`
- [ ] He testeado en `localhost:5000`
- [ ] Entiendo las 3 marcas y sus colores
- [ ] Sé dónde ir a preguntar dudas

---

¡Bienvenido al desarrollo multi-marca de Ebooksparalavida! 🚀

**Rama activa:** `feature/multi-brand-evolution`  
**Estado:** Arquitectura conceptual ✅  
**Próximo paso:** Crear blueprints vacíos y templates base
