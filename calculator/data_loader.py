"""
calculator/data_loader.py
Central data access layer for The Cost of Waiting.

Responsible for:
- Loading CSV files with proper encoding (UTF-8 with and without BOM).
- Cleaning data artifacts in memory (e.g. non-numeric characters in bmi_meal_spending.csv)
  WITHOUT mutating raw files on disk.
- Providing validated, cached access to reference datasets.
"""

from __future__ import annotations

import os
from typing import Any
import pandas as pd

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

_CACHE: dict[str, pd.DataFrame] = {}


def get_data_path(filename: str) -> str:
    """Return the absolute path to a file in the data/ directory."""
    return os.path.join(_DATA_DIR, filename)


def load_cleaned_meal_spending(csv_path: str | None = None) -> pd.DataFrame:
    """Load and clean bmi_meal_spending.csv in memory.

    Cleans trailing '+' from age and spending columns without modifying the raw file.
    Columns returned:
    - sex: 'Male' / 'Female'
    - age_years: int (1 to 20; 20 represents 20+)
    - normal_bmi: float
    - obese_bmi: float
    - normal_annual_spending_myr: float
    - obese_annual_spending_myr: float
    - annual_difference_myr: float
    """
    cache_key = "meal_spending"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    path = csv_path or get_data_path("bmi_meal_spending.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Meal spending dataset not found at: {path}")

    raw_df = pd.read_csv(path, encoding="utf-8-sig")

    df = pd.DataFrame()
    df["sex"] = raw_df["Sex"].str.strip()

    # Clean 'Age (years)' where '20+' -> 20
    df["age_years"] = (
        raw_df["Age (years)"].astype(str).str.replace("+", "", regex=False).str.strip().astype(int)
    )

    df["normal_bmi"] = raw_df["Normal BMI"].astype(float)

    # Clean 'Obese BMI' where '30.0+' -> 30.0
    df["obese_bmi"] = (
        raw_df["Obese BMI"].astype(str).str.replace("+", "", regex=False).str.strip().astype(float)
    )

    df["normal_annual_spending_myr"] = raw_df["Average annual meal spending (MYR)"].astype(float)

    # Clean 'Obese annual meal spending (MYR)' where '7513.04+' -> 7513.04
    df["obese_annual_spending_myr"] = (
        raw_df["Obese annual meal spending (MYR)"]
        .astype(str)
        .str.replace("+", "", regex=False)
        .str.strip()
        .astype(float)
    )

    df["annual_difference_myr"] = (
        df["obese_annual_spending_myr"] - df["normal_annual_spending_myr"]
    ).round(2)

    _CACHE[cache_key] = df
    return df


def load_sector_inflation_rates(csv_path: str | None = None) -> pd.DataFrame:
    """Load the DOSM Sector Inflation Dataset.

    Covers 1980–2105 across 4 sectors:
    - 'Food & Non-Alcoholic Beverages'
    - 'Clothing & Footwear'
    - 'Health (Medicines & Healthcare-Related Products)'
    - 'Transportation'
    """
    cache_key = "sector_inflation"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    path = csv_path or get_data_path(
        "Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv"
    )
    if not os.path.exists(path):
        raise FileNotFoundError(f"Inflation dataset not found at: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    _CACHE[cache_key] = df
    return df


def load_transport_costs(csv_path: str | None = None) -> pd.DataFrame:
    """Load malaysia_transport_costs_adult_obese_nonobese_child.csv."""
    cache_key = "transport_costs"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    path = csv_path or get_data_path("malaysia_transport_costs_adult_obese_nonobese_child.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transport cost dataset not found at: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    _CACHE[cache_key] = df
    return df


def load_person_year_costs(csv_path: str | None = None) -> pd.DataFrame:
    """Load malaysia_obesity_cost_person_year.csv (synthetic Malaysian cohort)."""
    cache_key = "person_year"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    path = csv_path or get_data_path("malaysia_obesity_cost_person_year.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Person-year cost dataset not found at: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    _CACHE[cache_key] = df
    return df


def load_clothing_observations(csv_path: str | None = None) -> pd.DataFrame:
    """Load SizeCost_Malaysia_Granular_Size_Observations.csv."""
    cache_key = "clothing"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    path = csv_path or get_data_path("SizeCost_Malaysia_Granular_Size_Observations.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Clothing observations dataset not found at: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    _CACHE[cache_key] = df
    return df
