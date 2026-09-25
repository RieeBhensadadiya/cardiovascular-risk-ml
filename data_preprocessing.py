"""
Data Preprocessing Script
Conforms directly to: 'DATA PREPROCESSING: A Simple Student Guide for Cleaning CSV / Tabular Data with Pandas & NumPy'
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def run_data_preprocessing(input_path="cardio_train.csv", output_path="cardio_cleaned.csv", plots_dir="eda_plots"):
    os.makedirs(plots_dir, exist_ok=True)
    print("=" * 60)
    print("STEP 1: UNDERSTAND THE DATA")
    print("=" * 60)

    # 1. Load dataset
    df = pd.read_csv(input_path, sep=';' if ';' in open(input_path).readline() else ',')
    print(f"Dataset loaded. Initial shape: {df.shape}")
    print("\nFirst 5 rows (df.head()):")
    print(df.head())
    print("\nDataset Info (df.info()):")
    df.info()
    print("\nSummary Statistics (df.describe()):")
    print(df.describe())

    print("\n" + "=" * 60)
    print("STEP 2: CLEAN COLUMN NAMES")
    print("=" * 60)
    # F. Clean Column Names
    # df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print("Cleaned column names:", list(df.columns))

    print("\n" + "=" * 60)
    print("STEP 3: CHECK & HANDLE MISSING VALUES")
    print("=" * 60)
    missing_count = df.isnull().sum()
    missing_pct = df.isnull().mean() * 100
    missing_summary = pd.DataFrame({"Missing Count": missing_count, "Percentage (%)": missing_pct})
    print(missing_summary)

    # If any missing values exist, apply the guide's rules:
    # Numeric -> fill with median; Categorical -> fill with mode
    if df.isnull().values.any():
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
        print("Missing values treated. Remaining missing:", df.isnull().sum().sum())
    else:
        print("No missing values found in dataset.")

    print("\n" + "=" * 60)
    print("STEP 4: REMOVE DUPLICATE ROWS & UNNECESSARY IDS")
    print("=" * 60)
    dup_count = df.duplicated().sum()
    print(f"Number of duplicate rows: {dup_count}")
    if dup_count > 0:
        df.drop_duplicates(inplace=True)
        print(f"Dropped duplicate rows. New shape: {df.shape}")

    if 'id' in df.columns:
        df.drop('id', axis=1, inplace=True)
        print("Dropped 'id' column.")

    print("\n" + "=" * 60)
    print("STEP 5: FIX DATA TYPES")
    print("=" * 60)
    # Convert age from days into years (if max age > 150)
    if df['age'].max() > 150:
        df['age'] = (df['age'] / 365.25).round(1)
        print("Converted 'age' from days to years.")

    print("Data types after conversion:")
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("STEP 6: DETECT & HANDLE OUTLIERS (IQR METHOD)")
    print("=" * 60)
    # Guide IQR method:
    # Q1 = df['col'].quantile(0.25)
    # Q3 = df['col'].quantile(0.75)
    # IQR = Q3 - Q1
    # lower = Q1 - 1.5 * IQR
    # upper = Q3 + 1.5 * IQR
    numeric_outlier_cols = ['height', 'weight', 'ap_hi', 'ap_lo']
    initial_len = len(df)

    for col in numeric_outlier_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        
        # Clinical sanity bounds along with IQR
        if col == 'ap_hi':
            lower = max(lower, 70)
            upper = min(upper, 240)
        elif col == 'ap_lo':
            lower = max(lower, 40)
            upper = min(upper, 160)
        elif col == 'height':
            lower = max(lower, 120)
            upper = min(upper, 220)
        elif col == 'weight':
            lower = max(lower, 35)
            upper = min(upper, 200)

        outliers_before = ((df[col] < lower) | (df[col] > upper)).sum()
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        print(f"[{col}] Q1={q1:.1f}, Q3={q3:.1f}, IQR={iqr:.1f} | Bounds: [{lower:.1f}, {upper:.1f}] | Removed: {outliers_before} rows")

    # Inherent logical constraint: ap_hi must be >= ap_lo
    df = df[df['ap_hi'] >= df['ap_lo']]
    print(f"Total rows before outlier handling: {initial_len}, after: {len(df)} (Retained: {len(df)/initial_len*100:.2f}%)")

    # Feature Engineering (BMI and Pulse Pressure)
    df['bmi'] = (df['weight'] / ((df['height'] / 100) ** 2)).round(2)
    df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']

    print("\n" + "=" * 60)
    print("STEP 7: VISUALIZATIONS (GRAPHS FOR NUMERICAL & CATEGORICAL DATA)")
    print("=" * 60)
    # A. Numerical Data Graphs: Histogram, Box Plot, Scatter Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    df['age'].hist(ax=axes[0, 0], bins=20, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Histogram of Age')
    axes[0, 0].set_xlabel('Age (Years)')

    sns.boxplot(x=df['weight'], ax=axes[0, 1], color='lightgreen')
    axes[0, 1].set_title('Box Plot of Weight (Outliers Checked)')

    sns.scatterplot(x='age', y='ap_hi', data=df.sample(min(2000, len(df))), ax=axes[1, 0], alpha=0.5, color='coral')
    axes[1, 0].set_title('Scatter Plot: Age vs Systolic BP (ap_hi)')

    sns.boxplot(x='cardio', y='bmi', data=df.sample(min(2000, len(df))), ax=axes[1, 1], palette='Set2')
    axes[1, 1].set_title('Box Plot: BMI by Cardiovascular Disease Target')
    plt.tight_layout()
    num_plot_path = os.path.join(plots_dir, 'numerical_visualizations.png')
    plt.savefig(num_plot_path, dpi=150)
    plt.close()
    print(f"Numerical visualizations saved to: {num_plot_path}")

    # B. Categorical Data Graphs: Bar Chart, Pie Chart, Count Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    df['gender'].value_counts().plot(kind='bar', ax=axes[0], color=['dodgerblue', 'salmon'])
    axes[0].set_title('Bar Chart: Gender (1=Female, 2=Male)')
    axes[0].set_xlabel('Gender')
    axes[0].set_ylabel('Count')

    df['cholesterol'].value_counts().plot(kind='pie', ax=axes[1], autopct='%1.1f%%', colors=['#66b3ff','#99ff99','#ff9999'])
    axes[1].set_title('Pie Chart: Cholesterol Distribution')
    axes[1].set_ylabel('')

    sns.countplot(x='smoke', hue='cardio', data=df, ax=axes[2], palette='Blues')
    axes[2].set_title('Count Plot: Smoke vs Cardio')
    plt.tight_layout()
    cat_plot_path = os.path.join(plots_dir, 'categorical_visualizations.png')
    plt.savefig(cat_plot_path, dpi=150)
    plt.close()
    print(f"Categorical visualizations saved to: {cat_plot_path}")

    print("\n" + "=" * 60)
    print("STEP 8: SCALE NUMERIC COLUMNS (MINMAX & STANDARD SCALER)")
    print("=" * 60)
    scaler = MinMaxScaler()
    scale_cols = ['age', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi', 'pulse_pressure']
    scaled_features = scaler.fit_transform(df[scale_cols])
    scaled_df = pd.DataFrame(scaled_features, columns=[f"{c}_scaled" for c in scale_cols])
    print(f"Scaled {len(scale_cols)} numeric columns with MinMaxScaler.")
    print("Sample of scaled numerical columns:")
    print(scaled_df.head(3))

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print("\n" + "=" * 60)
    print(f"SUCCESS: Cleaned dataset saved to: {output_path}")
    print(f"Final Cleaned Dataset Shape: {df.shape}")
    print("=" * 60)
    return df

if __name__ == "__main__":
    run_data_preprocessing()
