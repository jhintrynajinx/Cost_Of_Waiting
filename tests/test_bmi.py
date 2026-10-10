"""
tests/test_bmi.py
Unit tests for calculator/bmi.py.

Run with:
    python -m pytest tests/test_bmi.py -v
"""

import pytest
from calculator.bmi import calculate_bmi, classify_bmi_adult, is_obese_adult


# ---------------------------------------------------------------------------
# calculate_bmi
# ---------------------------------------------------------------------------

class TestCalculateBmi:
    def test_typical_healthy_weight(self):
        """BMI for 70 kg, 170 cm should be approximately 24.22."""
        result = calculate_bmi(70, 170)
        assert result == pytest.approx(24.22, abs=0.01)

    def test_rounding_to_two_decimal_places(self):
        """Result should always be rounded to 2 decimal places."""
        result = calculate_bmi(80, 175)
        assert result == round(result, 2)

    def test_zero_weight_raises(self):
        with pytest.raises(ValueError, match="weight_kg"):
            calculate_bmi(0, 170)

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError):
            calculate_bmi(-5, 170)

    def test_zero_height_raises(self):
        with pytest.raises(ValueError, match="height_cm"):
            calculate_bmi(70, 0)

    def test_negative_height_raises(self):
        with pytest.raises(ValueError):
            calculate_bmi(70, -160)

    def test_obese_range(self):
        """Known obese BMI: 100 kg, 160 cm → 39.06."""
        result = calculate_bmi(100, 160)
        assert result == pytest.approx(39.06, abs=0.01)


# ---------------------------------------------------------------------------
# classify_bmi_adult
# ---------------------------------------------------------------------------

class TestClassifyBmiAdult:
    def test_underweight_boundary(self):
        assert classify_bmi_adult(18.4) == "Underweight"

    def test_normal_weight_lower_boundary(self):
        assert classify_bmi_adult(18.5) == "Normal weight"

    def test_normal_weight_upper_boundary(self):
        assert classify_bmi_adult(24.9) == "Normal weight"

    def test_overweight_lower_boundary(self):
        assert classify_bmi_adult(25.0) == "Overweight"

    def test_overweight_upper_boundary(self):
        assert classify_bmi_adult(29.9) == "Overweight"

    def test_obese_boundary(self):
        assert classify_bmi_adult(30.0) == "Obese"

    def test_obese_high_value(self):
        assert classify_bmi_adult(45.0) == "Obese"


# ---------------------------------------------------------------------------
# is_obese_adult
# ---------------------------------------------------------------------------

class TestIsObeseAdult:
    def test_exactly_30_is_obese(self):
        assert is_obese_adult(30.0) is True

    def test_above_30_is_obese(self):
        assert is_obese_adult(35.5) is True

    def test_below_30_is_not_obese(self):
        assert is_obese_adult(29.99) is False

    def test_underweight_is_not_obese(self):
        assert is_obese_adult(17.0) is False


# ---------------------------------------------------------------------------
# Paediatric BMI (WHO 2007)
# ---------------------------------------------------------------------------

from calculator.bmi import (
    calculate_child_bmi_z_score,
    interpret_child_bmi,
    classify_bmi_child,
)


class TestChildBmiClassification:
    def test_ten_year_old_boy_obese(self):
        """At 120 months (age 10), WHO +2 SD cut-off for boys is ~22.1. BMI 24 should be Obese."""
        result = interpret_child_bmi(bmi=24.0, age_months=120, sex="male")
        assert result["category"] == "Obese"
        assert result["is_obese"] is True
        assert result["z_score"] > 2.0
        assert "screening" in result["disclaimer"].lower()

    def test_ten_year_old_boy_normal_weight(self):
        """At 120 months, median BMI is ~16.6. BMI 16.5 should be Normal weight."""
        result = interpret_child_bmi(bmi=16.5, age_months=120, sex="male")
        assert result["category"] == "Normal weight"
        assert result["is_obese"] is False
        assert -2.0 <= result["z_score"] <= 1.0

    def test_ten_year_old_girl_overweight(self):
        """At 120 months, WHO +1 SD for girls is ~19.0. BMI 20.0 should be Overweight."""
        result = interpret_child_bmi(bmi=20.0, age_months=120, sex="female")
        assert result["category"] == "Overweight"
        assert result["is_obese"] is False
        assert 1.0 < result["z_score"] <= 2.0

    def test_age_years_conversion(self):
        """Passing age_years=10 should compute 120 months."""
        result = interpret_child_bmi(bmi=24.0, age_years=10, sex="male")
        assert result["age_months"] == 120
        assert result["category"] == "Obese"

    def test_classify_bmi_child_convenience_string(self):
        category = classify_bmi_child(bmi=24.0, age_years=10, sex="male")
        assert category == "Obese"

    def test_under_five_years_raises(self):
        """Ages below 61 months must raise ValueError indicating WHO 2007 limit."""
        with pytest.raises(ValueError, match="below the WHO 2007"):
            interpret_child_bmi(bmi=18.0, age_months=60, sex="male")

    def test_over_nineteen_years_raises(self):
        """Ages above 228 months must raise ValueError indicating paediatric limit."""
        with pytest.raises(ValueError, match="exceeds the paediatric WHO 2007"):
            interpret_child_bmi(bmi=25.0, age_months=229, sex="male")

    def test_zero_or_negative_bmi_raises(self):
        with pytest.raises(ValueError, match="positive"):
            calculate_child_bmi_z_score(bmi=-10.0, age_months=120, sex="male")

    def test_invalid_sex_raises(self):
        with pytest.raises(ValueError, match="Unrecognized sex"):
            interpret_child_bmi(bmi=20.0, age_months=120, sex="unknown")

