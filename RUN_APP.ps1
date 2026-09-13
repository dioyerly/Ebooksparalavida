# Script para ejecutar Ebooksparalavida en Windows

Write-Host "🚀 Iniciando Ebooksparalavida..." -ForegroundColor Cyan

# 1. Crear venv si no existe
if (-not (Test-Path ".\.venv")) {
    Write-Host "📦 Creando ambiente virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

# 2. Activar venv
Write-Host "⚙️  Activando ambiente..." -ForegroundColor Yellow
& ".\\.venv\Scripts\Activate.ps1"

# 3. Instalar dependencias
Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
pip install -q flask flask-sqlalchemy

# 4. Crear .env si no existe
if (-not (Test-Path ".\.env")) {
    Write-Host "⚙️  Creando archivo .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

# 5. Ejecutar la app
Write-Host ""
Write-Host "✅ Listo! Iniciando servidor..." -ForegroundColor Green
Write-Host "📍 Abre: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "🔐 Admin: http://127.0.0.1:5000/admin" -ForegroundColor Cyan
Write-Host ""

python -m flask --app backend.app run --debug
