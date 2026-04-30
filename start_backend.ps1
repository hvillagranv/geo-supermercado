# Script para iniciar el backend
# Ejecutar: .\start_backend.ps1

Write-Host "Iniciando servidor backend FastAPI..." -ForegroundColor Green
Write-Host "URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentacion API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Set-Location backend
python -m uvicorn app.main:app --reload
