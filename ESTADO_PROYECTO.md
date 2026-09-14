# Estado del Proyecto - Tienda de Ebooks

**Última actualización:** 14 de septiembre 2026
**Estado:** En desarrollo - Almacenamiento persistente implementado

---

## 1. QUÉ ES ESTA PÁGINA / OBJETIVO

Es una **tienda de ebooks online** donde:
- Los clientes compran ebooks interactivos y PDFs
- Pagan con Mercado Pago (dinero real)
- Reciben acceso a descargar/leer sus ebooks
- Tú tienes un panel admin para crear productos y subir ebooks

**Dominio:** estrategia.site (ya configurado y activo)
**Hosting:** Render.com (gratis)
**Base de datos:** MySQL en Hostinger (ya tienes)

---

## 2. ESTADO ACTUAL - QUÉ FUNCIONA

### ✓ FUNCIONANDO:
- [x] Página de inicio (home)
- [x] Tienda con listado de productos
- [x] Página de detalle de producto
- [x] Carrito de compras
- [x] Checkout con Mercado Pago (pagos REALES)
- [x] Admin panel para crear productos
- [x] Autenticación admin (Usuario: admin@estrategia.site, Pass: Admin123456)
- [x] Almacenamiento de ebooks en GitHub (PERSISTENTE)
- [x] Descarga automática de ebooks al iniciar Render

### ⚠️ INCOMPLETO:
- [ ] Subida de ebooks desde admin panel
- [ ] Sistema de descargas/acceso de clientes
- [ ] Confirmación de pago por email
- [ ] Panel de analytics (parcial)
- [ ] Integración final con base de datos MySQL

---

## 3. PROBLEMA QUE ACABA DE RESOLVERSE

**ANTES:** Los ebooks desaparecían cada vez que Render se reiniciaba (almacenamiento ephemeral)

**SOLUCIÓN IMPLEMENTADA:**
- Todos los ebooks se guardan en GitHub (carpeta `ebooks_github/`)
- Un script (`download_ebooks.sh`) descarga los ebooks de GitHub cuando Render inicia
- Esto es GRATIS y FUNCIONA SIEMPRE

**Ebooks actualmente guardados en GitHub:**
- convivir-sin-apagar-incendios.pdf
- kit-convivir-sin-apagar-incendios.pdf
- primero-tu-mente-despues-tu-hogar.pdf
- Descubre_tu_identidad_como_lectora.pdf
- the-romance-reader-kit.html (interactivo)
- kit-primero-tu-mente-despues-tu-hogar.zip

---

## 4. PRÓXIMO PASO IMPORTANTE - DECIDIR BASE DE DATOS

**Necesitamos elegir UNA de estas dos opciones:**

### OPCIÓN A: Usar MySQL de Hostinger (que ya tienes)
```
Base de datos: u748338755_tienda_de_libros_electronicos_
Usuario: u748338755_ebooksadmin
Sitio: estrategia.site
```

**Ventajas:**
- Ya lo tienes pagado
- Todo centralizado en Hostinger
- Menos cosas que administrar

**Desventajas:**
- Más lento (conexión por red)
- Más complicado de configurar

**Qué hacer:**
1. Obtener el HOST de MySQL desde Hostinger (probablemente algo como: `mysql123.hostinger.com`)
2. Obtener la CONTRASEÑA del usuario `u748338755_ebooksadmin`
3. Pasar esa información para que configure en Render

---

### OPCIÓN B: Usar PostgreSQL gratis de Render
**Ventajas:**
- Más rápido (misma red)
- Más simple de configurar
- Completamente gratis

**Desventajas:**
- Separado de Hostinger
- No centralizado

**Qué hacer:**
- Simplemente decir "usa Render PostgreSQL"
- Se configura automáticamente

---

## 5. ARCHIVOS PRINCIPALES DEL PROYECTO

```
ebooks-store/
├── backend/
│   ├── app.py              # Aplicación principal Flask
│   ├── models.py           # Modelos de base de datos (SQLAlchemy)
│   ├── services.py         # Lógica de Mercado Pago, PayPal, Email
│   └── templates/          # Páginas HTML
│       ├── admin/
│       │   └── dashboard.html    # Panel admin
│       ├── home.html             # Página de inicio
│       ├── shop.html             # Tienda
│       ├── product.html          # Detalle de producto
│       ├── cart.html             # Carrito
│       └── checkout.html         # Checkout
├── ebooks_github/          # Ebooks guardados en GitHub (PERSISTENTE)
│   ├── *.pdf               # Archivos PDF
│   └── *.html              # Ebooks interactivos
├── storage/                # Carpeta donde se descargan los ebooks
│   ├── ebooks/
│   ├── interactive_ebooks/
│   └── personalized_ebooks/
├── download_ebooks.sh      # Script que descarga ebooks de GitHub
├── run.sh                  # Script que inicia la app
├── Procfile                # Configuración de Render
├── requirements-prod.txt   # Dependencias Python
├── wsgi.py                 # Punto de entrada WSGI
└── .env.render             # Variables de entorno (SEGURO en Render)
```

---

## 6. FLUJO ACTUAL DE LA TIENDA

```
Cliente accede a estrategia.site
        ↓
Ve la tienda y productos (desde app.py)
        ↓
Selecciona producto y va al carrito
        ↓
Hace checkout
        ↓
Paga con Mercado Pago (PAGO REAL)
        ↓
Recibe confirmación
        ↓
[FALTA] Debería recibir ebook o acceso a descargar
```

---

## 7. QUÉ FALTA POR HACER

### PRIORITARIO:

1. **Decidir base de datos** (MySQL Hostinger O PostgreSQL Render)
   - Tiempo: 5 minutos (solo decidir y pasar datos)

2. **Subida de ebooks desde admin**
   - Crear formulario en admin dashboard
   - Guardar archivos en base de datos (como BLOB)
   - Tiempo: 1-2 horas

3. **Sistema de descargas para clientes**
   - Cuando cliente compra, obtiene token de acceso
   - Puede descargar ebook con ese token
   - Token tiene expiración (opcional)
   - Tiempo: 1-2 horas

4. **Email de confirmación**
   - Cliente recibe email con enlace de descarga
   - Email con resumen de compra
   - Tiempo: 1 hora

5. **Conectar con base de datos MySQL**
   - Actualizar DATABASE_URL en Render
   - Migrar datos si es necesario
   - Tiempo: 30 minutos

### SECUNDARIO (después):

6. Panel de analytics completo
7. Integración con PayPal (opcional)
8. Cupones y descuentos
9. Historial de compras del cliente
10. Mejoras visuales/diseño

---

## 8. CREDENCIALES Y ACCESO

### Render.com
- URL: https://dashboard.render.com
- App: ebooksparalavida
- Dominio: estrategia.site (apunta aquí)

### Admin Panel de la Tienda
- URL: https://estrategia.site/admin
- Usuario: admin@estrategia.site
- Contraseña: Admin123456

### GitHub
- Repositorio: https://github.com/dioyerly/Ebooksparalavida
- Rama: main
- Todos los ebooks en: ebooks_github/

### Hostinger
- Dominio: estrategia.site
- MySQL disponible en panel de control

### Mercado Pago
- Token de producción ya configurado
- APP_USR-6834717159645607-091410-aecfbe1beea80419678af36ab422c344-437116311
- (En variables de entorno de Render)

---

## 9. CÓMO CONTINUAR MAÑANA

1. **Abre esta archivo** (ESTADO_PROYECTO.md)
2. **Revisa la sección "PRÓXIMO PASO"**
3. **Elige: MySQL Hostinger O PostgreSQL Render**
4. **Avísame tu decisión**
5. **Seguimos con la subida de ebooks y descargas**

---

## 10. NOTAS IMPORTANTES

### ❌ NO HACER:
- No cambiar de hosting otra vez
- No agregar más dependencias complicadas
- No modificar a mano archivos en Render

### ✓ SIEMPRE:
- Subir cambios a GitHub (todo se actualiza automáticamente en Render)
- Guardar ebooks en la solución elegida (GitHub o BD)
- Probar pagos en https://estrategia.site/pay (sandbox si necesitas)

### COSTOS FINALES:
- Hostinger: $200/año (ya pagado)
- Render: GRATIS
- PostgreSQL Render: GRATIS
- GitHub: GRATIS
- **Total adicional: $0**

---

## 11. COMANDOS ÚTILES

```bash
# Subir cambios a GitHub (esto redeploya en Render automáticamente)
git add .
git commit -m "Descripción del cambio"
git push origin main

# Ver logs de Render (si algo falla)
# Ir a: https://dashboard.render.com → tu app → Logs

# Acceder al admin
# https://estrategia.site/admin
```

---

## 12. PRÓXIMAS CONVERSACIONES

Cuando abras esto mañana en tu casa:

1. ¿Decidiste qué base de datos usar?
2. ¿Qué ebooks necesitas agregar?
3. ¿Necesitas probar un pago de verdad o en sandbox?
4. ¿Qué tipo de confirmación quieres enviar al cliente?

---

**ESTADO RESUMIDO:**
- ✓ Hosting funcionando
- ✓ Dominio activo
- ✓ Pagos con Mercado Pago listos
- ✓ Almacenamiento de ebooks persistente
- ⏳ Falta conectar BD y sistema de descargas

**SIGUIENTE:** Decidir base de datos y implementar subida/descarga de ebooks.
