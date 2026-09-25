@echo off
title CardioScan Full-Stack ML Launcher
echo ==========================================================
echo Starting CardioScan ML Backend & Frontend Application...
echo ==========================================================

:: 1. Start FastAPI ML Backend in a dedicated window
echo [1/3] Launching ML Backend on port 5000...
start "Cardio ML Backend (Port 5000)" cmd /k "python main.py"

:: 2. Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

:: 3. Start Vite React Frontend in a dedicated window
echo [2/3] Launching React Frontend on port 5173...
start "CardioScan Frontend (Port 5173)" cmd /k "cd cardiovascular-ui && npm run dev"

:: 4. Open application in default web browser
echo [3/3] Opening http://localhost:5173 in browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173/predict

echo ==========================================================
echo Application is running!
echo Frontend: http://localhost:5173
echo Backend:  http://127.0.0.1:5000 (Model: cardio_model.joblib)
echo Keep both command windows open while using the app.
echo ==========================================================
pause
