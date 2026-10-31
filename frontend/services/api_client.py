import json
import logging
from typing import Any, Dict, List, Optional, Tuple
import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

logger = logging.getLogger(__name__)


class APIClient:
    """Client for interacting with the SkillProof AI FastAPI backend."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def check_health(self) -> Tuple[bool, str]:
        """Check if backend /health endpoint responds.

        Returns (is_healthy, message).
        """
        try:
            url = f"{self.base_url}/health"
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json() if resp.content else {}
                return True, data.get("status", "healthy")
            return False, f"Backend returned HTTP {resp.status_code}"
        except (ConnectionError, Timeout):
            return False, f"Could not connect to backend at {self.base_url} (Connection refused/timeout)"
        except Exception as e:
            return False, f"Health check failed: {str(e)}"

    def start_analysis(
        self, candidate_id: str, repo_url: str, claimed_skills: List[str]
    ) -> Tuple[bool, Dict[str, Any], str]:
        """Call POST /api/analyze to trigger agentic skill verification.

        Returns (success, response_dict, error_message).
        """
        url = f"{self.base_url}/api/analyze"
        payload = {
            "candidate_id": candidate_id,
            "repo_url": repo_url,
            "claimed_skills": claimed_skills,
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code in (200, 201, 202):
                return True, resp.json(), ""
            return False, {}, f"API error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable at {self.base_url}: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def get_session(self, session_id: str) -> Tuple[bool, Dict[str, Any], str]:
        """Call GET /api/session/{session_id} to fetch real-time session progress and findings.

        Returns (success, session_dict, error_message).
        """
        url = f"{self.base_url}/api/session/{session_id}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                return True, resp.json(), ""
            return False, {}, f"Session not found or error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def submit_viva_answer(
        self, session_id: str, question_id: str, answer: str
    ) -> Tuple[bool, Dict[str, Any], str]:
        """Call POST /api/viva/{session_id}/answer.

        Returns (success, evaluation_result, error_message).
        """
        url = f"{self.base_url}/api/viva/{session_id}/answer"
        payload = {
            "question_id": question_id,
            "answer": answer,
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                return True, resp.json(), ""
            return False, {}, f"API error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def submit_approval(
        self, session_id: str, decision: str, reviewer_notes: str, reviewer_id: str = "rev_lead_01"
    ) -> Tuple[bool, Dict[str, Any], str]:
        """Call POST /api/approve/{session_id}.

        decision: 'approved' | 'rejected'
        """
        url = f"{self.base_url}/api/approve/{session_id}"
        payload = {
            "decision": decision,
            "reviewer_notes": reviewer_notes,
            "reviewer_id": reviewer_id,
        }
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                return True, resp.json(), ""
            return False, {}, f"Approval error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def issue_credential(self, session_id: str) -> Tuple[bool, Dict[str, Any], str]:
        """Call POST /api/credential/{session_id}/issue."""
        url = f"{self.base_url}/api/credential/{session_id}/issue"
        try:
            resp = requests.post(url, timeout=self.timeout)
            if resp.status_code in (200, 201):
                return True, resp.json(), ""
            return False, {}, f"Issuance error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def get_credential(self, credential_id: str) -> Tuple[bool, Dict[str, Any], str]:
        """Call GET /api/credential/{credential_id}."""
        url = f"{self.base_url}/api/credential/{credential_id}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                return True, resp.json(), ""
            return False, {}, f"Credential fetch error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"

    def verify_credential(self, credential_id: str) -> Tuple[bool, Dict[str, Any], str]:
        """Call GET /api/credential/{credential_id}/verify.

        Returns (is_valid, verification_data, error_message).
        """
        url = f"{self.base_url}/api/credential/{credential_id}/verify"
        try:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                is_valid = data.get("status") == "VALID" or data.get("valid", False) is True
                return is_valid, data, ""
            return False, {}, f"Verification error {resp.status_code}: {resp.text}"
        except (ConnectionError, Timeout) as e:
            return False, {}, f"Backend unreachable: {e}"
        except Exception as e:
            return False, {}, f"Request failed: {str(e)}"
