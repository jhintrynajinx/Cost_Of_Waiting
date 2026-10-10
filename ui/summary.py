"""
ui/summary.py
Results summary layout for the Cost of Waiting application.

Renders the calculator output as a readable Streamlit section:
- Key metrics (total cost, most expensive category)
- Cost breakdown table
- Charts (imported from ui/charts.py)
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from ui.charts import bar_chart_cost_breakdown, waterfall_chart_cost_categories


def render_summary(results: dict[str, float] | None = None) -> None:
    """Render the results summary section.

    Parameters
    ----------
    results : dict[str, float] or None
        Keys are cost category names; values are total lifetime costs in MYR.
        Pass None (or omit) to render a placeholder while the calculator
        is under development.

    Example input
    -------------
    results = {
        "Food": 15000.0,
        "Clothing": 3200.0,
        "Transportation": 8400.0,
        "Healthcare": 42000.0,
        "Inflation adjustment": 9100.0,
    }
    """
    st.markdown("## Results")

    if results is None:
        st.info(
            "Results will appear here once the calculator is complete. "
            "Enter your details above and click **Calculate**.",
            icon="📊",
        )
        return

    total = sum(results.values())
    top_category = max(results, key=results.get)  # type: ignore[arg-type]

    # --- Key metrics ---
    col1, col2 = st.columns(2)
    col1.metric("Total additional lifetime cost", f"MYR {total:,.0f}")
    col2.metric("Largest cost driver", top_category)

    st.divider()

    # --- Breakdown table ---
    st.markdown("### Cost breakdown")
    df = pd.DataFrame(
        {"Category": list(results.keys()), "Total cost (MYR)": list(results.values())}
    )
    df["Share (%)"] = (df["Total cost (MYR)"] / total * 100).round(1)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # --- Charts ---
    st.markdown("### Visualisation")

    categories = list(results.keys())
    values = list(results.values())

    col_bar, col_waterfall = st.columns(2)

    with col_bar:
        fig_bar = bar_chart_cost_breakdown(categories, values)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_waterfall:
        fig_wf = waterfall_chart_cost_categories(categories, values)
        st.plotly_chart(fig_wf, use_container_width=True)
