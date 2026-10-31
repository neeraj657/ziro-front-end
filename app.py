"""SkillProof AI — Root Streamlit Application Launcher.

Delegates execution to skillproof/frontend/app.py while ensuring all local imports resolve correctly.
"""
import os
import sys

# Add skillproof/frontend directory to sys.path
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skillproof", "frontend")
if frontend_dir not in sys.path:
    sys.path.insert(0, frontend_dir)

# Execute the master frontend app script
import runpy

app_path = os.path.join(frontend_dir, "app.py")
runpy.run_path(app_path, run_name="__main__")

