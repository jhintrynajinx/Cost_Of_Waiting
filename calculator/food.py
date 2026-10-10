"""
calculator/food.py
Food expenditure projections for obese vs. healthy-weight individuals in Malaysia.

Data Source & Provenance
-------------------------
Uses data/bmi_meal_spending.csv.
The dataset documents baseline meal spending (RM 3,600/yr for ages 1-6 up to
RM 5,760/yr for age 20+) and obese meal spending.

Methodological & Evidence Disclosure:
- Obese meal spending in the reference dataset was derived mathematically by scaling
  baseline meal spending by the ratio of (Obese BMI / Normal BMI).
- This represents an illustrative caloric-scaled spending model, not an empirical
  longitudinal dietary survey.
"""

from __future__ import annotations

import pandas as pd
from calculator.data_loader import load_cleaned_meal_spending


def estimate_annual_food_cost_difference(
    weight_status: str,
    age_years: int,
    sex: str,
    food_prices_df: pd.DataFrame | None = None,
) -> float:
    """Estimate the annual food expenditure difference attributable to obesity.

    Parameters
    ----------
    weight_status : str
        Weight category, e.g. 'Obese', 'Overweight', 'Normal weight'.
        Only 'Obese' incurs the full modelled caloric surplus spending.
    age_years : int
        Current age in whole years.
    sex : str
        'male' or 'female' (case-insensitive).
    food_prices_df : pd.DataFrame, optional
        Pre-loaded meal spending dataframe.

    Returns
    -------
    float
        Annual excess food expenditure in MYR. Returns 0.0 for non-obese individuals.
    """
    if str(weight_status).strip().lower() not in {"obese", "obesity"}:
        return 0.0

    df = food_prices_df if food_prices_df is not None else load_cleaned_meal_spending()

    norm_sex = "Male" if sex.strip().lower() in {"male", "boy", "boys", "m"} else "Female"

    # Dataset has ages 1 to 20 (where 20 represents 20+)
    lookup_age = min(max(int(age_years), 1), 20)

    match = df[(df["sex"] == norm_sex) & (df["age_years"] == lookup_age)]
    if match.empty:
        # Fallback to age 20+ row
        match = df[(df["sex"] == norm_sex) & (df["age_years"] == 20)]

    diff = float(match.iloc[0]["annual_difference_myr"])
    return round(diff, 2)


def get_food_spending_breakdown(
    weight_status: str,
    age_years: int,
    sex: str,
) -> dict[str, object]:
    """Return detailed food spending comparison and evidence notes."""
    df = load_cleaned_meal_spending()
    norm_sex = "Male" if sex.strip().lower() in {"male", "boy", "boys", "m"} else "Female"
    lookup_age = min(max(int(age_years), 1), 20)

    match = df[(df["sex"] == norm_sex) & (df["age_years"] == lookup_age)]
    row = match.iloc[0]

    is_obese = str(weight_status).strip().lower() in {"obese", "obesity"}
    diff = float(row["annual_difference_myr"]) if is_obese else 0.0

    return {
        "normal_annual_spending_myr": float(row["normal_annual_spending_myr"]),
        "obese_annual_spending_myr": float(row["obese_annual_spending_myr"]),
        "annual_difference_myr": diff,
        "is_modelled": True,
        "assumption_note": (
            "Modelled estimate: obese meal spending scales with WHO BMI ratio benchmarks "
            "applied to Malaysian baseline food spending."
        ),
    }
