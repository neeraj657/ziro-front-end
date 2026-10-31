# Real-time Fraud Detection Machine Learning Service

A modular Python service to detect suspicious credit transactions in real-time.

## Architecture
- `preprocessing.py`: Feature extraction and outlier-resistant `RobustScaler` fitting.
- `model.py`: Random Forest classifier with `balanced` sample weighting and ROC-AUC evaluation.
- `train.py`: Leakage-free 5-fold Stratified Cross-Validation pipeline.
- `test_model.py`: Automated pytest verification suite.

## Running Tests
```bash
pytest test_model.py -v
```
