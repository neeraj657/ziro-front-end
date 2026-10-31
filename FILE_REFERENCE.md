# 📁 SkillProof AI — Complete File Reference & Inventory

> **Document Purpose**: Exhaustive, line-by-line engineering breakdown of every source file, component, service, test, and dataset in the SkillProof AI repository.

---

## 1. Directory Tree & Architecture Overview

```
c:\Users\K.R.NEERAJ\Downloads\ziro frontend\
├── app.py                          # Root Streamlit Launcher (delegates to skillproof/frontend)
├── README.md                       # Comprehensive platform documentation & setup guide
├── pytest.ini                      # Pytest runner configuration
├── .gitignore                      # Git exclusion rules (.venv, caches, etc.)
│
├── skillproof/                     # Master Enterprise Application Package
│   └── frontend/
│       ├── app.py                  # Master Streamlit router across 12 pages
│       ├── config.py               # Application constants, design tokens, skills taxonomy
│       ├── requirements.txt        # Runtime Python dependencies
│       ├── .env.example            # Environment configuration template
│       │
│       ├── assets/
│       │   └── styles.css          # Production Navy / Dark Slate / Royal Blue CSS System
│       │
│       ├── services/
│       │   ├── api_client.py       # Robust HTTP REST client for FastAPI backend (Laptop 1)
│       │   ├── session_manager.py  # Reactive session state store, empty session init, HMAC signing
│       │   └── validators.py       # Strict HTTPS GitHub URL & Candidate ID validation
│       │
│       ├── components/
│       │   ├── sidebar.py          # Persistent navigation sidebar & backend health status
│       │   ├── dashboard.py        # Overview dashboard with dynamic input & zero synthetic data
│       │   ├── candidate_form.py   # Candidate submission form & pipeline dispatch
│       │   ├── agent_timeline.py   # Multi-agent execution DAG & re-planning trace
│       │   ├── repository_explorer.py # Discovered module tree & package inspection
│       │   ├── code_inspector.py   # AST class/function extractor & complexity viewer
│       │   ├── evidence_graph.py   # Skill evidence cards & classification filtering
│       │   ├── test_results.py     # Sandboxed pytest execution telemetry & assertions
│       │   ├── git_analysis.py     # Git forensics, commit cadence, diff distribution
│       │   ├── originality_analysis.py # AST similarity scanner & ethical boilerplate audit
│       │   ├── skill_assessment.py # Plotly radar charts & dual-axis score breakdown
│       │   ├── viva_interface.py   # Code-specific viva Q&A with 5-metric AI evaluation
│       │   ├── reviewer_console.py # Mandatory human auditor approval gate
│       │   ├── credential_viewer.py# HMAC-SHA256 certificate, employer verify, tamper sandbox
│       │   └── evaluation_dashboard.py # 16-case benchmark metrics & confusion matrix
│       │
│       ├── pages/                  # 12 lightweight Streamlit page router endpoints
│       │   ├── overview.py
│       │   ├── verification.py
│       │   ├── agent_workspace.py
│       │   ├── repository_intelligence.py
│       │   ├── evidence_explorer.py
│       │   ├── git_forensics.py
│       │   ├── originality.py
│       │   ├── skill_assessment.py
│       │   ├── technical_viva.py
│       │   ├── reviewer_approval.py
│       │   ├── credentials.py
│       │   └── evaluation_lab.py
│       │
│       ├── evaluation/
│       │   ├── test_cases.json     # 16 deterministic benchmark test cases
│       │   ├── run_evaluation.py   # Benchmark execution engine (CLI & UI)
│       │   ├── metrics.py          # Accuracy, precision, recall, F1, confusion matrix
│       │   └── test_evaluation.py  # Pytest test file for evaluation metrics
│       │
│       └── tests/
│           ├── test_api_client.py  # API client error handling & connection tests
│           ├── test_session_state.py# Session state store & cryptographic HMAC tests
│           ├── test_evaluation_ui.py# 16-case benchmark suite test
│           └── test_submission_flow.py # HTTPS URL validation & candidate ID tests
│
├── frontend/                       # Alternate / Prototype Frontend Package
│   ├── app.py                      # Prototype Streamlit launcher
│   ├── config.py                   # Prototype design tokens
│   ├── requirements.txt            # Dependencies declaration
│   ├── components/                 # Prototype components (delegates to master dashboard)
│   ├── services/                   # Prototype services (api_client, validators)
│   └── evaluation/                 # Prototype evaluation suite & synthetic data generator
│
├── demo_data/                      # Synthetic Repositories for Demonstration
│   ├── cand_001_ml_repo/           # Full ML project (model.py, preprocessing.py, train.py, tests)
│   └── cand_002_insufficient_repo/ # Stub repo with insufficient evidence (main.py)
│
└── tests/
    └── test_skillproof.py          # Root-level Pytest suite (Aegis fixture, HMAC, benchmark)
```

---

## 2. Core Root Files

### `app.py` (Root)
- **Purpose**: Master launcher script located at the workspace root to enable single-command startup (`streamlit run app.py`).
- **Imports**: `os`, `sys`.
- **Imported By**: User invocation via Streamlit CLI.
- **Main Logic**:
  - Dynamically prepends `skillproof/frontend` to `sys.path`.
  - Reads and executes `skillproof/frontend/app.py` using Python `exec()`.
- **Data In/Out**: No internal state; acts as an execution trampoline.
- **Dependencies**: Depends on the existence of `skillproof/frontend/app.py`.

### `README.md` (Root)
- **Purpose**: Complete platform architecture, installation, and presentation documentation.
- **Key Sections**: Windows installation steps, Two-Laptop network setup, API integration table, 14-step judge presentation walkthrough.

### `pytest.ini` (Root)
- **Purpose**: Defines automated test discovery rules.
- **Configured Paths**: `testpaths = skillproof/frontend/tests tests`.
- **Ignored Folders**: `demo_data`, `components`.
- **Naming Conventions**: `python_files = test_*.py`, `python_classes = Test*`, `python_functions = test_*`.

---

## 3. Services Layer (`skillproof/frontend/services/`)

### `validators.py`
- **Purpose**: Input validation engine preventing invalid or malicious inputs before network calls or session staging.
- **Imports**: `re`, `urllib.parse.urlparse`, `typing.Tuple`.
- **Imported By**: `skillproof/frontend/components/dashboard.py`, `candidate_form.py`, `tests/test_submission_flow.py`.
- **Key Functions**:
  1. `validate_github_url(url: str) -> Tuple[bool, str]`:
     - Enforces HTTPS-only scheme (`https://`).
     - Rejects `http://`, `ftp://`, or missing schemes.
     - Enforces exact hostname `github.com` or `www.github.com`.
     - Rejects deceptive domains (e.g., `github.com.example.com`).
     - Validates repository path structure: `https://github.com/owner/repo`.
     - Rejects reserved GitHub keywords (`login`, `settings`, `explore`, `trending`, `pricing`).
     - Validates regex characters `^[A-Za-z0-9_.-]+$`.
  2. `extract_github_repo_info(url: str) -> Tuple[str, str]`:
     - Parses URL and returns `(owner, repo_name)`.
     - Strips trailing `.git` extensions.
  3. `validate_candidate_id(cand_id: str) -> Tuple[bool, str]`:
     - Ensures candidate ID is non-empty, stripped of whitespace, and has a minimum length of 2 characters.
- **Data In**: Raw user strings from text input fields.
- **Data Out**: `(True, "")` or `(False, "Error message")`.

### `api_client.py`
- **Purpose**: Reusable HTTP REST client for communicating with the FastAPI backend on Laptop 1 (`http://127.0.0.1:8000`).
- **Imports**: `requests`, `json`, `logging`, `typing.Tuple`, `typing.Dict`, `typing.List`, `typing.Any`, `requests.exceptions`.
- **Imported By**: `sidebar.py`, `dashboard.py`, `candidate_form.py`, `viva_interface.py`, `reviewer_console.py`, `credential_viewer.py`, `tests/test_api_client.py`.
- **Key Class**: `APIClient(base_url: str, timeout: int)`
- **Methods**:
  - `_safe_request(method, endpoint, **kwargs) -> Tuple[bool, Any, str]`: Uniform error-handling wrapper catching `ConnectionError`, `Timeout`, and HTTP error codes (`400`, `401`, `404`, `422`, `500`).
  - `check_health() -> Tuple[bool, str]`: Queries `GET /health`.
  - `start_analysis(candidate_id, repo_url, claimed_skills, description) -> Tuple[bool, dict, str]`: Calls `POST /api/analyze`.
  - `get_session(session_id) -> Tuple[bool, dict, str]`: Queries `GET /api/session/{session_id}`.
  - `get_timeline(session_id) -> Tuple[bool, list, str]`: Queries `GET /api/session/{session_id}/timeline`.
  - `get_evidence(session_id) -> Tuple[bool, dict, str]`: Queries `GET /api/session/{session_id}/evidence`.
  - `get_report(session_id) -> Tuple[bool, dict, str]`: Queries `GET /api/session/{session_id}/report`.
  - `get_viva_questions(session_id) -> Tuple[bool, list, str]`: Queries `GET /api/viva/{session_id}/questions`.
  - `submit_viva_answer(session_id, question_id, answer) -> Tuple[bool, dict, str]`: Calls `POST /api/viva/{session_id}/answer`.
  - `submit_approval(session_id, decision, reviewer_notes, reviewer_id) -> Tuple[bool, dict, str]`: Calls `POST /api/approve/{session_id}`.
  - `issue_credential(session_id) -> Tuple[bool, dict, str]`: Calls `POST /api/credential/{session_id}/issue`.
  - `get_credential(credential_id) -> Tuple[bool, dict, str]`: Queries `GET /api/credential/{credential_id}`.
  - `verify_credential(credential_id, payload) -> Tuple[bool, dict, str]`: Calls `POST /api/credential/verify` with fallback to `GET /api/credential/{id}/verify`.
- **Data In**: Session IDs, candidate data, viva answers, reviewer approvals.
- **Data Out**: Parsed JSON responses or human-readable connection error messages.

### `session_manager.py`
- **Purpose**: Reactive state container managing `st.session_state`, candidate sessions, cryptographic HMAC signatures, and benchmark fixtures.
- **Imports**: `hashlib`, `hmac`, `json`, `datetime`, `streamlit as st`, `typing`.
- **Imported By**: Every component in `skillproof/frontend/components/` and all test suites.
- **Key Functions & Classes**:
  - `compute_signature(payload: dict, secret: str) -> str`: Produces a deterministic 64-character SHA256 hex digest over canonicalized JSON.
  - `verify_signature(payload: dict, signature: str, secret: str) -> bool`: Validates cryptographic integrity via `hmac.compare_digest()`.
  - `get_empty_session() -> dict`: Produces a clean initial state dictionary where candidate ID, repository URL, skills, and metrics are completely empty.
  - `get_default_aegis_session() -> dict`: Canonical deterministic fixture for `CAND-001` (`https://github.com/arshavardhan/AegisAi`) used in benchmark tests and offline demonstrations.
  - `SessionManager`: Static class exposing:
    - `init_session()`: Guarantees initialization of session state keys.
    - `get_session()`: Retrieves the active session dictionary.
    - `set_session(session_data)`: Replaces active session with backend data.
    - `clear_session()`: Resets all active candidate parameters to empty.

---

## 4. UI Components Layer (`skillproof/frontend/components/`)

| File Name | Purpose | Key Render Function | Key Interactions |
| :--- | :--- | :--- | :--- |
| `sidebar.py` | Navigation & connection telemetry | `render_sidebar()` | Shows active candidate pill, 12 navigation links, backend health badge, IP configuration. |
| `dashboard.py` | Overview & dynamic repository selection | `render_overview_dashboard()` | "START NEW VERIFICATION" section, empty input fields, "OPEN REPOSITORY" button, "PREPARE VERIFICATION" button with confirmation card. |
| `candidate_form.py` | Pipeline dispatch form | `render_candidate_submission_form()` | Form inputs for Candidate ID, GitHub URL, skills; dispatches `POST /api/analyze`; polls backend. |
| `agent_timeline.py` | Multi-agent execution visualizer | `render_agent_workspace_timeline()` | Visualizes DAG execution stages: Plan → Act → Observe → Critique → Re-Plan → Act Again → Verify. |
| `repository_explorer.py` | Codebase structure inspection | `render_repository_explorer()` | Shows target repo URL, owner/name, default branch, discovered package modules. |
| `code_inspector.py` | AST signature & complexity viewer | `render_code_inspector()` | Class hierarchies, method signatures, top-level imports, cyclomatic complexity scores. |
| `evidence_graph.py` | Skill evidence cards | `render_evidence_explorer()` | Granular cards mapping claimed skills to AST line ranges, passing tests, and findings. |
| `test_results.py` | Test verification report | `render_test_results()` | Pytest pass/fail counts, execution time, harness coverage, individual assertion records. |
| `git_analysis.py` | Git forensics & provenance | `render_git_forensics()` | Plotly commit code diff distribution (additions vs deletions), cumulative growth, author provenance. |
| `originality_analysis.py` | AST similarity & boilerplate audit | `render_originality_analysis()` | Originality index, boilerplate pattern matching, ethical auditing notice. |
| `skill_assessment.py` | Multidimensional scoring engine | `render_skill_assessment_dashboard()` | Dual Plotly radar chart comparing code implementation vs viva comprehension score. |
| `viva_interface.py` | Technical interview Q&A | `render_technical_viva()` | Code-specific questions, candidate answer input, 5-metric AI evaluation rubric. |
| `reviewer_console.py` | Human auditor checkpoint | `render_reviewer_approval_console()` | Mandatory sign-off gate (APPROVE / REJECT), auditor notes, audit dossier summary. |
| `credential_viewer.py` | Cryptographic credential ledger | `render_credential_viewer()` | Digital certificate display, JSON download, employer verification portal, live tamper rejection test. |
| `evaluation_dashboard.py` | Benchmark evaluation lab | `render_evaluation_dashboard()` | 16-case benchmark metrics (Accuracy, Precision, Recall, F1), confusion matrix heatmap, case ledger. |

---

## 5. Evaluation & Benchmark Framework (`skillproof/frontend/evaluation/`)

### `metrics.py`
- **Purpose**: Computes mathematical evaluation metrics for model and agent verification.
- **Key Function**:
  `calculate_metrics(y_true, y_pred, tool_successes, tool_totals, test_exec_successes, test_exec_totals, guardrail_successes, guardrail_totals, signatures_verified, signatures_tested) -> dict`
- **Outputs**:
  - `accuracy`: $(TP + TN) / \text{Total}$
  - `precision`: $TP / (TP + FP)$
  - `recall`: $TP / (TP + FN)$
  - `f1`: $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
  - `tool_success_rate`, `test_execution_success`, `guardrail_success`, `credential_verification_rate`
  - `confusion_matrix`: $2 \times 2$ matrix `[[TN, FP], [FN, TP]]`.

### `test_cases.json`
- **Purpose**: Deterministic dataset containing 16 benchmark test scenarios with exact expected outcomes (`ground_truth`, `status`, `recommendation`, `score`, `tool_success`, `test_success`, `guardrail_success`, `signature_valid`).

### `run_evaluation.py`
- **Purpose**: Harness that loads `test_cases.json`, evaluates each case (including live cryptographic verification for TC-16), and calls `calculate_metrics()`. Exposes `run_benchmark()` for both CLI execution and Streamlit UI display.

### `test_evaluation.py`
- **Purpose**: Pytest validation file ensuring that `test_cases.json` is structurally valid and `run_benchmark()` executes with 100% decision convergence.

---

## 6. Demonstration Datasets (`demo_data/`)

### `cand_001_ml_repo/`
- **Purpose**: Fully functional synthetic Machine Learning repository demonstrating exemplary engineering:
  - `model.py`: `FraudDetector` class wrapping `RandomForestClassifier` with balanced class weights and `LogisticRegression` baseline.
  - `preprocessing.py`: Outlier-resistant feature engineering with `RobustScaler`.
  - `train.py`: Data-leakage-free `StratifiedKFold` cross-validation.
  - `test_model.py`: Pytest suite with 100% passing unit tests.
  - `requirements.txt`: Standard ML dependencies.

### `cand_002_insufficient_repo/`
- **Purpose**: Minimal synthetic repository demonstrating insufficient evidence:
  - `main.py`: Single file containing `print("Hello World")`.
  - Zero models, zero tests, zero database drivers. Used to test rejection guardrails.

---

## 7. Architecture Code Audit & Findings

| Finding Category | File / Module | Observation | Action / Reality |
| :--- | :--- | :--- | :--- |
| **Duplicate Package** | `frontend/` vs `skillproof/frontend/` | `frontend/` was the initial prototype; `skillproof/frontend/` is the full 12-page enterprise architecture. | `app.py` in root delegates to `skillproof/frontend/app.py`. `frontend/components/dashboard.py` delegates to `skillproof/frontend/components/dashboard.py`. |
| **Clean Separation** | `services/api_client.py` | Strictly handles HTTP REST communication without importing backend packages. | Backend runs autonomously on Laptop 1; frontend runs on Laptop 2. |
| **Zero Synthetic Data** | `components/dashboard.py` | Candidate inputs start completely empty; no hardcoded repos or candidate IDs appear on load. | Verified; users can enter any valid public GitHub repository. |
| **Input Validation** | `services/validators.py` | Strict HTTPS validation, rejects deceptive domains (`github.com.example.com`). | Verified with 100% pass rate in `test_submission_flow.py`. |
| **Dead Code / Stubs** | `pages/*.py` | Each page file is 8 lines long, acting as a forwarder to `components/*.py`. | Intentional architectural design pattern to keep routing modular. |
