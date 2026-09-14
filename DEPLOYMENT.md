# 🚀 Guía de Despliegue a Hostinger

## Estado: LISTO PARA PRODUCCIÓN

Tu app está lista para subir a Hostinger. Sigue estos pasos exactos.

---

## **PASO 1: Acceder a Hostinger Panel**

1. Ve a https://hpanel.hostinger.com/login
2. Inicia sesión con tus credenciales
3. En el menú izquierdo, click en **"Sitios web"**
4. Haz click en **estrategia.site**

---

## **PASO 2: Configurar Base de Datos PostgreSQL**

### En Hostinger Panel:

1. Dentro de tu sitio, ve a **"Bases de datos"** (o MySQL/PostgreSQL)
2. Click en **"Crear base de datos"**
3. Nombre: `ebooks_store_prod`
4. Usuario: `ebooksadmin`
5. Contraseña: **GENERA UNA SEGURA** (cópiala)
6. Click "Crear"

Guarda estos datos:
```
HOST: (Hostinger te lo da, algo como: mysql.hostinger.com)
DATABASE: ebooks_store_prod
USER: ebooksadmin
PASSWORD: (la que creaste)
PORT: 5432 (para PostgreSQL)
```

---

## **PASO 3: Acceder por SSH**

### Opción A: Desde Hostinger Panel

1. En tu sitio, ve a **"Acceso SSH"**
2. Activa si no está activado
3. Copia los datos de conexión:
   - Host: (algo como: 123.456.789.10)
   - Usuario: (tu usuario de Hostinger)
   - Puerto: 22

### Opción B: Desde Terminal (PowerShell)

```powershell
ssh tu_usuario@123.456.789.10 -p 22
```

Contraseña: (la de tu cuenta Hostinger)

---

## **PASO 4: Descargar Git en el Servidor**

Una vez conectado por SSH:

```bash
# Verificar si Git está instalado
git --version

# Si no está, instalarlo (si tienes acceso root)
sudo apt-get install git

# Si no funciona, Hostinger ya lo tiene instalado
```

---

## **PASO 5: Subir Código a Hostinger**

### Opción A: Con Git (Recomendado)

```bash
# Ir a la carpeta del sitio
cd ~/public_html

# Clonar tu repositorio (si tienes GitHub)
git clone https://github.com/tu-usuario/ebooks-store.git .

# O copiar manualmente los archivos por SFTP
```

### Opción B: Por File Manager (Hostinger Panel)

1. En Hostinger, ve a **"File Manager"**
2. Accede a `public_html`
3. Sube todos los archivos EXCEPTO:
   - `.venv/` (carpeta virtual env)
   - `.git/` (carpeta git)
   - `__pycache__/`
   - `.env` (vas a crear uno nuevo)

---

## **PASO 6: Crear .env para Producción**

En SSH o por File Manager, crea `/home/tu_usuario/public_html/.env`:

```bash
# Configuración de Base de Datos
DATABASE_URL=postgresql://ebooksadmin:TU_CONTRASEÑA@localhost:5432/ebooks_store_prod

# Seguridad
SECRET_KEY=genera-una-clave-aleatoria-muy-segura-aqui

# Admin
ADMIN_EMAIL=tu-email@example.com
ADMIN_PASSWORD=contraseña-segura-cambiar

# Mercado Pago (si tienes credenciales reales)
MP_ACCESS_TOKEN=tu-token-real-aqui

# PayPal
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=

# Email (SendGrid)
SENDGRID_API_KEY=

# SMTP (para emails)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=
SMTP_FROM=tu-email@estrategia.site

# URLs
PUBLIC_BASE_URL=https://estrategia.site
ARS_PER_USD=1450
ARS_PER_EUR=1650
```

---

## **PASO 7: Instalar Dependencias Python**

En SSH:

```bash
# Ir a la carpeta
cd ~/public_html

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements-prod.txt

# Instalar PostgreSQL driver
pip install psycopg2-binary
```

---

## **PASO 8: Crear Tablas en Base de Datos**

En SSH:

```bash
# Activar entorno virtual
source venv/bin/activate

# Crear tablas
python3 << EOF
from backend.app import app, db
with app.app_context():
    db.create_all()
    print("✓ Tablas creadas")
EOF
```

---

## **PASO 9: Configurar Python en Hostinger**

En Hostinger Panel del sitio:

1. Ve a **"Configuración de Python"** o **"Aplicaciones"**
2. Click en **"Nueva aplicación"** o **"Editar"**
3. Selecciona **Python 3.11+**
4. Ruta de la aplicación: `/home/tu_usuario/public_html`
5. Archivo WSGI: `wsgi.py`
6. Comando de entrada: `wsgi:app`
7. Click "Guardar"

**Hostinger iniciará tu app automáticamente**

---

## **PASO 10: Configurar SSL/HTTPS**

En Hostinger Panel:

1. Ve a **"Dominios"**
2. Selecciona **estrategia.site**
3. Click en **"SSL"**
4. Click **"Crear certificado Let's Encrypt"**
5. Espera a que se genere (2-5 minutos)

Hostinger lo instala automáticamente.

---

## **PASO 11: Crear Carpetas de Almacenamiento**

En SSH:

```bash
cd ~/public_html

# Crear carpetas
mkdir -p storage/ebooks
mkdir -p storage/interactive_ebooks
mkdir -p storage/personalized_ebooks

# Permisos
chmod 755 storage
chmod 755 storage/ebooks
chmod 755 storage/interactive_ebooks
chmod 755 storage/personalized_ebooks
```

---

## **PASO 12: Probar la App**

Abre en el navegador:

```
https://estrategia.site
```

Debería cargar tu tienda. ✓

---

## **PASO 13: Cargar Productos Reales**

1. Ve a `https://estrategia.site/admin/login`
2. Inicia sesión con las credenciales de .env
3. Crea tus productos
4. Sube PDFs a `storage/ebooks/`
5. Sube portadas

---

## **Checklist Final**

- [ ] Base de datos PostgreSQL creada
- [ ] SSH acceso funcionando
- [ ] Código subido a public_html
- [ ] .env creado con credenciales reales
- [ ] Dependencias instaladas
- [ ] Tablas de BD creadas
- [ ] Python configurado en Hostinger
- [ ] SSL/HTTPS activado
- [ ] Carpetas de almacenamiento creadas
- [ ] Admin funciona
- [ ] Tienda carga
- [ ] Pagos configurados

---

## **Solución de Problemas**

### "Error: ModuleNotFoundError: No module named 'flask'"
```bash
source venv/bin/activate
pip install Flask Flask-SQLAlchemy
```

### "Error: Database connection refused"
- Verificar credenciales en .env
- Verificar que PostgreSQL está corriendo en Hostinger
- Verificar HOST correcto

### "Error: SECRET_KEY not found"
- Verificar que .env existe en public_html
- Generar una clave segura

### "Error: PDFs no se descargan"
- Verificar que storage/ebooks/ existe
- Verificar permisos (chmod 755)

---

## **Contacto & Soporte**

Si algo no funciona:
1. Revisa los logs de Hostinger (Panel → Registros)
2. Verifica el .env
3. Verifica permisos de carpetas

**¡Listo para vender en producción!** 🎉
