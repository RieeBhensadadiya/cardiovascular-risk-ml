@echo off
echo ====================================================
echo Starting Cardiovascular Risk Prediction ML Backend...
echo ====================================================

python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

if not exist "cardio_model.joblib" (
    echo Model not found. Training model now...
    python train_model.py
)

echo Starting Flask API Server on http://127.0.0.1:5000 ...
python server.py
pause
