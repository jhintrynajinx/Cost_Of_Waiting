"""
calculator/transport.py
Transportation cost projections for obese vs. healthy-weight individuals in Malaysia.

Data Source & Provenance
-------------------------
Uses data/malaysia_transport_costs_adult_obese_nonobese_child.csv.

Methodological & Evidence Disclosure:
1. Children (ages < 18): The reference dataset specifies an annual transport cost of
   RM 600.00 for children across all weight categories. There is NO modelled or empirical
   differential between obese and non-obese children. Incremental transport cost is RM 0.00.
2. Adults (ages >= 18): An illustrative adult modal-shift model estimates an annual
   differential of RM 4,740.00 (RM 395.00/month).
   Assumption: Obese adults rely more on private cars and ride-hailing (Grab) rather than
   motorcycles or active walking/transit.
3. This is an illustrative assumption-based scenario, not a national household survey.
"""

from __future__ import annotations

import pandas as pd
from calculator.data_loader import load_transport_costs

ADULT_ANNUAL_TRANSPORT_DIFFERENCE_MYR = 4740.0  # RM 9,660 (obese) - RM 4,920 (non-obese)


def estimate_annual_transport_cost_difference(
    weight_status: str,
    age_years: int,
    transport_costs_df: pd.DataFrame | None = None,
) -> float:
    """Estimate the annual transport expenditure difference attributable to obesity.

    Parameters
    ----------
    weight_status : str
        'Obese', 'Overweight', 'Normal weight', etc.
    age_years : int
        Current age in whole years.
    transport_costs_df : pd.DataFrame, optional
        Optional pre-loaded transport dataframe.

    Returns
    -------
    float
        Annual additional transport cost in MYR.
        Returns 0.0 for all children under 18 and non-obese adults.
    """
    _ = transport_costs_df
    if str(weight_status).strip().lower() not in {"obese", "obesity"}:
        return 0.0

    # Under 18: No differential modelled for children
    if int(age_years) < 18:
        return 0.0

    return ADULT_ANNUAL_TRANSPORT_DIFFERENCE_MYR


def get_transport_cost_breakdown(
    weight_status: str,
    age_years: int,
) -> dict[str, object]:
    """Return transport cost breakdown and methodology notes."""
    is_obese = str(weight_status).strip().lower() in {"obese", "obesity"}
    is_child = int(age_years) < 18

    diff = estimate_annual_transport_cost_difference(weight_status, age_years)

    return {
        "annual_difference_myr": diff,
        "is_child": is_child,
        "assumption_note": (
            "Child transport costs show RM 0.00 differential in Malaysian data. "
            "Adult differential of RM 4,740.00/year applies at driving age (18+) "
            "based on illustrative modal-shift assumptions (private car/Grab vs transit/motorcycle)."
            if is_child
            else "Adult differential of RM 4,740.00/year based on illustrative modal-shift assumptions."
        ),
    }
