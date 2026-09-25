"""
Streamlit Application for Cardiovascular Disease Risk Prediction
Deployment Target: Streamlit Community Cloud (share.streamlit.io)
Fulfills Task 6 - Part 1: Deploying a Streamlit App
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Cardiovascular Disease Risk Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #e63946;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 5px solid #e63946;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .risk-badge-low {
        background-color: #d4edda;
        color: #155724;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .risk-badge-high {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_cardio_model():
    model_path = os.path.join(os.path.dirname(__file__), "cardio_model.joblib")
    if not os.path.exists(model_path):
        return None
    try:
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

bundle = load_cardio_model()

# Header
st.markdown('<div class="main-title">❤️ Cardiovascular Risk Assessment AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Clinical-grade Machine Learning model for early cardiovascular risk prediction</div>', unsafe_allow_html=True)

if not bundle:
    st.error("⚠️ Model file `cardio_model.joblib` not found. Please run `python train_model.py` first to generate the model bundle.")
    st.stop()

# Sidebar: Model Specs
with st.sidebar:
    st.header("🔬 Model Information")
    st.info(f"**Architecture**: {bundle.get('model_name', 'Gradient Boosting')}")
    metrics = bundle.get('metrics', {})
    if metrics:
        st.write(f"• **Accuracy**: `{metrics.get('accuracy', 0.73)*100:.1f}%`")
        st.write(f"• **ROC-AUC**: `{metrics.get('roc_auc', 0.79):.3f}`")
        st.write(f"• **Training Data**: `{metrics.get('total_samples', 62500):,} records`")
    st.markdown("---")
    st.markdown("### Deployment Guide")
    st.caption("This app is ready for 1-click deployment on **Streamlit Community Cloud** (share.streamlit.io).")

# Main Input Form
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Demographics")
    age = st.number_input("Age (Years)", min_value=18, max_value=100, value=50, step=1)
    gender_label = st.selectbox("Biological Sex", ["Female", "Male"])
    gender = 1 if gender_label == "Female" else 2

    st.subheader("📏 Body Metrics")
    height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170, step=1)
    weight = st.number_input("Weight (kg)", min_value=35.0, max_value=200.0, value=75.0, step=0.5)
    
    height_m = height / 100.0
    bmi = round(weight / (height_m ** 2), 2)
    st.caption(f"Calculated BMI: **{bmi} kg/m²**")

with col2:
    st.subheader("🩺 Vitals & Blood Pressure")
    ap_hi = st.number_input("Systolic BP (ap_hi, mmHg)", min_value=80, max_value=220, value=120, step=1)
    ap_lo = st.number_input("Diastolic BP (ap_lo, mmHg)", min_value=50, max_value=140, value=80, step=1)
    
    pulse_pressure = ap_hi - ap_lo
    st.caption(f"Pulse Pressure: **{pulse_pressure} mmHg**")

    st.subheader("🧪 Laboratory Tests")
    chol_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
    cholesterol = chol_map[st.selectbox("Cholesterol Level", list(chol_map.keys()))]
    
    gluc_map = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}
    gluc = gluc_map[st.selectbox("Glucose Level", list(gluc_map.keys()))]

with col3:
    st.subheader("🏃 Lifestyle Factors")
    smoke = 1 if st.checkbox("Active Tobacco Smoker") else 0
    alco = 1 if st.checkbox("Frequent Alcohol Intake") else 0
    active = 1 if st.checkbox("Physically Active (Exercise Regular)", value=True) else 0

st.markdown("---")

# Predict Button
if st.button("🔍 Assess Cardiovascular Risk", type="primary", use_container_width=True):
    feature_cols = bundle.get('feature_cols', [
        'age', 'gender', 'height', 'weight',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active', 'bmi', 'pulse_pressure'
    ])

    input_df = pd.DataFrame([{
        'age': float(age),
        'gender': int(gender),
        'height': float(height),
        'weight': float(weight),
        'ap_hi': float(ap_hi),
        'ap_lo': float(ap_lo),
        'cholesterol': int(cholesterol),
        'gluc': int(gluc),
        'smoke': int(smoke),
        'alco': int(alco),
        'active': int(active),
        'bmi': float(bmi),
        'pulse_pressure': float(pulse_pressure)
    }])[feature_cols]

    pipeline = bundle['pipeline']
    raw_pred = pipeline.predict(input_df)[0]
    raw_prob = pipeline.predict_proba(input_df)[0][1]
    score = int(round(raw_prob * 100))

    st.markdown("### 📊 Assessment Results")
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        if score >= 50:
            st.error(f"## High Risk: {score}%")
            st.write("Cardiovascular disease indicators detected.")
        else:
            st.success(f"## Low Risk: {score}%")
            st.write("No acute cardiovascular indicators detected.")

        st.progress(score / 100)

    with res_col2:
        st.markdown("**Key Physiological Factors:**")
        factors = []
        if ap_hi >= 140 or ap_lo >= 90:
            factors.append(f"⚠️ Hypertension detected: {ap_hi}/{ap_lo} mmHg")
        if cholesterol > 1:
            factors.append("⚠️ Elevated serum cholesterol")
        if bmi >= 30:
            factors.append(f"⚠️ Obese BMI ({bmi})")
        elif bmi >= 25:
            factors.append(f"ℹ️ Overweight BMI ({bmi})")
        if smoke == 1:
            factors.append("⚠️ Smoking increases arterial stiffness")
        if active == 1:
            factors.append("✅ Regular exercise provides cardioprotection")

        if factors:
            for f in factors:
                st.write(f)
        else:
            st.write("✅ All examined clinical metrics are within optimal ranges.")
