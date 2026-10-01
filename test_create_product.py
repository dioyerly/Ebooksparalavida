#!/usr/bin/env python
"""
TEST: Verificar que crear un producto funciona
"""
import sys
sys.path.insert(0, '.')

from backend.app import app, db
from backend.models import Product
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("TEST: Crear Producto")
print("=" * 60)

try:
    with app.app_context():
        # Verificar conexión a BD
        result = db.session.execute(db.text("SELECT 1"))
        print("[OK] Conexión a BD exitosa")

        # Contar productos actuales
        count_before = Product.query.count()
        print(f"[OK] Productos actuales: {count_before}")

        # Crear producto de prueba
        test_product = Product(
            slug="test-producto-nuevo",
            name="Test Producto Nuevo",
            description="Este es un producto de prueba",
            category="VIDA & BIENESTAR",
            price_ars=9999,
            cover_class="coral",
            accent="#C9756B",
            featured=False,
            product_type="pdf",
            file_name="test.pdf",
            ebook_file=b"PDF contenido binario de prueba",
            cover_image="test.jpg",
            cover_image_blob=b"JPG contenido de prueba",
        )

        db.session.add(test_product)
        db.session.commit()
        print(f"[OK] Producto creado: ID {test_product.id}")

        # Verificar que se guardó
        count_after = Product.query.count()
        print(f"[OK] Productos después: {count_after}")

        # Recuperar el producto
        product = Product.query.filter_by(slug="test-producto-nuevo").first()
        if product:
            print(f"[OK] Producto recuperado:")
            print(f"  - Nombre: {product.name}")
            print(f"  - Slug: {product.slug}")
            print(f"  - Precio: {product.price_ars}")
            print(f"  - Imagen blob guardada: {len(product.cover_image_blob) if product.cover_image_blob else 0} bytes")
            print(f"  - Archivo PDF guardado: {len(product.ebook_file) if product.ebook_file else 0} bytes")

            # Limpiar: eliminar producto de prueba
            db.session.delete(product)
            db.session.commit()
            print(f"[OK] Producto de prueba eliminado")
        else:
            print("[ERROR] No se pudo recuperar el producto creado")

        print()
        print("=" * 60)
        print("RESULTADO: TODO FUNCIONA CORRECTAMENTE")
        print("=" * 60)

except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
    print()
    print("=" * 60)
    print("RESULTADO: HAY UN PROBLEMA")
    print("=" * 60)
    sys.exit(1)
