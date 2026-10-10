"""
tests/test_clothing.py
Unit tests for calculator/clothing.py.
"""

import pytest
from calculator.clothing import (
    estimate_annual_clothing_cost_difference,
    get_clothing_cost_breakdown,
    ADULT_ANNUAL_CLOTHING_PREMIUM_MYR,
)


class TestClothingCostCalculation:
    def test_child_under_18_has_zero_difference(self):
        """Malaysian data does not document child plus-size premium."""
        cost = estimate_annual_clothing_cost_difference("Obese", 10)
        assert cost == 0.0

    def test_non_obese_adult_has_zero_difference(self):
        cost = estimate_annual_clothing_cost_difference("Normal weight", 25)
        assert cost == 0.0

    def test_obese_adult_has_market_premium(self):
        cost = estimate_annual_clothing_cost_difference("Obese", 25)
        assert cost == ADULT_ANNUAL_CLOTHING_PREMIUM_MYR

    def test_clothing_breakdown_notes(self):
        child_res = get_clothing_cost_breakdown("Obese", 10)
        assert child_res["is_child"] is True
        assert child_res["annual_difference_myr"] == 0.0
        assert "RM 0.00" in child_res["evidence_note"]

        adult_res = get_clothing_cost_breakdown("Obese", 25)
        assert adult_res["is_child"] is False
        assert adult_res["annual_difference_myr"] == ADULT_ANNUAL_CLOTHING_PREMIUM_MYR
