# Actualizaciones del Schema de Base de Datos

## Resumen

La estructura de datos base permanece casi idéntica. Solo se agrega una columna `marca` a la tabla `products` para identificar a qué universo pertenece cada producto.

---

## Cambios Requeridos

### Tabla: `products` (EXISTENTE)

**Agregar columna:**

```sql
ALTER TABLE products ADD COLUMN marca VARCHAR(50) NOT NULL DEFAULT 'ebooks';
```

**Valores permitidos:**
- `'ebooks'` - Productos de Ebooks para la vida
- `'yoyir'` - Productos de YOYI'R (agendas/planners)
- `'estrategia'` - Productos de EstrategIA (herramientas)

**Ejemplo de registros después:**

```
id | nombre              | marca       | tipo  | precio | file_blob
1  | Guía TDAH          | ebooks      | pdf   | 15.99  | [blob]
2  | Agenda 2025        | yoyir       | zip   | 12.99  | [blob]
3  | Herramienta Datos  | estrategia  | html  | 29.99  | [blob]
```

---

### Tabla: `orders` (SIN CAMBIOS)

Permanece igual. Cada orden contiene items de potencialmente diferentes marcas.

```
id | user_id | total | status | created_at | payment_method
1  | 5       | 58.97 | paid   | 2026-10-02 | mercado_pago
```

---

### Tabla: `order_items` (SIN CAMBIOS)

Permanece igual. Cada item almacena el product_id (que ya tiene asociada su marca via FK).

```
id | order_id | product_id | quantity | price | tipo_entrega
1  | 1        | 1          | 1        | 15.99 | pdf_download
2  | 1        | 2          | 1        | 12.99 | zip_download
3  | 1        | 3          | 1        | 30.00 | html_access
```

---

### Tabla: `users` (SIN CAMBIOS)

Permanece igual.

```
id | email | password | created_at
```

---

### Tabla: `sessions` (SIN CAMBIOS)

Flask maneja sesiones en memoria o base de datos (según config). No se modifica.

```python
session['cart'] = [
  {'product_id': 1, 'quantity': 1, 'marca': 'ebooks'},
  {'product_id': 2, 'quantity': 1, 'marca': 'yoyir'},
]
```

---

## Migraciones (Alembic)

Si usas Alembic para migraciones:

**Archivo: `alembic/versions/001_add_marca_column.py`**

```python
# Pseudo-código
def upgrade():
    op.add_column('products', 
        sa.Column('marca', sa.String(50), nullable=False, server_default='ebooks')
    )

def downgrade():
    op.drop_column('products', 'marca')
```

---

## Cambios en Modelos (SQLAlchemy)

**Antes:**
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    file_blob = db.Column(db.LargeBinary)
```

**Después:**
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    marca = db.Column(db.String(50), nullable=False, default='ebooks')  # NUEVO
    file_blob = db.Column(db.LargeBinary)
```

---

## Queries Esperadas

### Obtener productos por marca

```python
# Obtener todos los ebooks
ebooks = Product.query.filter_by(marca='ebooks').all()

# Obtener todos los planners YOYI'R
yoyir = Product.query.filter_by(marca='yoyir').all()

# Obtener herramientas EstrategIA
estrategia = Product.query.filter_by(marca='estrategia').all()
```

### Crear producto con marca

```python
nuevo_producto = Product(
    name='Mi Agenda 2025',
    price=12.99,
    marca='yoyir',
    file_blob=archivo_zip
)
db.session.add(nuevo_producto)
db.session.commit()
```

### Obtener total de ventas por marca

```python
# Query para obtener ingresos por marca
from sqlalchemy import func

ventas_por_marca = db.session.query(
    Product.marca,
    func.sum(OrderItem.price * OrderItem.quantity).label('total')
).join(OrderItem).group_by(Product.marca).all()

# Resultado:
# [('ebooks', 500.50), ('yoyir', 300.00), ('estrategia', 150.00)]
```

---

## Notas Importantes

1. **Sin cambios estructurales mayores**: La relación entre `orders` y `products` se mantiene.
2. **Backward compatible**: Productos existentes pueden asignarse a `'ebooks'` por defecto.
3. **Carrito agnóstico**: `session['cart']` funciona igual, solo se agrega `marca` como metadato.
4. **Admin puede filtrar**: En el panel admin, se pueden listar productos por marca.

---

## Rollback (Si es necesario)

Si necesitas volver atrás:

```sql
ALTER TABLE products DROP COLUMN marca;
```

O en Alembic: `alembic downgrade -1`
