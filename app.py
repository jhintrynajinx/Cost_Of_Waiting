"""
app.py — The Cost of Waiting
Malaysian Childhood Obesity Financial Decision-Support Web Application.
Faithfully reproduces the Google Stitch minimalist design layout.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st
from ui.styles import STITCH_CSS
from ui.screen_inputs import render_screen_inputs
from ui.screen_report import render_screen_report

# ---------------------------------------------------------------------------
# Page Configuration (Optimised for 1920x1080 Boardroom Presentation Screen)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="The Cost of Waiting — Pediatric Health Economics",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject Google Stitch CSS Stylesheet
st.markdown(STITCH_CSS, unsafe_allow_html=True)



# ---------------------------------------------------------------------------
# Session State Management & Routing
# ---------------------------------------------------------------------------
if "screen" not in st.session_state:
    st.session_state["screen"] = "inputs"

if st.session_state["screen"] == "inputs":
    render_screen_inputs()
else:
    render_screen_report()
