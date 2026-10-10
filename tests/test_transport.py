"""
tests/test_transport.py
Unit tests for calculator/transport.py.
"""

import pytest
from calculator.transport import (
    estimate_annual_transport_cost_difference,
    get_transport_cost_breakdown,
    ADULT_ANNUAL_TRANSPORT_DIFFERENCE_MYR,
)


class TestTransportCostCalculation:
    def test_child_under_18_has_zero_difference(self):
        """Child transport cost is identical across weight categories in reference dataset."""
        cost = estimate_annual_transport_cost_difference("Obese", 12)
        assert cost == 0.0

    def test_non_obese_adult_has_zero_difference(self):
        cost = estimate_annual_transport_cost_difference("Normal weight", 30)
        assert cost == 0.0

    def test_obese_adult_has_documented_difference(self):
        cost = estimate_annual_transport_cost_difference("Obese", 30)
        assert cost == ADULT_ANNUAL_TRANSPORT_DIFFERENCE_MYR

    def test_transport_breakdown_notes(self):
        child_res = get_transport_cost_breakdown("Obese", 8)
        assert child_res["is_child"] is True
        assert child_res["annual_difference_myr"] == 0.0
        assert "RM 0.00" in child_res["assumption_note"]

        adult_res = get_transport_cost_breakdown("Obese", 30)
        assert adult_res["is_child"] is False
        assert adult_res["annual_difference_myr"] == ADULT_ANNUAL_TRANSPORT_DIFFERENCE_MYR
