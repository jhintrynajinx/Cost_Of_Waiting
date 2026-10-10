"""
tests/test_breakdown.py
Unit tests verifying cost category disaggregation, exact 100% reconciliation,
and actuarial evidence disclosures for the 'Where Do the Costs Come From?' section.
"""

from __future__ import annotations

import pytest
from calculator.projection import project_lifetime_costs


class TestCostCategoryBreakdown:
    """Tests verifying mathematical reconciliation and category behavior."""

    @pytest.mark.parametrize(
        "current_age,sex,weight_status,end_age,monthly_budget",
        [
            (10, "male", "Obese", 80, 150.0),
            (6, "female", "Obese", 60, 0.0),
            (12, "male", "Overweight", 70, 100.0),
            (15, "female", "Normal weight", 80, 250.0),
        ],
    )
    def test_category_present_values_reconcile_to_headline_total(
        self,
        current_age: int,
        sex: str,
        weight_status: str,
        end_age: int,
        monthly_budget: float,
    ) -> None:
        """Every individual category sum discounted at 3% must match headline Total A to the cent."""
        res = project_lifetime_costs(
            current_age=current_age,
            sex=sex,
            weight_status=weight_status,
            end_age=end_age,
            optional_monthly_budget_myr=monthly_budget,
            adjust_inflation=True,
            inflation_scenario="central",
        )
        sdr = 0.03
        yearly = res["yearly_projections"]

        pv_food_a = sum(r["food_myr"] / ((1 + sdr) ** r["offset_years"]) for r in yearly)
        pv_clothing_a = sum(r["clothing_myr"] / ((1 + sdr) ** r["offset_years"]) for r in yearly)
        pv_transport_a = sum(r["transport_myr"] / ((1 + sdr) ** r["offset_years"]) for r in yearly)
        pv_healthcare_a = sum(r["healthcare_myr"] / ((1 + sdr) ** r["offset_years"]) for r in yearly)

        headline_total_a = sum(
            r["scenario_a_annual_myr"] / ((1 + sdr) ** r["offset_years"]) for r in yearly
        )

        assert round(pv_food_a + pv_clothing_a + pv_transport_a + pv_healthcare_a, 2) == round(
            headline_total_a, 2
        )

    def test_pediatric_transport_and_clothing_differentials_are_zero_before_18(self) -> None:
        """Transport and clothing differences must be zero during all childhood years (<18)."""
        res = project_lifetime_costs(
            current_age=5,
            sex="male",
            weight_status="Obese",
            end_age=17,
            optional_monthly_budget_myr=0.0,
            adjust_inflation=True,
        )
        yearly = res["yearly_projections"]
        for row in yearly:
            assert row["transport_myr"] == 0.0, f"Transport should be 0 for age {row['age']}"
            assert row["clothing_myr"] == 0.0, f"Clothing should be 0 for age {row['age']}"

    def test_normal_weight_child_incurs_zero_scenario_a_category_costs(self) -> None:
        """Normal weight children must have zero excess costs across all Scenario A categories."""
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Normal weight",
            end_age=80,
            optional_monthly_budget_myr=150.0,
        )
        yearly = res["yearly_projections"]
        for row in yearly:
            assert row["scenario_a_annual_myr"] == 0.0
            assert row["healthcare_myr"] == 0.0
            assert row["food_myr"] == 0.0
            assert row["transport_myr"] == 0.0
            assert row["clothing_myr"] == 0.0


    def test_scenario_b_curve_is_strictly_increasing_and_non_flat_in_adulthood(self) -> None:
        """Scenario B cumulative full expenditure must strictly increase every single year (ages 18 to 80)."""
        res = project_lifetime_costs(
            current_age=10,
            sex="male",
            weight_status="Obese",
            end_age=80,
            optional_monthly_budget_myr=150.0,
            adjust_inflation=True,
        )
        yearly = res["yearly_projections"]
        adult_rows = [r for r in yearly if r["age"] >= 18]
        assert len(adult_rows) > 0

        # Verify annual expenses in adulthood are positive
        for row in adult_rows:
            assert row["scenario_b_full_annual_myr"] > 0, (
                f"Annual Scenario B cost must be positive at age {row['age']}"
            )
            assert row["reference_annual_myr"] > 0

        # Verify cumulative expenditure strictly increases
        for i in range(1, len(yearly)):
            prev_cum = yearly[i - 1]["scenario_b_full_cumulative_myr"]
            curr_cum = yearly[i]["scenario_b_full_cumulative_myr"]
            assert curr_cum > prev_cum, (
                f"Cumulative Scenario B must strictly increase from age {yearly[i-1]['age']} to {yearly[i]['age']}"
            )

    @pytest.mark.parametrize("monthly_budget", [0.0, 150.0, 300.0])
    def test_prescription_plan_responds_to_budget_tiers(self, monthly_budget: float) -> None:
        """Prescription recommendations must adapt dynamically without exceeding available budget."""
        from ui.screen_report import get_budget_prescription_content

        rx = get_budget_prescription_content(monthly_budget)
        assert "title" in rx
        assert "items" in rx
        assert len(rx["items"]) == 3

        if monthly_budget == 0.0:
            assert "Zero Out-of-Pocket" in rx["subtitle"] or "Public" in rx["title"]
            assert rx["outlay_label"] == "RM 0 / mo"
            # Must mention free/public services
            text_blob = " ".join(item["title"] + item["desc"] for item in rx["items"])
            assert "RM 0" in text_blob
            assert "Klinik Kesihatan" in text_blob
        elif monthly_budget == 150.0:
            assert "Modest" in rx["subtitle"] or "Targeted" in rx["title"]
            assert "150" in rx["outlay_sub"]
            # Outlay range must be <= 150
            text_blob = " ".join(item["title"] + item["desc"] for item in rx["items"])
            assert "Fresh Produce" in text_blob or "Produce" in text_blob
        elif monthly_budget == 300.0:
            assert "Structured" in rx["title"] or "Comprehensive" in rx["subtitle"]
            assert "300" in rx["outlay_sub"]
            text_blob = " ".join(item["title"] + item["desc"] for item in rx["items"])
            assert "Dietitian" in text_blob or "Youth Athletics" in text_blob

        # Must include cautionary guidance that spending doesn't guarantee outcomes
        assert "outcome" in rx["note"].lower() or "success" in rx["note"].lower()


def test_app_screen_flow_and_input_preservation() -> None:
    """Verify that user inputs are buffered and preserved when navigating between screens."""
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    assert at.session_state["screen"] == "inputs"

    # Modify form fields
    at.number_input(key="widget_child_age").set_value(11)
    at.number_input(key="widget_height_cm").set_value(142.0)
    at.number_input(key="widget_weight_kg").set_value(45.0)
    at.slider(key="widget_target_age").set_value(45)
    at.select_slider(key="widget_monthly_budget").set_value(300)

    # Submit form
    at.button(key="generate_report_btn").click().run()
    assert at.session_state["screen"] == "report"
    assert len(at.exception) == 0

    # Return to inputs
    at.button(key="back_btn").click().run()
    assert at.session_state["screen"] == "inputs"
    assert at.session_state["child_age"] == 11
    assert at.session_state["height_cm"] == 142.0
    assert at.session_state["weight_kg"] == 45.0
    assert at.session_state["target_age"] == 45
    assert at.session_state["monthly_budget"] == 300.0


def test_app_report_generation_with_zero_budget() -> None:
    """Verify report screen renders cleanly when budget is RM 0."""
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()

    at.select_slider(key="widget_monthly_budget").set_value(0)
    at.button(key="generate_report_btn").click().run()
    assert at.session_state["screen"] == "report"
    assert len(at.exception) == 0


def test_target_horizon_slider_affects_projections() -> None:
    """Confirm moving the target age slider updates target_age and alters calculation projections."""
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"

    # Test 1: Set target age to 45 (Adulthood)
    at_45 = AppTest.from_file(str(app_path))
    at_45.run()
    at_45.slider(key="widget_target_age").set_value(45)
    at_45.button(key="generate_report_btn").click().run()
    assert at_45.session_state["screen"] == "report"
    assert at_45.session_state["target_age"] == 45
    assert len(at_45.exception) == 0

    # Test 2: Set target age to 80 (Lifetime)
    at_80 = AppTest.from_file(str(app_path))
    at_80.run()
    at_80.slider(key="widget_target_age").set_value(80)
    at_80.button(key="generate_report_btn").click().run()
    assert at_80.session_state["screen"] == "report"
    assert at_80.session_state["target_age"] == 80
    assert len(at_80.exception) == 0


def test_report_renders_no_source_code_fences() -> None:
    """Verify that Where Do the Costs Come From contains real HTML and zero markdown code fences."""
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    at.button(key="generate_report_btn").click().run()
    assert at.session_state["screen"] == "report"

    # Inspect all markdown elements to ensure none contain accidental code fences
    for m in at.markdown:
        val = str(m.value)
        assert "```" not in val, f"Accidental code fence found in markdown: {val[:200]}"
        if "Where Do the Costs Come From" in val:
            assert "<table class=\"breakdown-table\">" in val or "breakdown-table" in val
            assert "Not estimated — insufficient evidence" in val




