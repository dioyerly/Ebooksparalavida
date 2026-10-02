# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Crear wheels para todas las dependencias (ignorar paquetes de Windows)
RUN pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels \
    -r requirements.txt 2>&1 | grep -v "pywin32\|pypiwin32" || true

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar wheels desde builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instalar wheels (ignorar paquetes de Windows que no se construyeron)
RUN pip install --no-cache /wheels/* 2>&1 | grep -v "pywin32\|pypiwin32" || true

# Copiar código de la aplicación
COPY . .

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Puerto donde corre Fly.io
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

# Comando para iniciar la app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
