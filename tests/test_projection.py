"""
tests/test_projection.py
Unit tests for calculator/projection.py (Scenario A vs Scenario B comparison).
"""

import pytest
from calculator.projection import project_lifetime_costs


class TestProjectLifetimeCosts:
    def test_current_age_under_five_raises(self):
        with pytest.raises(ValueError, match="at least 5"):
            project_lifetime_costs(current_age=4, sex="male", weight_status="Obese")

    def test_end_age_over_eighty_raises(self):
        with pytest.raises(ValueError, match="cannot exceed 80"):
            project_lifetime_costs(current_age=10, sex="male", weight_status="Obese", end_age=81)

    def test_end_age_not_greater_than_current_age_raises(self):
        with pytest.raises(ValueError, match="strictly greater"):
            project_lifetime_costs(current_age=15, sex="male", weight_status="Obese", end_age=15)
        with pytest.raises(ValueError, match="strictly greater"):
            project_lifetime_costs(current_age=15, sex="male", weight_status="Obese", end_age=10)

    def test_negative_budget_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            project_lifetime_costs(
                current_age=10,
                sex="male",
                weight_status="Obese",
                optional_monthly_budget_myr=-50.0,
            )

    def test_identical_projection_period_across_scenarios(self):
        """Both scenarios must cover the exact same number of years from current_age to end_age."""
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Obese",
            end_age=80,
        )
        summary = res["summary"]
        yearly = res["yearly_projections"]

        expected_years = 80 - 10 + 1  # 71 years
        assert summary["projection_duration_years"] == expected_years
        assert len(yearly) == expected_years
        assert yearly[0]["age"] == 10
        assert yearly[-1]["age"] == 80

    def test_obese_child_produces_substantial_scenario_a_cost(self):
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Obese",
            end_age=80,
            adjust_inflation=True,
        )
        summary = res["summary"]
        assert summary["scenario_a_total_myr"] > 0
        assert summary["net_difference_myr"] > 0

        # Check breakdown
        bd = res["scenario_a_breakdown"]
        assert bd["food_myr"] > 0
        assert bd["clothing_myr"] > 0
        assert bd["transport_myr"] > 0
        assert bd["healthcare_myr"] > 0

    def test_normal_weight_child_has_zero_scenario_a_cost(self):
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Normal weight",
            end_age=80,
            optional_monthly_budget_myr=0.0,
        )
        assert res["summary"]["scenario_a_total_myr"] == 0.0
        assert res["summary"]["scenario_b_total_myr"] == 0.0
        assert res["summary"]["net_difference_myr"] == 0.0

    def test_parent_budget_reflected_in_scenario_b(self):
        monthly_budget = 100.0  # RM 100/mo
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Obese",
            end_age=80,
            optional_monthly_budget_myr=monthly_budget,
            adjust_inflation=False,
        )
        # From age 10 to 17 (8 childhood years) * 1200 RM/yr = 9600 RM
        # Plus 2 years of initial intervention at 800 RM/yr = 1600 RM
        # Total uninflated Scenario B = 9600 + 1600 = 11,200 RM
        expected_b = (8 * 1200.0) + (2 * 800.0)
        assert res["summary"]["scenario_b_total_myr"] == pytest.approx(expected_b, abs=1.0)

    def test_evidence_and_uncertainty_disclosures_present(self):
        res = project_lifetime_costs(current_age=10, sex="female", weight_status="Obese")
        disclosures = res["evidence_and_uncertainty"]
        assert "causal_disclaimer" in disclosures
        assert "data_sources" in disclosures
        assert len(disclosures["data_sources"]) >= 4
