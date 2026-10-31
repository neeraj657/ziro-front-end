import streamlit as st
from config import DEFAULT_BACKEND_URL
from evaluation.synthetic_data import get_demo_session
from services.api_client import APIClient


def render_viva_interface():
    """Render the Interactive Technical Viva Question & Answer Verification Suite."""
    if (
        "active_session" not in st.session_state
        or not st.session_state["active_session"]
    ):
        st.session_state["active_session"] = get_demo_session("CAND-001")

    session = st.session_state["active_session"]
    session_id = session.get("session_id", "sess_active")
    cand_id = session.get("candidate_id", "CAND-001")
    viva_questions = session.get("viva_questions", [])
    is_demo = session.get("is_demo_mode", True)

    backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
    api_client = APIClient(base_url=backend_url, timeout=5)
    is_live = st.session_state.get("backend_connected", False)

    # Header
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                        Candidate Technical Viva
                    </h1>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                        Targeted architectural inquiry generated directly from the candidate's codebase to confirm authentic implementation knowledge.
                    </p>
                </div>
                <div>
                    {'<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; color: #FCD34D; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">[DEMO VIVA SUITE]</span>' if is_demo else '<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">LIVE API VIVA</span>'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not viva_questions:
        st.warning(
            "No viva questions generated for this session. Candidate code may have insufficient depth or analysis is incomplete."
        )
        return

    # Questions and Answer cards
    for idx, q_data in enumerate(viva_questions):
        qid = q_data.get("id", f"Q{idx + 1}")
        q_text = q_data.get("question", "")
        q_context = q_data.get("context", "")
        sample_ans = q_data.get("sample_answer", "")
        eval_data = q_data.get("evaluation", {})

        st.markdown(
            f"""
            <div style="background: #20242B; border: 1px solid #343A44; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="background: rgba(25, 199, 181, 0.15); color: #A7F3D0; font-weight: 700; font-size: 0.8rem; padding: 4px 10px; border-radius: 6px; border: 1px solid #19C7B5;">
                        QUESTION {idx + 1} ({qid})
                    </span>
                    <span style="font-size: 0.75rem; color: #A5ABB5;">Target: {q_context}</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #F4F5F7; line-height: 1.4; margin-bottom: 14px;">
                    {q_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        ans_key = f"viva_ans_{qid}"
        # Fill button
        col_f1, col_f2 = st.columns([1, 3])
        with col_f1:
            if st.button(
                f"📝 Auto-fill Answer ({qid})",
                key=f"btn_fill_{qid}",
                help="Populate authentic demonstration response",
            ):
                st.session_state[ans_key] = sample_ans
                st.rerun()

        user_answer = st.text_area(
            f"Candidate Response for {qid}:",
            value=st.session_state.get(ans_key, sample_ans if idx == 0 else ""),
            key=f"input_{ans_key}",
            height=100,
            placeholder="Explain the architectural rationale and implementation details...",
        )

        c_sub1, c_sub2 = st.columns([1.5, 3])
        with c_sub1:
            submit_ans = st.button(
                f"📤 Submit Answer ({qid})",
                key=f"sub_btn_{qid}",
                type="primary",
            )

        # Evaluated display state
        eval_state_key = f"eval_res_{qid}"
        if submit_ans and user_answer.strip():
            if is_live:
                ok, live_eval, err = api_client.submit_viva_answer(
                    session_id=session_id,
                    question_id=qid,
                    answer=user_answer,
                )
                if ok:
                    st.session_state[eval_state_key] = live_eval
                else:
                    st.error(f"Viva submission error: {err}")
            else:
                # Deterministic grading
                is_short = len(user_answer.split()) < 10
                if is_short:
                    st.session_state[eval_state_key] = {
                        "technical_correctness": 35,
                        "understanding": 30,
                        "explanation_quality": 40,
                        "evidence_alignment": 35,
                        "feedback": "Answer is excessively superficial and does not explain the technical mechanics or code rationale.",
                    }
                else:
                    st.session_state[eval_state_key] = eval_data

        active_eval = st.session_state.get(eval_state_key, eval_data if idx == 0 else None)

        if active_eval:
            tc = active_eval.get("technical_correctness", 0)
            un = active_eval.get("understanding", 0)
            eq = active_eval.get("explanation_quality", 0)
            ea = active_eval.get("evidence_alignment", 0)
            fb = active_eval.get("feedback", "")

            avg_score = round((tc + un + eq + ea) / 4, 1)

            st.markdown(
                f"""
                <div style="background: #0B0F19; border: 1px solid #10B981; border-radius: 10px; padding: 16px; margin: 12px 0 24px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-weight: 700; color: #10B981; font-size: 0.9rem;">
                            🎯 AI EVALUATION RESULT: {avg_score}/100
                        </span>
                        <span style="font-size: 0.75rem; color: #94A3B8;">Multi-dimensional rubric</span>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.caption(f"Technical Correctness: {tc}%")
                st.progress(tc / 100)
            with m2:
                st.caption(f"Understanding: {un}%")
                st.progress(un / 100)
            with m3:
                st.caption(f"Explanation Quality: {eq}%")
                st.progress(eq / 100)
            with m4:
                st.caption(f"Evidence Alignment: {ea}%")
                st.progress(ea / 100)

            st.markdown(
                f"""
                    <div style="margin-top: 12px; font-size: 0.85rem; color: #E2E8F0; background: rgba(16, 185, 129, 0.08); padding: 10px; border-radius: 6px;">
                        <strong>Auditor Feedback:</strong> {fb}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Next Step
    st.markdown("<hr style='border-color: #233354; margin: 30px 0;'>", unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("⬅️ Back to Skill Evidence", use_container_width=True):
            st.session_state["current_page"] = "Skill Evidence"
            st.rerun()
    with col_v2:
        if st.button(
            "👤 Proceed to Human Reviewer Approval →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["current_page"] = "Credential Verification"
            st.rerun()
