import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes (allows calls from Vite dev server http://localhost:5173)
CORS(app, resources={r"/api/*": {"origins": "*"}})

MODEL_PATH = os.path.join(os.path.dirname(__file__), "cardio_model.joblib")
model_bundle = None

def load_model():
    global model_bundle
    if os.path.exists(MODEL_PATH):
        try:
            model_bundle = joblib.load(MODEL_PATH)
            print(f"[Backend] Successfully loaded model bundle from {MODEL_PATH}")
            print(f"[Backend] Model: {model_bundle.get('model_name')}, Metrics: {model_bundle.get('metrics')}")
        except Exception as e:
            print(f"[Backend] Error loading model: {e}")
            model_bundle = None
    else:
        print(f"[Backend] Model file not found at {MODEL_PATH}. Run 'python train_model.py' first.")

load_model()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model_bundle is not None,
        "model_name": model_bundle.get('model_name') if model_bundle else None,
        "metrics": model_bundle.get('metrics') if model_bundle else None,
        "trained_at": model_bundle.get('trained_at') if model_bundle else None
    }), 200

@app.route('/api/model-info', methods=['GET'])
def model_info():
    if not model_bundle:
        return jsonify({"error": "Model is not loaded"}), 503
    return jsonify({
        "model_name": model_bundle.get('model_name'),
        "metrics": model_bundle.get('metrics'),
        "feature_importance": model_bundle.get('feature_importance'),
        "feature_cols": model_bundle.get('feature_cols'),
        "trained_at": model_bundle.get('trained_at')
    }), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    if not model_bundle:
        return jsonify({"error": "Model not loaded on server. Please ensure train_model.py has been executed."}), 503

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Required fields
        required_fields = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
        missing = [f for f in required_fields if f not in data or data[f] == '' or data[f] is None]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        # Parse & sanitize inputs
        age = float(data['age'])
        # If age is given in days (>120), convert to years
        if age > 120:
            age = round(age / 365.25, 1)

        gender = int(data['gender'])
        height = float(data['height'])
        weight = float(data['weight'])
        ap_hi = float(data['ap_hi'])
        ap_lo = float(data['ap_lo'])
        cholesterol = int(data['cholesterol'])
        gluc = int(data['gluc'])
        smoke = int(data['smoke'])
        alco = int(data['alco'])
        active = int(data['active'])

        # Engineered features
        height_m = height / 100.0
        bmi = round(weight / (height_m ** 2), 2) if height_m > 0 else 0.0
        pulse_pressure = ap_hi - ap_lo

        # Prepare DataFrame with expected column order
        feature_cols = model_bundle.get('feature_cols', [
            'age', 'gender', 'height', 'weight',
            'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
            'smoke', 'alco', 'active', 'bmi', 'pulse_pressure'
        ])

        input_df = pd.DataFrame([{
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'ap_hi': ap_hi,
            'ap_lo': ap_lo,
            'cholesterol': cholesterol,
            'gluc': gluc,
            'smoke': smoke,
            'alco': alco,
            'active': active,
            'bmi': bmi,
            'pulse_pressure': pulse_pressure
        }])[feature_cols]

        pipeline = model_bundle['pipeline']
        raw_pred = pipeline.predict(input_df)[0]
        raw_prob = pipeline.predict_proba(input_df)[0][1]

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

        # Explainable factors for patient
        risk_factors = []
        if ap_hi >= 140 or ap_lo >= 90:
            risk_factors.append(f"Elevated Blood Pressure ({int(ap_hi)}/{int(ap_lo)} mmHg - Stage 2 Hypertension)")
        elif ap_hi >= 130 or ap_lo >= 80:
            risk_factors.append(f"Prehypertension ({int(ap_hi)}/{int(ap_lo)} mmHg)")
        if cholesterol == 3:
            risk_factors.append("Critically high cholesterol levels (Well above normal)")
        elif cholesterol == 2:
            risk_factors.append("Elevated cholesterol levels (Above normal)")
        if gluc >= 2:
            risk_factors.append("Elevated blood glucose levels")
        if bmi >= 30:
            risk_factors.append(f"Obesity category (BMI: {bmi})")
        elif bmi >= 25:
            risk_factors.append(f"Overweight category (BMI: {bmi})")
        if smoke == 1:
            risk_factors.append("Active tobacco smoking")
        if alco == 1:
            risk_factors.append("Regular alcohol consumption")
        if active == 0:
            risk_factors.append("Sedentary lifestyle (Low physical activity)")
        if age >= 55:
            risk_factors.append(f"Advanced age demographic ({int(age)} years)")

        protective_factors = []
        if active == 1:
            protective_factors.append("Active regular physical exercise")
        if smoke == 0:
            protective_factors.append("Non-smoker")
        if alco == 0:
            protective_factors.append("No excessive alcohol consumption")
        if cholesterol == 1:
            protective_factors.append("Normal healthy cholesterol")
        if gluc == 1:
            protective_factors.append("Normal blood glucose levels")
        if 18.5 <= bmi <= 24.9:
            protective_factors.append(f"Optimal healthy BMI ({bmi})")
        if ap_hi < 120 and ap_lo < 80:
            protective_factors.append(f"Optimal blood pressure ({int(ap_hi)}/{int(ap_lo)} mmHg)")

        response = {
            "success": True,
            "positive": positive,
            "score": score,
            "probability": round(float(raw_prob), 4),
            "risk_level": risk_level,
            "bmi": bmi,
            "pulse_pressure": pulse_pressure,
            "model_name": model_bundle.get("model_name", "Gradient Boosting Model"),
            "risk_factors": risk_factors,
            "protective_factors": protective_factors,
            "patient_summary": {
                "age": age,
                "gender": "Female" if gender == 1 else "Male",
                "height": height,
                "weight": weight,
                "bp": f"{int(ap_hi)}/{int(ap_lo)}",
                "cholesterol": "Normal" if cholesterol == 1 else "Above Normal" if cholesterol == 2 else "Well Above Normal",
                "glucose": "Normal" if gluc == 1 else "Above Normal" if gluc == 2 else "Well Above Normal"
            }
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"[Backend Error] {e}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"[Backend] Starting Cardiovascular Prediction API on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
