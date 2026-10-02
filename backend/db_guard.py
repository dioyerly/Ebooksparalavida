"""
DB Guard: Protección contra cambios de base de datos
Asegura que SOLO se use Hostinger u748338755_ebooks_store_
"""
import os
from urllib.parse import urlparse

HOSTINGER_DB = "u748338755_ebooks_store_"
HOSTINGER_HOST = "srv801.hstgr.io"
HOSTINGER_USER = "u748338755_ebooksadmin"

def validate_database_config():
    """
    Valida que DATABASE_URL apunte SOLO a Hostinger (producción).
    En desarrollo (FLASK_ENV != production) permite SQLite.
    """
    db_url = os.getenv("DATABASE_URL")
    flask_env = os.getenv("FLASK_ENV", "development")

    # En desarrollo: permite SQLite
    if flask_env != "production":
        if not db_url or db_url.startswith("sqlite"):
            print("[OK] BD Guard: Modo desarrollo - SQLite permitido")
            return True

    if not db_url:
        raise ValueError(
            "ERROR CRÍTICO: DATABASE_URL no configurada.\n"
            "Debes configurar DATABASE_URL en tu .env o Render env vars.\n"
            "DEBE ser: mysql+pymysql://u748338755_ebooksadmin:Chiara0712.@srv801.hstgr.io:3306/u748338755_ebooks_store_"
        )

    # Parsing URL
    try:
        parsed = urlparse(db_url)
    except:
        raise ValueError(f"ERROR: DATABASE_URL inválida: {db_url}")

    # Verificar que es MySQL (en producción)
    if not parsed.scheme.startswith("mysql"):
        raise ValueError(
            f"ERROR CRÍTICO: BD no es MySQL.\n"
            f"Encontrado: {parsed.scheme}\n"
            f"DEBE ser mysql+pymysql\n"
            f"URL: {db_url}"
        )
    
    # Verificar host
    if HOSTINGER_HOST not in parsed.hostname or not parsed.hostname:
        raise ValueError(
            f"ERROR CRÍTICO: HOST incorrecto.\n"
            f"Encontrado: {parsed.hostname}\n"
            f"DEBE ser: {HOSTINGER_HOST}\n"
            f"URL: {db_url}"
        )
    
    # Verificar BD
    db_name = parsed.path.lstrip("/")
    if db_name != HOSTINGER_DB:
        raise ValueError(
            f"ERROR CRÍTICO: Base de datos incorrecta.\n"
            f"Encontrada: {db_name}\n"
            f"DEBE ser: {HOSTINGER_DB}\n"
            f"URL: {db_url}"
        )
    
    # Verificar usuario
    if parsed.username != HOSTINGER_USER:
        raise ValueError(
            f"ERROR CRÍTICO: Usuario incorrecto.\n"
            f"Encontrado: {parsed.username}\n"
            f"DEBE ser: {HOSTINGER_USER}\n"
            f"URL: {db_url}"
        )
    
    print("[OK] BD Guard: Configuracion validada - Usando Hostinger u748338755_ebooks_store_")
    return True
