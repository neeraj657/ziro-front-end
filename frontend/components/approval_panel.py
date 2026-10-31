import streamlit as st
from config import DEFAULT_BACKEND_URL
from evaluation.synthetic_data import get_demo_session
from services.api_client import APIClient


def render_approval_panel():
    """Render the Human Reviewer Approval checkpoint interface.

    Enforces mandatory human auditor review before credential issuance.
    """
    if "active_session" not in st.session_state or not st.session_state["active_session"]:
        st.session_state["active_session"] = get_demo_session("CAND-001")

    session = st.session_state["active_session"]
    session_id = session.get("session_id", "sess_active")
    cand_id = session.get("candidate_id", "CAND-001")
    claimed_skills = session.get("claimed_skills", ["Python", "Machine Learning"])
    approval_data = session.get("approval", {})
    current_status = session.get("approval_status", "pending")
    is_demo = session.get("is_demo_mode", True)

    backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
    api_client = APIClient(base_url=backend_url, timeout=5)
    is_live = st.session_state.get("backend_connected", False)

    # Top Status Banner
    if current_status == "approved":
        banner_color = "#10B981"
        banner_bg = "rgba(16, 185, 129, 0.15)"
        banner_title = "✅ CANDIDATE STATUS: APPROVED BY HUMAN AUDITOR"
        banner_sub = f"Signed off by {approval_data.get('reviewer_id', 'rev_lead_01')}. Credential issuance unlocked."
    elif current_status == "rejected":
        banner_color = "#EF4444"
        banner_bg = "rgba(239, 68, 68, 0.15)"
        banner_title = "❌ CANDIDATE STATUS: REJECTED BY AUDITOR"
        banner_sub = "Verification failed or evidence is insufficient. Credential issuance blocked."
    else:
        banner_color = "#F59E0B"
        banner_bg = "rgba(245, 158, 11, 0.15)"
        banner_title = "⏳ CANDIDATE STATUS: PENDING HUMAN AUDITOR APPROVAL"
        banner_sub = "Policy rule active: Autonomous agents never auto-approve candidates without human oversight."

    st.markdown(
        f"""
        <div style="background: {banner_bg}; border: 2px solid {banner_color}; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: {banner_color}; margin-bottom: 4px;">
                {banner_title}
            </div>
            <div style="font-size: 0.9rem; color: #E2E8F0;">
                {banner_sub}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Verification Summary Card
    st.markdown(
        f"""
        <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: #F8FAFC; font-size: 1.15rem; font-weight: 700;">
                Complete Verification Dossier for {cand_id}
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                <div>
                    <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Claimed Skills</span>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #F8FAFC;">{', '.join(claimed_skills)}</div>
                </div>
                <div>
                    <span style="font-size: 0.75rem; color: #A5ABB5; text-transform: uppercase;">Overall Evidence Score</span>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #19C7B5;">{session.get('overall_score', 0)}/100</div>
                </div>
                <div>
                    <span style="font-size: 0.75rem; color: #A5ABB5; text-transform: uppercase;">Automated Tests</span>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #A7F3D0;">100% Pass Rate (3/3 unit tests)</div>
                </div>
                <div>
                    <span style="font-size: 0.75rem; color: #A5ABB5; text-transform: uppercase;">Git Provenance</span>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #19C7B5;">4 Incremental Commits across 7 days</div>
                </div>
                <div>
                    <span style="font-size: 0.75rem; color: #A5ABB5; text-transform: uppercase;">Viva Technical Average</span>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #A7F3D0;">95.3/100</div>
                </div>
                <div>
                    <span style="font-size: 0.75rem; color: #A5ABB5; text-transform: uppercase;">AI Recommendation</span>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #A7F3D0; text-transform: uppercase;">{session.get('recommendation', 'Review')}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Reviewer Action Form
    st.markdown(
        """
        <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h3 style="margin: 0 0 16px 0; color: #F8FAFC; font-size: 1.15rem; font-weight: 700;">
                Official Reviewer Sign-Off Decision
            </h3>
        """,
        unsafe_allow_html=True
    )

    with st.form("reviewer_approval_form"):
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            decision = st.radio(
                "Reviewer Decision:",
                ["Approve Candidate", "Reject Candidate"],
                index=0 if current_status != "rejected" else 1,
                horizontal=True
            )
        with col_d2:
            reviewer_id = st.text_input("Auditor / Reviewer ID:", value="rev_lead_01")

        default_notes = (
            "Exemplary implementation. All 3 unit tests pass, StratifiedKFold correctly prevents leakage, and candidate's viva explanations demonstrated authentic ownership."
            if decision == "Approve Candidate"
            else "Insufficient evidence or failure to demonstrate authentic technical ownership."
        )

        reviewer_notes = st.text_area(
            "Reviewer Rationale & Audit Notes (Mandatory):",
            value=approval_data.get("reviewer_notes", default_notes),
            height=100
        )

        submit_decision = st.form_submit_button(
            "🔒 Submit Official Auditor Decision",
            type="primary",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submit_decision:
        if not reviewer_notes.strip():
            st.error("Please provide formal audit rationale notes.")
            return

        api_decision = "approved" if decision == "Approve Candidate" else "rejected"

        if is_live:
            ok, resp, err = api_client.submit_approval(
                session_id=session_id,
                decision=api_decision,
                reviewer_notes=reviewer_notes,
                reviewer_id=reviewer_id
            )
            if ok:
                st.session_state["active_session"]["approval_status"] = api_decision
                st.session_state["active_session"]["approval"] = {
                    "decision": api_decision,
                    "reviewer_notes": reviewer_notes,
                    "reviewer_id": reviewer_id
                }
                st.success(f"Reviewer decision '{api_decision}' successfully recorded in backend!")
                st.rerun()
            else:
                st.error(f"Approval submission failed: {err}")
        else:
            # Deterministic simulation
            st.session_state["active_session"]["approval_status"] = api_decision
            st.session_state["active_session"]["approval"] = {
                "decision": api_decision,
                "reviewer_notes": reviewer_notes,
                "reviewer_id": reviewer_id
            }
            st.success(f"Official reviewer decision '{api_decision}' saved for session {session_id}!")
            st.rerun()
