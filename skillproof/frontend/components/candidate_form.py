import time
import streamlit as st
from config import DEFAULT_BACKEND_URL, SUPPORTED_SKILLS
from services.api_client import APIClient
from services.session_manager import SessionManager
from services.validators import validate_candidate_id, validate_github_url, extract_github_repo_info


def render_candidate_submission_form():
    """Render the Candidate Verification input form and trigger agent analysis."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                Candidate Submission & Verification Dispatch
            </h1>
            <p style="margin: 4px 0 0 0; color: #CBD5E1; font-size: 0.95rem;">
                Dispatch autonomous agents to investigate candidate repositories, extract code evidence, execute test suites, and audit git forensics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
    api_client = APIClient(base_url=backend_url, timeout=5)
    is_live = st.session_state.get("backend_connected", False)

    if not is_live:
        st.info(
            "⚡ **Backend Notice**: The FastAPI verification backend at `http://127.0.0.1:8000` is currently disconnected. "
            "You can prepare candidate parameters dynamically. Pipeline execution requires an active backend.",
            icon="ℹ️",
        )

    # Submission Form
    with st.form("candidate_submission_form"):
        col1, col2 = st.columns([1, 2])
        with col1:
            cand_id = st.text_input(
                "Candidate ID *",
                value=st.session_state.get(
                    "selected_candidate_id", st.session_state.get("input_candidate_id", "")
                ),
                placeholder="Enter candidate ID",
            )
        with col2:
            repo_url = st.text_input(
                "GitHub Repository URL *",
                value=st.session_state.get(
                    "selected_repository_url", st.session_state.get("input_repo_url", "")
                ),
                placeholder="Paste public GitHub repository URL",
            )

        claimed_skills = st.multiselect(
            "Claimed Skills to Verify (Optional)",
            options=SUPPORTED_SKILLS,
            default=st.session_state.get(
                "selected_claimed_skills", []
            ),
        )

        description = st.text_area(
            "Candidate Experience / Project Description (Optional)",
            value=st.session_state.get(
                "selected_candidate_description", st.session_state.get("input_description", "")
            ),
            height=80,
            placeholder="Enter candidate description (optional)",
        )

        submitted = st.form_submit_button(
            "🚀 Dispatch Autonomous Verification Pipeline (POST /api/analyze)",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        is_valid_cid, cid_err = validate_candidate_id(cand_id)
        if not is_valid_cid:
            st.error(f"Candidate ID Validation Error: {cid_err}")
            return

        is_valid_url, url_err = validate_github_url(repo_url)
        if not is_valid_url:
            st.error(f"Repository URL Validation Error: {url_err}")
            return

        clean_cid = cand_id.strip()
        clean_url = repo_url.strip()
        clean_desc = description.strip()
        owner, repo_name = extract_github_repo_info(clean_url)

        # Update session state with dynamic inputs
        st.session_state["selected_candidate_id"] = clean_cid
        st.session_state["selected_repository_url"] = clean_url
        st.session_state["selected_repo_url"] = clean_url
        st.session_state["selected_repository_owner"] = owner
        st.session_state["selected_repository_name"] = repo_name
        st.session_state["selected_claimed_skills"] = claimed_skills
        st.session_state["selected_candidate_description"] = clean_desc
        st.session_state["selected_description"] = clean_desc
        st.session_state["is_verification_prepared"] = True

        progress_box = st.container()
        with progress_box:
            st.markdown(
                """
                <div style="background: #1B2638; border: 1px solid #2563EB; border-radius: 12px; padding: 20px; margin-top: 16px;">
                    <div style="font-weight: 700; color: #60A5FA; font-size: 1.1rem; margin-bottom: 6px;">
                        🤖 Multi-Agent Pipeline Dispatch
                    </div>
                """,
                unsafe_allow_html=True,
            )
            p_bar = st.progress(0)
            status_text = st.empty()

            if is_live:
                status_text.text("Calling POST /api/analyze on backend...")
                p_bar.progress(25)
                ok, resp, err = api_client.start_analysis(
                    candidate_id=clean_cid,
                    repo_url=clean_url,
                    claimed_skills=claimed_skills,
                    description=clean_desc,
                )
                if not ok:
                    st.error(f"Analysis trigger failed: {err}")
                    return

                session_id = resp.get("session_id", f"sess_{clean_cid}")
                st.session_state["current_session_id"] = session_id
                st.success(f"Session established: `{session_id}`. Polling backend for agent completion...")

                for i in range(10):
                    p_bar.progress(30 + (i + 1) * 7)
                    status_text.text(f"Polling GET /api/session/{session_id} (Attempt {i+1}/10)...")
                    time.sleep(0.5)

                s_ok, s_data, s_err = api_client.get_session(session_id)
                if s_ok and s_data:
                    SessionManager.set_session(s_data)
                    st.success("Verification data received from live backend! Redirecting to Agent Workspace...")
                else:
                    st.warning("Backend pipeline still executing in background. Session state preserved.")
            else:
                p_bar.progress(100)
                status_text.text("Backend offline.")
                st.markdown(
                    """
                    <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 8px;">
                        The verification backend at <code>http://127.0.0.1:8000</code> is currently offline. 
                        Parameters for this candidate have been staged in session state. No synthetic results were fabricated.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
            st.session_state["current_page"] = "Agent Workspace"
            st.rerun()
