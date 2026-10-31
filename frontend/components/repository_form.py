import time
import streamlit as st
from config import DEFAULT_BACKEND_URL, SUPPORTED_SKILLS
from evaluation.synthetic_data import get_demo_session
from services.api_client import APIClient


def render_repository_form():
    """Render the Candidate Verification input form and trigger agent analysis."""
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                Verify Candidate Skills
            </h1>
            <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Dispatch autonomous agents to inspect GitHub repositories, audit git commits, evaluate test coverage, and score skill evidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check connection
    backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
    api_client = APIClient(base_url=backend_url, timeout=5)
    is_live, health_msg = api_client.check_health()

    if not is_live:
        st.info(
            "⚡ **Fallback Demo Mode Active**: The live FastAPI backend at `http://127.0.0.1:8000` is currently disconnected. "
            "Verification will execute using deterministic synthetic demonstration datasets labeled as `[DEMO DATA]` for jury evaluation.",
            icon="ℹ️",
        )

    # Main Verification Input Form
    with st.form("candidate_verification_form", clear_on_submit=False):
        st.markdown(
            """
            <div style="background: #20242B; border: 1px solid #343A44; border-radius: 12px; padding: 24px; margin-bottom: 20px;">
                <h3 style="margin: 0 0 16px 0; color: #F4F5F7; font-size: 1.15rem; font-weight: 700;">
                    Candidate Credentials & Repository Target
                </h3>
            """,
            unsafe_allow_html=True,
        )

        col_id, col_url = st.columns([1, 2])
        with col_id:
            cand_id = st.text_input(
                "Candidate ID",
                value=st.session_state.get("selected_candidate_id", ""),
                placeholder="e.g. CAND-1024 or AliceDev",
                help="Unique identifier for the applicant being verified",
            )

        with col_url:
            repo_url = st.text_input(
                "GitHub Repository URL",
                value=st.session_state.get("selected_repo_url", ""),
                placeholder="https://github.com/username/repository",
                help="Public GitHub repository URL containing candidate code",
            )

        selected_skills = st.multiselect(
            "Claimed Skills to Verify",
            options=SUPPORTED_SKILLS,
            default=st.session_state.get(
                "selected_claimed_skills", []
            ),
            help="Select one or more technologies claimed by the candidate",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "🚀 Start Autonomous Verification Pipeline",
            type="primary",
            use_container_width=True,
        )

    # Handle Submission
    if submitted:
        if not cand_id.strip():
            st.error("Please provide a valid Candidate ID.")
            return
        if not repo_url.strip() or not repo_url.startswith("http"):
            st.error("Please provide a valid HTTP/HTTPS GitHub repository URL.")
            return
        if not selected_skills:
            st.error("Please select at least one claimed skill to verify.")
            return

        progress_container = st.container()
        with progress_container:
            st.markdown(
                """
                <div style="background: #20242B; border: 1px solid #19C7B5; border-radius: 12px; padding: 20px; margin-top: 20px;">
                    <h4 style="margin: 0 0 8px 0; color: #19C7B5;">🤖 Agent Swarm Dispatched</h4>
                    <p style="margin: 0 0 12px 0; color: #A5ABB5; font-size: 0.9rem;">
                        Initializing autonomous pipeline: repository clone, static AST parsing, test suite execution, and git provenance check.
                    </p>
                """,
                unsafe_allow_html=True,
            )

            progress_bar = st.progress(0)
            status_text = st.empty()

            if is_live:
                # Live Backend Mode
                status_text.text("Calling POST /api/analyze...")
                success, resp, err = api_client.start_analysis(
                    candidate_id=cand_id,
                    repo_url=repo_url,
                    claimed_skills=selected_skills,
                )
                if not success:
                    st.error(f"Analysis trigger failed: {err}")
                    return

                session_id = resp.get("session_id", f"sess_{cand_id}")
                st.success(
                    f"Session created: `{session_id}`. Polling backend for completion..."
                )

                # Polling loop
                completed = False
                for attempt in range(15):
                    progress = min(10 + attempt * 6, 90)
                    progress_bar.progress(progress)
                    status_text.text(
                        f"Polling GET /api/session/{session_id} (Attempt {attempt + 1}/15)..."
                    )
                    time.sleep(1.0)

                    ok, sess_data, gerr = api_client.get_session(session_id)
                    if (
                        ok
                        and sess_data
                        and sess_data.get("status") in ("completed", "ready")
                    ):
                        progress_bar.progress(100)
                        status_text.text("Analysis complete!")
                        st.session_state["active_session"] = sess_data
                        completed = True
                        break

                if not completed:
                    st.warning(
                        "Session still processing in backend. Loading current state..."
                    )
                    st.session_state["active_session"] = sess_data

            else:
                # Fallback Demo Mode with realistic step-by-step agent simulation
                steps = [
                    (
                        15,
                        "Planning Agent: Decomposing verification goals for "
                        + ", ".join(selected_skills),
                    ),
                    (
                        35,
                        "Repository Inspector: Cloning and parsing project tree...",
                    ),
                    (55, "Code Analysis Agent: AST traversal & type signature check..."),
                    (
                        75,
                        "Git History Analyzer: Auditing commit cadence & commit hashes...",
                    ),
                    (
                        90,
                        "Evidence Evaluator: Running pytest harness & calculating scores...",
                    ),
                    (100, "Viva Preparation Agent: Generating technical viva questions..."),
                ]

                for p, msg in steps:
                    progress_bar.progress(p)
                    status_text.text(f"[DEMO SIMULATION] {msg}")
                    time.sleep(0.4)

                target_key = "CAND-002" if cand_id == "CAND-002" else "CAND-001"
                mock_session = get_demo_session(target_key)
                # Overwrite candidate ID and claimed skills with user input
                mock_session["candidate_id"] = cand_id
                mock_session["repo_url"] = repo_url
                mock_session["is_demo_mode"] = True
                st.session_state["active_session"] = mock_session

            st.markdown("</div>", unsafe_allow_html=True)
            st.success(
                f"✅ Verification pipeline finished for {cand_id}! Proceed to inspect Agent Activity or Skill Evidence."
            )

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(
                    "⚡ View Agent Activity Timeline", use_container_width=True
                ):
                    st.session_state["current_page"] = "Agent Activity"
                    st.rerun()
            with col_btn2:
                if st.button("🎯 View Skill Evidence", use_container_width=True):
                    st.session_state["current_page"] = "Skill Evidence"
                    st.rerun()
