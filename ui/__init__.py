"""
ui/
Streamlit UI components for the Cost of Waiting application.

Modules
-------
inputs      User-facing input widgets (age, sex, height, weight, etc.).
charts      Plotly chart builders for cost projections.
summary     Results summary layout and formatted output.

All modules in this package depend on Streamlit and Plotly.
Do not import calculator logic directly into this package —
call calculator functions from app.py and pass results in.
"""
