"""
tests/test_healthcare.py
Unit tests for calculator/healthcare.py.
"""

import pytest
from calculator.healthcare import (
    estimate_annual_healthcare_cost_difference,
    get_healthcare_cost_breakdown,
    HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP,
)


class TestHealthcareCostCalculation:
    def test_non_obese_has_zero_difference(self):
        assert estimate_annual_healthcare_cost_difference("Normal weight", 10) == 0.0
        assert estimate_annual_healthcare_cost_difference("Underweight", 45) == 0.0

    def test_child_bracket_cost(self):
        cost = estimate_annual_healthcare_cost_difference("Obese", 10)
        assert cost == HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP["child"]

    def test_adolescent_bracket_cost(self):
        cost = estimate_annual_healthcare_cost_difference("Obese", 15)
        assert cost == HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP["adolescent"]

    def test_adult_early_bracket_cost(self):
        cost = estimate_annual_healthcare_cost_difference("Obese", 25)
        assert cost == HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP["adult_early"]

    def test_adult_mid_bracket_cost(self):
        cost = estimate_annual_healthcare_cost_difference("Obese", 50)
        assert cost == HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP["adult_mid"]

    def test_older_adult_bracket_cost(self):
        cost = estimate_annual_healthcare_cost_difference("Obese", 70)
        assert cost == HEALTHCARE_DIFFERENTIAL_BY_AGE_GROUP["older_adult"]

    def test_breakdown_contains_synthetic_cohort_flag(self):
        res = get_healthcare_cost_breakdown("Obese", 10)
        assert res["is_synthetic_cohort"] is True
        assert "evidence_note" in res
