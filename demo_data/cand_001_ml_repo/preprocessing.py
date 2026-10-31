"""Transaction Preprocessing & Feature Engineering.

Applies robust quantile scaling and extracts time-series features.
"""
import pandas as pd
from sklearn.preprocessing import RobustScaler

def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop incomplete rows and extract temporal features."""
    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=["amount", "timestamp", "user_id"])
    cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"])
    cleaned["hour_of_day"] = cleaned["timestamp"].dt.hour
    cleaned["is_night_transaction"] = cleaned["hour_of_day"].apply(
        lambda h: 1 if (h < 6 or h > 22) else 0
    )
    return cleaned

def fit_scaler(X_train: pd.DataFrame) -> RobustScaler:
    """Fit robust scaler exclusively on training split to eliminate data leakage."""
    scaler = RobustScaler()
    scaler.fit(X_train[["amount", "frequency_score"]])
    return scaler

def transform_features(X: pd.DataFrame, scaler: RobustScaler) -> pd.DataFrame:
    """Transform continuous features using pre-fitted scaler."""
    X_scaled = X.copy()
    X_scaled[["amount", "frequency_score"]] = scaler.transform(X[["amount", "frequency_score"]])
    return X_scaled
