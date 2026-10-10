"""
calculator/
Pure calculation engine for the Cost of Waiting project.

Modules
-------
bmi         BMI calculation and WHO 2007 child growth reference classification.
food        Food expenditure projections based on Malaysian meal benchmarks.
clothing    Clothing expenditure projections based on Malaysian retail observations.
transport   Transportation cost projections based on Malaysian transit benchmarks.
healthcare  Healthcare cost projections based on Malaysian patient-year cohorts.
inflation   Inflation adjustment utilities using DOSM sector CPI series.
projection  Scenario A (Cost of Waiting) vs Scenario B (Cost of Acting Early) engine.
data_loader Central cached loader for project CSV datasets.

All modules in this package are independent of Streamlit and can be
imported and tested without a running web application.
"""

from calculator.bmi import (
    calculate_bmi,
    classify_bmi_adult,
    is_obese_adult,
    calculate_child_bmi_z_score,
    interpret_child_bmi,
    classify_bmi_child,
)
from calculator.food import (
    estimate_annual_food_cost_difference,
    get_food_spending_breakdown,
)
from calculator.clothing import (
    estimate_annual_clothing_cost_difference,
    get_clothing_cost_breakdown,
)
from calculator.transport import (
    estimate_annual_transport_cost_difference,
    get_transport_cost_breakdown,
)
from calculator.healthcare import (
    estimate_annual_healthcare_cost_difference,
    get_healthcare_cost_breakdown,
)
from calculator.inflation import (
    apply_compound_inflation,
    project_costs_over_years,
    get_sector_inflation_rate,
    compound_sector_cost,
)
from calculator.projection import project_lifetime_costs

__all__ = [
    "calculate_bmi",
    "classify_bmi_adult",
    "is_obese_adult",
    "calculate_child_bmi_z_score",
    "interpret_child_bmi",
    "classify_bmi_child",
    "estimate_annual_food_cost_difference",
    "get_food_spending_breakdown",
    "estimate_annual_clothing_cost_difference",
    "get_clothing_cost_breakdown",
    "estimate_annual_transport_cost_difference",
    "get_transport_cost_breakdown",
    "estimate_annual_healthcare_cost_difference",
    "get_healthcare_cost_breakdown",
    "apply_compound_inflation",
    "project_costs_over_years",
    "get_sector_inflation_rate",
    "compound_sector_cost",
    "project_lifetime_costs",
]
