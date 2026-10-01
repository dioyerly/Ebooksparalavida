# Setup: Flujo de Desarrollo Multi-Marca

## 🎯 Objetivo Inmediato
Configurar el repositorio Git para que ambas máquinas puedan trabajar en paralelo sin afectar la tienda en producción (rama `main`).

---

## ⚡ AHORA (Esta sesión)

### 1. Stash de los cambios ZIP actuales

Los cambios que hicimos de ZIP son **desarrollo**, deben ir a la rama de desarrollo, no a main.

```bash
cd "C:\Users\ANDAMIOS\Documents\dio personal\ebooks-store-20260930T125004Z-1-001\ebooks-store"

# Ver qué cambios tenemos
git status

# Stashear los cambios (guardarlos temporalmente)
git stash push -m "WIP: soporte para productos ZIP descargables"

# Verificar que quedamos limpio
git status  # Debe estar en main, sin cambios
```

### 2. Crear la rama de desarrollo en GitHub

```bash
# Desde cualquier rama (estamos en main, está bien)
git checkout -b feature/multi-brand-evolution

# Enviar la rama a GitHub
git push -u origin feature/multi-brand-evolution

# Verificar
git branch -a  # Debe ver: origin/feature/multi-brand-evolution
```

### 3. Restaurar los cambios ZIP en la rama de desarrollo

```bash
# Estamos en feature/multi-brand-evolution
git stash pop

# Verificar
git status  # Debe ver: backend/app.py y backend/models.py modificados

# Hacer commit
git add backend/app.py backend/models.py migrate_db.py ZIP_DOWNLOADABLE_PRODUCTS.md

git commit -m "feat: agregar soporte para productos descargables ZIP

- Extender modelo Product con campos zip_file y file_name_zip
- Implementar endpoint seguro GET /download/<token>/zip
- Agregar soporte en admin para tipo 'downloadable_zip'
- Incluir script de migración de BD
- Documentación completa de la nueva funcionalidad
- Rate limiting y validaciones de seguridad"

# Enviar a GitHub
git push origin feature/multi-brand-evolution
```

### 4. Crear archivo de configuración de desarrollo

Crea un archivo `.env.local` (para cada máquina) que no se sube a Git:

```bash
# En el directorio del proyecto

# Ya existe .env, ahora agrega .env.local a .gitignore si no está
echo ".env.local" >> .gitignore
git add .gitignore
git commit -m "chore: ignorar .env.local"
git push origin feature/multi-brand-evolution
```

---

## 📋 Estado Actual del Repositorio

### Ramas
```
main (producción - NO TOCAR)
└─ feature/multi-brand-evolution (desarrollo - AQUÍ SE TRABAJA)
```

### Cambios Guardados Localmente
```
feature/multi-brand-evolution
├── backend/app.py (con soporte ZIP)
├── backend/models.py (con columnas zip_file, file_name_zip)
├── migrate_db.py (migración de BD)
├── ZIP_DOWNLOADABLE_PRODUCTS.md (documentación)
├── test_zip_simple.py (verificación)
└── ARCHITECTURE_MULTI_BRAND.md (arquitectura)
```

---

## 🔄 Flujo de Trabajo PRÓXIMAS SESIONES

### Antes de empezar en CUALQUIER máquina

```bash
# 1. Asegúrate de estar en la rama correcta
git checkout feature/multi-brand-evolution

# 2. Descarga cambios de la otra máquina
git pull origin

# 3. Empieza tu trabajo
```

### Después de terminar cada sesión

```bash
# 1. Revisa qué cambiaste
git status
git diff

# 2. Agrega y commit
git add .
git commit -m "feat/fix: [descripción clara]"

# 3. Envía a GitHub
git push origin feature/multi-brand-evolution

# Confirma
git log --oneline -5  # Debe ver tu commit
```

---

## ✅ Checklist de Esta Sesión

- [ ] He ejecutado `git stash push` para guardar cambios ZIP
- [ ] He creado rama `feature/multi-brand-evolution` en GitHub
- [ ] He restaurado cambios ZIP en la rama nueva con `git stash pop`
- [ ] He hecho commit de cambios ZIP
- [ ] He subido rama a GitHub con `git push`
- [ ] He verificado que `main` quedó limpia sin cambios
- [ ] He configurado `.env.local` en .gitignore

---

## 🚨 Reglas de Oro

### ❌ NUNCA

```bash
# NO hagas commit directo en main
git commit -m "..." [mientras estés en main]

# NO hagas push a main
git push origin main

# NO borres la rama feature/multi-brand-evolution
git branch -D feature/multi-brand-evolution
```

### ✅ SIEMPRE

```bash
# Verifica en qué rama estás
git branch  # Debe estar en feature/multi-brand-evolution

# Antes de trabajar: descarga cambios
git pull origin

# Después de trabajar: sube cambios
git push origin
```

---

## 🔍 Verificación Final

Ejecuta esto para verificar que todo está correcto:

```bash
# Verifica que main está limpia y igual a GitHub
git checkout main
git status  # Debe estar "On branch main, nothing to commit"
git log --oneline -1  # Debe ser un commit antiguo (no tuyo)

# Verifica que feature/multi-brand-evolution tiene tus cambios
git checkout feature/multi-brand-evolution
git status  # Puede tener cambios sin commitear (OK)
git log --oneline -5  # Debe ver tus commits nuevos

# Verifica que puedes ver ambas ramas en GitHub
git branch -a | grep feature/multi-brand-evolution
```

---

## 💻 Primera Sincronización entre Máquinas

### Máquina A (ya hizo todo arriba)
```
Estado: Los cambios ZIP están en feature/multi-brand-evolution
        Ya subidos a GitHub
```

### Máquina B (próxima sesión)
```bash
cd ~/projects/ebooks-store

# Descarga la rama nueva
git fetch origin

# Cambia a la rama de desarrollo
git checkout feature/multi-brand-evolution

# Trae los cambios
git pull origin

# Verifica que ves los cambios ZIP
git log --oneline -5  # Debe ver commits de Máquina A
ls -la backend/models.py  # Debe tener el campo zip_file
```

---

## 📞 Soporte / Referencia

Si algo sale mal:

```bash
# Ver historial completo
git log --all --oneline --graph

# Ver cambios no subidos
git status
git diff

# Ver cambios en GitHub vs local
git fetch origin
git diff main origin/main
git diff feature/multi-brand-evolution origin/feature/multi-brand-evolution

# Si quieres deshacer cambios locales
git checkout -- backend/app.py  # Descarta cambios en este archivo
git restore backend/app.py      # Alternativa más nueva

# Si quieres ver qué está en GitHub
git show origin/feature/multi-brand-evolution:backend/models.py
```

---

## 🎬 Resumen Acciones Inmediatas

1. ✅ Stashear cambios ZIP
2. ✅ Crear rama `feature/multi-brand-evolution` en GitHub
3. ✅ Restaurar cambios ZIP en la rama
4. ✅ Hacer commit y push
5. ✅ Verificar que `main` quedó limpia
6. ✅ Documentar este flujo

**Resultado:** Main está intacta, cambios ZIP están seguros en rama de desarrollo, ambas máquinas pueden sincronizarse.

¿Listo?
