@echo off
echo ================================
echo Iniciando Backend FastAPI
echo ================================
echo URL: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.

cd backend
python -m uvicorn app.main:app --reload
