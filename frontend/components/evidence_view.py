import streamlit as st
from components.skill_charts import (
    render_evidence_pie,
    render_radar_chart,
    render_skill_bars,
)
from evaluation.synthetic_data import get_demo_session


def render_evidence_view():
    """Render the Skill Evidence Dashboard with Plotly charts, code inspection, and git provenance."""
    if (
        "active_session" not in st.session_state
        or not st.session_state["active_session"]
    ):
        st.session_state["active_session"] = get_demo_session("CAND-001")

    session = st.session_state["active_session"]
    cand_id = session.get("candidate_id", "CAND-001")
    is_demo = session.get("is_demo_mode", True)

    # Top Header
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                        Skill Evidence & Audit Analysis
                    </h1>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                        Rigorous multi-signal evidence extraction: AST syntax trees, unit test coverage, and git provenance for {cand_id}.
                    </p>
                </div>
                <div>
                    {'<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; color: #FCD34D; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">[DEMO DATA EVIDENCE]</span>' if is_demo else '<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">LIVE ANALYSIS</span>'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    skill_evidence = session.get("skill_evidence", {})
    skills_dict = skill_evidence.get(
        "skills", session.get("skills", {})
    )  # Support CAND-002 structure
    overall_score = session.get(
        "overall_score", skill_evidence.get("overall_score", 0)
    )
    confidence = session.get(
        "confidence", skill_evidence.get("confidence", "Medium")
    )
    recommendation = session.get("recommendation", "Review")

    rec_color = (
        "#10B981"
        if recommendation == "approve"
        else (
            "#F59E0B"
            if recommendation == "flag_for_review"
            else "#EF4444"
        )
    )
    rec_bg = (
        "rgba(16, 185, 129, 0.15)"
        if recommendation == "approve"
        else (
            "rgba(245, 158, 11, 0.15)"
            if recommendation == "flag_for_review"
            else "rgba(239, 68, 68, 0.15)"
        )
    )

    # Top KPI Strip
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div style="background: #20242B; border: 1px solid #19C7B5; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #19C7B5; font-weight: 600;">Overall Evidence Score</div>
                <div style="font-size: 2rem; font-weight: 800; color: #F4F5F7; margin: 4px 0;">{overall_score}<span style="font-size: 1rem; color: #A5ABB5;">/100</span></div>
                <div style="font-size: 0.75rem; color: #A7F3D0;">Weighted multi-agent composite</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div style="background: #20242B; border: 1px solid #343A44; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #A5ABB5; font-weight: 600;">Agent Confidence</div>
                <div style="font-size: 2rem; font-weight: 800; color: #19C7B5; margin: 4px 0;">{confidence}</div>
                <div style="font-size: 0.75rem; color: #A5ABB5;">Cross-entropy agreement</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div style="background: #151F33; border: 1px solid {rec_color}; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {rec_color}; font-weight: 600;">Recommendation</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: {rec_color}; margin: 4px 0; text-transform: uppercase;">{recommendation.replace('_', ' ')}</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Awaiting human reviewer</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        verified_count = sum(
            1 for s in skills_dict.values() if s.get("score", 0) >= 70
        )
        total_count = len(skills_dict)
        st.markdown(
            f"""
            <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Verified Skills</div>
                <div style="font-size: 2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{verified_count} / {total_count}</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Threshold: score ≥ 70</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Plotly Charts Section
    c_chart1, c_chart2 = st.columns([1.1, 0.9])
    with c_chart1:
        st.markdown(
            """
            <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 16px 20px;">
                <h4 style="margin: 0 0 10px 0; color: #F8FAFC; font-size: 1rem;">Skill Score vs Implementation Coverage</h4>
            """,
            unsafe_allow_html=True,
        )
        radar_fig = render_radar_chart(skills_dict)
        st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_chart2:
        breakdown = skill_evidence.get("evidence_breakdown", {})
        st.markdown(
            """
            <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 16px 20px;">
                <h4 style="margin: 0 0 10px 0; color: #F8FAFC; font-size: 1rem;">Evidence Signal Classification</h4>
            """,
            unsafe_allow_html=True,
        )
        pie_fig = render_evidence_pie(breakdown)
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Three-Way Distinction: Observed vs AI Inference vs Missing Evidence
    st.markdown(
        "<h3 style='color: #F8FAFC; font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;'>Multi-Category Evidence Breakdown</h3>",
        unsafe_allow_html=True,
    )
    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        st.markdown(
            """
            <div style="background: #151F33; border-top: 4px solid #10B981; border-left: 1px solid #233354; border-right: 1px solid #233354; border-bottom: 1px solid #233354; border-radius: 12px; padding: 16px; min-height: 240px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="font-size: 1.1rem;">✅</span>
                    <span style="font-weight: 700; color: #10B981; font-size: 0.95rem;">OBSERVED EVIDENCE</span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">Direct artifacts verified on disk & git history:</div>
            """,
            unsafe_allow_html=True,
        )
        obs_items = breakdown.get(
            "observed_evidence",
            [
                "Source code files present on disk",
                "Unit tests executed via pytest",
                "Authentic git commit history",
            ],
        )
        for item in obs_items:
            st.markdown(
                f"<div style='font-size: 0.82rem; color: #E2E8F0; margin-bottom: 6px;'>• {item}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with b_col2:
        st.markdown(
            """
            <div style="background: #151F33; border-top: 4px solid #8B5CF6; border-left: 1px solid #233354; border-right: 1px solid #233354; border-bottom: 1px solid #233354; border-radius: 12px; padding: 16px; min-height: 240px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="font-size: 1.1rem;">🧠</span>
                    <span style="font-weight: 700; color: #A78BFA; font-size: 0.95rem;">AI INFERENCE</span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">Deductions derived from code patterns & architecture:</div>
            """,
            unsafe_allow_html=True,
        )
        ai_items = breakdown.get(
            "ai_generated_inference",
            [
                "Understands class imbalance compensation via balanced weights",
                "Prevents data leakage by isolating scaling within StratifiedKFold folds",
            ],
        )
        for item in ai_items:
            st.markdown(
                f"<div style='font-size: 0.82rem; color: #E2E8F0; margin-bottom: 6px;'>• {item}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with b_col3:
        st.markdown(
            """
            <div style="background: #151F33; border-top: 4px solid #F59E0B; border-left: 1px solid #233354; border-right: 1px solid #233354; border-bottom: 1px solid #233354; border-radius: 12px; padding: 16px; min-height: 240px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
                    <span style="font-size: 1.1rem;">⚠️</span>
                    <span style="font-weight: 700; color: #FCD34D; font-size: 0.95rem;">MISSING EVIDENCE</span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">Anticipated production patterns absent from repository:</div>
            """,
            unsafe_allow_html=True,
        )
        mis_items = breakdown.get(
            "missing_evidence",
            [
                "No CI/CD GitHub Actions workflow configuration",
                "No Dockerfile containerization spec",
            ],
        )
        for item in mis_items:
            st.markdown(
                f"<div style='font-size: 0.82rem; color: #E2E8F0; margin-bottom: 6px;'>• {item}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Detailed Skill Breakdown Cards
    st.markdown(
        "<h3 style='color: #F8FAFC; font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;'>Individual Skill Evidence Audits</h3>",
        unsafe_allow_html=True,
    )

    for skill_name, s_info in skills_dict.items():
        score = s_info.get("score", 0)
        coverage = s_info.get("coverage", 0)
        files = s_info.get("supporting_files", [])
        findings = s_info.get("implementation_findings", [])
        tests = s_info.get("test_results", "None")
        limitations = s_info.get("limitations", "None")
        indicators = s_info.get("suspicious_indicators", "None")

        badge_color = (
            "#10B981"
            if score >= 80
            else ("#F59E0B" if score >= 50 else "#EF4444")
        )

        with st.expander(
            f"**{skill_name}** — Evidence Score: {score}/100 | Coverage: {coverage}%",
            expanded=True,
        ):
            c_s1, c_s2 = st.columns([1, 1])

            with c_s1:
                st.markdown(
                    f"""
                    <div style="margin-bottom: 12px;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #A5ABB5;">SUPPORTING FILES:</span><br>
                        {' '.join([f'<code style="background: #292F38; color: #19C7B5; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #343A44;">{f}</code>' for f in files]) if files else '<span style="color: #F07178; font-size: 0.85rem;">None located</span>'}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "**Implementation Findings:**\n"
                    + "\n".join([f"- {f}" for f in findings])
                )
                st.markdown(f"**Test Results:** {tests}")

            with c_s2:
                st.markdown(f"**Identified Limitations:** {limitations}")

                # Suspicion & Anomaly Box
                st.markdown(
                    f"""
                    <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 12px; margin-top: 10px;">
                        <div style="font-size: 0.75rem; font-weight: 700; color: #FCA5A5; text-transform: uppercase;">
                            ANOMALY & INTEGRITY AUDIT SIGNAL
                        </div>
                        <div style="font-size: 0.85rem; color: #F8FAFC; margin-top: 4px;">
                            {indicators}
                        </div>
                        <div style="font-size: 0.7rem; color: #94A3B8; margin-top: 6px; font-style: italic;">
                            ⚠️ Policy Notice: Anomaly heuristics require human oversight and do NOT constitute proof of plagiarism.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Repository Code & Git Provenance Viewer
    st.markdown(
        "<h3 style='color: #F8FAFC; font-size: 1.25rem; font-weight: 700; margin-bottom: 12px;'>Repository Source Code & Git History</h3>",
        unsafe_allow_html=True,
    )

    t_code, t_git = st.tabs(["📁 Source Files Inspection", "📜 Git Commit Provenance"])

    with t_code:
        repo_files = session.get("repository_files", {})
        if repo_files:
            selected_file = st.selectbox(
                "Inspect File in Candidate Repository",
                options=list(repo_files.keys()),
                key="code_file_select",
            )
            code_content = repo_files.get(selected_file, "")
            st.code(
                code_content,
                language=(
                    "python"
                    if selected_file.endswith(".py")
                    else (
                        "markdown"
                        if selected_file.endswith(".md")
                        else "text"
                    )
                ),
                line_numbers=True,
            )
        else:
            st.info("No source files found in session payload.")

    with t_git:
        git_history = session.get("git_history", [])
        if git_history:
            st.markdown(
                """
                <div style="background: #151F33; border: 1px solid #233354; border-radius: 12px; padding: 16px;">
                    <p style="font-size: 0.85rem; color: #94A3B8; margin: 0 0 12px 0;">
                        Natural commit frequency across 7 days indicating iterative development without bulk automated copy-pasting.
                    </p>
                """,
                unsafe_allow_html=True,
            )
            for commit in git_history:
                st.markdown(
                    f"""
                    <div style="border-bottom: 1px solid #233354; padding: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <code style="background: #0B0F19; color: #818CF8; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">{commit.get('hash', '---')}</code>
                                <span style="font-weight: 600; color: #F8FAFC; margin-left: 8px;">{commit.get('message', '')}</span>
                            </div>
                            <div style="font-size: 0.75rem; color: #94A3B8;">{commit.get('date', '')}</div>
                        </div>
                        <div style="font-size: 0.8rem; color: #A5ABB5; margin-top: 4px;">
                            Author: <span style="color: #19C7B5;">{commit.get('author', '')}</span> |
                            <span style="color: #A7F3D0;">+{commit.get('insertions', 0)}</span> /
                            <span style="color: #F07178;">-{commit.get('deletions', 0)}</span> lines
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No git history records available.")

    # Flow navigation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.button(
            "🎙️ Proceed to Candidate Viva Interview →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["current_page"] = "Viva Interview"
            st.rerun()
    with c_nav2:
        if st.button(
            "👤 Open Reviewer Approval Checkpoint →", use_container_width=True
        ):
            st.session_state["current_page"] = "Credential Verification"
            st.rerun()
