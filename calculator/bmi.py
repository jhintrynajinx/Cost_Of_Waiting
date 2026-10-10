"""
calculator/bmi.py
BMI calculation and weight-status classification for children and adults.

References
----------
- WHO Child Growth Standards (2006) for children aged 0–5.
- WHO Growth Reference for School-Age Children and Adolescents (2007) for ages 5–19.
- WHO adult BMI classification for ages 18+.
- Centers for Disease Control and Prevention (CDC) BMI percentile guidance.

Note: For children and adolescents (under 18), BMI-for-age percentile is the
standard measure. Age- and sex-specific cut-offs are required. This module
provides the adult formula and a placeholder for the paediatric percentile
lookup, which will be populated once the reference dataset is loaded.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Adult BMI
# ---------------------------------------------------------------------------

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index (BMI).

    Parameters
    ----------
    weight_kg : float
        Body weight in kilograms.
    height_cm : float
        Standing height in centimetres.

    Returns
    -------
    float
        BMI value rounded to two decimal places.

    Raises
    ------
    ValueError
        If weight or height are non-positive.

    Examples
    --------
    >>> calculate_bmi(70, 170)
    24.22
    """
    if weight_kg <= 0:
        raise ValueError(f"weight_kg must be positive, got {weight_kg}")
    if height_cm <= 0:
        raise ValueError(f"height_cm must be positive, got {height_cm}")

    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi_adult(bmi: float) -> str:
    """Classify BMI using WHO adult cut-off points.

    Parameters
    ----------
    bmi : float
        BMI value as returned by :func:`calculate_bmi`.

    Returns
    -------
    str
        One of: 'Underweight', 'Normal weight', 'Overweight', 'Obese'.

    References
    ----------
    WHO (2000). Obesity: preventing and managing the global epidemic.
    Technical Report Series 894. Geneva: World Health Organization.

    Examples
    --------
    >>> classify_bmi_adult(17.0)
    'Underweight'
    >>> classify_bmi_adult(22.0)
    'Normal weight'
    >>> classify_bmi_adult(27.5)
    'Overweight'
    >>> classify_bmi_adult(32.0)
    'Obese'
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def is_obese_adult(bmi: float) -> bool:
    """Return True if the adult BMI meets the WHO obesity threshold (≥ 30).

    Parameters
    ----------
    bmi : float
        BMI value.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_obese_adult(29.9)
    False
    >>> is_obese_adult(30.0)
    True
    """
    return bmi >= 30.0


# ---------------------------------------------------------------------------
# Paediatric BMI (WHO 2007 Growth Reference, Ages 5–19 / Months 61–228)
# ---------------------------------------------------------------------------

import math
import os
import pandas as pd

_WHO_GROWTH_DF: pd.DataFrame | None = None
_DEFAULT_WHO_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "who2007_bmi_for_age_lms.csv",
)


def load_who_growth_reference(csv_path: str | None = None) -> pd.DataFrame:
    """Load and validate the WHO 2007 BMI-for-age LMS growth reference table.

    Parameters
    ----------
    csv_path : str, optional
        Path to ``who2007_bmi_for_age_lms.csv``. Defaults to project ``data/`` path.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed or filtered by sex and month.
    """
    global _WHO_GROWTH_DF
    path = csv_path or _DEFAULT_WHO_CSV
    if not os.path.exists(path):
        raise FileNotFoundError(f"WHO reference file not found at: {path}")

    required_cols = {"sex", "month", "L", "M", "S", "pub_sd_neg2", "pub_sd_pos1", "pub_sd_pos2"}
    df = pd.read_csv(path, encoding="utf-8-sig")
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"WHO reference CSV missing required columns: {missing}")

    df["sex"] = df["sex"].str.strip().str.lower()
    df["month"] = df["month"].astype(int)
    for col in ["L", "M", "S", "pub_sd_neg2", "pub_sd_pos1", "pub_sd_pos2"]:
        df[col] = df[col].astype(float)

    _WHO_GROWTH_DF = df
    return df


def normalize_child_sex(sex: str) -> str:
    """Normalize sex string to 'boys' or 'girls' for WHO 2007 lookup.

    Raises
    ------
    ValueError
        If sex is unrecognized.
    """
    cleaned = sex.strip().lower()
    if cleaned in {"male", "boy", "boys", "m"}:
        return "boys"
    if cleaned in {"female", "girl", "girls", "f"}:
        return "girls"
    raise ValueError(f"Unrecognized sex '{sex}'. Must be 'male' or 'female'.")


def calculate_child_bmi_z_score(
    bmi: float,
    age_months: int,
    sex: str,
    ref_df: pd.DataFrame | None = None,
) -> float:
    """Calculate WHO 2007 BMI-for-age Z-score (standard deviation score, SDS) using the LMS method.

    Formula:
        Z = ((BMI / M)^L - 1) / (L * S)  if L != 0
        Z = ln(BMI / M) / S              if L == 0

    Parameters
    ----------
    bmi : float
        Calculated body mass index (kg/m²).
    age_months : int
        Child's age in completed months (61 to 228 months, representing 5–19 years).
    sex : str
        'male'/'boy' or 'female'/'girl'.
    ref_df : pd.DataFrame, optional
        Pre-loaded reference table.

    Returns
    -------
    float
        BMI z-score rounded to 2 decimal places.

    Raises
    ------
    ValueError
        If age_months is outside the WHO 2007 reference range (61 to 228 months).
    """
    if bmi <= 0:
        raise ValueError(f"bmi must be positive, got {bmi}")
    if age_months < 61 or age_months > 228:
        raise ValueError(
            f"WHO 2007 growth reference supports ages 61 to 228 months (5.08 to 19.0 years). "
            f"Got age_months={age_months}."
        )

    norm_sex = normalize_child_sex(sex)
    df = ref_df if ref_df is not None else (_WHO_GROWTH_DF if _WHO_GROWTH_DF is not None else load_who_growth_reference())

    match = df[(df["sex"] == norm_sex) & (df["month"] == age_months)]
    if match.empty:
        raise ValueError(f"No WHO growth reference entry found for sex={norm_sex}, month={age_months}")

    row = match.iloc[0]
    L = float(row["L"])
    M = float(row["M"])
    S = float(row["S"])

    if abs(L) < 1e-7:
        z = math.log(bmi / M) / S
    else:
        z = (((bmi / M) ** L) - 1.0) / (L * S)

    return round(z, 2)


def interpret_child_bmi(
    bmi: float,
    age_years: float | int | None = None,
    sex: str = "male",
    age_months: int | None = None,
    ref_df: pd.DataFrame | None = None,
) -> dict[str, object]:
    """Provide age-appropriate WHO 2007 BMI classification for children aged 5–19.

    WHO 2007 Cut-offs (Ages 5–19):
    - Severe thinness: Z < -3 SD
    - Thinness: -3 SD <= Z < -2 SD (or BMI < pub_sd_neg2)
    - Normal weight: -2 SD <= Z <= +1 SD
    - Overweight: +1 SD < Z <= +2 SD (equivalent to adult BMI 25 at 19 years)
    - Obese: Z > +2 SD (equivalent to adult BMI 30 at 19 years)

    Returns
    -------
    dict[str, object]
        Detailed screening assessment including category, z-score, thresholds,
        and medical disclaimers.
    """
    if age_months is None:
        if age_years is None:
            raise ValueError("Either age_months or age_years must be provided.")
        age_months = int(round(age_years * 12))

    if age_months < 61:
        raise ValueError(
            f"Child age ({age_months} months / {age_months/12:.1f} years) is below the WHO 2007 "
            "growth reference range (minimum 61 months / 5 years 1 month). "
            "Children under 5 require the WHO 2006 Child Growth Standards."
        )
    if age_months > 228:
        raise ValueError(
            f"Age ({age_months} months / {age_months/12:.1f} years) exceeds the paediatric WHO 2007 "
            "reference range (maximum 228 months / 19 years). Please use adult BMI classification."
        )

    z = calculate_child_bmi_z_score(bmi, age_months, sex, ref_df=ref_df)

    norm_sex = normalize_child_sex(sex)
    df = ref_df if ref_df is not None else (_WHO_GROWTH_DF if _WHO_GROWTH_DF is not None else load_who_growth_reference())
    row = df[(df["sex"] == norm_sex) & (df["month"] == age_months)].iloc[0]

    sd_neg2 = float(row["pub_sd_neg2"])
    sd_pos1 = float(row["pub_sd_pos1"])
    sd_pos2 = float(row["pub_sd_pos2"])

    if z > 2.0:
        category = "Obese"
    elif z > 1.0:
        category = "Overweight"
    elif z >= -2.0:
        category = "Normal weight"
    elif z >= -3.0:
        category = "Thinness"
    else:
        category = "Severe thinness"

    is_obese = category == "Obese"

    return {
        "category": category,
        "is_obese": is_obese,
        "z_score": z,
        "age_months": age_months,
        "age_years": round(age_months / 12, 1),
        "sex": "Male" if norm_sex == "boys" else "Female",
        "bmi": bmi,
        "cutoffs": {
            "thinness_threshold": sd_neg2,
            "overweight_threshold": sd_pos1,
            "obese_threshold": sd_pos2,
        },
        "is_screening_tool": True,
        "disclaimer": (
            "Screening information only, not a medical diagnosis. WHO growth references "
            "identify population-level risk. Individual clinical assessment by a healthcare "
            "professional is required."
        ),
    }


def classify_bmi_child(bmi: float, age_years: float, sex: str) -> str:
    """Classify BMI-for-age for children and adolescents (ages 5–19).

    Convenience function returning the string category name.
    """
    try:
        res = interpret_child_bmi(bmi, age_years=age_years, sex=sex)
        return str(res["category"])
    except ValueError as e:
        return f"Out of reference range: {e}"

