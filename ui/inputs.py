"""
ui/inputs.py
Streamlit input widgets for collecting user profile data.

Returns a plain Python dict so the rest of the app can pass values to the
calculator layer without any Streamlit dependency leaking through.
"""

from __future__ import annotations

import streamlit as st


def render_user_inputs() -> dict[str, object]:
    """Render all user input widgets and return collected values.

    Returns
    -------
    dict[str, object]
        Keys and value types:
        - ``age``        : int   — current age in years (2–17)
        - ``sex``        : str   — 'male' or 'female'
        - ``height_cm``  : float — height in centimetres
        - ``weight_kg``  : float — weight in kilograms
        - ``end_age``    : int   — projection end age (default 80)

    Note
    ----
    This function is a placeholder. Widgets are defined but not yet wired
    to the calculation engine.
    """
    st.markdown("### Your details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Current age (years)",
            min_value=2,
            max_value=17,
            value=10,
            step=1,
            help="This calculator focuses on children and adolescents aged 2–17.",
        )
        height_cm = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=220.0,
            value=140.0,
            step=0.5,
        )

    with col2:
        sex = st.selectbox(
            "Sex",
            options=["male", "female"],
            format_func=str.capitalize,
        )
        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=5.0,
            max_value=200.0,
            value=50.0,
            step=0.5,
        )

    st.markdown("### Projection settings")
    end_age = st.slider(
        "Project costs through age",
        min_value=20,
        max_value=80,
        value=80,
        step=1,
        help="The calculator will estimate cumulative costs from your current age to this age.",
    )

    return {
        "age": int(age),
        "sex": str(sex),
        "height_cm": float(height_cm),
        "weight_kg": float(weight_kg),
        "end_age": int(end_age),
    }
