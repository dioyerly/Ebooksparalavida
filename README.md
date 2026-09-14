# Ebooks para la vida

Tienda online MVP para ebooks digitales en español. Está construida con Flask, SQLite y plantillas server-rendered para que el primer flujo de compra sea rápido de desplegar y fácil de mantener.

## Qué incluye

- Home responsive con catálogo, filtros por categoría, detalle de producto, FAQ y enlaces de marca.
- Carrito basado en sesión y checkout con datos de comprador.
- Modo demo local para Mercado Pago y PayPal: crea una orden `paid_demo` y permite probar el flujo completo sin credenciales.
- Tokens únicos de descarga para servir el PDF comprado de forma privada, sin caducidad de acceso.
- Panel admin protegido por sesión para revisar órdenes, ingresos y crear productos.
- Carpeta privada `storage/ebooks/` para PDFs reales. El PDF no se expone como archivo público.

## Ejecutar localmente en Windows

Requiere Python 3.11+.

```powershell
cd c:\Users\Andrea\Documents\Dio\ebooks-store
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
flask --app backend.app run --debug
```

Abrí http://127.0.0.1:5000. La base SQLite y los productos de ejemplo se crean automáticamente al iniciar.

Panel: http://127.0.0.1:5000/admin/login
Credenciales por defecto de desarrollo: `admin@ebooksparalavida.com` / `admin123`. Cambialas en `.env` antes de compartir el entorno.

## Configurar PDFs

Colocá los archivos en `storage/ebooks/` y asigná el nombre en `Product.file_name` desde una migración o desde el panel cuando se amplíe el formulario de carga. El endpoint `/download/<token>` valida estado, token y vencimiento antes de servir el archivo.

## Pagos reales antes de producción

1. Creá credenciales de prueba y producción en Mercado Pago Developers y PayPal Developer.
2. Agregá `MP_ACCESS_TOKEN`, `PAYPAL_CLIENT_ID` y `PAYPAL_CLIENT_SECRET` al `.env` de producción.
3. Implementá la creación de preferencias/órdenes en `backend/services/` y sus webhooks en rutas HTTPS públicas.
4. Cambiá el estado de la orden solo después de validar el pago consultando la API del proveedor. Nunca confíes en un `success` del navegador.
5. Configurá SMTP o SendGrid para enviar el token al email del comprador.
6. Usá PostgreSQL, HTTPS, un `SECRET_KEY` aleatorio y rate limiting en descarga para producción.

## Despliegue sugerido

Para un primer deploy podés usar Render, Railway o DigitalOcean con Gunicorn y PostgreSQL. Configurá `PUBLIC_BASE_URL`, las variables de pago, el almacenamiento privado de PDFs y los webhooks HTTPS. El archivo `database/schema.sql` sirve como referencia del modelo relacional.

## Ebooks HTML interactivos

Los productos con tipo `HTML Interactivo` usan un archivo HTML offline como origen. El archivo original se guarda en `storage/interactive_ebooks/` y nunca se modifica. Luego del pago demo, el servidor genera una copia en `storage/personalized_ebooks/` con el email del comprador y un código único de 8 caracteres; el login del archivo valida ambos datos mediante `localStorage` sin conexión a internet.

El panel admin permite elegir `PDF/EPUB` o `HTML Interactivo`. Para enviar el archivo adjunto en producción, completá `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` y `SMTP_FROM` en `.env`. Sin SMTP configurado, el modo demo imprime el email y el código en la consola.
