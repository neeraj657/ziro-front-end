# SkillProof AI — Frontend Application

This directory contains the Streamlit application, UI components, API services, and benchmark evaluation suite.

## Running the App
From workspace root:
```bash
streamlit run app.py
```
Or from within `frontend/`:
```bash
streamlit run app.py
```

## Structure
- `app.py`: Main Streamlit multi-page router with dark navy theme styling.
- `config.py`: Application parameters, design tokens, and candidate presets.
- `components/`: Modular UI widgets (dashboard, repository form, timeline, evidence charts, viva, approval, credential).
- `services/api_client.py`: Reusable HTTP client for FastAPI backend (`http://127.0.0.1:8000`).
- `evaluation/`: 12-case benchmark evaluation suite (`test_cases.json`, `run_evaluation.py`, `metrics.py`, `synthetic_data.py`).
