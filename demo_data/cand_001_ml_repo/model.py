"""Fraud Detection Model Architecture.

Demonstrates class-imbalance aware Random Forest and baseline evaluation.
"""
from typing import Dict, Any
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
import joblib

class FraudDetector:
    def __init__(self, n_estimators: int = 150, max_depth: int = 10, random_state: int = 42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            class_weight="balanced"
        )
        self.baseline = LogisticRegression(max_iter=1000)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Fit baseline and target models on training fold."""
        self.baseline.fit(X_train, y_train)
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance using ROC-AUC and minority class precision/recall."""
        preds = self.model.predict(X_test)
        probs = self.model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, preds, average="binary", zero_division=0
        )
        return {
            "roc_auc": round(float(auc), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1": round(float(f1), 4)
        }

    def save(self, filepath: str) -> None:
        """Serialize trained model artifact to disk."""
        joblib.dump(self.model, filepath)
