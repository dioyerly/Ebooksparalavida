import os
if os.path.exists("ebooks_store.db"):
    os.remove("ebooks_store.db")
    print("🗑️ BD vieja eliminada")

from backend.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

try:
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        print("✅ Base de datos lista para usar")
except Exception as e:
    print(f"❌ Error: {e}")
