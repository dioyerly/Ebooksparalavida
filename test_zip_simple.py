"""
Script simple de verificación para soporte ZIP - sin dependencias externas.
Solo valida que los archivos tienen el código correcto.
"""
import os
import sys

def test_model_file():
    """Verifica que models.py tiene los campos ZIP."""
    print("\n1. Verificando models.py...")
    try:
        with open('backend/models.py', 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ('zip_file = db.Column' in content, "Campo zip_file"),
            ('file_name_zip = db.Column' in content, "Campo file_name_zip"),
            ('LargeBinary(length=(2 ** 32) - 1)' in content, "LONGBLOB para archivos grandes"),
        ]

        all_ok = True
        for check, desc in checks:
            if check:
                print(f"   [OK] {desc}")
            else:
                print(f"   [FAIL] {desc}")
                all_ok = False

        return all_ok
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_app_file():
    """Verifica que app.py tiene el soporte ZIP."""
    print("\n2. Verificando app.py...")
    try:
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ('def download_zip(token):' in content, "Funcion download_zip"),
            ('@app.get("/download/<token>/zip")' in content, "Decorador @app.get download_zip"),
            ('product_type == "downloadable_zip"' in content, "Validacion de tipo downloadable_zip"),
            ('if product_type == "downloadable_zip":' in content, "Manejo en admin_create_product"),
            ('application/zip' in content, "MIME type application/zip"),
            ('zip_file' in content, "Procesamiento de zip_file"),
            ('file_name_zip' in content, "Manejo de file_name_zip"),
            ('secure_filename' in content and '.zip' in content, "Validacion de extension .zip"),
        ]

        all_ok = True
        for check, desc in checks:
            if check:
                print(f"   [OK] {desc}")
            else:
                print(f"   [FAIL] {desc}")
                all_ok = False

        return all_ok
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_migration_file():
    """Verifica que el script de migracion existe."""
    print("\n3. Verificando migrate_db.py...")
    try:
        if not os.path.exists('migrate_db.py'):
            print(f"   [FAIL] Archivo no existe")
            return False

        with open('migrate_db.py', 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ('migrate_add_zip_support' in content, "Funcion migrate_add_zip_support"),
            ('zip_file' in content, "Migracion de zip_file"),
            ('file_name_zip' in content, "Migracion de file_name_zip"),
            ('LONGBLOB' in content or 'LargeBinary' in content, "Tipo de dato LONGBLOB"),
        ]

        all_ok = True
        for check, desc in checks:
            if check:
                print(f"   [OK] {desc}")
            else:
                print(f"   [FAIL] {desc}")
                all_ok = False

        return all_ok
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_documentation():
    """Verifica que existe la documentacion."""
    print("\n4. Verificando documentacion...")
    try:
        if not os.path.exists('ZIP_DOWNLOADABLE_PRODUCTS.md'):
            print(f"   [FAIL] Documentacion no existe")
            return False

        print(f"   [OK] ZIP_DOWNLOADABLE_PRODUCTS.md existe")

        with open('ZIP_DOWNLOADABLE_PRODUCTS.md', 'r', encoding='utf-8') as f:
            content = f.read()

        topics = [
            ('Instalacion' in content or 'instalacion' in content.lower(), "Seccion de instalacion"),
            ('downloadable_zip' in content, "Mencion de tipo downloadable_zip"),
            ('Endpoint' in content or 'endpoint' in content.lower(), "Documentacion de endpoints"),
            ('/download/<token>/zip' in content, "Ruta de descarga ZIP"),
        ]

        all_ok = True
        for check, desc in topics:
            if check:
                print(f"   [OK] {desc}")
            else:
                print(f"   [WARN] {desc}")

        return all_ok
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 70)
    print("PRUEBA DE IMPLEMENTACION - SOPORTE PARA PRODUCTOS DESCARGABLES ZIP")
    print("=" * 70)

    tests = [
        test_model_file,
        test_app_file,
        test_migration_file,
        test_documentation,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"   [ERROR] Exception: {e}")
            results.append(False)

    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} verificaciones exitosas")
    print("=" * 70)

    if passed == total:
        print("\nIMPLEMENTACION EXITOSA!")
        print("\nProximos pasos:")
        print("1. Ejecuta: python migrate_db.py")
        print("2. Reinicia el servidor Flask")
        print("3. Ve a /admin y crea un producto con tipo 'downloadable_zip'")
        return True
    else:
        print("\nHay problemas que revisar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
