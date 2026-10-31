# 🛡️ SkillProof AI — Agentic Skill Verification Platform

> **Hackathon MVP**: Autonomous multi-agent candidate skill verification, static AST code auditing, git provenance checking, interactive technical viva, human-in-the-loop signoff, and cryptographically signed verifiable credentials.

---

## 🌟 Key Features

1. **Autonomous Multi-Agent Telemetry**:
   - **Planning Agent**: Decomposes candidate claims and target repository structure.
   - **Repository Inspector**: Clones tree, validates dependencies (`requirements.txt`, `package.json`).
   - **Code Analysis Agent**: AST parsing, type hints, code quality, idiomatic patterns.
   - **Git History Analyzer**: Audits commit timestamps, author provenance, and detects single-commit bulk dumps.
   - **Evidence Evaluator**: Runs automated test suites (`pytest`), computes coverage, and calculates multi-signal evidence scores.
   - **Re-planning Agent**: Dynamic adaptive depth adjustments.
   - **Viva Preparation Agent**: Generates targeted technical interview questions referencing the candidate's actual implementation code.
   - **Human Reviewer Checkpoint**: Strict human auditor sign-off gate before credential issuance.

2. **Categorized Evidence Dashboard**:
   - 🟢 **Observed Evidence**: Verifiable code, pytest test runs, and multi-day git commits.
   - 🟣 **AI Inference**: Architectural patterns, data leakage prevention, algorithm choice.
   - 🟡 **Missing Evidence**: Absent CI/CD, missing Dockerfiles, unverified claims.
   - ⚠️ **Anomaly & Plagiarism Policy**: Informational audit signals only; never claims proven plagiarism without human review.

3. **Interactive Candidate Viva**:
   - Code-specific architectural interview questions.
   - Instant AI evaluation on:
     - Technical Correctness
     - Conceptual Understanding
     - Explanation Quality
     - Evidence Alignment

4. **Cryptographic Credential Ledger**:
   - Generates tamper-evident verifiable credentials signed with **HMAC-SHA256**.
   - Employer verification portal (`GET /api/credential/{credential_id}/verify`).
   - Interactive **Tamper Rejection Demo** (Step 13) showing that altering even a single character in the credential payload invalidates the cryptographic signature.

5. **Deterministic 12-Case Benchmark Suite**:
   - Complete evaluation framework covering 12 distinct scenarios (Valid Python, React, ML repos, failing tests, empty repo, invalid URL, insufficient evidence, commit anomalies, viva failure, tampered signature).
   - Generates Accuracy (100%), Precision (100%), Recall (100%), F1-Score (1.000), Failure Handling Rate (100%), and Confusion Matrix.

---

## 📂 Project Structure

```
├── app.py                          # Root Streamlit launcher
├── README.md                       # Complete platform documentation
├── tests/
│   └── test_skillproof.py          # Pytest automated test suite
├── demo_data/
│   ├── README.md                   # Synthetic test data guide
│   ├── cand_001_ml_repo/           # Full synthetic ML project (model.py, train.py, etc.)
│   └── cand_002_insufficient_repo/ # Stub repo with insufficient evidence
└── frontend/
    ├── app.py                      # Main Streamlit dashboard application
    ├── config.py                   # Design tokens, API endpoints, candidate presets
    ├── requirements.txt            # Streamlit, Pandas, Plotly, Pytest, Requests
    ├── components/
    │   ├── sidebar.py              # Navigation, backend status indicator, demo presets
    │   ├── dashboard.py            # Executive KPI metrics and throughput charts
    │   ├── repository_form.py      # Candidate submission form with live polling
    │   ├── agent_timeline.py       # Live multi-agent execution timeline
    │   ├── evidence_view.py        # Skill radar chart, code viewer, git provenance
    │   ├── skill_charts.py         # Plotly radar, bar, donut, and confusion matrix charts
    │   ├── viva_interface.py       # Question-and-answer interview suite with grading
    │   ├── approval_panel.py       # Human auditor approval interface
    │   ├── credential_view.py      # Credential issuance, employer verify & tamper test
    │   └── evaluation_panel.py     # 12-case benchmark dashboard & confusion matrix
    ├── services/
    │   └── api_client.py           # Robust HTTP client for FastAPI backend
    └── evaluation/
        ├── test_cases.json         # 12 benchmark test cases with ground truth
        ├── run_evaluation.py       # Automated benchmark runner (CLI & UI)
        ├── metrics.py              # Precision, recall, F1, confusion matrix engine
        └── synthetic_data.py       # Deterministic datasets & HMAC cryptography
```

---

## 💻 Windows Setup & Installation Instructions

### Prerequisites
- Python 3.11+ installed on Windows
- Git (optional)

### Step 1: Open PowerShell or Command Prompt
Navigate to the project root:
```powershell
cd "c:\Users\K.R.NEERAJ\Downloads\ziro frontend"
```

### Step 2: Initialize & Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts execution scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r frontend\requirements.txt
```

### Step 4: Run the Application
Start the Streamlit application using either command:
```powershell
streamlit run app.py
```
or
```powershell
streamlit run frontend\app.py
```

The web interface will automatically open at:
`http://localhost:8501`

---

## 🧪 Running Automated Tests

Run the automated Pytest test suite:
```powershell
pytest tests -v
```

Execute the standalone 12-case benchmark CLI evaluation:
```powershell
python frontend\evaluation\run_evaluation.py
```

---

## 📡 API Integration Contract

The frontend connects to the FastAPI backend running at `http://127.0.0.1:8000` (configurable in the UI sidebar).

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check endpoint returning backend status |
| `POST` | `/api/analyze` | Initiates autonomous multi-agent repository verification |
| `GET` | `/api/session/{session_id}` | Polls verification status, agent timeline, and evidence |
| `POST` | `/api/viva/{session_id}/answer` | Submits candidate answers and returns AI rubric score |
| `POST` | `/api/approve/{session_id}` | Human reviewer formal sign-off (Approve / Reject) |
| `POST` | `/api/credential/{session_id}/issue` | Issues HMAC-SHA256 signed verifiable credential JSON |
| `GET` | `/api/credential/{credential_id}` | Fetches issued credential metadata |
| `GET` | `/api/credential/{credential_id}/verify`| Employer verification returning `VALID` or `INVALID` |

### ⚡ Fallback Demo Mode
If the FastAPI backend is temporarily offline, SkillProof AI automatically activates **Fallback Demo Mode**:
- Displays a prominent status pill: `[DEMO DATA]`
- Prevents UI crashes and preserves full interactivity for judges
- Uses deterministic synthetic data for `CAND-001` (Pass) and `CAND-002` (Fail)
- Never claims fake backend responses as real analysis

---

## 🎯 14-Step Presentation Walkthrough for Hackathon Judges

1. **Step 1 — Open Dashboard**: View platform metrics (48 analyzed, 34 verified, 84.6% avg score).
2. **Step 2 — Verify Candidate**: Open "Verify Candidate", click "🧪 Populate CAND-001 (Valid ML Engineer)".
3. **Step 3 — Start Agent Analysis**: Click `🚀 Start Autonomous Verification Pipeline` and observe live polling / agent dispatch.
4. **Step 4 — Live Agent Execution Timeline**: Inspect the chronological trace across Planning, Repository Inspector, AST Parser, Git Analyzer, and Evidence Evaluator.
5. **Step 5 — Repository & Git Inspection**: Navigate to "Skill Evidence" and explore `model.py`, `preprocessing.py`, and the 4-commit git log across 7 days.
6. **Step 6 — Skill Scores**: Review Plotly radar chart, coverage bars, and the Three-Way Category breakdown (Observed, AI Inference, Missing).
7. **Step 7 — Candidate Viva**: Switch to "Viva Interview", review generated questions, and click `📝 Auto-fill Answer (Q1)`.
8. **Step 8 — AI Evaluation**: Click `📤 Submit Answer (Q1)` to inspect technical correctness (96%), understanding (98%), and feedback.
9. **Step 9 — Human Reviewer Checkpoint**: Switch to "Credential Verification" -> "1. Reviewer Sign-Off". Notice that credentials cannot be issued without human approval.
10. **Step 10 — Approve Candidate**: Select "Approve Candidate", enter auditor notes, and submit formal sign-off.
11. **Step 11 — Issue Signed Credential**: Switch to "2. Issue Credential", click `⚡ Issue Cryptographically Signed Credential`, view digital certificate and click `📥 Download Signed Credential (JSON)`.
12. **Step 12 — Verify Credential as Employer**: Switch to "3. Employer Verification", click `🔍 Verify Authenticity` and observe `STATUS: VALID CREDENTIAL`.
13. **Step 13 — Tamper Detection Test**: Switch to "4. Tamper Detection Test", click `🛡️ Execute Cryptographic Tamper Test` and demonstrate `🚨 INVALID — HMAC SIGNATURE MISMATCH DETECTED` when a payload is modified.
14. **Step 14 — 12-Case Evaluation Benchmark**: Navigate to "Evaluation Metrics", run the automated harness, and inspect the 100% accuracy metrics and confusion matrix.

