# Panel Administrativo - Guía Completa

## Acceso al Panel

```
URL: http://127.0.0.1:5000/admin
Email: admin@ebooksparalavida.com
Contraseña: admin123 (cambiar en .env)
```

## Secciones Disponibles

### 1. **Resumen (Overview)**
Vista principal con gráficos y ranking en tiempo real:

- **Gráfico de Ingresos**: Visualiza tendencias de ventas últimas 4 semanas
- **Top 5 Productos Más Vendidos**: Cuáles ebooks tienen más ingresos
- **Top 5 Productos Más Clicleados**: Cuáles atraen más atención
- **Últimas 10 Órdenes**: Actividad reciente de compras

**Datos Mostrados:**
- Ingresos acumulados y últimos 30 días
- Total de órdenes pagadas
- Cantidad de clientes únicos
- Total de productos en catálogo
- Total de clics registrados
- Visitantes únicos

### 2. **Órdenes**
Tabla completa de todas las órdenes realizadas:

| Campo | Significado |
|-------|------------|
| ID | Número de orden |
| Cliente | Nombre del comprador |
| Email | Email registrado |
| Monto | Precio total en ARS |
| Método | Mercado Pago, PayPal, demo |
| Estado | `paid`, `paid_demo`, `pending` |
| Fecha | Cuándo se realizó la compra |

### 3. **Análisis de Productos**
Tabla comparativa de performance de cada ebook:

| Métrica | Significado |
|---------|------------|
| Producto | Nombre del ebook |
| Categoría | Clasificación |
| Precio | Precio en ARS |
| Clics | Cuántas personas abrieron el producto |
| Ventas | Cuántas compras generó |
| Tasa de Conversión | % de clics que resultaron en compra |

**Interpretación:**
- Alta tasa de conversión (>30%): Producto bien presentado
- Baja tasa de conversión (<10%): Revisar descripción o precio
- Muchos clics, pocas ventas: Producto atrae pero no convence

### 4. **Clientes**
Lista de todos los compradores ordenados por gasto total:

| Campo | Significado |
|-------|------------|
| Nombre | Nombre del cliente |
| Email | Email registrado |
| Órdenes | Cantidad de compras realizadas |
| Total Gastado | Ingresos totales por cliente |
| Última Compra | Fecha de última transacción |

**Casos de Uso:**
- Identificar clientes VIP (alto gasto)
- Clientes recurrentes (múltiples órdenes)
- Contacto para descuentos o nuevos lanzamientos

### 5. **Crear Producto**
Formulario para agregar nuevos ebooks al catálogo:

```
Nombre: "Mente en calma"
Slug: "mente-en-calma"  # Usado en URL: /producto/mente-en-calma
Categoría: "VIDA & BIENESTAR"
Precio: 8900
Color: Coral, Teal, Amarillo, Verde suave
Mostrar en portada: ✓
Descripción: [texto completo del ebook]
```

## Tracking de Datos

El sistema registra automáticamente:

### Visitas a Página
Cada vez que alguien entra a la web se registra:
- Página visitada (home, /producto/x, /tienda, etc.)
- Fecha y hora
- Session ID único del navegador
- User-Agent (dispositivo/navegador)
- Referrer (de dónde vino)

### Clics en Producto
Cada clic en un producto o tarjeta registra:
- Producto clicleado (ID y nombre)
- Fecha y hora
- Session ID del navegador
- Referrer

**Nota:** El session_id es anónimo y generado por navegador, nunca se asocia con email/identificación personal.

## Métricas Clave Explicadas

### Conversión de Clics a Ventas
```
Tasa Conversión = (Número de Ventas / Número de Clics) × 100
```

**Ejemplos:**
- 100 clics, 10 ventas = 10% de conversión (normal)
- 100 clics, 30 ventas = 30% de conversión (excelente)
- 100 clics, 2 ventas = 2% de conversión (revisar descripción)

### Ingresos Acumulados vs Últimos 30 días
- **Acumulados**: Desde que existe la tienda
- **Últimos 30 días**: Tendencia reciente (más importante para analizar)

### Visitantes Únicos
- Basado en session_id único por navegador
- Permite ver cuántas personas diferentes visitaron
- Diferente a "visitas totales" (una persona puede visitarmúltiples veces)

## Tips para Usar el Panel

1. **Revisar Semanalmente:**
   - Vende bien la tienda? ¿Hay tendencias?
   - ¿Qué productos atraen pero no convierten?

2. **Optimización de Productos:**
   - Si un producto tiene muchos clics pero pocas ventas: mejorar descripción o fotos
   - Si tiene pocas visitas: necesita más promoción

3. **Gestión de Clientes:**
   - Ver clientes recurrentes (buena señal de satisfacción)
   - Contactar a clientes VIP para feedback o nuevos lanzamientos

4. **Planificación:**
   - Usar ingresos por día para ver patrones
   - Lanzar nuevos productos cuando hay actividad alta

## Base de Datos

### Nuevas Tablas Agregadas

```sql
-- Registra cada clic en un producto
CREATE TABLE product_click (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL,
  product_name VARCHAR(160),
  clicked_at DATETIME,
  user_session_id VARCHAR(120),
  referrer VARCHAR(255)
);

-- Registra cada visita a una página
CREATE TABLE page_visit (
  id INTEGER PRIMARY KEY,
  page_path VARCHAR(255),
  visited_at DATETIME,
  user_session_id VARCHAR(120),
  user_agent VARCHAR(500),
  referrer VARCHAR(255)
);
```

## API Endpoints (para desarrollo)

```
GET /api/admin/stats
  → Estadísticas principales y gráficos

GET /api/admin/orders
  → Lista completa de órdenes

GET /api/admin/products-analytics
  → Análisis de clics vs ventas por producto

POST /api/track-click
  → Registra clic (se llama automáticamente desde frontend)

POST /api/track-visit
  → Registra visita de página (se llama automáticamente)
```

## Próximas Mejoras Sugeridas

- [ ] Exportar datos a CSV
- [ ] Email con resumen semanal
- [ ] Predicción de ventas
- [ ] A/B testing de descripciones
- [ ] Seguimiento de afiliados
- [ ] Cupones y descuentos

---

**Última actualización:** 2026-09-13
