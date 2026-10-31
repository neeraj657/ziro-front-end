import streamlit as st
from config import APP_ICON, APP_NAME, APP_TAGLINE, DEFAULT_BACKEND_URL
from evaluation.synthetic_data import get_demo_session
from services.api_client import APIClient


def render_sidebar() -> str:
    """Render the application sidebar with branding, navigation, connection status,

    and demo scenario presets.
    Returns the selected navigation page name.
    """
    with st.sidebar:
        # Logo & Header
        st.markdown(
            f"""
            <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #233354; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 2rem;">{APP_ICON}</span>
                    <div>
                        <h2 style="margin: 0; font-size: 1.4rem; color: #F8FAFC; font-weight: 700; letter-spacing: -0.5px;">{APP_NAME}</h2>
                        <span style="font-size: 0.75rem; color: #818CF8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">AGENTIC VERIFICATION</span>
                    </div>
                </div>
                <p style="margin: 8px 0 0 0; font-size: 0.8rem; color: #94A3B8; line-height: 1.3;">
                    {APP_TAGLINE}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation Menu
        PAGES = [
            ("📊 Dashboard", "Dashboard"),
            ("🔍 Verify Candidate", "Verify Candidate"),
            ("⚡ Agent Activity", "Agent Activity"),
            ("🎯 Skill Evidence", "Skill Evidence"),
            ("🎙️ Viva Interview", "Viva Interview"),
            ("🛡️ Credential Verification", "Credential Verification"),
            ("📈 Evaluation Metrics", "Evaluation Metrics"),
        ]

        if "current_page" not in st.session_state:
            st.session_state["current_page"] = "Dashboard"

        # Find current index
        page_labels = [p[0] for p in PAGES]
        page_keys = [p[1] for p in PAGES]
        curr_idx = (
            page_keys.index(st.session_state["current_page"])
            if st.session_state["current_page"] in page_keys
            else 0
        )

        selected_label = st.radio(
            "Navigation",
            page_labels,
            index=curr_idx,
            label_visibility="collapsed",
        )
        selected_key = page_keys[page_labels.index(selected_label)]
        st.session_state["current_page"] = selected_key

        st.markdown("<hr style='border-color: #233354; margin: 20px 0;'>", unsafe_allow_html=True)

        # Backend Connection Status Check
        backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
        api_client = APIClient(base_url=backend_url, timeout=3)
        is_healthy, status_msg = api_client.check_health()
        st.session_state["backend_connected"] = is_healthy

        if is_healthy:
            st.markdown(
                """
                <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10B981; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 600; color: #10B981; font-size: 0.85rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></span>
                        FASTAPI BACKEND ONLINE
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Live API active at 127.0.0.1:8000</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid #F59E0B; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 600; color: #F59E0B; font-size: 0.85rem;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #F59E0B;"></span>
                        DEMO FALLBACK MODE
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">
                        Backend disconnected. Exploring precomputed synthetic evidence for hackathon jury.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Quick Demo Presets
        st.markdown(
            "<p style='font-size: 0.8rem; font-weight: 700; color: #818CF8; margin-bottom: 8px;'>QUICK DEMO SCENARIOS</p>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟢 CAND-001 (Pass)", use_container_width=True, help="Load Valid ML candidate with 93% verified score"):
                st.session_state["active_session"] = get_demo_session("CAND-001")
                st.session_state["candidate_id"] = "CAND-001"
                st.session_state["repo_url"] = "https://github.com/synthetic-lab/fraud-detection-ml"
                st.session_state["claimed_skills"] = ["Python", "Machine Learning"]
                st.rerun()

        with col2:
            if st.button("🔴 CAND-002 (Fail)", use_container_width=True, help="Load Insufficient Evidence candidate"):
                st.session_state["active_session"] = get_demo_session("CAND-002")
                st.session_state["candidate_id"] = "CAND-002"
                st.session_state["repo_url"] = "https://github.com/synthetic-lab/empty-stub-repo"
                st.session_state["claimed_skills"] = ["Python", "FastAPI", "SQL"]
                st.rerun()

        # Config Collapsible
        with st.expander("⚙️ Backend Configuration", expanded=False):
            new_url = st.text_input("Backend Base URL", value=backend_url)
            if new_url != backend_url:
                st.session_state["backend_url"] = new_url
                st.rerun()
            st.caption("Default: http://127.0.0.1:8000")

        # Footer
        st.markdown(
            """
            <div style="font-size: 0.7rem; color: #64748B; text-align: center; margin-top: 30px;">
                SkillProof AI • Hackathon MVP Edition<br>
                Empowering trust through agentic verification
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state["current_page"]
