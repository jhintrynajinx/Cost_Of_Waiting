"""
calculator/healthcare.py
Healthcare cost projections for obese vs. healthy-weight individuals in Malaysia.

Data Source & Provenance
-------------------------
Uses data/malaysia_obesity_cost_person_year.csv (18,000 modelled Malaysian patient-years).

Methodological & Evidence Disclosure:
1. Synthetic cohort: The dataset is a synthetic micro-simulation cohort designed to reflect
   Malaysian epidemiologic comorbidity incidence and public/private healthcare utilization.
2. Age-graded differential: Healthcare expenditure differences vary by age bracket:
   - Child (5–12 years): +RM 1,490.68/year
   - Adolescent (13–17 years): +RM 2,164.66/year
   - Adult (18–39 years): +RM 2,599.12/year
   - Adult (40–59 years): +RM 3,337.09/year
   - Older adult (60+ years): +RM 4,333.24/year
3. Causal caveat: Cross-sectional spending differences reflect observed resource utilization
   associated with obesity comorbidities; they do not guarantee clinical savings from any
   single intervention.
"""

from __future__ import annotations

import pandas as pd

HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP: dict[str, float] = {
    "child": 1490.68,       # ages 5-12
    "adolescent": 2164.66,  # ages 13-17
    "adult_early": 2599.12, # ages 18-39
    "adult_mid": 3337.09,   # ages 40-59
    "older_adult": 4333.24, # ages 60+
}


def get_healthcare_age_bracket(age_years: int) -> str:
    """Return the internal age bracket key for a given age in years."""
    age = int(age_years)
    if age <= 12:
        return "child"
    elif age <= 17:
        return "adolescent"
    elif age <= 39:
        return "adult_early"
    elif age <= 59:
        return "adult_mid"
    else:
        return "older_adult"


def estimate_annual_healthcare_cost_difference(
    weight_status: str,
    age_years: int,
    sex: str = "male",
    healthcare_costs_df: pd.DataFrame | None = None,
) -> float:
    """Estimate annual additional healthcare expenditure attributable to obesity.

    Parameters
    ----------
    weight_status : str
        'Obese', 'Overweight', 'Normal weight', etc.
    age_years : int
        Current age in years.
    sex : str
        'male' or 'female'.
    healthcare_costs_df : pd.DataFrame, optional
        Optional healthcare reference dataframe.

    Returns
    -------
    float
        Annual additional healthcare cost in MYR.
        Returns 0.0 for non-obese individuals.
    """
    _ = sex, healthcare_costs_df
    if str(weight_status).strip().lower() not in {"obese", "obesity"}:
        return 0.0

    bracket = get_healthcare_age_bracket(age_years)
    diff = HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP[bracket]
    return round(diff, 2)


def get_healthcare_cost_breakdown(
    weight_status: str,
    age_years: int,
) -> dict[str, object]:
    """Return healthcare cost differential details with disclosure notes."""
    bracket = get_healthcare_age_bracket(age_years)
    is_obese = str(weight_status).strip().lower() in {"obese", "obesity"}
    diff = HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP[bracket] if is_obese else 0.0

    return {
        "age_bracket": bracket,
        "annual_difference_myr": diff,
        "is_synthetic_cohort": True,
        "evidence_note": (
            "Derived from 18,000 modelled Malaysian patient-years (malaysia_obesity_cost_person_year.csv). "
            "Reflects Malaysian public/private comorbidity treatment and monitoring patterns."
        ),
    }
