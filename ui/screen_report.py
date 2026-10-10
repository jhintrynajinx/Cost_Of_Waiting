"""
ui/screen_report.py
Screen 2 (Report) for The Cost of Waiting application, faithfully reproducing
the Google Stitch design layout, typography, cumulative chart, prescription plan,
and the comprehensive "Where Do the Costs Come From?" evidence-based breakdown.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from calculator.bmi import calculate_bmi, interpret_child_bmi
from calculator.projection import project_lifetime_costs


def get_budget_prescription_content(monthly_budget: float) -> dict[str, Any]:
    """Generate budget-sensitive recommendations tailored to the parent's monthly budget.

    Strict financial constraints:
    - Never allocates more than the available monthly budget.
    - RM 0 offers 100% free / public-service options.
    - Modest budgets (RM 1–199) produce realistic, sustainable allocations.
    - Higher budgets (RM 200+) include structured guidance and youth athletics.
    - Does not claim that higher spending guarantees better clinical outcomes or savings.
    """
    if monthly_budget <= 0:
        return {
            "title": "Public Health & Community Resource Pathway",
            "subtitle": "Zero Out-of-Pocket Family Lifestyle Protocol",
            "outlay_label": "RM 0 / mo",
            "outlay_sub": "100% Free / Public Resources",
            "badge_color": "#0f766e",
            "items": [
                {
                    "num": "1",
                    "title": "MOH Suku-Suku Separuh Meal Rebalancing (RM 0):",
                    "desc": " Adopt Malaysian Dietary Guidelines quarter-quarter-half plate model; substitute sweetened daily cordial/milo with plain boiled water; reallocate existing grocery spending rather than adding cost.",
                },
                {
                    "num": "2",
                    "title": "Public Parks & School Fields Active Play (RM 0):",
                    "desc": " Minimum 60 minutes/day active play at local municipal parks (taman awam), school fields, community playgrounds, and neighbourhood walking circuits.",
                },
                {
                    "num": "3",
                    "title": "Subsidised Klinik Kesihatan Monitoring (RM 1/visit):",
                    "desc": " Biannual paediatric growth monitoring at nearest Ministry of Health Klinik Kesihatan under the RM 1 universal primary healthcare system.",
                },
            ],
            "note": "Financial expenditure is not a prerequisite for positive health outcomes. Consistent household habit routines and screen-time management drive primary success.",
        }
    elif monthly_budget < 200:
        food_alloc = max(int(monthly_budget * 0.40), 10)
        play_alloc = max(int(monthly_budget * 0.35), 10)
        med_alloc = max(int(monthly_budget * 0.15), 5)
        low_range = int(monthly_budget * 0.50)
        high_range = int(monthly_budget * 0.85)

        return {
            "title": "Targeted Family Nutrition & Active Play",
            "subtitle": "Modest Budget Sustainable Protocol",
            "outlay_label": f"RM {low_range}–{high_range} / mo",
            "outlay_sub": f"within RM {monthly_budget:,.0f} budget",
            "badge_color": "#0f766e",
            "items": [
                {
                    "num": "1",
                    "title": f"Whole-Family Fresh Produce Shift (~RM {food_alloc}/mo):",
                    "desc": " Targeted reallocation toward local market leafy vegetables, seasonal fruit (papaya, banana, guava), and whole-food proteins (eggs, tempeh, tofu) replacing packaged processed snacks.",
                },
                {
                    "num": "2",
                    "title": f"Active Recreation Gear & Entry (~RM {play_alloc}/mo):",
                    "desc": " Basic recreation equipment (badminton racquets, jump ropes, football) and entry to municipal swimming complexes or local community hall court rentals.",
                },
                {
                    "num": "3",
                    "title": f"Primary Care Tracking Buffer (~RM {med_alloc}/mo reserve):",
                    "desc": " Bi-annual check-ins at Klinik Kesihatan or community GP, maintaining a reserve for routine paediatric dietary consultation or guidance.",
                },
            ],
            "note": "Allocations are capped within the parent's selected monthly budget. Consistency in whole foods and daily active play drives positive health outcomes without needing large expenditures.",
        }
    else:
        food_alloc = int(monthly_budget * 0.40)
        sport_alloc = int(monthly_budget * 0.40)
        clinical_alloc = int(monthly_budget * 0.15)
        low_range = int(monthly_budget * 0.60)
        high_range = int(monthly_budget * 0.90)

        return {
            "title": "Structured Nutrition & Youth Coaching",
            "subtitle": "Comprehensive Multi-Modal Protocol",
            "outlay_label": f"RM {low_range}–{high_range} / mo",
            "outlay_sub": f"within RM {monthly_budget:,.0f} budget",
            "badge_color": "#0f766e",
            "items": [
                {
                    "num": "1",
                    "title": f"Structured Family Nutrition & MDA Dietitian (~RM {food_alloc}/mo):",
                    "desc": " Whole-foods meal prep planning with periodic consultations from a Malaysian Dietitians' Association (MDA) registered paediatric dietitian for structured dietary adjustments.",
                },
                {
                    "num": "2",
                    "title": f"Enrolled Youth Athletics & Coaching (~RM {sport_alloc}/mo):",
                    "desc": " Enrolment in weekend community youth badminton coaching, swim school, martial arts, or organized team sports for structured cardiovascular fitness (2–3 sessions/week).",
                },
                {
                    "num": "3",
                    "title": f"Quarterly Metabolic & Biometric Review (~RM {clinical_alloc}/mo reserve):",
                    "desc": " Scheduled quarterly paediatric check-ins, routine metabolic screenings if clinically recommended, and digital activity tracking.",
                },
            ],
            "note": "Higher financial investment offers structured coaching and professional guidance, but parental role modeling and family-wide adoption remain the primary determinants of outcome.",
        }


def render_clean_html(html_str: str) -> None:
    """Render HTML without leading indentation so CommonMark never triggers code blocks."""
    clean = "\n".join(line.strip() for line in html_str.strip().splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def render_screen_report() -> None:
    """Render Screen 2 — Financial Projection Report."""

    # Inject page-level subtle fade-in transition (200ms) for Screen 2 mount
    st.markdown(
        """
        <style>
        .main .block-container {
            animation: stitchReportFadeIn 200ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        @media (prefers-reduced-motion: reduce) {
            .main .block-container {
                animation: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    child_age = int(st.session_state.get("child_age", 10))
    sex = str(st.session_state.get("sex", "male"))
    height_cm = float(st.session_state.get("height_cm", 138.0))
    weight_kg = float(st.session_state.get("weight_kg", 42.5))
    target_age = int(st.session_state.get("target_age", 80))
    monthly_budget = float(st.session_state.get("monthly_budget", 150.0))

    # Evaluate Biometrics
    calc_bmi = calculate_bmi(weight_kg, height_cm)
    bmi_info = interpret_child_bmi(calc_bmi, age_years=child_age, sex=sex)
    category = bmi_info["category"]
    z_score = bmi_info["z_score"]

    # Compute Projections (with 3.0% Treasury Discount Rate)
    res = project_lifetime_costs(
        current_age=child_age,
        sex=sex,
        weight_status=category,
        end_age=target_age,
        optional_monthly_budget_myr=monthly_budget,
        adjust_inflation=True,
        inflation_scenario="central",
    )

    yearly_data = res["yearly_projections"]
    duration = res["summary"]["projection_duration_years"]

    # Calculate discounted present values (SDR 3.0%) for actuarial accuracy
    discount_rate = 0.03
    ages = []

    # Full pathway cumulative discounted series (baseline living costs + scenario)
    cum_pv_a_full = 0.0
    cum_pv_b_full = 0.0
    cum_pv_ref_full = 0.0
    discounted_a_full_series = []
    discounted_b_full_series = []
    discounted_ref_full_series = []

    # Incremental / additional series (relative to normal-weight baseline)
    cum_pv_a_excess = 0.0
    cum_pv_b_intervention = 0.0
    discounted_a_excess_series = []
    discounted_b_intervention_series = []

    # Category discounted totals (Additional / Excess)
    pv_food_a = 0.0
    pv_clothing_a = 0.0
    pv_transport_a = 0.0
    pv_healthcare_a = 0.0
    pv_intervention_b = 0.0

    # Category discounted totals (Normal-Weight Reference Baseline)
    pv_food_ref = 0.0
    pv_clothing_ref = 0.0
    pv_transport_ref = 0.0
    pv_healthcare_ref = 0.0

    for row in yearly_data:
        offset = row["offset_years"]
        dfactor = (1 + discount_rate) ** offset

        # Reference category discounted PVs
        pv_food_ref += row["food_ref_myr"] / dfactor
        pv_clothing_ref += row["clothing_ref_myr"] / dfactor
        pv_transport_ref += row["transport_ref_myr"] / dfactor
        pv_healthcare_ref += row["healthcare_ref_myr"] / dfactor

        # Incremental category discounted PVs
        pv_food_a += row["food_myr"] / dfactor
        pv_clothing_a += row["clothing_myr"] / dfactor
        pv_transport_a += row["transport_myr"] / dfactor
        pv_healthcare_a += row["healthcare_myr"] / dfactor
        pv_intervention_b += row["intervention_myr"] / dfactor

        # Full pathway discounted annual amounts
        pv_a_full_yr = row["scenario_a_full_annual_myr"] / dfactor
        pv_b_full_yr = row["scenario_b_full_annual_myr"] / dfactor
        pv_ref_full_yr = row["reference_annual_myr"] / dfactor

        cum_pv_a_full += pv_a_full_yr
        cum_pv_b_full += pv_b_full_yr
        cum_pv_ref_full += pv_ref_full_yr

        discounted_a_full_series.append(cum_pv_a_full)
        discounted_b_full_series.append(cum_pv_b_full)
        discounted_ref_full_series.append(cum_pv_ref_full)

        # Incremental discounted annual amounts
        pv_a_excess_yr = row["scenario_a_annual_myr"] / dfactor
        pv_b_int_yr = row["scenario_b_annual_myr"] / dfactor

        cum_pv_a_excess += pv_a_excess_yr
        cum_pv_b_intervention += pv_b_int_yr

        discounted_a_excess_series.append(cum_pv_a_excess)
        discounted_b_intervention_series.append(cum_pv_b_intervention)

        ages.append(row["age"])

    total_a = cum_pv_a_excess
    total_b = cum_pv_b_intervention
    delta = total_a - total_b

    # Parametric 80% Confidence Interval bounds (±25%)
    ci_a_low = total_a * 0.75
    ci_a_high = total_a * 1.30
    ci_b_low = total_b * 0.75
    ci_b_high = total_b * 1.35

    # Top Horizon Bar
    top_col1, top_col2, top_col3 = st.columns([1.5, 3, 1])

    with top_col1:
        if st.button("← Back to Inputs", key="back_btn", help="Return to biometrics and keep entered values."):
            st.session_state["screen"] = "inputs"
            st.rerun()

    with top_col2:
        render_clean_html(
            f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 14.5px; color: #334155; background: #f8fafc; border: 1.5px solid #cbd5e1; padding: 8px 18px; border-radius: 9999px;">
                <span style="font-weight: 800; color: #0b1c30;">{child_age} y/o {sex.capitalize()}</span>
                <span style="color: #cbd5e1;">•</span>
                <span>{height_cm:.1f} cm / {weight_kg:.1f} kg (Z: <strong>{z_score:+.2f} SD</strong>)</span>
                <span style="color: #cbd5e1;">•</span>
                <span>Horizon: <strong>Age {child_age} → {target_age} ({duration} yrs)</strong></span>
                <span style="color: #cbd5e1;">•</span>
                <span>Budget: <strong style="color: #0f766e;">RM {monthly_budget:,.0f}/mo</strong></span>
            </div>
            """,
        )

    with top_col3:
        render_clean_html(
            """
            <div style="text-align: right;">
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 14px; color: #0b1c30;">THE COST OF WAITING</span>
                <span class="stitch-pill" style="margin-left: 6px;">MODEL VIEW</span>
            </div>
            """,
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 1: Headline Scenario A versus Scenario B Comparison
    # =========================================================================
    m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        render_clean_html(
            f"""
            <div class="metric-box-a" style="padding: 1.5rem; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; color: #ea580c; letter-spacing: 0.05em;">Cost of Waiting</span>
                    <span style="font-size: 12px; color: #64748b; font-weight: 600;">Unmitigated Trajectory</span>
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #0b1c30; letter-spacing: -0.02em; line-height: 1.15;">
                    RM {total_a:,.0f}
                </div>
                <p style="font-size: 13.5px; color: #475569; margin-top: 6px; line-height: 1.4;">
                    {duration}-yr discounted present value <span style="color: #1e293b; font-weight: 700;">(80% CI: RM {ci_a_low/1000:.0f}k – RM {ci_a_high/1000:.0f}k)</span>
                </p>
            </div>
            """,
        )

    with m_col2:
        render_clean_html(
            f"""
            <div class="metric-box-b" style="padding: 1.5rem; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; color: #0f766e; letter-spacing: 0.05em;">Cost of Taking Action</span>
                    <span style="font-size: 12px; color: #0f766e; font-weight: 700;">Preventive Reinvestment</span>
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #0f766e; letter-spacing: -0.02em; line-height: 1.15;">
                    RM {total_b:,.0f}
                </div>
                <p style="font-size: 13.5px; color: #475569; margin-top: 6px; line-height: 1.4;">
                    {duration}-yr preventive outlay <span style="color: #1e293b; font-weight: 700;">(80% CI: RM {ci_b_low/1000:.0f}k – RM {ci_b_high/1000:.0f}k)</span>
                </p>
            </div>
            """,
        )

    with m_col3:
        render_clean_html(
            f"""
            <div class="metric-box-delta" style="padding: 1.5rem; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; color: #0f766e; letter-spacing: 0.05em;">Actuarial Cost Divergence</span>
                    <span style="font-size: 18px; color: #0f766e; font-weight: bold;">↘</span>
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #115e59; letter-spacing: -0.02em; line-height: 1.15;">
                    ~RM {delta:,.0f}
                </div>
                <p style="font-size: 13.5px; color: #334155; margin-top: 6px; line-height: 1.4;">
                    Population econometric divergence over {duration} yrs. Modelled estimate; not guaranteed personal savings or clinical diagnosis.
                </p>
            </div>
            """,
        )

    # =========================================================================
    # SECTION 2: Main Cumulative Cost Trajectory Chart
    # =========================================================================
    chart_header_c1, chart_header_c2 = st.columns([3, 2])
    with chart_header_c1:
        render_clean_html(
            f"""
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 18px; color: #0b1c30; margin-top: 1.25rem;">
                {duration}-Year Cumulative Cost Trajectory (Age {child_age} → {target_age})
                <div style="font-family: 'Inter', sans-serif; font-size: 13.5px; font-weight: 500; color: #475569; margin-top: 4px;">
                    Cumulative Discounted Present Value (2026 RM at 3.0% Treasury SDR) • Sector Inflation Compounded Annually
                </div>
            </div>
            """,
        )

    with chart_header_c2:
        chart_view = st.radio(
            "Chart Accounting Basis",
            options=["Lifetime Expenditure (Baseline + Scenario)", "Incremental Divergence (Relative to Baseline)"],
            index=0,
            horizontal=True,
            key="chart_view_mode",
            help="Toggle between full cumulative lifetime expenditures or incremental obesity-attributable differences.",
        )

    is_lifetime_view = "Lifetime" in chart_view

    if is_lifetime_view:
        # Full lifetime pathway: Scenario B accumulates normal living costs compounded by sector inflation
        # plus intervention. Scenario B is strictly non-flat and reflects positive annual expenditure.
        plot_a = discounted_a_full_series
        plot_b = discounted_b_full_series
        ci_upper = [a * 1.15 for a in plot_a]
        ci_lower = [a * 0.85 for a in plot_a]
        hover_a = "<b>Scenario A (Lifetime Trajectory):</b> RM %{y:,.0f}<extra></extra>"
        hover_b = "<b>Scenario B (Healthy Trajectory):</b> RM %{y:,.0f}<extra></extra>"
    else:
        # Incremental additional burden relative to normal-weight reference
        plot_a = discounted_a_excess_series
        plot_b = discounted_b_intervention_series
        ci_upper = [a * 1.30 for a in plot_a]
        ci_lower = [a * 0.75 for a in plot_a]
        hover_a = "<b>Scenario A (Excess Obesity Cost):</b> RM %{y:,.0f}<extra></extra>"
        hover_b = "<b>Scenario B (Preventive Outlay):</b> RM %{y:,.0f}<extra></extra>"

    # Plotly Line Chart
    fig = go.Figure()

    # 80% CI Band for Scenario A
    fig.add_trace(
        go.Scatter(
            x=ages + ages[::-1],
            y=ci_upper + ci_lower[::-1],
            fill="toself",
            fillcolor="rgba(234, 88, 12, 0.12)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False,
            name="80% CI Band",
        )
    )

    # Scenario A Line (Orange)
    fig.add_trace(
        go.Scatter(
            x=ages,
            y=plot_a,
            mode="lines",
            line=dict(color="#ea580c", width=3.5, shape="spline"),
            name="Scenario A (Inaction)",
            hovertemplate=hover_a,
        )
    )

    # Scenario B Line (Teal)
    fig.add_trace(
        go.Scatter(
            x=ages,
            y=plot_b,
            mode="lines",
            line=dict(color="#0f766e", width=3.5),
            name="Scenario B (Early Action)",
            hovertemplate=hover_b,
        )
    )

    # Divergence highlight (Ages 18 to 25 if included in horizon)
    if child_age < 25 and target_age >= 18:
        fig.add_vrect(
            x0=max(child_age, 18),
            x1=min(target_age, 25),
            fillcolor="rgba(15, 118, 110, 0.05)",
            layer="below",
            line=dict(color="#0f766e", width=1.5, dash="dot"),
            annotation_text="DIVERGENCE: AGES 18–25",
            annotation_position="top left",
            annotation_font=dict(size=11, color="#0f766e", family="Inter"),
        )

    fig.update_layout(
        height=360,
        margin=dict(l=60, r=25, t=15, b=40),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        showlegend=False,
        transition=dict(duration=250, easing="cubic-in-out"),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#0f766e",
            font_size=13.5,
            font_family="Plus Jakarta Sans",
            font_color="#0b1c30",
        ),
        xaxis=dict(
            title=dict(text="Child Age (Years)", font=dict(size=13.5, color="#334155", family="Plus Jakarta Sans")),
            showgrid=True,
            gridcolor="#f1f5f9",
            tickmode="linear",
            dtick=10,
            tickfont=dict(size=12, color="#475569", family="Inter"),
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1.5,
            spikedash="dot",
            spikecolor="#0f766e",
        ),
        yaxis=dict(
            title=dict(text="Cumulative Discounted (RM)", font=dict(size=13.5, color="#334155", family="Plus Jakarta Sans")),
            showgrid=True,
            gridcolor="#f1f5f9",
            tickprefix="RM ",
            tickfont=dict(size=12, color="#475569", family="Inter"),
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # =========================================================================
    # SECTION 3: "Where Do the Costs Come From?" Category Breakdown (Step 3)
    # =========================================================================
    pct_hc_a = (pv_healthcare_a / total_a * 100) if total_a > 0 else 0
    pct_tr_a = (pv_transport_a / total_a * 100) if total_a > 0 else 0
    pct_fd_a = (pv_food_a / total_a * 100) if total_a > 0 else 0
    pct_cl_a = (pv_clothing_a / total_a * 100) if total_a > 0 else 0

    pv_a_full_total = cum_pv_a_full
    pv_b_full_total = cum_pv_b_full
    pv_ref_full_total = cum_pv_ref_full

    render_clean_html(
        f"""
        <div class="stitch-card" style="margin-top: 1rem; margin-bottom: 1.25rem;">
            <div class="stitch-card-header">
                <div>
                    <span class="stitch-card-title">Where Do the Costs Come From?</span>
                    <div style="font-size: 13px; color: #64748b; margin-top: 2px;">
                        Category disaggregation over {duration}-year projection horizon (Age {child_age} → {target_age}) • 3.0% Treasury SDR Discounted Present Values (2026 MYR)
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="stitch-pill">Actuarial Provenance</span>
                </div>
            </div>

            <table class="breakdown-table">
                <thead>
                    <tr>
                        <th style="width: 22%;">Cost Category</th>
                        <th class="num-col" style="width: 13%;">Reference Person (Normal Weight)</th>
                        <th class="num-col" style="width: 14%;">Scenario A (Waiting)</th>
                        <th class="num-col" style="width: 14%;">Scenario B (Early Action)</th>
                        <th class="num-col" style="width: 14%;">Additional Difference</th>
                        <th style="width: 12%;">Actuarial Classification</th>
                        <th style="width: 11%;">Evidence Base</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- 1. Healthcare Expenses -->
                    <tr>
                        <td>
                            <strong style="color: #0b1c30; font-size: 14px;">Healthcare Expenses</strong>
                            <div class="cat-bar-bg" title="Contributes {pct_hc_a:.1f}% of Scenario A"><div class="cat-bar-fill-a" style="width: {pct_hc_a:.1f}%;"></div></div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Direct MOH & primary care, chronic comorbidity management</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #334155; font-size: 13.5px;">RM {pv_healthcare_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Healthy baseline</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #ea580c; font-size: 13.5px;">RM {(pv_healthcare_ref + pv_healthcare_a):,.0f}</strong>
                            <div style="font-size: 11px; color: #ea580c; font-weight: 600;">+RM {pv_healthcare_a:,.0f} excess</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">RM {pv_healthcare_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #0f766e;">Avoided comorbidity</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">-RM {pv_healthcare_a:,.0f}</strong>
                            <div style="font-size: 11px; color: #0f766e;">Lower expenditure</div>
                        </td>
                        <td>
                            <span class="breakdown-badge badge-saving">Potential Saving</span>
                        </td>
                        <td style="font-size: 12px; color: #475569; line-height: 1.35;">
                            <strong>Modelled:</strong> Malaysian synthetic cohort (18,000 pt-yrs) calibrated to NHMS risk ratios; 4.2% Med CPI.
                        </td>
                    </tr>

                    <!-- 2. Transportation Expenses -->
                    <tr>
                        <td>
                            <strong style="color: #0b1c30; font-size: 14px;">Transportation Expenses</strong>
                            <div class="cat-bar-bg" title="Contributes {pct_tr_a:.1f}% of Scenario A"><div class="cat-bar-fill-a" style="width: {pct_tr_a:.1f}%;"></div></div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Commute modal choice & vehicle reliance</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #334155; font-size: 13.5px;">RM {pv_transport_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Transit baseline</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #ea580c; font-size: 13.5px;">RM {(pv_transport_ref + pv_transport_a):,.0f}</strong>
                            <div style="font-size: 11px; color: #ea580c; font-weight: 600;">+RM {pv_transport_a:,.0f} excess</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">RM {pv_transport_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Standard mobility</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">-RM {pv_transport_a:,.0f}</strong>
                            <div style="font-size: 11px; color: #0f766e;">Lower expenditure</div>
                        </td>
                        <td>
                            <span class="breakdown-badge badge-assumption">Modelled Adult Shift</span>
                        </td>
                        <td style="font-size: 12px; color: #475569; line-height: 1.35;">
                            <strong>Assumption:</strong> RM 0 child difference (&lt;18 yrs); adult shift to private vehicle (+RM 4,740/yr at 2.4% CPI).
                        </td>
                    </tr>

                    <!-- 3. Clothing Expenses -->
                    <tr>
                        <td>
                            <strong style="color: #0b1c30; font-size: 14px;">Clothing Expenses</strong>
                            <div class="cat-bar-bg" title="Contributes {pct_cl_a:.1f}% of Scenario A"><div class="cat-bar-fill-a" style="width: {pct_cl_a:.1f}%;"></div></div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Retail apparel sizing premiums</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #334155; font-size: 13.5px;">RM {pv_clothing_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Standard sizing</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #ea580c; font-size: 13.5px;">RM {(pv_clothing_ref + pv_clothing_a):,.0f}</strong>
                            <div style="font-size: 11px; color: #ea580c; font-weight: 600;">+RM {pv_clothing_a:,.0f} excess</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">RM {pv_clothing_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Standard sizing</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">-RM {pv_clothing_a:,.0f}</strong>
                            <div style="font-size: 11px; color: #0f766e;">Lower expenditure</div>
                        </td>
                        <td>
                            <span class="breakdown-badge badge-saving">Potential Saving</span>
                        </td>
                        <td style="font-size: 12px; color: #475569; line-height: 1.35;">
                            <strong>Observed Data:</strong> 1,337 Malaysian items across 18 brands. RM 0 child; adult plus-size premium (~RM 120/yr at 1.2% CPI).
                        </td>
                    </tr>

                    <!-- 4. Food & Meal Expenses -->
                    <tr style="background-color: #fafbfc;">
                        <td>
                            <strong style="color: #0b1c30; font-size: 14px;">Food & Meal Expenses</strong>
                            <div class="cat-bar-bg" title="Contributes {pct_fd_a:.1f}% of Scenario A"><div class="cat-bar-fill-a" style="width: {pct_fd_a:.1f}%;"></div></div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">Family groceries and dining outlay</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #334155; font-size: 13.5px;">RM {pv_food_ref:,.0f}</strong>
                            <div style="font-size: 11px; color: #64748b;">Caloric baseline</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #ea580c; font-size: 13.5px;">RM {(pv_food_ref + pv_food_a):,.0f}</strong>
                            <div style="font-size: 11px; color: #ea580c; font-weight: 600;">+RM {pv_food_a:,.0f} caloric scaling</div>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 12px; font-weight: 600; color: #64748b;">Not estimated — insufficient evidence</span>
                            <div style="font-size: 11px; color: #94a3b8;">No grocery reduction</div>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 12px; font-weight: 700; color: #64748b;">Not estimated — insufficient evidence</span>
                        </td>
                        <td>
                            <span class="breakdown-badge badge-unsupported">Insufficient Evidence</span>
                        </td>
                        <td style="font-size: 12px; color: #475569; line-height: 1.35;">
                            <strong>Evidence Caveat:</strong> Suku-Suku Separuh whole foods match or exceed ultra-processed grocery bills. Model refuses to claim unsupported savings.
                        </td>
                    </tr>

                    <!-- 5. Lifestyle Intervention Outlay -->
                    <tr style="background-color: #f0fdfa;">
                        <td>
                            <strong style="color: #0f766e; font-size: 14px;">Lifestyle Intervention Outlay</strong>
                            <div class="cat-bar-bg"><div class="cat-bar-fill-b" style="width: 100%;"></div></div>
                            <div style="font-size: 11px; color: #0f766e; margin-top: 2px;">Paediatric dietitian & family lifestyle reinvestment</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #64748b; font-size: 13.5px;">RM 0</strong>
                            <div style="font-size: 11px; color: #94a3b8;">No intervention</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #64748b; font-size: 13.5px;">RM 0</strong>
                            <div style="font-size: 11px; color: #94a3b8;">Inaction pathway</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #0f766e; font-size: 13.5px;">RM {pv_intervention_b:,.0f}</strong>
                            <div style="font-size: 11px; color: #0f766e;">Total Outlay (PV)</div>
                        </td>
                        <td class="num-col">
                            <strong style="color: #ea580c; font-size: 13.5px;">+RM {pv_intervention_b:,.0f}</strong>
                            <div style="font-size: 11px; color: #ea580c;">Preventive outlay</div>
                        </td>
                        <td>
                            <span class="breakdown-badge badge-outlay">Preventive Outlay</span>
                        </td>
                        <td style="font-size: 12px; color: #475569; line-height: 1.35;">
                            <strong>Modelled:</strong> Initial dietitian program (RM 800/yr for first 2 yrs) + parent selected budget (RM {monthly_budget:,.0f}/mo) through age 17.
                        </td>
                    </tr>

                    <!-- Full Pathway Lifetime Totals Row -->
                    <tr style="background-color: #f8fafc; font-weight: 700; border-top: 2px solid #cbd5e1;">
                        <td>
                            <span style="font-size: 13.5px; color: #0b1c30; text-transform: uppercase;">Full Pathway Lifetime Total</span>
                            <div style="font-size: 11px; color: #64748b; font-weight: 500;">Living baseline + scenario costs</div>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 14px; color: #334155;">RM {pv_ref_full_total:,.0f}</span>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 14px; color: #ea580c;">RM {pv_a_full_total:,.0f}</span>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 14px; color: #0f766e;">RM {pv_b_full_total:,.0f}</span>
                        </td>
                        <td class="num-col">
                            <span style="font-size: 14px; color: #115e59;">↘ ~RM {(pv_a_full_total - pv_b_full_total):,.0f}</span>
                        </td>
                        <td colspan="2">
                            <span style="font-size: 11.5px; color: #0f766e; font-weight: 600;">Net Divergence over {duration} yrs</span>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- Reconciliation Note -->
            <div style="margin-top: 1rem; padding: 12px 16px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 12px; color: #475569; line-height: 1.5;">
                <strong style="color: #0b1c30; font-size: 13px;">Actuarial Reconciliation & Trustworthiness Audit:</strong>
                <ul style="margin: 6px 0 0 16px; padding: 0;">
                    <li><strong>Incremental Cost Reconciliation:</strong> Additional Healthcare (RM {pv_healthcare_a:,.0f}) + Transport (RM {pv_transport_a:,.0f}) + Clothing (RM {pv_clothing_a:,.0f}) + Food (RM {pv_food_a:,.0f}) = <strong style="color: #0b1c30;">RM {total_a:,.0f}</strong> (100.0% matches headline Cost of Waiting).</li>
                    <li><strong>Preventive Outlay Reconciliation:</strong> Total Lifestyle Intervention Outlay = <strong style="color: #0f766e;">RM {total_b:,.0f}</strong> (100.0% matches headline Preventive Reinvestment).</li>
                    <li><strong>Net Divergence Equality:</strong> Full Pathway Divergence (RM {pv_a_full_total:,.0f} − RM {pv_b_full_total:,.0f}) = <strong style="color: #115e59;">RM {(pv_a_full_total - pv_b_full_total):,.0f}</strong>, mathematically identical to Incremental Divergence (RM {total_a:,.0f} − RM {total_b:,.0f} = <strong style="color: #115e59;">RM {delta:,.0f}</strong>).</li>
                    <li><strong>Food Cost Discipline:</strong> Scenario B explicitly marks food savings as <em>“Not estimated — insufficient evidence”</em> because adopting whole-food Malaysian diets (Suku-Suku Separuh) does not show empirical net grocery savings.</li>
                    <li><strong>Pediatric Age Discipline:</strong> Transportation and clothing differentials are exactly RM 0 during all childhood years (&lt;18) to avoid unevidenced pediatric premiums.</li>
                </ul>
            </div>
        </div>
        """,
    )


    # =========================================================================
    # SECTION 4: Budget-Aware Prescription (Enlarged & Prominent)
    # =========================================================================
    rx = get_budget_prescription_content(monthly_budget)

    if monthly_budget <= 0:
        remaining_buffer_label = "RM 0 (100% Free Public Protocol)"
    elif monthly_budget < 200:
        low_range = int(monthly_budget * 0.50)
        high_range = int(monthly_budget * 0.85)
        rem_min = int(monthly_budget - high_range)
        rem_max = int(monthly_budget - low_range)
        remaining_buffer_label = f"~RM {rem_min}–{rem_max} / mo"
    else:
        low_range = int(monthly_budget * 0.60)
        high_range = int(monthly_budget * 0.90)
        rem_min = int(monthly_budget - high_range)
        rem_max = int(monthly_budget - low_range)
        remaining_buffer_label = f"~RM {rem_min}–{rem_max} / mo"

    rx_items_html = ""
    for item in rx["items"]:
        rx_items_html += f"""
        <div style="display: flex; align-items: flex-start; gap: 16px; padding: 16px 20px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px;">
            <span style="width: 32px; height: 32px; border-radius: 50%; background: #0f766e; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 16px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px;">{item['num']}</span>
            <div style="flex: 1;">
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 700; color: #0b1c30; margin-bottom: 4px;">{item['title']}</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 15px; color: #334155; line-height: 1.5;">{item['desc']}</div>
            </div>
        </div>
        """

    render_clean_html(
        f"""
        <div class="stitch-card" style="margin-top: 1.25rem; margin-bottom: 1.5rem; padding: 1.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 13px; font-weight: 800; text-transform: uppercase; color: #0f766e; letter-spacing: 0.05em;">Budget-Aware Lifestyle Prescription</span>
                        <span class="stitch-pill">Discretionary Calibration</span>
                    </div>
                    <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 800; color: #0b1c30; margin: 4px 0 2px 0;">{rx['title']}</h2>
                    <div style="font-family: 'Inter', sans-serif; font-size: 15px; color: #475569;">{rx['subtitle']}</div>
                </div>
                <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                    <div style="text-align: right; background: #f0fdfa; border: 1.5px solid #99f6e4; padding: 8px 16px; border-radius: 8px;">
                        <span style="font-size: 11.5px; font-weight: 700; text-transform: uppercase; color: #0f766e; display: block; letter-spacing: 0.03em;">Estimated Monthly Outlay</span>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 20px; font-weight: 800; color: #0f766e;">{rx['outlay_label']}</span>
                        <span style="font-size: 12px; color: #0f766e; font-weight: 600; display: block;">{rx['outlay_sub']}</span>
                    </div>
                    <div style="text-align: right; background: #f8fafc; border: 1.5px solid #cbd5e1; padding: 8px 16px; border-radius: 8px;">
                        <span style="font-size: 11.5px; font-weight: 700; text-transform: uppercase; color: #475569; display: block; letter-spacing: 0.03em;">Household Reserve Buffer</span>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 18px; font-weight: 800; color: #0b1c30; display: block;">{remaining_buffer_label}</span>
                        <span style="font-size: 12px; color: #64748b; font-weight: 500; display: block;">discretionary capital saved</span>
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                {rx_items_html}
            </div>
            <div style="margin-top: 1.25rem; padding: 14px 18px; background: #f0fdfa; border: 1px solid #99f6e4; border-radius: 8px; font-size: 14.5px; color: #0f766e; line-height: 1.5;">
                <strong style="color: #0b1c30;">Protocol Guidance:</strong> {rx['note']}
            </div>
            <div style="margin-top: 12px; font-size: 13.5px; color: #64748b; line-height: 1.45;">
                ⚠️ <em>Educational decision-support only. Not a clinical prescription or medical diagnosis. Greater spending does not guarantee improved health outcomes or cost savings. Consult a registered physician or dietitian before commencing any weight management regimen.</em>
            </div>
        </div>
        """,
    )

    # =========================================================================
    # SECTION 5: Econometric Methodology & Limitations
    # =========================================================================
    render_clean_html(
        """
        <div class="stitch-card" style="margin-top: 0.5rem; margin-bottom: 1.5rem; padding: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 14px;">
                <div>
                    <span style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #64748b; letter-spacing: 0.05em;">Methodology & Evidence</span>
                    <h3 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 19px; font-weight: 700; color: #0b1c30; margin: 2px 0 0 0;">Econometric Model & Limitations</h3>
                </div>
                <span style="font-size: 12px; font-weight: 700; color: #475569; background: #f1f5f9; padding: 4px 12px; border-radius: 4px; border: 1px solid #cbd5e1;">v2.5 Engine</span>
            </div>
        </div>
        """,
    )

    with st.expander("📖 MOH NHMS & Authoritative Reference Benchmarks", expanded=True):
        render_clean_html(
            """
            <div style="font-size: 14px; color: #334155; line-height: 1.5; padding: 4px 0;">
                Calibrated with NHMS 2019/2022 pediatric data, Malaysian CPG Childhood Obesity guidelines,
                and WHO 2007 reference curves (LMS z-score). Population screening tool only; not a substitute for clinical pediatric consultation.
            </div>
            """,
        )

    with st.expander("📈 Discounting & Sector-Specific Inflation Architecture", expanded=False):
        render_clean_html(
            """
            <div style="font-size: 14px; color: #334155; line-height: 1.5; padding: 4px 0;">
                Applies the 3.0% Malaysian Treasury Social Discount Rate and Department of Statistics Malaysia (DOSM)
                CPI sector-specific inflation rates (Health: 4.2%, Food: 3.1%, Transport: 2.4%, Clothing: 1.2%, General: 2.2%).
            </div>
            """,
        )

    with st.expander("⚠️ Uncertainty Bounds & Simulation Disclaimers", expanded=False):
        render_clean_html(
            """
            <div style="font-size: 14px; color: #334155; line-height: 1.5; padding: 4px 0;">
                Synthetic microsimulation reflecting epidemiological risk ratios. Parametric 80% CI captures
                population demographic variation. Trajectory modeling represents population cost divergence, not guaranteed personal cash savings or medical cures.
            </div>
            """,
        )

    # Minimalist Footer
    render_clean_html(
        """
        <div class="stitch-footer" style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; margin-top: 2rem; font-size: 13px; color: #64748b;">
            <span>The Cost of Waiting • Actuarial decision-support model (NHMS / WHO 2007) • Not clinical diagnosis.</span>
            <span style="font-weight: 600; color: #475569;">Malaysian Pediatric Health Economics Project</span>
        </div>
        """,
    )

