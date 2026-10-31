import os
import sys
import pytest

# Ensure skillproof/frontend is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skillproof", "frontend")))

from services.session_manager import (
    compute_signature,
    verify_signature,
    get_default_aegis_session,
)
from evaluation.run_evaluation import run_benchmark, load_test_cases
from services.api_client import APIClient


def test_aegis_data_structure():
    """Verify CAND-001 AegisAI demonstration structures."""
    cand1 = get_default_aegis_session()
    assert cand1["candidate_id"] == "CAND-001"
    assert cand1["repo_url"] == "https://github.com/arshavardhan/AegisAi"
    assert "timeline" in cand1
    assert "code_files" in cand1
    assert "aegis/core/base.py" in cand1["code_files"]
    assert "aegis/uncertainty/monte_carlo.py" in cand1["code_files"]


def test_cryptographic_signature_validity():
    """Verify HMAC-SHA256 signature generation and canonical verification."""
    payload = {
        "credential_id": "SP-CRED-2026-AEGIS-01",
        "candidate_id": "CAND-001",
        "score": 94,
        "skills": ["Python", "Machine Learning"]
    }
    sig = compute_signature(payload)
    assert isinstance(sig, str) and len(sig) == 64  # SHA256 hex length
    assert verify_signature(payload, sig) is True


def test_cryptographic_tamper_detection():
    """Verify tamper detection: modifying payload must invalidate signature."""
    genuine_payload = {
        "credential_id": "SP-CRED-2026-AEGIS-01",
        "candidate_id": "CAND-001",
        "level": "Junior Engineer",
        "score": 75
    }
    sig = compute_signature(genuine_payload)

    # Malicious actor tampers with level
    tampered_payload = genuine_payload.copy()
    tampered_payload["level"] = "Principal AI Architect"

    assert verify_signature(tampered_payload, sig) is False


def test_evaluation_benchmark_all_16_cases():
    """Verify 16-case deterministic evaluation benchmark achieves high fidelity."""
    cases = load_test_cases()
    assert len(cases) >= 15

    eval_output = run_benchmark()
    m = eval_output["metrics"]
    results = eval_output["results"]

    assert len(results) == 16
    assert m["total_test_cases"] == 16
    assert m["accuracy"] == 1.0
    assert m["precision"] == 1.0
    assert m["recall"] == 1.0
    assert m["f1"] == 1.0
    assert m["credential_verification_rate"] == 1.0


def test_api_client_graceful_error_handling():
    """Verify APIClient gracefully handles unreachable backend without unhandled crash."""
    client = APIClient(base_url="http://127.0.0.1:9999", timeout=1)
    healthy, msg = client.check_health()
    assert healthy is False
    assert "Cannot connect" in msg or "Ensure Laptop 1 is running" in msg

    success, data, err = client.start_analysis("TEST-01", "https://github.com/fake/repo", ["Python"])
    assert success is False
    assert len(err) > 0
