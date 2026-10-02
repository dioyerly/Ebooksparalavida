# Ebooksparalavida — Rama de Desarrollo Multi-Marca

🚀 **Rama:** `feature/multi-brand-evolution`

Esta rama contiene la arquitectura y documentación para la **evolución multi-marca** de la plataforma Ebooksparalavida.

---

## ⚠️ IMPORTANTE

✋ **Esta rama NO modifica producción** (`main`)

- ✅ Diseño arquitectónico
- ✅ Documentación conceptual
- ✅ Testing en `localhost:5000`
- ❌ NO se publica a Fly.io hasta que esté completamente lista

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

## 🚀 Cómo Empezar

### 1. Traer la rama de desarrollo

```bash
git checkout feature/multi-brand-evolution
git pull origin feature/multi-brand-evolution
```

### 2. Instalar dependencias (si cambiaron)

```bash
pip install -r requirements.txt
```

### 3. Levantar el servidor

```bash
flask run
# Abre http://localhost:5000/
```

### 4. Leer la documentación

**Comienza aquí:**
1. [`docs/PROJECT-MASTER.md`](./docs/PROJECT-MASTER.md) — Visión global
2. [`docs/architecture/blueprint-structure.md`](./docs/architecture/blueprint-structure.md) — Cómo organizar código
3. [`docs/design/color-palettes.md`](./docs/design/color-palettes.md) — Paletas de color
4. [`docs/design/home-narrative.md`](./docs/design/home-narrative.md) — Cómo se ve el home

---

## 📋 Fases de Desarrollo

### ✅ Fase 1: Arquitectura (ACTUAL)
- [x] Documentación conceptual
- [x] Estructura de carpetas
- [ ] Primer commit

### 🔄 Fase 2-8: Implementación
Ver roadmap en [`PROJECT-MASTER.md`](./docs/PROJECT-MASTER.md)

---

## 🎨 Las Tres Marcas

| Marca | URL Base | Colores | Productos |
|-------|----------|---------|-----------|
| **Ebooks para la vida** | `/ebooks` | Beige, Teal, Coral | PDF/EPUB |
| **YOYI'R** | `/yoyir` | Lavanda, Morado | ZIP (Agendas) |
| **EstrategIA** | `/estrategia` | Oscuro, Neón, Magenta | HTML Interactivas |

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

## 🚫 Prohibiciones

❌ **NO HAGAS:**

1. NO merges a `main` sin autorización explícita
2. NO cambios en `app.py` principal sin documentar
3. NO modificar `config.py` sin revisar impacto
4. NO alterar base de datos en producción
5. NO tocar blueprints ya en producción

✅ **EN SU LUGAR:**

- Trabaja siempre en `feature/multi-brand-evolution`
- Documenta cambios en comments de código
- Prueba en `localhost` antes de comprometer
- Haz commits descriptivos
- Avisa si necesitas cambios en la BD

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
