import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

SECRET_KEY = "skillproof-hackathon-hmac-key-2026"


def generate_credential_signature(data: Dict[str, Any], secret: str = SECRET_KEY) -> str:
    """Generate deterministic HMAC-SHA256 cryptographic signature for credential payload."""
    serialized = json.dumps(data, sort_keys=True)
    return hmac.new(secret.encode("utf-8"), serialized.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_credential_signature(data: Dict[str, Any], signature: str, secret: str = SECRET_KEY) -> bool:
    """Verify if HMAC-SHA256 signature matches credential data."""
    expected = generate_credential_signature(data, secret)
    return hmac.compare_digest(expected, signature)


# ==========================================
# Synthetic Candidate 1: CAND-001 (Valid ML)
# ==========================================

CAND_001_FILES = {
    "model.py": '''"""Fraud Detection Model Pipeline."""
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

    def fit(self, X_train, y_train):
        self.baseline.fit(X_train, y_train)
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test) -> dict:
        preds = self.model.predict(X_test)
        probs = self.model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average="binary")
        return {"roc_auc": round(auc, 4), "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}

    def save(self, filepath: str):
        joblib.dump(self.model, filepath)
''',
    "preprocessing.py": '''"""Data Preprocessing & Feature Engineering Module."""
import pandas as pd
from sklearn.preprocessing import RobustScaler

def clean_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=["amount", "timestamp", "user_id"])
    cleaned["hour_of_day"] = pd.to_datetime(cleaned["timestamp"]).dt.hour
    cleaned["is_night_transaction"] = cleaned["hour_of_day"].apply(lambda h: 1 if (h < 6 or h > 22) else 0)
    return cleaned

def fit_scaler(X_train: pd.DataFrame) -> RobustScaler:
    scaler = RobustScaler()
    scaler.fit(X_train[["amount", "frequency_score"]])
    return scaler

def transform_features(X: pd.DataFrame, scaler: RobustScaler) -> pd.DataFrame:
    X_scaled = X.copy()
    X_scaled[["amount", "frequency_score"]] = scaler.transform(X[["amount", "frequency_score"]])
    return X_scaled
''',
    "train.py": '''"""Training and Cross-Validation Pipeline."""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from preprocessing import clean_transaction_data, fit_scaler, transform_features
from model import FraudDetector

def run_training():
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
        detector.fit(X_tr_s, y_tr)
        metrics = detector.evaluate(X_val_s, y_val)
        auc_scores.append(metrics["roc_auc"])

    return {"mean_roc_auc": np.mean(auc_scores), "folds": auc_scores}

if __name__ == "__main__":
    results = run_training()
    print(f"Stratified CV Mean ROC-AUC: {results['mean_roc_auc']:.4f}")
''',
    "test_model.py": '''"""Automated Test Suite for Fraud Detector."""
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

def test_model_evaluation_metrics():
    X_train = np.array([[1.0, 2.0], [2.0, 3.0], [0.5, 1.0], [3.0, 4.0]])
    y_train = np.array([0, 0, 1, 0])
    detector = FraudDetector(n_estimators=10)
    detector.fit(X_train, y_train)
    eval_res = detector.evaluate(X_train, y_train)
    assert "roc_auc" in eval_res
    assert "precision" in eval_res
    assert "recall" in eval_res
''',
    "requirements.txt": '''scikit-learn>=1.4.0
pandas>=2.2.0
numpy>=1.26.0
joblib>=1.3.0
pytest>=8.0.0
''',
    "README.md": '''# Fraud Detection ML Service
Real-time credit transaction anomaly detection using robust scaling and balanced Random Forests.
'''
}

CAND_001_GIT_HISTORY = [
    {
        "hash": "d4a8e19",
        "date": "2026-10-24 14:22:10",
        "author": "CAND-001 <cand001@synthetic.dev>",
        "message": "feat(core): initial transaction schema and robust feature scaling",
        "files_changed": 2,
        "insertions": 84,
        "deletions": 0
    },
    {
        "hash": "b2c910f",
        "date": "2026-10-26 11:05:42",
        "author": "CAND-001 <cand001@synthetic.dev>",
        "message": "feat(model): implement FraudDetector with balanced class weights and ROC-AUC evaluation",
        "files_changed": 1,
        "insertions": 48,
        "deletions": 6
    },
    {
        "hash": "f81d44c",
        "date": "2026-10-28 16:30:15",
        "author": "CAND-001 <cand001@synthetic.dev>",
        "message": "refactor(train): add StratifiedKFold to prevent data leakage across validation folds",
        "files_changed": 1,
        "insertions": 52,
        "deletions": 18
    },
    {
        "hash": "7e3b9aa",
        "date": "2026-10-30 09:12:00",
        "author": "CAND-001 <cand001@synthetic.dev>",
        "message": "test: add comprehensive pytest suite for preprocessing and model evaluation",
        "files_changed": 1,
        "insertions": 45,
        "deletions": 0
    }
]

CAND_001_AGENT_TIMELINE = [
    {
        "agent": "Planning Agent",
        "action": "Decompose Verification Plan",
        "tool": "plan_pipeline",
        "observation": "Identified claimed skills: Python (Advanced), Machine Learning (Intermediate/Advanced). Target repo: fraud-detection-ml.",
        "result": "Created 5-stage agent verification plan: Repo Inspection -> Static Code Analysis -> Git Authenticity -> Skill Evidence Scoring -> Viva Generation.",
        "timestamp": "10:14:02"
    },
    {
        "agent": "Repository Inspector",
        "action": "Clone & Parse Project Tree",
        "tool": "repo_tree_analyzer",
        "observation": "Found 6 project files. Valid README, modular structure, requirements.txt specifies scikit-learn, pandas, numpy, pytest.",
        "result": "Verified project structure is well-architected. Detected test_model.py with unit test coverage.",
        "timestamp": "10:14:15"
    },
    {
        "agent": "Code Analysis Agent",
        "action": "AST & Quality Inspection",
        "tool": "ast_code_parser",
        "observation": "Analyzed model.py, preprocessing.py, train.py. Found type annotations, robust scaling to handle outliers, and StratifiedKFold cross-validation.",
        "result": "Observed 0 critical syntax or logic bugs. Code exhibits idiomatic Python 3 standards.",
        "timestamp": "10:14:28"
    },
    {
        "agent": "Git History Analyzer",
        "action": "Commit Timeline & Diff Analysis",
        "tool": "git_log_inspector",
        "observation": "Inspected 4 historical commits across 7 days. Incremental feature additions, authentic commit messages, logical refactoring progression.",
        "result": "Git authenticity verified: Natural engineering cadence with no bulk single-commit paste patterns.",
        "timestamp": "10:14:41"
    },
    {
        "agent": "Evidence Evaluator",
        "action": "Execute Test Harness & Calculate Evidence",
        "tool": "test_runner & scoring_engine",
        "observation": "Ran test suite: 3 test suites passed (100% pass rate). ROC-AUC reaches 0.941. Clean separation of concerns.",
        "result": "Calculated Skill Evidence Scores: Python: 94/100, Machine Learning: 92/100. Overall Evidence Confidence: 93%.",
        "timestamp": "10:14:55"
    },
    {
        "agent": "Re-planning Agent",
        "action": "Adaptive Verification Check",
        "tool": "planner_recheck",
        "observation": "Confidence thresholds exceeded. Low anomaly score. No need for deeper secondary AST disassembly.",
        "result": "Approved progression directly to Viva Interview Question Generation.",
        "timestamp": "10:15:02"
    },
    {
        "agent": "Viva Preparation Agent",
        "action": "Generate Targeted Technical Viva",
        "tool": "viva_generator",
        "observation": "Formulated 3 deep technical viva questions targeting specific architectural decisions in candidate's preprocessing and train.py code.",
        "result": "Viva questions compiled and ready for candidate interview.",
        "timestamp": "10:15:14"
    },
    {
        "agent": "Human Reviewer Checkpoint",
        "action": "Awaiting Human Reviewer Approval",
        "tool": "reviewer_gate",
        "observation": "All automated stages completed successfully with high confidence.",
        "result": "Pending final human auditor sign-off.",
        "timestamp": "10:15:20"
    }
]

CAND_001_SKILL_EVIDENCE = {
    "overall_score": 93,
    "confidence": "High",
    "skills": {
        "Python": {
            "score": 94,
            "coverage": 96,
            "supporting_files": ["model.py", "preprocessing.py", "train.py", "test_model.py"],
            "implementation_findings": [
                "Idiomatic object-oriented class design with encapsulated estimator (`FraudDetector`).",
                "Explicit type hinting on function arguments and return types (`-> dict`, `-> pd.DataFrame`).",
                "Clean modular imports and proper `__name__ == '__main__'` entrypoint separation."
            ],
            "test_results": "3 of 3 unit tests passed (100% pass rate) via pytest harness.",
            "limitations": "Does not enforce strict mypy static type checking configurations.",
            "suspicious_indicators": "None. Coding style and git commit cadence align with legitimate original work."
        },
        "Machine Learning": {
            "score": 92,
            "coverage": 90,
            "supporting_files": ["model.py", "train.py", "preprocessing.py"],
            "implementation_findings": [
                "Class-imbalance compensation using `class_weight='balanced'` in RandomForest.",
                "Robust scaling (`RobustScaler`) prevents transaction amount outliers from distorting gradients.",
                "Rigorous `StratifiedKFold` cross-validation with fold-isolated scaling to eliminate data leakage."
            ],
            "test_results": "ROC-AUC metric verified at 0.941 across validation splits; precision/recall trade-off properly computed.",
            "limitations": "Model hyperparameter exploration is currently hardcoded rather than driven by Optuna or automated Bayesian search.",
            "suspicious_indicators": "None. Architectural choices reflect practical applied ML domain expertise."
        }
    },
    "evidence_breakdown": {
        "observed_evidence": [
            "Source code files present: model.py, preprocessing.py, train.py, test_model.py.",
            "Pytest test cases executing with 100% pass rate.",
            "Realistic multi-day Git commit history with incremental improvements."
        ],
        "ai_generated_inference": [
            "Inferred high proficiency in preventing data leakage based on train-val fold scaling.",
            "Inferred understanding of financial anomaly distributions from use of RobustScaler over MinMaxScaler."
        ],
        "missing_evidence": [
            "No automated CI/CD GitHub Actions workflow file found in repository.",
            "No Dockerfile container packaging evidence present."
        ],
        "suspicion_notes": "No anomalies detected. (Informational note: Anomaly heuristics require human oversight and do not constitute proof of plagiarism)."
    }
}

CAND_001_VIVA_QUESTIONS = [
    {
        "id": "Q1",
        "question": "In `preprocessing.py`, why did you apply feature scaling (`fit_scaler`) after splitting the dataset into folds rather than fitting the scaler once on the entire dataset upfront?",
        "context": "Targets data leakage awareness in preprocessing pipeline.",
        "sample_answer": "Fitting the scaler on the whole dataset before cross-validation would cause data leakage because test/validation fold statistics (like medians and IQR) would leak into the training features. Fitting solely on the training fold guarantees an unbiased performance estimate.",
        "evaluation": {
            "technical_correctness": 96,
            "understanding": 98,
            "explanation_quality": 94,
            "evidence_alignment": 95,
            "feedback": "Outstanding answer. Candidate accurately identified data leakage risks and correctly explained why quantile/median statistics must remain fold-isolated."
        }
    },
    {
        "id": "Q2",
        "question": "In `model.py`, why did you prioritize `roc_auc` and PR metrics over standard `accuracy` when evaluating the FraudDetector?",
        "context": "Targets class imbalance evaluation knowledge in machine learning.",
        "sample_answer": "In fraud detection, the target classes are severely imbalanced (typically 95%+ non-fraud). A naive model predicting all zeros would attain 95% accuracy while catching zero fraud cases. ROC-AUC and Precision-Recall F1 evaluate ranking ability and minority-class recall regardless of baseline class frequency.",
        "evaluation": {
            "technical_correctness": 95,
            "understanding": 97,
            "explanation_quality": 95,
            "evidence_alignment": 96,
            "feedback": "Precise and complete reasoning. Directly explains why standard accuracy is misleading on skewed classification distributions."
        }
    },
    {
        "id": "Q3",
        "question": "How did you configure `FraudDetector` in `model.py` to handle the low frequency of fraudulent transactions during tree induction?",
        "context": "Targets algorithmic adaptation for minority class representation.",
        "sample_answer": "I set `class_weight='balanced'` in the RandomForestClassifier. This automatically adjusts sample weights inversely proportional to class frequencies, forcing split criteria like Gini/Entropy to penalize misclassifications of fraudulent records much more heavily.",
        "evaluation": {
            "technical_correctness": 94,
            "understanding": 95,
            "explanation_quality": 92,
            "evidence_alignment": 94,
            "feedback": "Clear explanation of sample weighting mechanics and split criterion sensitivity."
        }
    }
]

# ==========================================
# Synthetic Candidate 2: CAND-002 (Insufficient Evidence)
# ==========================================

CAND_002_SESSION = {
    "session_id": "sess_cand002_fail",
    "candidate_id": "CAND-002",
    "repo_url": "https://github.com/synthetic-lab/empty-stub-repo",
    "claimed_skills": ["Python", "FastAPI", "SQL"],
    "status": "completed",
    "approval_status": "rejected",
    "overall_score": 24,
    "confidence": "Low",
    "recommendation": "reject",
    "skills": {
        "Python": {
            "score": 35,
            "coverage": 30,
            "supporting_files": ["main.py"],
            "implementation_findings": ["Contains 12 lines of basic script with no functions or classes."],
            "test_results": "No test files located in repository.",
            "limitations": "Lack of unit tests, lack of type annotations, no structure.",
            "suspicious_indicators": "Single initial commit timestamped 10 minutes prior to submission."
        },
        "FastAPI": {
            "score": 20,
            "coverage": 15,
            "supporting_files": ["main.py"],
            "implementation_findings": ["One GET '/' endpoint returning static JSON string 'Hello World'."],
            "test_results": "No API tests or TestClient scripts found.",
            "limitations": "No models (Pydantic), no routers, no dependency injection, no authentication.",
            "suspicious_indicators": "Verbatim copy of FastAPI introductory tutorial snippet."
        },
        "SQL": {
            "score": 0,
            "coverage": 0,
            "supporting_files": [],
            "implementation_findings": ["Zero database connection files, models, or migrations."],
            "test_results": "N/A",
            "limitations": "Claimed skill completely absent from codebase.",
            "suspicious_indicators": "Skill claimed without any supporting repository evidence."
        }
    },
    "reviewer_notes": "Rejected: Candidate claimed advanced SQL and FastAPI, but repository contains only a single-file 'Hello World' tutorial copy without tests or database interaction."
}


def get_demo_session(candidate_id: str = "CAND-001") -> Dict[str, Any]:
    """Retrieve complete precomputed deterministic session data for demo presentation."""
    if candidate_id == "CAND-002":
        return CAND_002_SESSION

    session_id = "sess_cand001_demo_verified"
    credential_payload = {
        "credential_id": "SP-CRED-2026-001",
        "candidate_id": "CAND-001",
        "verified_skills": [
            {"skill": "Python", "score": 94, "level": "Advanced"},
            {"skill": "Machine Learning", "score": 92, "level": "Advanced"}
        ],
        "evidence_summary": {
            "overall_score": 93,
            "test_pass_rate": 1.0,
            "repo_url": "https://github.com/synthetic-lab/fraud-detection-ml",
            "audit_verdict": "Verified & Approved"
        },
        "viva_result": {
            "average_score": 95.3,
            "assessment": "Demonstrated authentic implementation knowledge."
        },
        "issuer": "SkillProof AI Autonomous Verification Authority",
        "issued_at": "2026-10-31T10:15:30Z",
        "status": "VALID"
    }

    sig = generate_credential_signature(credential_payload)

    return {
        "session_id": session_id,
        "candidate_id": "CAND-001",
        "repo_url": "https://github.com/synthetic-lab/fraud-detection-ml",
        "claimed_skills": ["Python", "Machine Learning"],
        "status": "completed",
        "approval_status": "approved",
        "overall_score": 93,
        "confidence": "High",
        "recommendation": "approve",
        "timeline": CAND_001_AGENT_TIMELINE,
        "repository_files": CAND_001_FILES,
        "git_history": CAND_001_GIT_HISTORY,
        "skill_evidence": CAND_001_SKILL_EVIDENCE,
        "viva_questions": CAND_001_VIVA_QUESTIONS,
        "approval": {
            "decision": "approved",
            "reviewer_notes": "Exemplary implementation. All 3 unit tests pass, StratifiedKFold correctly prevents leakage, and candidate's viva explanations demonstrated authentic ownership.",
            "reviewer_id": "rev_lead_01",
            "timestamp": "2026-10-31T10:15:25Z"
        },
        "credential": {
            "credential_id": "SP-CRED-2026-001",
            "data": credential_payload,
            "signature": sig,
            "signature_algorithm": "HMAC-SHA256",
            "status": "VALID"
        }
    }


def get_mock_dashboard_stats() -> Dict[str, Any]:
    """Retrieve top-level dashboard metrics for the platform."""
    return {
        "total_analyzed": 48,
        "verified_credentials": 34,
        "pending_approvals": 5,
        "rejected_candidates": 9,
        "avg_evidence_score": 84.6,
        "recent_verifications": [
            {"candidate_id": "CAND-001", "skills": "Python, ML", "score": 93, "status": "Approved", "date": "10 min ago"},
            {"candidate_id": "CAND-PY-01", "skills": "Python, FastAPI", "score": 88, "status": "Approved", "date": "1 hour ago"},
            {"candidate_id": "CAND-002", "skills": "Python, FastAPI, SQL", "score": 24, "status": "Rejected", "date": "2 hours ago"},
            {"candidate_id": "CAND-REACT-02", "skills": "React, JavaScript", "score": 92, "status": "Approved", "date": "3 hours ago"},
            {"candidate_id": "CAND-TST-05", "skills": "Python, FastAPI", "score": 42, "status": "Rejected", "date": "4 hours ago"}
        ]
    }
