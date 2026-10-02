# Mapa de Rutas - Plataforma Multi-Marca

## Rutas Públicas (Sin Autenticación)

### Home y Portales

```
GET  /                          → home_unified() - Página de inicio narrativa
     - Muestra la fusión de 3 marcas
     - Portales visuales a cada universo
     - No tiene tema, es neutra (transición)
```

---

### Marca: Ebooks para la vida

```
GET  /ebooks                    → ebooks_bp.catalog()
     - Catálogo completo de ebooks
     - Filtros por categoría, búsqueda
     - Body class: "theme-ebooks"

GET  /ebooks/<product_id>       → ebooks_bp.product_detail()
     - Página de producto individual
     - Opción "Agregar al carrito"
     - Body class: "theme-ebooks"

GET  /ebooks/category/<cat>     → ebooks_bp.category()
     - Catálogo filtrado por categoría
     - Body class: "theme-ebooks"

GET  /ebooks/search?q=<query>   → ebooks_bp.search()
     - Búsqueda de ebooks
     - Body class: "theme-ebooks"
```

---

### Marca: YOYI'R

```
GET  /yoyir                     → yoyir_bp.catalog()
     - Catálogo de agendas/planners
     - Filtros, búsqueda
     - Body class: "theme-yoyir"

GET  /yoyir/<product_id>        → yoyir_bp.product_detail()
     - Página de producto individual
     - Opción "Agregar al carrito"
     - Body class: "theme-yoyir"

GET  /yoyir/category/<cat>      → yoyir_bp.category()
     - Catálogo filtrado por categoría
     - Body class: "theme-yoyir"

GET  /yoyir/search?q=<query>    → yoyir_bp.search()
     - Búsqueda de planners
     - Body class: "theme-yoyir"
```

---

### Marca: EstrategIA

```
GET  /estrategia                → estrategia_bp.catalog()
     - Catálogo de herramientas/micro-apps
     - Filtros, búsqueda
     - Body class: "theme-estrategia"

GET  /estrategia/<product_id>   → estrategia_bp.product_detail()
     - Página de producto individual
     - Opción "Acceder" o "Agregar al carrito"
     - Body class: "theme-estrategia"

GET  /estrategia/app/<app_id>   → estrategia_bp.view_app()
     - Visor de micro-app HTML
     - Acceso por token/sesión
     - Body class: "theme-estrategia"

GET  /estrategia/search?q=<q>   → estrategia_bp.search()
     - Búsqueda de herramientas
     - Body class: "theme-estrategia"
```

---

### Carrito (Agnóstico de Marca)

```
GET  /cart                      → cart_bp.view_cart()
     - Ver carrito (items de cualquier marca)
     - Muestra total
     - Body class: depende de última marca visitada (o neutra)

POST /cart/add                  → cart_bp.add_to_cart()
     - Agregar producto al carrito
     - Acepta marca y product_id

POST /cart/remove/<product_id>  → cart_bp.remove_from_cart()
     - Remover producto del carrito

POST /cart/clear                → cart_bp.clear_cart()
     - Vaciar carrito
```

---

### Checkout y Pagos (Agnóstico de Marca)

```
GET  /checkout                  → checkout_bp.checkout_view()
     - Página de confirmación y datos de comprador
     - Muestra items del carrito
     - Formulario de datos

POST /checkout/pay              → checkout_bp.process_payment()
     - Procesa pago con Mercado Pago
     - Crea orden en BD
     - Redirige a MP

POST /checkout/webhook/mp       → checkout_bp.webhook_mercadopago()
     - Webhook de Mercado Pago
     - Confirma pago
     - Genera descarga/acceso

GET  /checkout/success/<order_id> → checkout_bp.payment_success()
     - Página de confirmación de compra
     - Enlace de descarga

GET  /order/<order_id>          → checkout_bp.view_order()
     - Detalles de orden
     - (Requiere autenticación o token)
```

---

### Descarga y Acceso (Post-Compra)

```
GET  /download/<token>          → checkout_bp.download_file()
     - Descarga de archivo (PDF, ZIP, etc.)
     - Token válido solo para usuario autenticado

GET  /leer/<access_code>        → estrategia_bp.read_interactive()
     - Acceso a producto interactivo HTML
     - Redirige a /estrategia/app/<app_id>
```

---

## Rutas Protegidas (Requieren Login)

### Perfil de Usuario

```
GET  /profile                   → user_bp.profile()
     - Datos del usuario
     - Histórico de compras

GET  /profile/orders            → user_bp.orders_history()
     - Lista de órdenes del usuario
     - Enlaces a descargas
```

---

### Admin (Requiere autenticación y rol admin)

```
GET  /admin                     → admin_bp.dashboard()
     - Dashboard general
     - Estadísticas por marca

GET  /admin/products            → admin_bp.products_list()
     - Listar todos los productos
     - Filtros por marca

POST /admin/products/create     → admin_bp.create_product()
     - Crear nuevo producto
     - Seleccionar marca
     - Subir archivo

POST /admin/products/<id>/edit  → admin_bp.edit_product()
     - Editar producto
     - Cambiar marca, precio, archivo

POST /admin/products/<id>/delete → admin_bp.delete_product()
     - Eliminar producto

GET  /admin/orders              → admin_bp.orders_list()
     - Listar todas las órdenes
     - Filtros por marca, fecha

GET  /admin/stats               → admin_bp.stats()
     - Estadísticas de ventas
     - Gráficos por marca
     - Top productos
```

---

## Contexto de Marca en Rutas

### Variable de Sesión

```python
session['current_brand'] = 'ebooks' | 'yoyir' | 'estrategia' | None
```

Se establece cuando el usuario entra a `/ebooks`, `/yoyir` o `/estrategia`.

### En Templates

```html
<body class="theme-{{ brand }}">
  ...
</body>
```

Donde `brand` viene del contexto: `render_template('template.html', brand='ebooks')`

---

## Notas sobre Navegación

1. **Navbar global**: Disponible en todas las páginas
   - Logo/Home (enlace a /)
   - Buscador unificado (redirige a marca actual o home)
   - Enlace a cada marca (Ebooks, YOYI'R, EstrategIA)
   - Carrito (siempre visible)
   - Perfil/Login

2. **Carrito**: Mismo independiente de marca
   - Muestra items de TODAS las marcas
   - Cálculo unificado

3. **Checkout**: Igual para todo
   - Acepta items de cualquier marca
   - Un solo pago

4. **Admin**: Gestiona todo
   - Selecciona marca al crear/editar
   - Ve estadísticas por marca

---

## Cambios Respecto a la Tienda Actual

**Antes (Monolítica):**
```
/products → Catálogo global
/product/<id> → Detalle
/cart, /checkout, /admin → Igual
```

**Ahora (Multi-marca):**
```
/ → Home narrativa (NUEVA)
/ebooks/*, /yoyir/*, /estrategia/* → Blueprints separados (NUEVA)
/cart, /checkout, /admin → Igual (compartidos)
```

La funcionalidad base es la misma, solo reorganizada visualmente y por marca.
