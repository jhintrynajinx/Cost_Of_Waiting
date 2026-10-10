"""
ui/screen_inputs.py
Screen 1 (Inputs) for The Cost of Waiting application.
Minimalist Google Stitch design, streamlined single controls for horizon age and budget,
automatic live BMI-for-age screening indicator update without redundant buttons.
"""

from __future__ import annotations

import streamlit as st
from calculator.bmi import calculate_bmi, interpret_child_bmi


def render_screen_inputs() -> None:
    """Render Screen 1 — Inputs & Biometric Calibration."""
    # Initialize persistent session state defaults if not already present
    if "child_age" not in st.session_state:
        st.session_state["child_age"] = 10
    if "sex" not in st.session_state:
        st.session_state["sex"] = "male"
    if "height_cm" not in st.session_state:
        st.session_state["height_cm"] = 138.0
    if "weight_kg" not in st.session_state:
        st.session_state["weight_kg"] = 42.5
    if "target_age" not in st.session_state:
        st.session_state["target_age"] = 80
    if "monthly_budget" not in st.session_state:
        st.session_state["monthly_budget"] = 150.0

    # Top Horizon Navigation Bar
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 15px; color: #0b1c30; letter-spacing: -0.02em;">THE COST OF WAITING</span>
                <span class="stitch-pill">INPUT PARAMETERS</span>
                <span style="color: #cbd5e1;">|</span>
                <span style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Malaysian Pediatric Health Economics</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with header_col2:
        top_btn_c1, top_btn_c2 = st.columns([1, 1])
        with top_btn_c1:
            st.markdown(
                '<div style="text-align: right; padding-top: 4px; font-size: 11px; color: #64748b;"><strong style="color: #0f766e;">Currency:</strong> MYR (RM)</div>',
                unsafe_allow_html=True,
            )
        with top_btn_c2:
            if st.button("Reset Defaults", key="reset_btn", help="Reset all parameters to baseline Malaysian defaults."):
                defaults = {
                    "child_age": 10,
                    "sex": "male",
                    "height_cm": 138.0,
                    "weight_kg": 42.5,
                    "target_age": 80,
                    "monthly_budget": 150.0,
                }
                for k, v in defaults.items():
                    st.session_state[k] = v
                # Clean up widget keys to avoid stale overrides
                for wk in ["widget_child_age", "widget_sex", "widget_height_cm", "widget_weight_kg", "widget_target_age", "widget_monthly_budget"]:
                    if wk in st.session_state:
                        del st.session_state[wk]
                st.rerun()

    # Subtitle Header Row
    st.markdown(
        """
        <div style="border-bottom: 1.5px solid #e2e8f0; padding-bottom: 1.25rem; margin-bottom: 1.75rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #0f766e; display: inline-block;"></span>
                <span style="font-size: 12.5px; font-weight: 700; color: #0f766e; text-transform: uppercase; letter-spacing: 0.06em;">NHMS 2019 / WHO 2007 Actuarial Model</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
                <div>
                    <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 32px; font-weight: 800; color: #0b1c30; margin: 0; line-height: 1.2;">Child Health Profile & Simulation Parameters</h1>
                    <p style="font-family: 'Inter', sans-serif; font-size: 15.5px; color: #475569; margin: 6px 0 0 0;">Calibrate biometric markers and projection horizon to estimate lifetime healthcare trajectories.</p>
                </div>
                <div>
                    <span style="font-size: 13px; font-weight: 700; background: #f8fafc; border: 1px solid #cbd5e1; padding: 6px 14px; border-radius: 6px; color: #334155;">Pediatric Standard: 5;0–17;11 yrs</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------------------------
    # Main Input Columns (Live, responsive controls without redundant buttons)
    # ---------------------------------------------------------------------------
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="stitch-card-header">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 700; color: #0f766e; text-transform: uppercase; letter-spacing: 0.04em;">01 • Child Information & Biometrics</span>
                <span style="font-size: 12.5px; font-weight: 600; color: #475569; background: #f8fafc; padding: 3px 10px; border-radius: 4px; border: 1px solid #cbd5e1;">Standard LMS Anthropometry</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            child_age = st.number_input(
                "Child Age (years)",
                min_value=5,
                max_value=17,
                value=int(st.session_state["child_age"]),
                step=1,
                key="widget_child_age",
                help="Cohort range: 5 to 17 completed years.",
            )
            st.caption("Cohort range: 5 to 17 yrs")

        with sub_c2:
            sex_options = ["male", "female"]
            curr_idx = 0 if st.session_state["sex"] == "male" else 1
            sex = st.radio(
                "Biological Sex",
                options=sex_options,
                index=curr_idx,
                format_func=lambda x: "Male" if x == "male" else "Female",
                horizontal=True,
                key="widget_sex",
                help="LMS z-score lookup baseline.",
            )
            st.caption("LMS z-score lookup baseline")

        sub_c3, sub_c4 = st.columns(2)
        with sub_c3:
            height_cm = st.number_input(
                "Height (Stature in cm)",
                min_value=90.0,
                max_value=200.0,
                value=float(st.session_state["height_cm"]),
                step=0.5,
                key="widget_height_cm",
                help="Precision: ±0.5 cm stadiometer.",
            )
            st.caption("Precision: ±0.5 cm stadiometer")

        with sub_c4:
            weight_kg = st.number_input(
                "Current Weight (kg)",
                min_value=15.0,
                max_value=160.0,
                value=float(st.session_state["weight_kg"]),
                step=0.1,
                key="widget_weight_kg",
                help="Calibrated scale measurement.",
            )
            st.caption("Digital/calibrated beam scale")

        # Live Automatic Screening Status Evaluation
        calc_bmi = calculate_bmi(weight_kg, height_cm)
        bmi_info = interpret_child_bmi(calc_bmi, age_years=int(child_age), sex=sex)
        category = bmi_info["category"]
        z_score = bmi_info["z_score"]

        if category in {"Obese", "Overweight"}:
            badge_class = "stitch-badge-bmi"
            text_color = "#ea580c"
            badge_dot = "#ea580c"
        else:
            badge_class = "stitch-badge-bmi-ok"
            text_color = "#0f766e"
            badge_dot = "#0f766e"

        st.markdown(
            f"""
            <div class="{badge_class}" style="padding: 1.25rem; border-radius: 12px; margin-top: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: {text_color}; letter-spacing: 0.05em;">Calculated Screening Status</span>
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 800; color: {text_color};">BMI {calc_bmi:.2f} kg/m²</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px; font-size: 14.5px; color: #334155;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: {badge_dot}; display: inline-block;"></span>
                    <span>z-score: <strong>{z_score:+.2f} SD</strong> • {category} reference range</span>
                </div>
                <div style="margin-top: 10px; font-size: 13px; color: #64748b; line-height: 1.4; border-top: 1px dashed rgba(15,118,110,0.2); padding-top: 8px;">
                    ⚠️ <em>BMI-for-age is an epidemiological screening indicator, not a clinical diagnosis. Consult a paediatrician for clinical assessment.</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        # Card 02: Actuarial Horizon (Single reliable control with prominent dynamic readout)
        st.markdown(
            """
            <div class="stitch-card-header">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 700; color: #0f766e; text-transform: uppercase; letter-spacing: 0.04em;">02 • Actuarial Horizon</span>
                <span style="font-size: 12.5px; font-weight: 600; color: #475569; background: #f8fafc; padding: 3px 10px; border-radius: 4px; border: 1px solid #cbd5e1;">DOSM Life Tables</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        min_target = max(18, int(child_age) + 1)
        max_target = 80
        saved_target = int(st.session_state.get("target_age", 80))
        valid_default_target = max(min_target, min(saved_target, max_target))

        # Prominent headline label before slider
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 700; color: #0b1c30;">Projection Target Age</span>
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 800; color: #0f766e; background: #f0fdfa; border: 1.5px solid #99f6e4; padding: 4px 14px; border-radius: 6px;">
                    Project costs until age {valid_default_target}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        target_age = st.slider(
            "Project costs until age (years)",
            min_value=min_target,
            max_value=max_target,
            value=valid_default_target,
            step=1,
            label_visibility="collapsed",
            key="widget_target_age",
            help="Drag slider to project costs from child age until target adulthood age (up to age 80).",
        )

        span_years = max(int(target_age) - int(child_age), 1)
        span_months = span_years * 12

        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 6px; margin-bottom: 1.5rem; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
                <div>
                    <span style="font-size: 14px; color: #475569;">Selected Horizon:</span>
                    <strong style="font-size: 16px; color: #0b1c30; margin-left: 6px;">Age {target_age}</strong>
                </div>
                <div>
                    <span style="font-size: 13px; text-transform: uppercase; color: #475569; font-weight: 600;">Projection Span:</span>
                    <strong style="font-size: 15px; color: #0f766e; margin-left: 6px;">{span_years} Years ({span_months} Months)</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Card 03: Monthly Lifestyle Budget (Single discrete select_slider control with prominent readout)
        st.markdown(
            """
            <div class="stitch-card-header">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 700; color: #0f766e; text-transform: uppercase; letter-spacing: 0.04em;">03 • Monthly Lifestyle Budget</span>
                <span style="font-size: 12.5px; font-weight: 600; color: #475569; background: #f8fafc; padding: 3px 10px; border-radius: 4px; border: 1px solid #cbd5e1;">Household Sensitivity</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        budget_options = [0, 50, 100, 150, 200, 300, 500]
        saved_budget = int(st.session_state.get("monthly_budget", 150))
        if saved_budget not in budget_options:
            saved_budget = min(budget_options, key=lambda x: abs(x - saved_budget))

        prominent_budget_str = f"RM {saved_budget:,.0f}/month" if saved_budget > 0 else "RM 0 (Free Public Care)"

        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 700; color: #0b1c30;">Monthly Lifestyle Budget</span>
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 800; color: #0f766e; background: #f0fdfa; border: 1.5px solid #99f6e4; padding: 4px 14px; border-radius: 6px;">
                    {prominent_budget_str}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        monthly_budget = st.select_slider(
            "Monthly Lifestyle Budget (Discretionary Reinvestment)",
            options=budget_options,
            value=saved_budget,
            format_func=lambda x: "RM 0" if x == 0 else f"RM {x}",
            label_visibility="collapsed",
            key="widget_monthly_budget",
            help="Select monthly household budget tier (RM 0, 50, 100, 150, 200, 300, 500). RM 0 provides free MOH/public health recommendations.",
        )

        if monthly_budget == 0:
            budget_note = "Zero out-of-pocket: Recommends MOH Klinik Kesihatan, school fields, and Suku-Suku Separuh meal rebalancing."
        elif monthly_budget <= 150:
            budget_note = f"Moderate tier: Recommends fresh produce reallocation and community recreation up to RM {monthly_budget}/month."
        else:
            budget_note = f"Comprehensive tier: Recommends structured nutrition and youth athletic activities within RM {monthly_budget}/month."

        st.markdown(
            f"""
            <div style="font-size: 14px; color: #334155; padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-top: 6px; line-height: 1.45;">
                <strong style="color: #0f766e;">Budget Allocation Protocol:</strong> {budget_note}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Always keep session state synchronized with entered values
    st.session_state["child_age"] = int(child_age)
    st.session_state["sex"] = str(sex)
    st.session_state["height_cm"] = float(height_cm)
    st.session_state["weight_kg"] = float(weight_kg)
    st.session_state["target_age"] = int(target_age)
    st.session_state["monthly_budget"] = float(monthly_budget)

    # ---------------------------------------------------------------------------
    # Bottom Action Bar
    # ---------------------------------------------------------------------------
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    action_col1, action_col2 = st.columns([3, 1])
    with action_col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; padding: 14px 18px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px;">
                <span style="width: 10px; height: 10px; border-radius: 50%; background: #0f766e; display: inline-block;"></span>
                <div>
                    <div style="font-size: 14.5px; font-weight: 700; color: #0b1c30;">Actuarial Calibration Ready</div>
                    <div style="font-size: 13.5px; color: #475569;">Cohort Age {child_age} → {target_age} yrs • Discretionary Budget: {prominent_budget_str} • Live screening indicator updated</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col2:
        generate_clicked = st.button(
            "Generate Trajectory →",
            key="generate_report_btn",
            type="primary",
            use_container_width=True,
            help="Validate parameters and generate actuarial report.",
        )

    if generate_clicked:
        validation_errors = []
        if not (5 <= child_age <= 17):
            validation_errors.append(f"Child age must be between 5 and 17 years; got {child_age}.")
        if not (90.0 <= height_cm <= 200.0):
            validation_errors.append(f"Height must be between 90.0 cm and 200.0 cm; got {height_cm:.1f} cm.")
        if not (15.0 <= weight_kg <= 160.0):
            validation_errors.append(f"Weight must be between 15.0 kg and 160.0 kg; got {weight_kg:.1f} kg.")
        if target_age <= child_age:
            validation_errors.append(f"Target horizon age ({target_age}) must be strictly greater than child age ({child_age}).")
        if target_age > 80:
            validation_errors.append(f"Target horizon age cannot exceed 80 years; got {target_age}.")
        if monthly_budget < 0:
            validation_errors.append(f"Monthly budget must be non-negative; got RM {monthly_budget:.2f}.")

        if validation_errors:
            for err in validation_errors:
                st.error(f"⚠️ Validation Error: {err}")
        else:
            # Route to report screen
            st.session_state["screen"] = "report"
            st.rerun()

    # Minimalist Footer
    st.markdown(
        """
        <div class="stitch-footer" style="font-size: 13px; color: #64748b; padding-top: 1.25rem; margin-top: 2rem;">
            The Cost of Waiting • Illustrative actuarial decision-support model based on Malaysian NHMS and WHO growth standards • Not a clinical diagnosis • Strictly confidential hackathon prototype.
        </div>
        """,
        unsafe_allow_html=True,
    )
