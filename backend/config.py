import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'ebooks_store.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ebooksparalavida.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5000")
    MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "")
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
    PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    ARS_PER_USD = float(os.getenv("ARS_PER_USD", "1450"))
    ARS_PER_EUR = float(os.getenv("ARS_PER_EUR", "1650"))
