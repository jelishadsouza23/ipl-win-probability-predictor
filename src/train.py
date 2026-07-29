import os
import sys
# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import log_loss, accuracy_score, brier_score_loss, roc_auc_score
from xgboost import XGBClassifier

from src.data_prep import load_and_preprocess_data
from src.feature_engineering import prepare_feature_matrix

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')


def train_and_evaluate_models():
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    print("Step 1: Loading & Cleaning IPL dataset...")
    df = load_and_preprocess_data()

    print("Step 2: Engineering features...")
    X, y, groups, categorical_cols, numerical_cols = prepare_feature_matrix(df)

    # Train/Test Split by match_id (GroupShuffleSplit to avoid data leakage)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    X_train, y_train = X.iloc[train_idx], y[train_idx]
    X_test, y_test = X.iloc[test_idx], y[test_idx]

    print(f"Train set: {len(X_train)} balls ({len(np.unique(groups[train_idx]))} matches)")
    print(f"Test set:  {len(X_test)} balls ({len(np.unique(groups[test_idx]))} matches)")

    # Define Preprocessor Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
            ('num', StandardScaler(), numerical_cols)
        ]
    )

    # Models to test
    classifiers = {
        'Logistic Regression (Baseline)': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=10, min_samples_leaf=5, random_state=42),
        'XGBoost': XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.08, eval_metric='logloss', random_state=42)
    }

    best_model_name = None
    best_log_loss = float('inf')
    best_pipeline = None

    print("\n--- Model Evaluation Results ---")

    results = []

    for name, clf in classifiers.items():
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])

        pipeline.fit(X_train, y_train)
        probs = pipeline.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.5).astype(int)

        loss = log_loss(y_test, probs)
        brier = brier_score_loss(y_test, probs)
        acc = accuracy_score(y_test, preds)
        auc = roc_auc_score(y_test, probs)

        results.append({
            'Model': name,
            'Log Loss': round(loss, 4),
            'Brier Score': round(brier, 4),
            'Accuracy': round(acc, 4),
            'ROC AUC': round(auc, 4)
        })

        print(f"{name:30s} -> Log Loss: {loss:.4f} | Brier Score: {brier:.4f} | Accuracy: {acc*100:.2f}% | AUC: {auc:.4f}")

        if loss < best_log_loss:
            best_log_loss = loss
            best_model_name = name
            best_pipeline = pipeline

    print(f"\nWinning architecture: {best_model_name} with Log Loss = {best_log_loss:.4f}")

    # Probability Calibration step for the best pipeline
    print("\nStep 3: Calibrating probabilities with CalibratedClassifierCV...")
    calibrated_pipeline = Pipeline([
        ('preprocessor', best_pipeline.named_steps['preprocessor']),
        ('calibrated_classifier', CalibratedClassifierCV(
            estimator=best_pipeline.named_steps['classifier'],
            method='isotonic',
            cv=3
        ))
    ])
    
    calibrated_pipeline.fit(X_train, y_train)
    cal_probs = calibrated_pipeline.predict_proba(X_test)[:, 1]
    cal_loss = log_loss(y_test, cal_probs)
    cal_acc = accuracy_score(y_test, (cal_probs >= 0.5).astype(int))

    print(f"Calibrated {best_model_name} -> Log Loss: {cal_loss:.4f} | Accuracy: {cal_acc*100:.2f}%")

    # Plot & Save Calibration Curve
    prob_true, prob_pred = calibration_curve(y_test, cal_probs, n_bins=10)
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], [0, 1], 'k--', label='Perfectly Calibrated')
    plt.plot(prob_pred, prob_true, 's-', label=f'{best_model_name} (Calibrated)')
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('Fraction of Positives (Actual Win Rate)')
    plt.title(f'IPL Win Probability Calibration Curve - {best_model_name}')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    curve_path = os.path.join(MODELS_DIR, 'calibration_curve.png')
    plt.savefig(curve_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved calibration curve plot to {curve_path}")

    # Save artifact
    model_artifact_path = os.path.join(MODELS_DIR, 'ipl_win_probability_model.joblib')
    artifact_payload = {
        'pipeline': calibrated_pipeline,
        'model_name': best_model_name,
        'categorical_cols': categorical_cols,
        'numerical_cols': numerical_cols,
        'test_log_loss': cal_loss,
        'test_accuracy': cal_acc
    }
    joblib.dump(artifact_payload, model_artifact_path)
    print(f"Successfully saved final calibrated model artifact to {model_artifact_path}")

    return calibrated_pipeline, pd.DataFrame(results)

if __name__ == '__main__':
    train_and_evaluate_models()
