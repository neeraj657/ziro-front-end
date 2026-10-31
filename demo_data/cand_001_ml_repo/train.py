"""End-to-end training pipeline with 5-fold Stratified Cross-Validation."""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from preprocessing import clean_transaction_data, fit_scaler, transform_features
from model import FraudDetector

def run_training_experiment():
    np.random.seed(42)
    n_samples = 2500
    df = pd.DataFrame({
        "user_id": np.random.randint(1000, 2000, n_samples),
        "timestamp": pd.date_range("2026-01-01", periods=n_samples, freq="15min"),
        "amount": np.random.exponential(scale=75.0, size=n_samples),
        "frequency_score": np.random.normal(5.0, 1.5, n_samples),
        "is_fraud": np.random.choice([0, 1], size=n_samples, p=[0.94, 0.06])
    })

    cleaned = clean_transaction_data(df)
    X = cleaned[["amount", "frequency_score", "is_night_transaction"]]
    y = cleaned["is_fraud"]

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    auc_scores = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

        scaler = fit_scaler(X_tr)
        X_tr_s = transform_features(X_tr, scaler)
        X_val_s = transform_features(X_val, scaler)

        detector = FraudDetector()
        detector.fit(X_tr_s.values, y_tr.values)
        metrics = detector.evaluate(X_val_s.values, y_val.values)
        auc_scores.append(metrics["roc_auc"])

    mean_auc = float(np.mean(auc_scores))
    return {"mean_roc_auc": round(mean_auc, 4), "fold_scores": auc_scores}

if __name__ == "__main__":
    res = run_training_experiment()
    print(f"5-Fold Stratified Cross Validation Mean ROC-AUC: {res['mean_roc_auc']}")
