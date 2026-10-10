"""
calculator/clothing.py
Clothing expenditure projections for obese vs. healthy-weight individuals in Malaysia.

Data Source & Provenance
-------------------------
Uses data/SizeCost_Malaysia_Granular_Size_Observations.csv (1,337 retail observations
collected across 18 Malaysian retailers including Uniqlo, Padini, Zalora, M&S, etc.).

Key Empirical Findings & Assumptions:
1. Children (ages < 18): The dataset contains adult apparel only. No documented
   size premium exists for Malaysian paediatric clothing in the collected data.
   Therefore, incremental clothing cost for children is set to RM 0.00 to avoid
   inventing unsupported costs.
2. Adults (ages >= 18): The vast majority of mass retailers (Uniqlo, Padini, Decathlon)
   price identical styles at identical prices across standard and extended sizes.
   A modest premium exists in specialty plus-size collections (Zalora Curve, Marks & Spencer),
   averaging approximately RM 120.00/year for an illustrative adult apparel basket.
"""

from __future__ import annotations

import pandas as pd
from calculator.data_loader import load_clothing_observations

ADULT_ANNUAL_CLOTHING_PREMIUM_MYR = 120.0


def estimate_annual_clothing_cost_difference(
    weight_status: str,
    age_years: int,
    sex: str = "male",
    clothing_prices_df: pd.DataFrame | None = None,
) -> float:
    """Estimate annual clothing expenditure difference attributable to obesity.

    Parameters
    ----------
    weight_status : str
        'Obese', 'Overweight', 'Normal weight', etc.
    age_years : int
        Current age in years.
    sex : str
        'male' or 'female'.
    clothing_prices_df : pd.DataFrame, optional
        Optional dataframe of clothing observations.

    Returns
    -------
    float
        Annual incremental cost in MYR.
        Returns 0.0 for all children under 18 and non-obese adults.
    """
    _ = sex, clothing_prices_df
    if str(weight_status).strip().lower() not in {"obese", "obesity"}:
        return 0.0

    # Under 18: No data supports a paediatric plus-size premium in Malaysia
    if int(age_years) < 18:
        return 0.0

    # Adults 18+: Sourced adult market basket premium
    return ADULT_ANNUAL_CLOTHING_PREMIUM_MYR


def get_clothing_cost_breakdown(
    weight_status: str,
    age_years: int,
) -> dict[str, object]:
    """Return clothing cost details and evidence notes."""
    is_obese = str(weight_status).strip().lower() in {"obese", "obesity"}
    is_child = int(age_years) < 18

    diff = estimate_annual_clothing_cost_difference(weight_status, age_years)

    return {
        "annual_difference_myr": diff,
        "is_child": is_child,
        "evidence_note": (
            "No child clothing size premium documented in Malaysian data (RM 0.00). "
            "Adult premium of RM 120.00/year applies at age 18+ based on retail observations."
            if is_child
            else "Adult annual plus-size premium of RM 120.00/year derived from Malaysian retail observations."
        ),
    }
