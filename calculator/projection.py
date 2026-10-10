"""
calculator/projection.py
Lifetime projection model comparing Scenario A (Cost of Waiting) vs Scenario B (Cost of Acting Early).

Model Design Principles:
1. Identical Horizons: Both scenarios are projected over the exact same period,
   from the child's current age to a user-selected end age (capped at 80).
2. Category-Specific Inflation: Uses DOSM sector inflation rates (Food 3.1%,
   Clothing 1.2%, Transport 2.4%, Healthcare 4.2%, General 2.2%) to project nominal ringgit.
3. Realistic Positive Trajectories:
   - Scenario B (Cost of Acting Early): Models the healthy reference pathway, including
     normal living expenses (food, healthcare, transport, clothing) compounded by sector
     inflation, plus childhood early intervention expenses. Cumulative expenditure rises
     smoothly as positive living costs accumulate over time.
   - Scenario A (Cost of Waiting): Child remains on an obese trajectory. Incurs baseline
     living costs plus additional obesity-attributable costs across food, healthcare,
     transport (adulthood modal shift), and clothing (adulthood retail premium).
4. Causal & Uncertainty Disclosure: Output clearly flags that differences represent
   modelled trajectory comparisons, not clinical guarantees.
"""

from __future__ import annotations

from typing import Any
import pandas as pd
from calculator.data_loader import load_cleaned_meal_spending, load_transport_costs
from calculator.food import estimate_annual_food_cost_difference
from calculator.clothing import estimate_annual_clothing_cost_difference
from calculator.transport import estimate_annual_transport_cost_difference
from calculator.healthcare import (
    estimate_annual_healthcare_cost_difference,
    get_healthcare_age_bracket,
)
from calculator.inflation import compound_sector_cost

# Normal-weight reference healthcare direct costs by age bracket (from Malaysian synthetic cohort)
HEALTHCARE_REFERENCE_BY_BRACKET: dict[str, float] = {
    "child": 1853.48,       # ages 5-12
    "adolescent": 1703.70,  # ages 13-17
    "adult_early": 1839.26, # ages 18-39
    "adult_mid": 2215.69,   # ages 40-59
    "older_adult": 3636.60, # ages 60+
}


def project_lifetime_costs(
    current_age: int,
    sex: str,
    weight_status: str,
    end_age: int = 80,
    optional_monthly_budget_myr: float = 0.0,
    adjust_inflation: bool = True,
    inflation_scenario: str = "central",
) -> dict[str, Any]:
    """Calculate year-by-year projections for Scenario A and Scenario B.

    Parameters
    ----------
    current_age : int
        Current age of the child in years (must be >= 5 and < end_age).
    sex : str
        'male' or 'female'.
    weight_status : str
        'Obese', 'Overweight', or 'Normal weight'.
    end_age : int
        Target projection age (must be > current_age and <= 80).
    optional_monthly_budget_myr : float
        Parent's optional monthly lifestyle/intervention budget in MYR.
    adjust_inflation : bool
        Whether to adjust for category-specific Malaysian inflation.
    inflation_scenario : str
        'central', 'low', or 'high'.

    Returns
    -------
    dict[str, Any]
        Structured results dictionary containing year-by-year series, totals,
        category breakdowns, and evidence notes.
    """
    if current_age < 5:
        raise ValueError(f"current_age must be at least 5 years; got {current_age}")
    if end_age > 80:
        raise ValueError(f"end_age cannot exceed 80; got {end_age}")
    if end_age <= current_age:
        raise ValueError(
            f"end_age ({end_age}) must be strictly greater than current_age ({current_age})"
        )
    if optional_monthly_budget_myr < 0:
        raise ValueError(
            f"optional_monthly_budget_myr must be non-negative; got {optional_monthly_budget_myr}"
        )

    is_obese = str(weight_status).strip().lower() in {"obese", "obesity"}

    # Load reference datasets for baseline normal-weight spending
    meal_df = load_cleaned_meal_spending()
    norm_sex = "Male" if sex.strip().lower() in {"male", "boy", "boys", "m"} else "Female"

    yearly_data: list[dict[str, Any]] = []

    # Cumulative sums for additional (excess) costs
    cum_scenario_a_excess = 0.0
    cum_scenario_b_intervention = 0.0

    cum_food_excess = 0.0
    cum_clothing_excess = 0.0
    cum_transport_excess = 0.0
    cum_healthcare_excess = 0.0

    # Cumulative sums for full living pathway costs
    cum_scenario_a_full = 0.0
    cum_scenario_b_full = 0.0
    cum_reference_full = 0.0

    cum_food_ref = 0.0
    cum_clothing_ref = 0.0
    cum_transport_ref = 0.0
    cum_healthcare_ref = 0.0

    total_intervention_cost = 0.0

    start_calendar_year = 2026

    for offset, age in enumerate(range(current_age, end_age + 1)):
        calendar_year = start_calendar_year + offset

        # -------------------------------------------------------------------
        # 1. Reference Person Baseline Living Costs (Normal-Weight Malaysian)
        # -------------------------------------------------------------------
        lookup_age = min(max(int(age), 1), 20)
        meal_match = meal_df[(meal_df["sex"] == norm_sex) & (meal_df["age_years"] == lookup_age)]
        food_ref_nominal = float(meal_match.iloc[0]["normal_annual_spending_myr"]) if not meal_match.empty else 4313.0

        h_bracket = get_healthcare_age_bracket(age)
        health_ref_nominal = HEALTHCARE_REFERENCE_BY_BRACKET.get(h_bracket, 1853.48)

        transport_ref_nominal = 600.0 if age < 18 else 4920.0
        clothing_ref_nominal = 450.0 if age < 18 else 1200.0

        # -------------------------------------------------------------------
        # 2. Additional (Excess) Costs Attributable to Obesity
        # -------------------------------------------------------------------
        food_excess_nominal = estimate_annual_food_cost_difference(weight_status, age, sex)
        clothing_excess_nominal = estimate_annual_clothing_cost_difference(weight_status, age, sex)
        transport_excess_nominal = estimate_annual_transport_cost_difference(weight_status, age)
        healthcare_excess_nominal = estimate_annual_healthcare_cost_difference(weight_status, age, sex)

        # -------------------------------------------------------------------
        # 3. Compound with Category-Specific Sector Inflation
        # -------------------------------------------------------------------
        if adjust_inflation:
            food_ref_cost = compound_sector_cost(food_ref_nominal, "food", offset, inflation_scenario)
            food_excess_cost = compound_sector_cost(food_excess_nominal, "food", offset, inflation_scenario)

            health_ref_cost = compound_sector_cost(health_ref_nominal, "healthcare", offset, inflation_scenario)
            health_excess_cost = compound_sector_cost(healthcare_excess_nominal, "healthcare", offset, inflation_scenario)

            transport_ref_cost = compound_sector_cost(transport_ref_nominal, "transport", offset, inflation_scenario)
            transport_excess_cost = compound_sector_cost(transport_excess_nominal, "transport", offset, inflation_scenario)

            clothing_ref_cost = compound_sector_cost(clothing_ref_nominal, "clothing", offset, inflation_scenario)
            clothing_excess_cost = compound_sector_cost(clothing_excess_nominal, "clothing", offset, inflation_scenario)
        else:
            food_ref_cost = food_ref_nominal
            food_excess_cost = food_excess_nominal

            health_ref_cost = health_ref_nominal
            health_excess_cost = healthcare_excess_nominal

            transport_ref_cost = transport_ref_nominal
            transport_excess_cost = transport_excess_nominal

            clothing_ref_cost = clothing_ref_nominal
            clothing_excess_cost = clothing_excess_nominal

        reference_annual_this_year = (
            food_ref_cost + health_ref_cost + transport_ref_cost + clothing_ref_cost
        )
        total_a_excess_this_year = (
            food_excess_cost + clothing_excess_cost + transport_excess_cost + health_excess_cost
        )

        # -------------------------------------------------------------------
        # 4. Scenario B: Early Action & Intervention Outlay
        # -------------------------------------------------------------------
        intervention_nominal = 0.0
        if is_obese and offset < 2:
            intervention_nominal += 800.0  # Paediatric dietitian + clinical lifestyle protocol

        if age <= 17 and optional_monthly_budget_myr > 0:
            intervention_nominal += optional_monthly_budget_myr * 12.0

        if adjust_inflation and intervention_nominal > 0:
            intervention_cost = compound_sector_cost(
                intervention_nominal, "general", offset, inflation_scenario
            )
        else:
            intervention_cost = intervention_nominal

        # Total full pathway expenditures:
        scenario_b_annual_this_year = reference_annual_this_year + intervention_cost
        scenario_a_annual_this_year = reference_annual_this_year + total_a_excess_this_year

        # Update cumulative trackers
        cum_food_excess += food_excess_cost
        cum_clothing_excess += clothing_excess_cost
        cum_transport_excess += transport_excess_cost
        cum_healthcare_excess += health_excess_cost

        cum_food_ref += food_ref_cost
        cum_clothing_ref += clothing_ref_cost
        cum_transport_ref += transport_ref_cost
        cum_healthcare_ref += health_ref_cost

        cum_scenario_a_excess += total_a_excess_this_year
        cum_scenario_b_intervention += intervention_cost
        total_intervention_cost += intervention_cost

        cum_reference_full += reference_annual_this_year
        cum_scenario_a_full += scenario_a_annual_this_year
        cum_scenario_b_full += scenario_b_annual_this_year

        yearly_data.append({
            "age": age,
            "calendar_year": calendar_year,
            "offset_years": offset,
            # Additional / Incremental obesity & intervention costs (satisfies existing test suites):
            "scenario_a_annual_myr": round(total_a_excess_this_year, 2),
            "scenario_b_annual_myr": round(intervention_cost, 2),
            "scenario_a_cumulative_myr": round(cum_scenario_a_excess, 2),
            "scenario_b_cumulative_myr": round(cum_scenario_b_intervention, 2),
            # Full pathway lifetime expenditures (living baseline + scenario costs):
            "scenario_a_full_annual_myr": round(scenario_a_annual_this_year, 2),
            "scenario_b_full_annual_myr": round(scenario_b_annual_this_year, 2),
            "scenario_a_full_cumulative_myr": round(cum_scenario_a_full, 2),
            "scenario_b_full_cumulative_myr": round(cum_scenario_b_full, 2),
            "reference_annual_myr": round(reference_annual_this_year, 2),
            "reference_cumulative_myr": round(cum_reference_full, 2),
            # Category breakdown (additional & reference):
            "food_myr": round(food_excess_cost, 2),
            "food_ref_myr": round(food_ref_cost, 2),
            "clothing_myr": round(clothing_excess_cost, 2),
            "clothing_ref_myr": round(clothing_ref_cost, 2),
            "transport_myr": round(transport_excess_cost, 2),
            "transport_ref_myr": round(transport_ref_cost, 2),
            "healthcare_myr": round(health_excess_cost, 2),
            "healthcare_ref_myr": round(health_ref_cost, 2),
            "intervention_myr": round(intervention_cost, 2),
        })

    net_difference_myr = cum_scenario_a_excess - cum_scenario_b_intervention

    return {
        "summary": {
            "current_age": current_age,
            "end_age": end_age,
            "projection_duration_years": end_age - current_age + 1,
            "weight_status": weight_status,
            "is_obese": is_obese,
            "adjust_inflation": adjust_inflation,
            "inflation_scenario": inflation_scenario,
            # Incremental additional costs (matches test suite expectations):
            "scenario_a_total_myr": round(cum_scenario_a_excess, 2),
            "scenario_b_total_myr": round(total_intervention_cost, 2),
            "net_difference_myr": round(net_difference_myr, 2),
            "total_intervention_cost_myr": round(total_intervention_cost, 2),
            # Full pathway lifetime totals:
            "scenario_a_full_total_myr": round(cum_scenario_a_full, 2),
            "scenario_b_full_total_myr": round(cum_scenario_b_full, 2),
            "reference_full_total_myr": round(cum_reference_full, 2),
        },
        "scenario_a_breakdown": {
            "food_myr": round(cum_food_excess, 2),
            "clothing_myr": round(cum_clothing_excess, 2),
            "transport_myr": round(cum_transport_excess, 2),
            "healthcare_myr": round(cum_healthcare_excess, 2),
        },
        "reference_breakdown": {
            "food_myr": round(cum_food_ref, 2),
            "clothing_myr": round(cum_clothing_ref, 2),
            "transport_myr": round(cum_transport_ref, 2),
            "healthcare_myr": round(cum_healthcare_ref, 2),
        },
        "yearly_projections": yearly_data,
        "evidence_and_uncertainty": {
            "causal_disclaimer": (
                "Estimated difference between two projected pathways. Cross-sectional cost "
                "differences do not guarantee that intervention will yield the exact calculated financial savings."
            ),
            "data_sources": [
                "WHO 2007 Child Growth Reference (Ages 5-19)",
                "Department of Statistics Malaysia (DOSM) Sector Inflation Dataset",
                "Malaysian Obesity Cost Cohort (18,000 modelled patient-years)",
                "Malaysian Retail Clothing Observations (18 retailers)",
                "Malaysian Transport Modal-Shift Cost Dataset",
            ],
        },
    }
