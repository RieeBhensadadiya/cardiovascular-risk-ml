import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

def load_and_preprocess_data(csv_path="cardio_train.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")

    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path, sep=';')
    print(f"Initial raw rows: {len(df)}")

    # Deduplicate
    df = df.drop_duplicates().copy()
    if 'id' in df.columns:
        df.drop('id', axis=1, inplace=True)

    # Convert age from days to years if necessary (dataset is in days > 1000)
    if df['age'].max() > 150:
        df['age'] = (df['age'] / 365.25).round(1)

    # Clean outlier records based on physiological limits
    df = df[(df['ap_hi'] >= 60) & (df['ap_hi'] <= 240)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 160)]
    df = df[df['ap_hi'] >= df['ap_lo']]
    df = df[(df['height'] >= 100) & (df['height'] <= 240)]
    df = df[(df['weight'] >= 30) & (df['weight'] <= 220)]

    # Feature Engineering
    df['bmi'] = (df['weight'] / ((df['height'] / 100) ** 2)).round(2)
    df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']

    print(f"Cleaned valid records: {len(df)}")
    return df

def train_and_save_model(data_path="cardio_train.csv", model_output_path="cardio_model.joblib"):
    df = load_and_preprocess_data(data_path)

    feature_cols = [
        'age', 'gender', 'height', 'weight',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active', 'bmi', 'pulse_pressure'
    ]

    X = df[feature_cols]
    y = df['cardio']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples, Testing set: {X_test.shape[0]} samples")

    # Build model pipeline
    gb = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=4,
        subsample=0.9,
        random_state=42
    )

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', gb)
    ])

    print("Training Gradient Boosting Pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        'accuracy': float(round(accuracy_score(y_test, y_pred), 4)),
        'roc_auc': float(round(roc_auc_score(y_test, y_prob), 4)),
        'precision': float(round(precision_score(y_test, y_pred), 4)),
        'recall': float(round(recall_score(y_test, y_pred), 4)),
        'f1_score': float(round(f1_score(y_test, y_pred), 4)),
        'total_samples': int(len(df)),
        'test_samples': int(len(y_test))
    }

    print("\n" + "="*40)
    print("MODEL PERFORMANCE METRICS")
    print("="*40)
    for k, v in metrics.items():
        print(f"  {k:15}: {v}")
    print("="*40 + "\n")

    # Feature importances
    importances = pipeline.named_steps['classifier'].feature_importances_
    feat_importance = dict(sorted(
        {feat: float(round(imp, 4)) for feat, imp in zip(feature_cols, importances)}.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    # Package model bundle
    bundle = {
        'pipeline': pipeline,
        'feature_cols': feature_cols,
        'metrics': metrics,
        'feature_importance': feat_importance,
        'model_name': 'GradientBoostingClassifier (Ensemble)',
        'trained_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    joblib.dump(bundle, model_output_path)
    print(f"Successfully saved model bundle to '{model_output_path}'")
    return bundle

if __name__ == '__main__':
    train_and_save_model()
