# ⚡ INICIO RÁPIDO - Hostinger

## Resumen 30 segundos

Tu app está lista. Estos son los PASOS EXACTOS en orden:

---

## **AHORA MISMO (5 minutos)**

```
1. Abre: https://hpanel.hostinger.com/login
2. Login con tu email y contraseña de Hostinger
3. Click en "Sitios web" → "estrategia.site"
4. Click en "Bases de datos"
5. Crea PostgreSQL:
   - Nombre: ebooks_store_prod
   - Usuario: ebooksadmin
   - Contraseña: (genera segura, copia)
6. ESPERA a que se cree (2-3 minutos)
```

---

## **LUEGO (10 minutos)**

```
1. En Hostinger Panel del sitio
2. Click "Acceso SSH"
3. Copia estos datos:
   - Host: (números tipo 123.456.789.10)
   - Usuario: (tu usuario Hostinger)
   - Puerto: 22
```

---

## **POR TERMINAL (PowerShell) (15 minutos)**

```powershell
# Conectar por SSH
ssh tu_usuario@123.456.789.10 -p 22
# (Contraseña: la de tu cuenta Hostinger)

# Una vez conectado, ejecuta:
cd ~/public_html
git clone https://github.com/tu-usuario/ebooks-store.git .
# (O sube files manualmente por File Manager si no tienes GitHub)

# Luego:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt

# Crear base de datos:
python3 << EOF
from backend.app import app, db
with app.app_context():
    db.create_all()
EOF

# Crear carpetas:
mkdir -p storage/ebooks
mkdir -p storage/interactive_ebooks
mkdir -p storage/personalized_ebooks
chmod 755 storage/*
```

---

## **EN HOSTINGER PANEL (5 minutos)**

```
1. Ve a "Configuración de Python"
2. Selecciona Python 3.11+
3. Archivo WSGI: wsgi.py
4. Click "Guardar"
5. Espera que se reinicie la app
```

---

## **VERIFICAR QUE FUNCIONA**

Abre en navegador:
```
https://estrategia.site
```

Si ves tu tienda → ✅ LISTO

Si ves error → Revisa logs en Hostinger Panel

---

## **ARCHIVOS IMPORTANTES**

Antes de subir, configura:

- `DEPLOYMENT.md` - Instrucciones detalladas
- `.env.production` - Template para prod
- `requirements-prod.txt` - Dependencias limpias
- `wsgi.py` - Entrada para Hostinger

---

## **SI NECESITAS AYUDA**

1. Revisa `DEPLOYMENT.md` - Tiene todo explicado
2. Revisa logs en Hostinger Panel
3. Verifica que .env esté correcto

**¡Listo para vender!** 🚀
