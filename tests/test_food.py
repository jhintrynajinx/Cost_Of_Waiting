"""
tests/test_food.py
Unit tests for calculator/food.py.

Run with:
    python -m pytest tests/test_food.py -v
"""

import pytest
from calculator.food import (
    estimate_annual_food_cost_difference,
    get_food_spending_breakdown,
)


class TestEstimateAnnualFoodCostDifference:
    def test_normal_weight_returns_zero(self):
        """A healthy-weight individual should have zero additional food cost."""
        result = estimate_annual_food_cost_difference(
            weight_status="Normal weight",
            age_years=10,
            sex="male",
        )
        assert result == 0.0

    def test_obese_child_has_positive_cost(self):
        """An obese child should have a positive annual food cost differential."""
        result = estimate_annual_food_cost_difference(
            weight_status="Obese",
            age_years=10,
            sex="male",
        )
        assert result > 0.0
        # Male age 10 diff: 5742.00 - 4313.00 = 1429.00
        assert result == pytest.approx(1429.0, abs=0.1)

    def test_cost_is_non_negative(self):
        """The food cost difference should never be negative."""
        result = estimate_annual_food_cost_difference(
            weight_status="Obese",
            age_years=14,
            sex="female",
        )
        assert result >= 0.0

    def test_overweight_returns_zero_in_current_model(self):
        """Overweight individuals do not incur the obese caloric surplus tier in this model."""
        result = estimate_annual_food_cost_difference(
            weight_status="Overweight",
            age_years=10,
            sex="male",
        )
        assert result == 0.0

    def test_breakdown_contains_assumptions(self):
        breakdown = get_food_spending_breakdown(
            weight_status="Obese",
            age_years=10,
            sex="male",
        )
        assert breakdown["is_modelled"] is True
        assert "assumption_note" in breakdown
        assert breakdown["annual_difference_myr"] > 0
