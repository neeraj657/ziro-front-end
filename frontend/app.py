import os
import sys
import streamlit as st

# Ensure frontend root and parent workspace are in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import APP_ICON, APP_NAME, DEFAULT_BACKEND_URL
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.repository_form import render_repository_form
from components.agent_timeline import render_agent_timeline
from components.evidence_view import render_evidence_view
from components.viva_interface import render_viva_interface
from components.credential_view import render_credential_view
from components.evaluation_panel import render_evaluation_panel

# Configure Streamlit Page
st.set_page_config(
    page_title=f"{APP_NAME} — Agentic Skill Verification",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dark Theme CSS Injection (Midnight Graphite + Electric Teal + Soft Mint)
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F4F5F7;
    }

    /* Main background */
    .stApp {
        background-color: #111318;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #171A21;
        border-right: 1px solid #343A44;
    }

    /* Top header bar */
    header[data-testid="stHeader"] {
        background-color: rgba(17, 19, 24, 0.95);
        backdrop-filter: blur(12px);
    }

    /* Metric cards */
    [data-testid="metric-container"], [data-testid="stMetric"] {
        background: #20242B;
        border: 1px solid #343A44;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    /* Input text & select fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox > div > div > div,
    div[data-baseweb="input"] {
        background-color: #292F38 !important;
        color: #F4F5F7 !important;
        border: 1px solid #343A44 !important;
        border-radius: 8px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #8D95A3 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    div[data-baseweb="input"]:focus-within {
        border-color: #19C7B5 !important;
        box-shadow: 0 0 0 2px rgba(25, 199, 181, 0.25) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* Electric Teal background with #071A19 high-contrast dark text */
    .stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"] {
        background: #19C7B5 !important;
        border: none !important;
        color: #071A19 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(25, 199, 181, 0.35);
    }

    .stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover {
        background: #15B3A2 !important;
        color: #071A19 !important;
        box-shadow: 0 6px 20px rgba(25, 199, 181, 0.5);
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] * {
        color: #071A19 !important;
        font-weight: 700 !important;
    }

    .stButton > button[kind="secondary"],
    div.stButton > button[data-testid="baseButton-secondary"] {
        background-color: #20242B !important;
        color: #F4F5F7 !important;
        border: 1px solid #343A44 !important;
    }

    .stButton > button[kind="secondary"]:hover,
    div.stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #292F38 !important;
        border-color: #19C7B5 !important;
        color: #19C7B5 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #20242B !important;
        border: 1px solid #343A44 !important;
        border-radius: 8px !important;
        color: #F4F5F7 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #343A44;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #171A21;
        border-radius: 8px 8px 0 0;
        border: 1px solid #343A44;
        border-bottom: none;
        color: #A5ABB5;
        font-weight: 600;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #20242B !important;
        color: #19C7B5 !important;
        border-color: #19C7B5 !important;
    }

    /* Code blocks */
    code {
        font-family: 'JetBrains Mono', monospace;
        background-color: #171A21 !important;
        color: #A7F3D0 !important;
        border: 1px solid #343A44 !important;
    }

    /* Smooth scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #111318;
    }
    ::-webkit-scrollbar-thumb {
        background: #343A44;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #19C7B5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "active_session" not in st.session_state:
    st.session_state["active_session"] = {
        "candidate_id": "",
        "repo_url": "",
        "claimed_skills": [],
        "description": "",
        "status": "NOT_STARTED",
        "timeline": [],
        "skill_assessment": {},
        "viva_questions": [],
    }

if "backend_url" not in st.session_state:
    st.session_state["backend_url"] = DEFAULT_BACKEND_URL

# Render Navigation Sidebar
current_page = render_sidebar()

# Page Routing
if current_page == "Dashboard":
    render_dashboard()
elif current_page == "Verify Candidate":
    render_repository_form()
elif current_page == "Agent Activity":
    render_agent_timeline()
elif current_page == "Skill Evidence":
    render_evidence_view()
elif current_page == "Viva Interview":
    render_viva_interface()
elif current_page == "Credential Verification":
    render_credential_view()
elif current_page == "Evaluation Metrics":
    render_evaluation_panel()
else:
    render_dashboard()
