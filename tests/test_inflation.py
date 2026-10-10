"""
tests/test_inflation.py
Unit tests for calculator/inflation.py.

Run with:
    python -m pytest tests/test_inflation.py -v
"""

import pytest
from calculator.inflation import apply_compound_inflation, project_costs_over_years


# ---------------------------------------------------------------------------
# apply_compound_inflation
# ---------------------------------------------------------------------------

class TestApplyCompoundInflation:
    def test_zero_years_returns_present_value(self):
        """No time elapsed → value unchanged."""
        assert apply_compound_inflation(1000.0, 0.03, 0) == 1000.0

    def test_known_value_10_years_3_percent(self):
        """1000 MYR at 3% for 10 years → 1343.92 MYR."""
        result = apply_compound_inflation(1000.0, 0.03, 10)
        assert result == pytest.approx(1343.92, abs=0.01)

    def test_zero_rate_returns_present_value(self):
        """Zero inflation → value is unchanged regardless of years."""
        assert apply_compound_inflation(500.0, 0.0, 20) == 500.0

    def test_rounding_to_two_decimal_places(self):
        result = apply_compound_inflation(999.99, 0.025, 5)
        assert result == round(result, 2)

    def test_negative_years_raises(self):
        with pytest.raises(ValueError, match="years"):
            apply_compound_inflation(1000.0, 0.03, -1)

    def test_rate_below_minus_one_raises(self):
        with pytest.raises(ValueError, match="annual_rate"):
            apply_compound_inflation(1000.0, -1.5, 5)

    def test_high_inflation_increases_value(self):
        result = apply_compound_inflation(1000.0, 0.10, 5)
        assert result > 1000.0


# ---------------------------------------------------------------------------
# project_costs_over_years
# ---------------------------------------------------------------------------

class TestProjectCostsOverYears:
    def test_correct_number_of_rows(self):
        rows = project_costs_over_years(1000.0, 0.03, 2025, 2030)
        assert len(rows) == 6  # 2025, 2026, 2027, 2028, 2029, 2030

    def test_years_are_sequential(self):
        rows = project_costs_over_years(1000.0, 0.03, 2025, 2027)
        years = [r["year"] for r in rows]
        assert years == [2025, 2026, 2027]

    def test_first_year_equals_present_value(self):
        """Year 0 offset should equal the present value."""
        rows = project_costs_over_years(1000.0, 0.03, 2025, 2027)
        assert rows[0]["cost_myr"] == pytest.approx(1000.0, abs=0.01)

    def test_costs_increase_with_positive_rate(self):
        rows = project_costs_over_years(1000.0, 0.03, 2025, 2030)
        costs = [r["cost_myr"] for r in rows]
        assert costs == sorted(costs)

    def test_single_year_range(self):
        rows = project_costs_over_years(500.0, 0.05, 2025, 2025)
        assert len(rows) == 1
        assert rows[0]["year"] == 2025
        assert rows[0]["cost_myr"] == pytest.approx(500.0, abs=0.01)

    def test_end_year_before_start_raises(self):
        with pytest.raises(ValueError):
            project_costs_over_years(1000.0, 0.03, 2030, 2025)
