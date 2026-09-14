#!/bin/bash
set -e

echo "=========================================="
echo "INICIANDO DEPLOYMENT A HOSTINGER"
echo "=========================================="

cd ~/public_html

echo "1. Clonando repositorio..."
git clone https://github.com/dioyerly/Ebooksparalavida.git . || git pull

echo "2. Creando virtual environment..."
python3 -m venv venv

echo "3. Activando virtual environment..."
source venv/bin/activate

echo "4. Instalando dependencias..."
pip install -r requirements-prod.txt

echo "5. Creando carpetas de almacenamiento..."
mkdir -p storage/ebooks storage/interactive_ebooks storage/personalized_ebooks
chmod 755 storage/*

echo "6. Creando .env para producción..."
cat > .env << 'ENVEOF'
DATABASE_URL=postgresql://ebooksadmin:Abc123!@#$%^&@localhost:5432/ebooks_store_
SECRET_KEY=tu-clave-aleatoria-segura-aqui-cambiar
ADMIN_EMAIL=admin@estrategia.site
ADMIN_PASSWORD=contraseña-segura-cambiar
MP_ACCESS_TOKEN=
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
SENDGRID_API_KEY=
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=
SMTP_FROM=noreply@estrategia.site
PUBLIC_BASE_URL=https://estrategia.site
ARS_PER_USD=1450
ARS_PER_EUR=1650
ENVEOF

echo "7. Creando tablas en base de datos..."
python3 << 'PYEOF'
from backend.app import app, db
import os

with app.app_context():
    db.create_all()
    print("✓ Tablas de base de datos creadas")
PYEOF

echo ""
echo "=========================================="
echo "DEPLOYMENT COMPLETADO!"
echo "=========================================="
echo ""
echo "PRÓXIMOS PASOS:"
echo "1. Edita .env con contraseña real de BD"
echo "2. En Hostinger Panel, configura Python WSGI"
echo "3. Visita: https://estrategia.site"
echo ""
