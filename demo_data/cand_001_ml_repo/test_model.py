"""Automated unit and integration tests for Fraud Detection pipeline."""
import pytest
import pandas as pd
import numpy as np
from preprocessing import clean_transaction_data, fit_scaler, transform_features
from model import FraudDetector

def test_clean_transaction_data():
    df = pd.DataFrame({
        "user_id": [1, 2, None],
        "timestamp": ["2026-01-01 02:00:00", "2026-01-01 14:00:00", "2026-01-01 15:00:00"],
        "amount": [120.5, 45.0, 30.0]
    })
    cleaned = clean_transaction_data(df)
    assert len(cleaned) == 2
    assert "is_night_transaction" in cleaned.columns
    assert cleaned.iloc[0]["is_night_transaction"] == 1
    assert cleaned.iloc[1]["is_night_transaction"] == 0

def test_feature_scaling_leakage_free():
    train_df = pd.DataFrame({"amount": [10.0, 20.0, 30.0], "frequency_score": [1.0, 2.0, 3.0]})
    scaler = fit_scaler(train_df)
    test_df = pd.DataFrame({"amount": [40.0], "frequency_score": [4.0]})
    transformed = transform_features(test_df, scaler)
    assert transformed.shape == (1, 2)
    assert not np.isnan(transformed.values).any()

def test_model_evaluation_metrics():
    X_train = np.array([[1.0, 2.0], [2.0, 3.0], [0.5, 1.0], [3.0, 4.0], [1.2, 0.9]])
    y_train = np.array([0, 0, 1, 0, 1])
    detector = FraudDetector(n_estimators=10)
    detector.fit(X_train, y_train)
    eval_res = detector.evaluate(X_train, y_train)
    assert "roc_auc" in eval_res
    assert "precision" in eval_res
    assert "recall" in eval_res
    assert eval_res["roc_auc"] >= 0.5
