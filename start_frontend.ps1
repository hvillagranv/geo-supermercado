# Script para iniciar el frontend
# Ejecutar: .\start_frontend.ps1

Write-Host "Iniciando servidor frontend React..." -ForegroundColor Green
Write-Host "URL: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Set-Location frontend
npm run dev
