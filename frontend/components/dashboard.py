"""SkillProof AI — Root frontend dashboard component.

Delegates directly to skillproof.frontend.components.dashboard for unified
zero-synthetic-data production architecture.
"""
import os
import sys

_skillproof_frontend = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "skillproof", "frontend")
)
if _skillproof_frontend not in sys.path:
    sys.path.insert(0, _skillproof_frontend)

from components.dashboard import render_overview_dashboard, render_dashboard

__all__ = ["render_overview_dashboard", "render_dashboard"]
