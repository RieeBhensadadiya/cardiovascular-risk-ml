"""
FastAPI Backend for Cardiovascular Disease Risk Prediction
Deployment Target: Render (Web Service)
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
"""

import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

app = FastAPI(
    title="Cardiovascular Disease Risk Prediction API",
    description="Production ML API deployed on Render with FastAPI, serving a trained Gradient Boosting classifier.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 2. CORS Middleware Configuration (Task 6 Step A.2)
# ------------------------------------------------------------------------------
# Allows frontend deployed on Vercel or running locally to call the API
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for seamless student deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Load Model Bundle
# ------------------------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "cardio_model.joblib")
model_bundle = None

def get_model():
    global model_bundle
    if model_bundle is None:
        if os.path.exists(MODEL_PATH):
            try:
                model_bundle = joblib.load(MODEL_PATH)
                print(f"[FastAPI Backend] Loaded model from: {MODEL_PATH}")
            except Exception as e:
                print(f"[FastAPI Backend] Error loading model: {e}")
        else:
            print(f"[FastAPI Backend] Model file not found at {MODEL_PATH}")
    return model_bundle

@app.on_event("startup")
def startup_event():
    get_model()

# ------------------------------------------------------------------------------
# Pydantic Schemas
# ------------------------------------------------------------------------------
class PatientInput(BaseModel):
    age: float = Field(..., description="Age in years (or days)")
    gender: int = Field(..., description="1: Female, 2: Male")
    height: float = Field(..., description="Height in cm")
    weight: float = Field(..., description="Weight in kg")
    ap_hi: float = Field(..., description="Systolic blood pressure (mmHg)")
    ap_lo: float = Field(..., description="Diastolic blood pressure (mmHg)")
    cholesterol: int = Field(..., ge=1, le=3, description="1: Normal, 2: Above Normal, 3: Well Above Normal")
    gluc: int = Field(..., ge=1, le=3, description="1: Normal, 2: Above Normal, 3: Well Above Normal")
    smoke: int = Field(..., ge=0, le=1, description="0: No, 1: Yes")
    alco: int = Field(..., ge=0, le=1, description="0: No, 1: Yes")
    active: int = Field(..., ge=0, le=1, description="0: No, 1: Yes")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 52.0,
                "gender": 2,
                "height": 172.0,
                "weight": 80.0,
                "ap_hi": 130.0,
                "ap_lo": 85.0,
                "cholesterol": 2,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    bundle = get_model()
    return {
        "service": "Cardiovascular Prediction API",
        "framework": "FastAPI",
        "deployment": "Render",
        "status": "online",
        "model_loaded": bundle is not None,
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    bundle = get_model()
    return {
        "status": "healthy",
        "model_loaded": bundle is not None,
        "model_name": bundle.get('model_name') if bundle else None,
        "metrics": bundle.get('metrics') if bundle else None,
        "trained_at": bundle.get('trained_at') if bundle else None
    }

@app.get("/api/model-info")
def model_info():
    bundle = get_model()
    if not bundle:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model is not loaded")
    return {
        "model_name": bundle.get('model_name'),
        "metrics": bundle.get('metrics'),
        "feature_importance": bundle.get('feature_importance'),
        "feature_cols": bundle.get('feature_cols'),
        "trained_at": bundle.get('trained_at')
    }

@app.post("/api/predict")
def predict(data: PatientInput):
    bundle = get_model()
    if not bundle:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded on server. Please run 'python train_model.py' to generate 'cardio_model.joblib'."
        )

    try:
        # Age sanitation (convert days to years if entered in days)
        age = data.age
        if age > 120:
            age = round(age / 365.25, 1)

        # Feature engineering
        height_m = data.height / 100.0
        bmi = round(data.weight / (height_m ** 2), 2) if height_m > 0 else 0.0
        pulse_pressure = data.ap_hi - data.ap_lo

        feature_cols = bundle.get('feature_cols', [
            'age', 'gender', 'height', 'weight',
            'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
            'smoke', 'alco', 'active', 'bmi', 'pulse_pressure'
        ])

        input_df = pd.DataFrame([{
            'age': age,
            'gender': data.gender,
            'height': data.height,
            'weight': data.weight,
            'ap_hi': data.ap_hi,
            'ap_lo': data.ap_lo,
            'cholesterol': data.cholesterol,
            'gluc': data.gluc,
            'smoke': data.smoke,
            'alco': data.alco,
            'active': data.active,
            'bmi': bmi,
            'pulse_pressure': pulse_pressure
        }])[feature_cols]

        pipeline = bundle['pipeline']
        raw_pred = int(pipeline.predict(input_df)[0])
        raw_prob = float(pipeline.predict_proba(input_df)[0][1])

        score = int(round(raw_prob * 100))
        positive = bool(raw_pred == 1 or score >= 50)

        # Risk level determination
        if score <= 25:
            risk_level = "Low Risk"
        elif score <= 49:
            risk_level = "Moderate Risk"
        elif score <= 69:
            risk_level = "High Risk"
        else:
            risk_level = "Critical Risk"

        # Risk factors
        risk_factors = []
        if data.ap_hi >= 140 or data.ap_lo >= 90:
            risk_factors.append(f"Elevated Blood Pressure ({int(data.ap_hi)}/{int(data.ap_lo)} mmHg - Hypertension)")
        elif data.ap_hi >= 130 or data.ap_lo >= 80:
            risk_factors.append(f"Prehypertension ({int(data.ap_hi)}/{int(data.ap_lo)} mmHg)")
        if data.cholesterol == 3:
            risk_factors.append("Critically high cholesterol levels (Well above normal)")
        elif data.cholesterol == 2:
            risk_factors.append("Elevated cholesterol levels (Above normal)")
        if data.gluc >= 2:
            risk_factors.append("Elevated blood glucose levels")
        if bmi >= 30:
            risk_factors.append(f"Obesity category (BMI: {bmi})")
        elif bmi >= 25:
            risk_factors.append(f"Overweight category (BMI: {bmi})")
        if data.smoke == 1:
            risk_factors.append("Active tobacco smoking")
        if data.alco == 1:
            risk_factors.append("Regular alcohol consumption")
        if data.active == 0:
            risk_factors.append("Sedentary lifestyle (Low physical activity)")
        if age >= 55:
            risk_factors.append(f"Advanced age demographic ({int(age)} years)")

        protective_factors = []
        if data.active == 1:
            protective_factors.append("Active regular physical exercise")
        if data.smoke == 0:
            protective_factors.append("Non-smoker")
        if data.alco == 0:
            protective_factors.append("No excessive alcohol consumption")
        if data.cholesterol == 1:
            protective_factors.append("Normal healthy cholesterol")
        if data.gluc == 1:
            protective_factors.append("Normal blood glucose levels")
        if 18.5 <= bmi <= 24.9:
            protective_factors.append(f"Optimal healthy BMI ({bmi})")
        if data.ap_hi < 120 and data.ap_lo < 80:
            protective_factors.append(f"Optimal blood pressure ({int(data.ap_hi)}/{int(data.ap_lo)} mmHg)")

        return {
            "success": True,
            "positive": positive,
            "score": score,
            "probability": round(raw_prob, 4),
            "risk_level": risk_level,
            "bmi": bmi,
            "pulse_pressure": pulse_pressure,
            "model_name": bundle.get("model_name", "Gradient Boosting Model"),
            "risk_factors": risk_factors,
            "protective_factors": protective_factors,
            "patient_summary": {
                "age": age,
                "gender": "Female" if data.gender == 1 else "Male",
                "height": data.height,
                "weight": data.weight,
                "bp": f"{int(data.ap_hi)}/{int(data.ap_lo)}",
                "cholesterol": "Normal" if data.cholesterol == 1 else "Above Normal" if data.cholesterol == 2 else "Well Above Normal",
                "glucose": "Normal" if data.gluc == 1 else "Above Normal" if data.gluc == 2 else "Well Above Normal"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    print(f"[FastAPI] Starting server on http://0.0.0.0:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
