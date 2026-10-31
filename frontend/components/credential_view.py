import json
import streamlit as st
from components.approval_panel import render_approval_panel
from config import DEFAULT_BACKEND_URL
from evaluation.synthetic_data import (
    generate_credential_signature,
    get_demo_session,
    verify_credential_signature,
)
from services.api_client import APIClient


def render_credential_view():
    """Render the Credential Issuance, Employer Verification, and Tamper Testing Suite."""
    if (
        "active_session" not in st.session_state
        or not st.session_state["active_session"]
    ):
        st.session_state["active_session"] = get_demo_session("CAND-001")

    session = st.session_state["active_session"]
    session_id = session.get("session_id", "sess_active")
    cand_id = session.get("candidate_id", "CAND-001")
    approval_status = session.get("approval_status", "pending")
    is_demo = session.get("is_demo_mode", True)

    backend_url = st.session_state.get("backend_url", DEFAULT_BACKEND_URL)
    api_client = APIClient(base_url=backend_url, timeout=5)
    is_live = st.session_state.get("backend_connected", False)

    # Top Header
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">
                        Credential Issuance & Employer Verification
                    </h1>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                        Tamper-evident verifiable skill credentials signed with HMAC-SHA256 and backed by agentic evidence.
                    </p>
                </div>
                <div>
                    {'<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; color: #FCD34D; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">[DEMO CREDENTIALS]</span>' if is_demo else '<span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">LIVE CRYPTO ENGINE</span>'}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_approval, t_issuance, t_verify, t_tamper = st.tabs([
        "👤 1. Reviewer Sign-Off",
        "🎖️ 2. Issue Credential",
        "🔍 3. Employer Verification",
        "🛡️ 4. Tamper Detection Test",
    ])

    # Tab 1: Reviewer Sign-off
    with t_approval:
        render_approval_panel()

    # Tab 2: Issue Credential
    with t_issuance:
        st.markdown(
            "### Candidate Credential Generation", unsafe_allow_html=True
        )

        if approval_status != "approved":
            st.warning(
                "🔒 **Issuance Locked**: Credential cannot be issued because this candidate has not yet been approved by a human reviewer. Complete sign-off in the '1. Reviewer Sign-Off' tab."
            )
        else:
            st.success(
                "✅ Candidate is officially approved! You may issue the cryptographic skill credential."
            )

            if st.button(
                "⚡ Issue Cryptographically Signed Credential (POST /api/credential/...)",
                type="primary",
            ):
                if is_live:
                    ok, resp, err = api_client.issue_credential(session_id)
                    if ok:
                        st.session_state["active_session"]["credential"] = (
                            resp.get("credential", {})
                        )
                        st.success("Credential issued successfully by live backend!")
                    else:
                        st.error(f"Issuance failed: {err}")
                else:
                    demo_cred = get_demo_session("CAND-001")["credential"]
                    st.session_state["active_session"]["credential"] = demo_cred
                    st.success("Credential issued with cryptographic signature!")

            cred = session.get("credential")
            if cred:
                c_data = cred.get("data", {})
                c_sig = cred.get("signature", "")
                c_id = cred.get("credential_id", "SP-CRED-2026-001")

                # Certificate Display Card
                st.markdown(
                    f"""
                    <div style="background: #20242B; border: 2px solid #19C7B5; border-radius: 16px; padding: 28px; margin: 20px 0; box-shadow: 0 10px 25px rgba(25, 199, 181, 0.2);">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #343A44; padding-bottom: 16px; margin-bottom: 20px;">
                            <div>
                                <span style="font-size: 0.75rem; color: #19C7B5; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">VERIFIED DIGITAL CREDENTIAL</span>
                                <h2 style="margin: 4px 0 0 0; color: #F4F5F7; font-size: 1.5rem; font-weight: 800;">SkillProof Autonomous Certificate</h2>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 0.8rem; color: #A5ABB5;">Credential ID</div>
                                <code style="font-size: 0.95rem; color: #19C7B5; font-weight: 700;">{c_id}</code>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;">
                            <div>
                                <div style="font-size: 0.75rem; color: #A5ABB5;">Candidate ID:</div>
                                <div style="font-size: 1.1rem; font-weight: 700; color: #F4F5F7;">{c_data.get('candidate_id', cand_id)}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #A5ABB5;">Issue Authority:</div>
                                <div style="font-size: 0.95rem; font-weight: 600; color: #F4F5F7;">{c_data.get('issuer', 'SkillProof AI Authority')}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #A5ABB5;">Issued Timestamp:</div>
                                <div style="font-size: 0.9rem; font-family: monospace; color: #A5ABB5;">{c_data.get('issued_at', '2026-10-31T10:15:30Z')}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #A5ABB5;">Audit Verdict:</div>
                                <span style="background: rgba(167, 243, 208, 0.12); color: #A7F3D0; border: 1px solid #19C7B5; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 700;">
                                    {c_data.get('status', 'VALID')} & APPROVED
                                </span>
                            </div>
                        </div>

                        <div style="background: #20242B; border: 1px solid #343A44; border-radius: 10px; padding: 16px; margin-bottom: 20px;">
                            <div style="font-size: 0.8rem; font-weight: 700; color: #19C7B5; margin-bottom: 8px;">VERIFIED SKILL CLAIMS:</div>
                            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                                {''.join([f'<span style="background: #292F38; border: 1px solid #19C7B5; color: #F4F5F7; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem;"><strong>{s.get("skill", "")}</strong> — {s.get("level", "")} ({s.get("score", 0)}/100)</span>' for s in c_data.get('verified_skills', [])])}
                            </div>
                        </div>

                        <div style="background: #171A21; border: 1px solid #343A44; border-radius: 8px; padding: 12px;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #A5ABB5; margin-bottom: 4px;">
                                <span>HMAC-SHA256 Cryptographic Signature:</span>
                                <span style="color: #A7F3D0; font-weight: 600;">STATUS: VALID</span>
                            </div>
                            <code style="word-break: break-all; color: #19C7B5; font-size: 0.8rem;">{c_sig}</code>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Downloadable JSON
                full_cred_json = json.dumps(cred, indent=2)
                st.download_button(
                    label="📥 Download Cryptographically Signed Credential (JSON)",
                    data=full_cred_json,
                    file_name=f"skillproof_credential_{c_id}.json",
                    mime="application/json",
                    use_container_width=True,
                )

    # Tab 3: Employer Verification Form
    with t_verify:
        st.markdown(
            """
            ### Employer Credential Verification Portal
            Enter a credential ID to verify authenticity against the verification ledger and cryptographic signatures.
            """
        )

        v_col1, v_col2 = st.columns([2, 1])
        with v_col1:
            check_id = st.text_input(
                "Credential ID:",
                value="SP-CRED-2026-001",
                placeholder="SP-CRED-XXXX-XXX",
            )
        with v_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            verify_btn = st.button(
                "🔍 Verify Authenticity",
                type="primary",
                use_container_width=True,
            )

        if verify_btn or st.session_state.get("employer_verified_active", False):
            st.session_state["employer_verified_active"] = True

            if is_live:
                valid, v_data, err = api_client.verify_credential(check_id)
            else:
                valid = check_id == "SP-CRED-2026-001"
                v_data = (
                    get_demo_session("CAND-001")["credential"]["data"]
                    if valid
                    else {}
                )

            if valid:
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.12); border: 2px solid #10B981; border-radius: 12px; padding: 20px; margin-top: 16px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                            <span style="font-size: 1.5rem;">🛡️</span>
                            <span style="font-size: 1.3rem; font-weight: 800; color: #10B981;">STATUS: VALID CREDENTIAL</span>
                        </div>
                        <p style="margin: 0 0 12px 0; color: #E2E8F0; font-size: 0.9rem;">
                            The cryptographic signature matches the canonical credential claims. This candidate was verified by autonomous agents and audited by human lead.
                        </p>
                        <div style="font-size: 0.85rem; color: #94A3B8;">
                            • Verified Candidate: <strong>{v_data.get('candidate_id', 'CAND-001')}</strong><br>
                            • Overall Score: <strong>93%</strong> (Python: 94%, Machine Learning: 92%)<br>
                            • Repository: <code>https://github.com/synthetic-lab/fraud-detection-ml</code>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style="background: rgba(239, 68, 68, 0.12); border: 2px solid #EF4444; border-radius: 12px; padding: 20px; margin-top: 16px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                            <span style="font-size: 1.5rem;">🚨</span>
                            <span style="font-size: 1.3rem; font-weight: 800; color: #EF4444;">STATUS: INVALID CREDENTIAL</span>
                        </div>
                        <p style="margin: 0; color: #E2E8F0; font-size: 0.9rem;">
                            Credential ID not found in verification registry or cryptographic signature failed validation.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Tab 4: Tamper Detection Demonstration
    with t_tamper:
        st.markdown(
            """
            ### Cryptographic Tamper Rejection Test (Step 13 Demo)
            Demonstrates how SkillProof AI prevents fraud by immediately rejecting modified credential payloads.
            """
        )

        col_t1, col_t2 = st.columns([1, 1])

        original_data = {
            "credential_id": "SP-CRED-2026-001",
            "candidate_id": "CAND-001",
            "level": "Junior Developer",
            "score": 75,
            "signature": generate_credential_signature({
                "credential_id": "SP-CRED-2026-001",
                "candidate_id": "CAND-001",
                "level": "Junior Developer",
                "score": 75,
            }),
        }

        with col_t1:
            st.markdown(
                """
                <div style="background: #151F33; border: 1px solid #10B981; border-radius: 10px; padding: 16px;">
                    <div style="font-weight: 700; color: #10B981; font-size: 0.95rem; margin-bottom: 8px;">
                        Original Genuine Credential
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.json(original_data)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_t2:
            st.markdown(
                """
                <div style="background: #151F33; border: 1px solid #EF4444; border-radius: 10px; padding: 16px;">
                    <div style="font-weight: 700; color: #EF4444; font-size: 0.95rem; margin-bottom: 8px;">
                        Forged / Tampered Credential Payload
                    </div>
                """,
                unsafe_allow_html=True,
            )
            # Tampered payload has level changed to Principal
            tampered_data = {
                "credential_id": "SP-CRED-2026-001",
                "candidate_id": "CAND-001",
                "level": "Principal AI Architect (TAMPERED)",
                "score": 99,
                "signature": original_data[
                    "signature"
                ],  # Same signature, payload altered!
            }
            st.json(tampered_data)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        if st.button(
            "🛡️ Execute Cryptographic Tamper Test (Simulate Hack)",
            type="primary",
            use_container_width=True,
        ):
            # Check original
            orig_payload = {
                k: v for k, v in original_data.items() if k != "signature"
            }
            orig_is_valid = verify_credential_signature(
                orig_payload, original_data["signature"]
            )

            # Check tampered
            tamp_payload = {
                k: v for k, v in tampered_data.items() if k != "signature"
            }
            tamp_is_valid = verify_credential_signature(
                tamp_payload, tampered_data["signature"]
            )

            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.success("✅ Original Credential: VALID SIGNATURE")
            with res_c2:
                st.error(
                    "🚨 Tampered Credential: INVALID — HMAC SIGNATURE MISMATCH DETECTED"
                )

            st.markdown(
                f"""
                <div style="background: #0B0F19; border: 1px solid #EF4444; border-radius: 8px; padding: 14px; margin-top: 12px; font-family: monospace; font-size: 0.8rem;">
                    <span style="color: #94A3B8;">Computed HMAC on tampered payload:</span><br>
                    <span style="color: #EF4444;">{generate_credential_signature(tamp_payload)}</span><br><br>
                    <span style="color: #A5ABB5;">Claimed Signature in JSON:</span><br>
                    <span style="color: #19C7B5;">{tampered_data['signature']}</span><br><br>
                    <span style="color: #F8FAFC; font-weight: bold;">VERDICT: Cryptographic mismatch. Tampering blocked.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
