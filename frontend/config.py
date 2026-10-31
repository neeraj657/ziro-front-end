import os

# SkillProof AI — Configuration
APP_NAME = "SkillProof AI"
APP_TAGLINE = "Autonomous Agentic Skill & Credential Verification Platform"
APP_ICON = "🛡️"

# Backend API Configuration
DEFAULT_BACKEND_URL = os.environ.get("SKILLPROOF_BACKEND_URL", "http://127.0.0.1:8000")
API_TIMEOUT_SECONDS = int(os.environ.get("SKILLPROOF_API_TIMEOUT", "10"))

# Supported Skills for Verification
SUPPORTED_SKILLS = [
    "Python",
    "JavaScript",
    "React",
    "Machine Learning",
    "SQL",
    "FastAPI",
]

# Theme: Midnight Graphite + Electric Teal + Soft Mint
COLORS = {
    "background": "#111318",       # Midnight Graphite
    "surface": "#171A21",          # Deep Charcoal
    "surface_card": "#20242B",     # Dark Slate
    "surface_card_hover": "#292F38",
    "border": "#343A44",           # Slate Grey
    "border_light": "#454D59",
    "primary": "#19C7B5",          # Electric Teal
    "primary_hover": "#15B3A2",
    "secondary": "#A7F3D0",        # Soft Mint
    "accent_blue": "#19C7B5",
    "accent_cyan": "#19C7B5",
    "accent_purple": "#A7F3D0",
    "success": "#19C7B5",
    "success_bg": "rgba(167, 243, 208, 0.12)",
    "warning": "#F0B45A",          # Amber
    "warning_bg": "rgba(240, 180, 90, 0.12)",
    "danger": "#F07178",           # Coral
    "danger_bg": "rgba(240, 113, 120, 0.12)",
    "text_main": "#F4F5F7",        # Off-white
    "text_muted": "#A5ABB5",       # Cool Grey
    "text_dim": "#8D95A3",
    "btn_text_dark": "#071A19",    # Dark text on Electric Teal
}
