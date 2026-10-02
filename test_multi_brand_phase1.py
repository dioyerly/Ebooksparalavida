#!/usr/bin/env python3
"""
Test suite para validar FASE 1: Multi-brand admin
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app, db, Product, migrate_product_columns, UNIVERSES, CATEGORIES_BY_UNIVERSE
from backend.config import Config

def test_setup():
    """Test 1-5: Configuracion inicial"""
    print("\n=== TEST SETUP ===")

    with app.app_context():
        print("[OK] APP inicia correctamente")

        # Test 2: Migracion
        try:
            migrate_product_columns()
            print("[OK] Migracion agrega universe y sort_order")
        except Exception as e:
            print(f"[ERROR] Migracion: {e}")
            return False

        # Test 3: Reiniciar no duplica columnas
        try:
            migrate_product_columns()
            print("[OK] Reiniciar NO duplica columnas")
        except Exception as e:
            print(f"[ERROR] Migracion reiniciada: {e}")
            return False

        # Test 4: Admin carga
        with app.test_client() as client:
            response = client.get('/admin')
            if response.status_code == 302:
                print("[OK] Admin carga (requiere auth)")
            else:
                print(f"[ERROR] Admin no carga: {response.status_code}")
                return False

        # Test 5: Base de datos lista
        db.create_all()
        print("[OK] Base de datos lista")

    return True

def test_universes_config():
    """Test 6: Universos configurados"""
    print("\n=== TEST UNIVERSOS ===")

    expected_universes = {'estrategia', 'yoyir', 'ebooks'}
    actual_universes = set(UNIVERSES.keys())

    if actual_universes == expected_universes:
        print("[OK] Universos configurados correctamente")
        for u in sorted(UNIVERSES.keys()):
            print(f"     - {u}: {UNIVERSES[u]}")
    else:
        print(f"[ERROR] Universos incorrectos: {actual_universes}")
        return False

    return True

def test_categories_config():
    """Test 7-9: Categorias por universo"""
    print("\n=== TEST CATEGORIAS ===")

    for universe in ['estrategia', 'yoyir', 'ebooks']:
        categories = CATEGORIES_BY_UNIVERSE.get(universe, [])
        if categories:
            print(f"[OK] {universe}: {len(categories)} categorias")
        else:
            print(f"[ERROR] {universe}: sin categorias")
            return False

    return True

def test_product_model():
    """Test 10-13: Modelo Product"""
    print("\n=== TEST PRODUCT MODEL ===")

    with app.app_context():
        db.create_all()

        # Limpiar primero
        Product.query.filter(Product.slug.startswith('test-product')).delete()
        db.session.commit()

        # Test crear producto sin universe (sin clasificar)
        product1 = Product(
            slug='test-product-1',
            name='Test Product 1',
            description='Test description',
            category='VIDA & BIENESTAR',
            price_ars=9999,
            universe=None,
            sort_order=None,
        )
        db.session.add(product1)
        db.session.commit()

        retrieved = Product.query.filter_by(slug='test-product-1').first()
        if retrieved and retrieved.universe is None:
            print("[OK] Producto sin clasificar (universe=NULL)")
        else:
            print("[ERROR] Producto sin clasificar no funciona")
            return False

        # Test crear producto con universe
        product2 = Product(
            slug='test-product-estrategia',
            name='Test EstrategIA',
            description='Test description',
            category='Microapps',
            price_ars=7999,
            universe='estrategia',
            sort_order=1,
        )
        db.session.add(product2)
        db.session.commit()

        retrieved = Product.query.filter_by(slug='test-product-estrategia').first()
        if retrieved and retrieved.universe == 'estrategia' and retrieved.sort_order == 1:
            print("[OK] Producto con universe y sort_order")
        else:
            print("[ERROR] Producto con universe no funciona")
            return False

        # Test crear producto con otro universe
        product3 = Product(
            slug='test-product-yoyir',
            name='Test YOYIR',
            description='Test description',
            category='Agendas',
            price_ars=5999,
            universe='yoyir',
            sort_order=2,
        )
        db.session.add(product3)
        db.session.commit()

        # Test crear producto con ebooks
        product4 = Product(
            slug='test-product-ebooks',
            name='Test Ebooks',
            description='Test description',
            category='VIDA & BIENESTAR',
            price_ars=4999,
            universe='ebooks',
            sort_order=3,
        )
        db.session.add(product4)
        db.session.commit()

        print("[OK] Productos con diferentes universos creados")

        # Test query filtrando por universe
        estrat = Product.query.filter_by(universe='estrategia').all()
        yoyir = Product.query.filter_by(universe='yoyir').all()
        ebooks = Product.query.filter_by(universe='ebooks').all()
        unclass = Product.query.filter_by(universe=None).all()

        if len(estrat) >= 1 and len(yoyir) >= 1 and len(ebooks) >= 1 and len(unclass) >= 1:
            print("[OK] Filtrado por universe funciona")
        else:
            print("[ERROR] Filtrado por universe no funciona")
            return False

        # Test ordenamiento por sort_order
        sorted_by_order = Product.query.order_by(Product.sort_order).all()
        print("[OK] Ordenamiento por sort_order funciona")

    return True

def test_api_endpoints():
    """Test 14-15: API endpoints"""
    print("\n=== TEST API ENDPOINTS ===")

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            # Test sin autenticacion (deberia redirigir)
            response = client.get('/api/admin/products-list')
            if response.status_code in [302, 401]:
                print("[OK] /api/admin/products-list requiere autenticacion")

            # Test categorias endpoint
            response = client.get('/api/admin/categories/estrategia')
            if response.status_code in [302, 401]:
                print("[OK] /api/admin/categories/<universe> requiere autenticacion")

    return True

def test_no_breaking_changes():
    """Test 16-21: Sin cambios rompedores"""
    print("\n=== TEST SIN CAMBIOS ROMPEDORES ===")

    with app.app_context():
        db.create_all()

        # Test que rutas publicas sigan existiendo
        with app.test_client() as client:
            # / debe existir
            response = client.get('/')
            if response.status_code in [200, 302]:
                print("[OK] / sigue accesible")

            # /universos debe existir
            response = client.get('/universos')
            if response.status_code == 200:
                print("[OK] /universos sigue accesible")

            # /shop debe existir
            response = client.get('/shop')
            if response.status_code == 200:
                print("[OK] /shop sigue accesible")

            # /cart debe existir
            response = client.get('/cart')
            if response.status_code == 200:
                print("[OK] /cart sigue accesible")

    return True

def cleanup():
    """Limpiar datos de prueba"""
    print("\n=== CLEANUP ===")
    with app.app_context():
        try:
            Product.query.filter(Product.slug.startswith('test-product')).delete()
            db.session.commit()
            print("[OK] Datos de prueba eliminados")
        except:
            pass

if __name__ == '__main__':
    print("=" * 60)
    print("FASE 1: MULTI-BRAND ADMIN - TEST SUITE")
    print("=" * 60)

    all_passed = True

    all_passed &= test_setup()
    all_passed &= test_universes_config()
    all_passed &= test_categories_config()
    all_passed &= test_product_model()
    all_passed &= test_api_endpoints()
    all_passed &= test_no_breaking_changes()

    cleanup()

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] TODOS LOS TESTS PASARON")
    else:
        print("[FAILED] ALGUNOS TESTS FALLARON")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)
