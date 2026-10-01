# Productos Descargables ZIP - Guía Completa

## Resumen

Ahora puedes crear productos descargables en formato ZIP (agendas, planners, kits de recursos, etc.) directamente desde el panel administrativo. Los clientes podrán descargar el archivo ZIP de forma segura después de una compra válida.

## Tipos de Producto Disponibles

| Tipo | Descripción | Cómo se descarga |
|------|-------------|-----------------|
| `pdf` | Ebook en PDF y/o EPUB | Página de selección (PDF o EPUB) |
| `html_interactive` | Ebook interactivo HTML protegido | Acceso directo con código de acceso |
| `downloadable_zip` | Archivo ZIP descargable | Descarga directa del ZIP |

## Instalación de la Nueva Funcionalidad

### 1. Actualizar la Base de Datos

Si ya tienes datos existentes, ejecuta el script de migración para agregar las nuevas columnas:

```bash
python migrate_db.py
```

**Nota:** Si es una instalación nueva, ejecuta:
```bash
python init_db.py
```

### 2. Reiniciar la Aplicación

Después de la migración, reinicia el servidor Flask:
```bash
python -m flask run
```

## Crear un Producto ZIP en el Admin

### Paso 1: Acceder al Panel Administrativo
```
http://127.0.0.1:5000/admin
Email: admin@ebooksparalavida.com
Contraseña: admin123
```

### Paso 2: Ir a "Crear Producto"

En el formulario de creación de producto:

```
Nombre:        [Mi Agenda 2025                     ]
Slug:          [agenda-2025                       ]
Categoría:     [VIDA & BIENESTAR        ▼]
Precio ARS:    [5900                              ]
Tipo Producto: [downloadable_zip         ▼]
              (Seleccionar tipo ZIP)
```

### Paso 3: Subir el Archivo ZIP

Cuando seleccionas "downloadable_zip" como tipo, aparecerá un campo para subir archivo:

```
Archivo ZIP:   [Seleccionar archivo...] 
              (Solo aceptamos .zip - máx 512 MB)
```

Sube tu archivo ZIP. El sistema:
- Valida que sea un archivo .zip
- Lo guarda de forma segura en la base de datos como BLOB
- Lo renombra como `{slug}.zip` para seguridad

### Paso 4: Imagen de Portada (Opcional)

Sube una imagen de portada como de costumbre:
```
Imagen:        [Seleccionar imagen...]
```

### Paso 5: Crear

Haz clic en "Crear Producto" y listo.

## Flujo de Compra del Cliente

1. Cliente ve el producto en la tienda
2. Agrega al carrito
3. Va a checkout y paga (Mercado Pago o PayPal)
4. Recibe email con enlace de descarga: `/download/{token}`
5. Al hacer clic, se descarga el ZIP automáticamente

## Editar un Producto ZIP Existente

### Desde el Admin

1. Ir a "Mis Productos"
2. Buscar el producto ZIP
3. Hacer clic en "Editar"
4. Cambiar el archivo ZIP en el campo correspondiente
5. Guardar cambios

El nuevo archivo reemplaza al anterior. Los clientes que ya compraron acceden con el archivo actualizado en próximas descargas.

## Endpoints Implementados

### Para Clientes

```
GET /download/<token>
  → Si es ZIP: redirige a /download/<token>/zip
  → Si es PDF/EPUB: muestra página de selección

GET /download/<token>/zip
  → Descarga el archivo ZIP
  → Requiere: token válido, orden pagada, producto ZIP
  → Rate limit: 30 descargas por minuto
  → Content-Type: application/zip
  → Content-Disposition: attachment
```

### Para Admin

```
GET /admin/products/<id>/edit
  → Ahora devuelve "has_zip": true/false

POST /admin/products/<id>/edit
  → Aceptar uploads de "zip_file"
  → Validar extensión .zip
  → Almacenar en product.zip_file (LONGBLOB)

POST /admin/products
  → Soportar "product_type": "downloadable_zip"
  → Procesar archivo ZIP en creación
```

## Seguridad

### Protecciones Implementadas

1. **Validación de Extensión:** Solo archivos .zip
2. **Validación de Token:** Token debe ser válido y estar asociado a orden pagada
3. **Almacenamiento Seguro:** Archivo guardado como BLOB en base de datos
4. **Rate Limiting:** 30 descargas por minuto máximo
5. **Sin Ejecución:** El ZIP nunca se descomprime en el servidor
6. **Nombre Seguro:** Renombrado automáticamente a `{slug}.zip`

### Lo que NO hacemos

- ❌ No descomprimimos ni ejecutamos archivos ZIP
- ❌ No validamos contenido dentro del ZIP
- ❌ No permitimos acceso sin pago válido
- ❌ No compartimos el archivo con usuarios no autorizados

## Consideraciones Técnicas

### Tamaño de Archivos

Los archivos ZIP se almacenan como LONGBLOB (máximo 4 GB teóricamente, pero recomendamos máximo 512 MB).

Si necesitas aumentar el límite en tu servidor, ajusta en Flask:
```python
MAX_CONTENT_LENGTH = 512 * 1024 * 1024  # 512 MB
```

### Base de Datos

Las nuevas columnas agregadas:
```sql
ALTER TABLE product ADD COLUMN zip_file LONGBLOB;
ALTER TABLE product ADD COLUMN file_name_zip VARCHAR(255);
```

### Email

Cuando un cliente compra un producto ZIP:
1. Recibe email con asunto: "¡Tu compra está lista!"
2. El enlace de descarga es: `/download/{token}`
3. Al hacer clic, se descarga el ZIP automáticamente (no muestra página intermedia)

## Ejemplos de Uso

### Ejemplo 1: Agenda Descargable
```
Nombre: Agenda 2025 - Modelo Mensual
Slug: agenda-2025-mensual
Tipo: downloadable_zip
Archivo: agenda-2025.zip (contiene PDFs mensuales)
Precio: 4900 ARS
```

### Ejemplo 2: Kit de Recursos
```
Nombre: Kit Productividad Completo
Slug: kit-productividad
Tipo: downloadable_zip
Archivo: kit-productividad.zip (contiene worksheets, checklists, plantillas)
Precio: 8900 ARS
```

### Ejemplo 3: Templates y Planillas
```
Nombre: 50 Templates HTML para tu blog
Slug: templates-html-blog
Tipo: downloadable_zip
Archivo: templates.zip (HTML, CSS, imágenes)
Precio: 7900 ARS
```

## Troubleshooting

### "Debes subir el archivo ZIP descargable"
El campo de archivo está vacío. Verifica que hayas seleccionado un archivo .zip.

### "El archivo debe ser .zip para un producto descargable"
Solo se aceptan archivos con extensión .zip. Renombra tu archivo si es necesario.

### "Esta descarga no está disponible para esta orden"
El cliente está intentando descargar sin haber pagado. Verifica que el estado de la orden sea "paid" o "paid_demo".

### El cliente descarga un archivo vacío o corrupto
Verifica:
1. El ZIP se subió correctamente (revisá el tamaño en la BD)
2. El archivo ZIP original no está corrupto
3. Prueba re-subir un nuevo ZIP

## Diferencias con PDF/EPUB

| Aspecto | ZIP | PDF/EPUB |
|--------|-----|---------|
| Descarga | Directa | Selecciona formato |
| Interactividad | No | No (excepto HTML) |
| Múltiples formatos | Solo .zip | PDF + EPUB |
| Protección de dispositivo | No | No |
| Personalización | No | Sí (para HTML) |

## Preguntas Frecuentes

**¿Puedo tener PDF, EPUB y ZIP en el mismo producto?**
No, cada producto tiene un tipo específico. Si necesitas múltiples formatos, crea productos separados o bundlea todo en un ZIP.

**¿El cliente puede descargar múltiples veces?**
Sí, con el mismo token puede descargar cuantas veces quiera (limitado a 30 por minuto).

**¿Qué pasa si actualizo el ZIP después de que el cliente compró?**
En futuras descargas obtendrá el ZIP actualizado. Si necesitas mantener el original, crea una versión nueva del producto.

**¿Puedo comprimir el ZIP más?**
No desde la app, pero tu archivo ZIP debe estar optimizado antes de subirlo. Usa herramientas como 7-Zip o WinRAR.

**¿Funciona en dispositivos móviles?**
Sí, el navegador manejará la descarga normalmente (según la configuración del dispositivo).
