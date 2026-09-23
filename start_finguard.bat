@echo off
title FinGuard AI - Master Launcher
echo ========================================================
echo Starting FinGuard AI: ML Backend, Core Backend, Frontend
echo ========================================================

REM 1. Start ML Inference Microservice (Port 8001)
start "FinGuard - ML Backend (Port 8001)" cmd /k "cd /d %~dp0ml-backend && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"

REM Wait 2 seconds for ML model initialization
timeout /t 2 /nobreak >nul

REM 2. Start Core FastAPI Backend (Port 8000)
start "FinGuard - Core Backend (Port 8000)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait 2 seconds
timeout /t 2 /nobreak >nul

REM 3. Start Next.js Frontend (Port 3000)
start "FinGuard - Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo All 3 services have been launched in separate terminal windows:
echo - Frontend UI:   http://localhost:3000
echo - Core Backend:  http://127.0.0.1:8000/docs
echo - ML Backend:    http://127.0.0.1:8001/ready
echo ========================================================
pause
