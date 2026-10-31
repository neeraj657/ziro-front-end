import streamlit as st
from evaluation.synthetic_data import get_demo_session

AGENT_ICONS = {
    "Planning Agent": "🧠",
    "Repository Inspector": "🔎",
    "Code Analysis Agent": "💻",
    "Git History Analyzer": "📜",
    "Evidence Evaluator": "📊",
    "Re-planning Agent": "🔄",
    "Viva Preparation Agent": "🎙️",
    "Human Reviewer Checkpoint": "👤",
}

AGENT_COLORS = {
    "Planning Agent": "#19C7B5",
    "Repository Inspector": "#A7F3D0",
    "Code Analysis Agent": "#19C7B5",
    "Git History Analyzer": "#F0B45A",
    "Evidence Evaluator": "#A7F3D0",
    "Re-planning Agent": "#F0B45A",
    "Viva Preparation Agent": "#19C7B5",
    "Human Reviewer Checkpoint": "#F0B45A",
}


def render_agent_timeline():
    """Render the Live Agent Timeline showing tool calls, observations, and stage results."""
    # Ensure active session
    if "active_session" not in st.session_state or not st.session_state["active_session"]:
        st.session_state["active_session"] = get_demo_session("CAND-001")

    session = st.session_state["active_session"]
    cand_id = session.get("candidate_id", "CAND-001")
    repo_url = session.get("repo_url", "https://github.com/synthetic-lab/fraud-detection-ml")
    session_id = session.get("session_id", "sess_active")
    is_demo = session.get("is_demo_mode", True)

    # Top Header
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                        Live Agent Execution Timeline
                    </h1>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                        Autonomous multi-agent verification trace: actions, tool calls, observations, and findings.
                    </p>
                </div>
                <div>
                    {'<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; color: #FCD34D; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">[DEMO DATA — PRECOMPUTED TRAJECTORY]</span>' if is_demo else '<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">LIVE BACKEND TRACE</span>'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Candidate Meta Card
    st.markdown(
        f"""
        <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 16px 20px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="color: #94A3B8; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;">Candidate</span>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">{cand_id}</div>
                </div>
                <div>
                    <span style="color: #A5ABB5; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;">Repository</span>
                    <div style="font-size: 0.9rem; font-family: monospace; color: #19C7B5;">{repo_url}</div>
                </div>
                <div>
                    <span style="color: #A5ABB5; font-size: 0.8rem; text-transform: uppercase; font-weight: 600;">Session ID</span>
                    <div style="font-size: 0.9rem; font-family: monospace; color: #A7F3D0;">{session_id}</div>
                </div>
                <div>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                        Ready for Review
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    timeline_events = session.get("timeline", [])
    if not timeline_events:
        st.info("No timeline events found in current session. Dispatch analysis from the 'Verify Candidate' tab.")
        return

    # Render Chronological Agent Cards
    for idx, event in enumerate(timeline_events):
        agent_name = event.get("agent", "Agent")
        icon = AGENT_ICONS.get(agent_name, "🤖")
        color = AGENT_COLORS.get(agent_name, "#19C7B5")
        action = event.get("action", "Execution")
        tool = event.get("tool", "internal_call")
        observation = event.get("observation", "")
        result = event.get("result", "")
        timestamp = event.get("timestamp", "00:00:00")

        st.markdown(
            f"""
            <div style="display: flex; gap: 16px; margin-bottom: 16px;">
                <!-- Step Number & Line -->
                <div style="display: flex; flex-direction: column; align-items: center; min-width: 40px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #171A21; border: 2px solid {color}; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">
                        {icon}
                    </div>
                    {f'<div style="width: 2px; flex-grow: 1; background: #343A44; margin: 6px 0;"></div>' if idx < len(timeline_events)-1 else ''}
                </div>

                <!-- Event Details Card -->
                <div style="flex-grow: 1; background: #20242B; border: 1px solid #343A44; border-radius: 12px; padding: 18px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.25);">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-weight: 700; color: #F4F5F7; font-size: 1.05rem;">{agent_name}</span>
                            <span style="background: rgba(99, 102, 241, 0.12); color: {color}; border: 1px solid {color}; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">
                                {action}
                            </span>
                        </div>
                        <div style="font-size: 0.75rem; color: #94A3B8; font-family: monospace;">
                            ⏱️ {timestamp}
                        </div>
                    </div>

                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 0.8rem; color: #A5ABB5; font-weight: 600;">TOOL INVOKED:</span>
                        <code style="background: #292F38; color: #19C7B5; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 6px; border: 1px solid #343A44;">{tool}</code>
                    </div>

                    <div style="background: #0B0F19; border-left: 3px solid {color}; border-radius: 0 6px 6px 0; padding: 10px 14px; margin-bottom: 10px;">
                        <div style="font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 4px;">OBSERVATION</div>
                        <div style="font-size: 0.85rem; color: #E2E8F0; line-height: 1.4;">{observation}</div>
                    </div>

                    <div style="display: flex; align-items: flex-start; gap: 8px; font-size: 0.85rem; color: #10B981;">
                        <span style="font-weight: 700; color: #6EE7B7; text-transform: uppercase; font-size: 0.75rem;">RESULT:</span>
                        <span style="color: #F8FAFC;">{result}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Next Step CTA
    col_cta1, col_cta2 = st.columns([1, 1])
    with col_cta1:
        if st.button("🎯 Inspect Skill Evidence & Scores →", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Skill Evidence"
            st.rerun()
    with col_cta2:
        if st.button("🎙️ Jump to Viva Technical Interview →", use_container_width=True):
            st.session_state["current_page"] = "Viva Interview"
            st.rerun()
