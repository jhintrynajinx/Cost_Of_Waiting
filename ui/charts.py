"""
ui/charts.py
Plotly chart builders for the Cost of Waiting application.

Each function accepts a pandas DataFrame or plain Python data structures
and returns a Plotly Figure object. Call st.plotly_chart(fig) in app.py
or summary.py to render them.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def line_chart_cumulative_cost(
    df: pd.DataFrame,
    x_col: str = "age",
    y_col: str = "cumulative_cost_myr",
    title: str = "Cumulative additional cost over lifetime (MYR)",
) -> go.Figure:
    """Line chart of cumulative obesity-related cost vs. age.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns matching *x_col* and *y_col*.
    x_col : str
        Column to use as the x-axis (default: 'age').
    y_col : str
        Column to use as the y-axis (default: 'cumulative_cost_myr').
    title : str
        Chart title.

    Returns
    -------
    plotly.graph_objects.Figure

    Note
    ----
    TODO: wire to real projection data once the calculation engine is complete.
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: "Age (years)", y_col: "MYR"},
        markers=True,
    )
    fig.update_layout(hovermode="x unified")
    return fig


def bar_chart_cost_breakdown(
    categories: list[str],
    values: list[float],
    title: str = "Additional lifetime cost by category (MYR)",
) -> go.Figure:
    """Horizontal bar chart showing cost contribution per category.

    Parameters
    ----------
    categories : list[str]
        Cost category labels (e.g. ['Food', 'Clothing', ...]).
    values : list[float]
        Corresponding total costs in MYR.
    title : str
        Chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    fig = go.Figure(
        go.Bar(
            x=values,
            y=categories,
            orientation="h",
            marker_color="#E74C3C",
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="MYR",
        yaxis_title="Category",
        hovermode="y unified",
    )
    return fig


def waterfall_chart_cost_categories(
    categories: list[str],
    values: list[float],
    title: str = "Cost breakdown — waterfall (MYR)",
) -> go.Figure:
    """Waterfall chart showing cumulative cost build-up across categories.

    Parameters
    ----------
    categories : list[str]
        Cost category labels.
    values : list[float]
        Cost contribution per category in MYR.
    title : str
        Chart title.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    measures = ["relative"] * len(categories) + ["total"]
    x_labels = categories + ["Total"]
    y_values = values + [sum(values)]

    fig = go.Figure(
        go.Waterfall(
            measure=measures,
            x=x_labels,
            y=y_values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )
    fig.update_layout(title=title, showlegend=False)
    return fig
