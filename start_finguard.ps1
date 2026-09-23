# FinGuard AI - PowerShell Master Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting FinGuard AI: ML Backend, Core Backend, Frontend" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

# 1. Start ML Inference Microservice (Port 8001)
Write-Host "1. Launching ML Backend on port 8001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\ml-backend'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload"

Start-Sleep -Seconds 2

# 2. Start Core FastAPI Backend (Port 8000)
Write-Host "2. Launching Core Backend on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 2

# 3. Start Next.js Frontend (Port 3000)
Write-Host "3. Launching Next.js Frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host ""
Write-Host "All 3 services have been launched in separate PowerShell windows:" -ForegroundColor Green
Write-Host "- Frontend UI:   http://localhost:3000" -ForegroundColor Cyan
Write-Host "- Core Backend:  http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "- ML Backend:    http://127.0.0.1:8001/ready" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Green
