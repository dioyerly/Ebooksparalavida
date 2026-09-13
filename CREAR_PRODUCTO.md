# 📚 Cómo Crear y Subir un Producto (Ebook)

## 🎯 Ubicación del Formulario

En el panel administrativo:
- **URL**: http://127.0.0.1:5000/admin
- **Tab**: "Crear Producto"

## 📝 Campos del Formulario

### 1. **Nombre del Ebook** (Requerido)
```
Ejemplo: "Mente en calma"
```
- El nombre que verán los clientes
- Aparece en la tienda y en órdenes

### 2. **Slug (URL)** (Requerido)
```
Ejemplo: "mente-en-calma"
```
- Usado en la URL del producto: `/producto/mente-en-calma`
- Solo letras, números y guiones
- Debe ser único (no puede repetirse)

### 3. **Categoría** (Requerido)
```
Ejemplos:
- VIDA & BIENESTAR
- TRABAJO & CARRERA
- APRENDER & DOMINAR
- FINANZAS & DINERO
```
- Aparece en los filtros de la tienda
- Agrupa productos relacionados

### 4. **Precio (ARS)** (Requerido)
```
Ejemplo: 6999
```
- En pesos argentinos
- Solo números, sin símbolos
- El panel muestra automáticamente conversión a USD/EUR

### 5. **Color de Portada** (Requerido)
```
Opciones:
- 🎨 Coral (rojo/rosa)
- 🎨 Teal (azul-verde)
- 🎨 Amarillo (sun)
- 🎨 Verde suave (lavender)
```
- Usado si NO subes imagen de portada
- El sistema genera un diseño bonito con este color

### 6. **Mostrar en Portada** (Opcional)
```
☑️ Sí / ☐ No
```
- Marca esto para mostrar el producto destacado en la home
- Máximo recomendado: 4-6 productos destacados

### 7. **Descripción** (Requerido)
```
Ejemplo:
"Herramientas amables para entender tu TDAH, bajar el ruido 
y recuperar foco. A diferencia de los métodos convencionales 
basados en disciplina rígida, este libro propone un cambio de 
paradigma: no esforzarte más, sino hacer que tu casa te pida menos."
```
- Texto largo con todos los detalles del ebook
- Aparece en la página del producto
- Puede tener múltiples párrafos
- **Consejo**: Explica beneficios, no solo características

### 8. **📥 Archivo PDF del Ebook** (Requerido)
```
Formatos aceptados: .pdf
Ejemplo de archivo: "mente-en-calma.pdf"
```
**¿Dónde se guarda?**
- Ubicación: `storage/ebooks/mente-en-calma.pdf`
- Solo accesible mediante descarga con token único
- No se expone como archivo público (seguro)

**Tamaño recomendado:**
- Máximo: No hay límite especificado, pero recomendado <50MB
- La mayoría de ebooks están entre 2-20MB

### 9. **🖼️ Imagen de Portada** (Opcional)
```
Formatos aceptados: .jpg, .jpeg, .png, .gif
Ejemplo: "mente-en-calma.jpg"
```
**¿Dónde se guarda?**
- Ubicación: `frontend/assets/images/mente-en-calma.jpg`
- Se accede desde la web públicamente
- Aparece en tarjetas de producto y detalle

**Recomendaciones:**
- Tamaño: 400x600px (vertical)
- Peso: <500KB (para carga rápida)
- Formato: JPG (mejor compresión) o PNG

**Si NO subes imagen:**
- El sistema genera automáticamente una portada con:
  - El color que elegiste (Coral, Teal, etc.)
  - Nombre del ebook
  - Categoría
  - Logo de Ebooks para la vida

---

## 🚀 Ejemplo Paso a Paso

### 1. Organiza tus archivos
```
📁 En tu computadora:
├── mente-en-calma.pdf          (tu ebook)
└── mente-en-calma.jpg          (portada bonita)
```

### 2. Ve a Admin → Crear Producto
```
http://127.0.0.1:5000/admin
[Click en tab "Crear Producto"]
```

### 3. Completa el formulario
```
Nombre:           "Mente en calma"
Slug:             "mente-en-calma"
Categoría:        "VIDA & BIENESTAR"
Precio:           6999
Color:            Coral
Mostrar:          ☑️ Sí
Descripción:      [Texto completo...]
PDF:              [Buscar archivo PDF]
Portada:          [Buscar imagen JPG]
```

### 4. Click en "Crear Producto →"

### 5. ✅ Listo!
- El producto aparece inmediatamente en la tienda
- Los clientes pueden verlo
- Empieza a registrarse clics y visitas en el panel

---

## 📊 Qué Sucede Después de Crear

### En la Base de Datos
Se guarda:
```
- Nombre, slug, categoría, precio
- Descripción completa
- Archivo PDF: storage/ebooks/mente-en-calma.pdf
- Imagen: frontend/assets/images/mente-en-calma.jpg
- Color de portada (si no hay imagen)
```

### En la Tienda
El producto aparece:
- ✅ En /tienda (vista de catálogo)
- ✅ En /producto/mente-en-calma (página de detalle)
- ✅ En /home (si marcaste "Mostrar en portada")
- ✅ En búsqueda/filtros

### En el Panel Admin
Puedes ver:
- 📈 Cuántas veces fue clicleado
- 📦 Cuántas veces fue vendido
- 💹 Tasa de conversión (clics → ventas)

---

## ⚠️ Errores Comunes y Soluciones

### ❌ Error: "Slug ya existe"
**Causa:** Ya existe un producto con ese slug
**Solución:** Cambia el slug a algo único
```
"mente-en-calma" → "mente-en-calma-v2"
```

### ❌ Error: "Archivo debe ser PDF"
**Causa:** Subiste un archivo .doc, .zip, etc.
**Solución:** Convierte a PDF primero
```
Word → Guardar como PDF
```

### ❌ Error: "Slug solo puede tener letras y guiones"
**Causa:** Usaste espacios, mayúsculas o caracteres especiales
**Solución:** Formatea correctamente
```
"Mente En Calma"    → "mente-en-calma"
"mente_en_calma"    → "mente-en-calma"
"mente en calma 2"  → "mente-en-calma-2"
```

### ❌ Error: "El campo es requerido"
**Causa:** Dejaste algún campo vacío
**Solución:** Completa todos los campos marcados con (Requerido)

---

## 🎨 Consejos para Mejores Resultados

### Descripción que Vende
❌ Malo:
```
"Este es un ebook sobre TDAH"
```

✅ Bueno:
```
"Herramientas amables para entender tu TDAH, bajar el ruido 
y recuperar foco. A diferencia de los métodos convencionales 
basados en disciplina rígida, este libro propone un cambio de 
paradigma: no esforzarte más, sino hacer que tu casa te pida menos.

✓ Descarga inmediata
✓ Lectura desde cualquier dispositivo
✓ +200 páginas de contenido práctico"
```

### Imagen de Portada
- **Usa portadas profesionales** (Canva, Photoshop, diseñador)
- **Asegúrate de que sea vertical** (más alta que ancha)
- **Incluye título principal y subtítulo**
- **Usa colores atractivos y legibles**

### Precio
- **Investigar precios similares** en el mercado
- **Considerar valor percibido** del contenido
- **Promociones**: Puedes bajar precio temporalmente
- **Bundles/Kits**: Combina productos a mayor precio

### Categoría
- **Elige bien la categoría** (afecta filtros)
- **Clientes buscan por categoría** antes de por producto
- **Sé específico**: "VIDA & BIENESTAR" es mejor que "Otros"

---

## 💾 Almacenamiento de Archivos

### PDFs (Ebooks)
```
📁 storage/ebooks/
├── mente-en-calma.pdf
├── casa-en-flujo.pdf
├── semana-liviana.pdf
└── ...
```
- **Privado**: No accesible directo desde URL
- **Seguro**: Descarga mediante token único por cliente
- **Backup recomendado**: Copia los archivos regularmente

### Imágenes (Portadas)
```
📁 frontend/assets/images/
├── mente-en-calma.jpg
├── casa-en-flujo.jpg
├── semana-liviana.jpg
└── ...
```
- **Público**: Visible en la web
- **Optimizado**: Cargue rápido
- **Backup recomendado**: Copia los archivos regularmente

---

## 🔄 Actualizar un Producto Existente

Por ahora, si necesitas cambiar:
- Nombre, descripción, precio, categoría
- → Necesitas soporte técnico (editar en base de datos)

Sugerencia futura:
- Agregar sección "Editar Producto" en admin
- Permitir cambiar imagen y descripción

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo subir varios formatos (EPUB, MOBI)?**
A: Por ahora solo PDF. Futura mejora: permitir múltiples formatos.

**P: ¿Se puede editar un producto después de crearlo?**
A: Nombre, precio, etc. requieren edición manual. Futura mejora: formulario de edición.

**P: ¿Cuántos productos puedo crear?**
A: Ilimitados. Solo depende del espacio en disco.

**P: ¿Dónde veo las descargas de mis ebooks?**
A: En admin → Órdenes. Cada cliente tiene un token único.

**P: ¿Se puede eliminar un producto?**
A: Por ahora no desde el panel. Contacta soporte para eliminar.

---

**Última actualización:** 2026-09-13
**Versión:** 1.0 - Upload de archivos incluido
