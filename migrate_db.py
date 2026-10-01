"""
Migración para agregar soporte de archivos ZIP descargables.
Agrega las columnas zip_file y file_name_zip a la tabla product.
"""
import os
from sqlalchemy import inspect, text
from backend.config import Config
from flask import Flask
from backend.models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def migrate_add_zip_support():
    """Add ZIP file support columns to product table if they don't exist."""
    with app.app_context():
        inspector = inspect(db.engine)

        # Get existing columns in product table
        existing_columns = {col['name'] for col in inspector.get_columns('product')}

        # Add zip_file if missing
        if 'zip_file' not in existing_columns:
            print("Agregando columna 'zip_file'...")
            db.engine.execute(text(
                "ALTER TABLE product ADD COLUMN zip_file LONGBLOB"
            ))
            print("✅ Columna 'zip_file' agregada")

        # Add file_name_zip if missing
        if 'file_name_zip' not in existing_columns:
            print("Agregando columna 'file_name_zip'...")
            db.engine.execute(text(
                "ALTER TABLE product ADD COLUMN file_name_zip VARCHAR(255)"
            ))
            print("✅ Columna 'file_name_zip' agregada")

        print("✅ Migración completada exitosamente")

if __name__ == "__main__":
    try:
        migrate_add_zip_support()
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
