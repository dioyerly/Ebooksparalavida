# 💳 Guía: Activar Pagos en Ebooksparalavida

## 🎯 Estado Actual

✅ **Sistema de carrito**: Funcional
✅ **Checkout**: Funcional  
✅ **Modo Demo**: Funcional (simula pagos)
✅ **Email de descarga**: En modo demo
⏳ **Pagos Reales**: Necesita configuración

---

## 📋 Flujo de Compra Actual

```
1. Cliente agrega producto al carrito
   ↓
2. Va a /cart (ve productos)
   ↓
3. Click "Continuar al pago"
   ↓
4. Llena nombre y email en /checkout
   ↓
5. Elige método de pago (Mercado Pago o PayPal)
   ↓
6. Click "Confirmar compra"
   ↓
7. En DEMO: Marca como pagado y va a /success
   En REAL: Redirige a plataforma de pago
   ↓
8. /success muestra orden y enlace de descarga
   ↓
9. Cliente descarga su ebook con token único
```

---

## 🧪 Modo Demo - Pruebas Locales (ACTUAL)

### ¿Cómo Funciona?

En modo demo (sin credenciales configuradas):
- ✅ Crear orden en base de datos
- ✅ Marcar como `paid_demo` automáticamente
- ✅ Ir a página de éxito
- ✅ Mostrar enlace de descarga
- ✅ Simular envío de email

### Probar Ahora

```
1. Abre: http://127.0.0.1:5000
2. Click en un ebook
3. Click "Comprar ebook"
4. Click "Carrito" (arriba)
5. Click "Continuar al pago"
6. Completa:
   - Nombre: Tu nombre
   - Email: tu@email.com
   - Método: Mercado Pago (o PayPal)
7. Click "Confirmar compra"
8. ✅ Verás página de éxito con opción de descargar
```

### Ver Órdenes en Admin

```
http://127.0.0.1:5000/admin
→ Tab "Órdenes"
→ Verás todas las órdenes demo
→ Click en orden para ver detalles
```

---

## 💰 Activar Pagos Reales

### Paso 1: Configurar Mercado Pago (Argentina)

#### 1.1 Crear Cuenta

1. Ve a https://www.mercadopago.com.ar
2. Crea cuenta o inicia sesión
3. Ve a "Configuración" → "Credenciales"
4. Busca "Access Token"

#### 1.2 Obtener Credenciales

En Mercado Pago:
```
- Modo: SANDBOX (para pruebas)
- Access Token: (copia este valor)
```

#### 1.3 Agregar a .env

```bash
# Edita: .env

MP_ACCESS_TOKEN=tu_access_token_aqui
```

#### 1.4 Probar con Tarjetas de Prueba

Mercado Pago proporciona tarjetas fake para probar:

**Visa APROBADO:**
```
Número: 4111 1111 1111 1111
Vencimiento: 11/25
CVV: 123
```

**Visa RECHAZADO:**
```
Número: 4532 1488 0343 6467
Vencimiento: 11/25
CVV: 123
```

**MasterCard APROBADO:**
```
Número: 5425 2334 3010 9903
Vencimiento: 12/25
CVV: 123
```

### Paso 2: Configurar PayPal (Compras Internacionales)

#### 2.1 Crear Cuenta Business

1. Ve a https://developer.paypal.com
2. Crea o inicia sesión con tu cuenta
3. Ve a "Apps & Credentials"
4. Usa SANDBOX (no Live, aún no)

#### 2.2 Obtener Credenciales

```
Client ID: (copia este valor)
Secret: (copia este valor)
```

#### 2.3 Agregar a .env

```bash
# Edita: .env

PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_CLIENT_SECRET=tu_secret_aqui
```

#### 2.4 Crear Cuentas de Prueba

En PayPal Developer:
```
Buyer Account: buyer-XXXXX@personal.example.com / password: 12345
Seller Account: seller-XXXXX@business.example.com / password: 12345
```

---

## 🧪 Pruebas en Modo Real

### Prueba 1: Flujo Completo con Mercado Pago

```
1. Actualiza .env con credenciales MP
2. Reinicia la app: python -m flask --app backend.app run
3. Compra un ebook (http://127.0.0.1:5000)
4. En checkout, elige "Mercado Pago"
5. Serás redirigido a MP
6. Usa tarjeta de prueba: 4111 1111 1111 1111
7. Completa con datos ficticios
8. Si aprueba, verás /success
```

### Prueba 2: Flujo Completo con PayPal

```
1. Actualiza .env con credenciales PayPal
2. Reinicia la app
3. Compra un ebook
4. En checkout, elige "PayPal"
5. Serás redirigido a PayPal Sandbox
6. Usa cuenta buyer-XXX@personal.example.com
7. Si aprueba, verás /success
```

### Prueba 3: Ver Órdenes Pagadas

```
Admin → Tab "Órdenes"
Verás:
- Órdenes en DEMO (status: paid_demo)
- Órdenes en REAL (status: paid)
```

---

## 📧 Sistema de Email (Opcional - SendGrid)

### ¿Qué Hace?

Envía email al cliente cuando compra:
```
Asunto: ¡Tu ebook está listo para descargar!

Contenido:
- Datos de la compra
- Enlace de descarga único
- Confirmar que nunca caduca
```

### Activar SendGrid

#### 1. Crear Cuenta

1. Ve a https://sendgrid.com
2. Crea cuenta gratis
3. Ve a "API Keys"
4. Crea una clave API

#### 2. Agregar a .env

```bash
SENDGRID_API_KEY=SG.tu_api_key_aqui
```

#### 3. Código está listo

El código ya está implementado en `backend/services.py`
Solo necesita activar con la clave API.

---

## ⚠️ Checklist Antes de Producción

- [ ] Cambiar SECRET_KEY en .env (no usar default)
- [ ] Usar acceso de Mercado Pago en MODO PRODUCCIÓN (no sandbox)
- [ ] Usar acceso de PayPal en MODO LIVE (no sandbox)
- [ ] Configurar SendGrid API Key
- [ ] Cambiar ADMIN_EMAIL y ADMIN_PASSWORD
- [ ] Cambiar PUBLIC_BASE_URL a tu dominio real
- [ ] Usar PostgreSQL (no SQLite)
- [ ] Usar HTTPS (no HTTP)
- [ ] Configurar backups de la base de datos
- [ ] Configurar backups de PDFs en storage/ebooks/

---

## 📊 Estados de Orden

```
pending      → Esperando pago
paid         → Pago confirmado por plataforma
paid_demo    → Pago simulado en modo demo
rejected     → Pago rechazado
cancelled    → Comprador canceló
```

---

## 🔄 Webhooks (Pago Confirmado)

### ¿Qué es?

Cuando cliente paga, Mercado Pago/PayPal envía notificación a tu servidor.

### ¿Qué hace?

```
1. Cliente paga
2. Plataforma de pago →  POST /webhook/mercadopago
3. Tu servidor recibe confirmación
4. Marca orden como "paid"
5. Genera token de descarga
```

### Estado Actual

⏳ Webhooks no están implementados aún.

**Solución provisional:**
- Órdenes marcadas como `paid` en modo real cuando plataforma redirige a /success
- Mejora futura: agregar verificación real via API

### Implementar (Futuro)

```python
@app.post("/webhook/mercadopago")
def webhook_mercadopago():
    # Recibir notificación de MP
    # Validar firma
    # Actualizar estado de orden
    # Retornar 200 OK
    pass
```

---

## 💾 Resumen de Archivos Actualizados

```
backend/app.py
  ├─ Importa MercadoPagoService, PayPalService, EmailService
  ├─ Ruta POST /checkout mejorada
  └─ Crea preferencias de pago

backend/services.py (NUEVO)
  ├─ MercadoPagoService
  ├─ PayPalService
  └─ EmailService

backend/templates/success.html (MEJORADO)
  ├─ Resumen de orden
  ├─ Enlace de descarga
  ├─ Instrucciones siguientes
  └─ Información de email

.env (REQUIERE CONFIG)
  ├─ MP_ACCESS_TOKEN = tu_token
  ├─ PAYPAL_CLIENT_ID = tu_id
  ├─ PAYPAL_CLIENT_SECRET = tu_secret
  └─ SENDGRID_API_KEY = tu_key
```

---

## 🚀 Próximos Pasos

### Corto Plazo (Esta Semana)
1. ✅ Activar Mercado Pago sandbox
2. ✅ Probar flujo completo
3. ✅ Probar descargas
4. ✅ Probar admin panel

### Mediano Plazo (Este Mes)
1. Implementar webhooks
2. Agregar verificación de pago en real-time
3. Mejorar email con SendGrid
4. Agregar recibos PDF

### Largo Plazo (Producción)
1. Pasar a credenciales LIVE
2. Configurar HTTPS
3. Usar PostgreSQL
4. Configurar backups
5. Dar de alta en Mercado Pago/PayPal como seller

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo vender sin activar pagos reales?**
A: Sí, el modo demo funciona completamente. Crea órdenes falsas para probar.

**P: ¿Qué pasa si cliente paga pero webhook falla?**
A: Mejora futura. Por ahora, consultar a MP/PayPal via API.

**P: ¿Cuánto cobra Mercado Pago?**
A: ~2.9% de comisión por transacción en Argentina.

**P: ¿PayPal es obligatorio?**
A: No. Mercado Pago es suficiente para Argentina. PayPal es opcional para compras internacionales.

**P: ¿Los clientes ven qué plataforma de pago usamos?**
A: Sí, lo eligen en el checkout.

**P: ¿Se puede cambiar de MP a PayPal después?**
A: Sí, totalmente flexible. Está configurado para soportar ambos.

---

**Última actualización:** 2026-09-13
**Versión:** Sistema de pagos integrado (modo demo + real)
