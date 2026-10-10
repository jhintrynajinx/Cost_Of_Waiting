"""
calculator/inflation.py
Inflation adjustment utilities for projecting future costs in Malaysian Ringgit.

Data Source & Provenance
-------------------------
Sector-specific rates and projections are sourced from:
Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv
Department of Statistics Malaysia (DOSM) Consumer Price Index (CPI) series (1980–2025)
and modelled projections (2026–2105).

Central projection annual rate assumptions:
- Food & Non-Alcoholic Beverages: ~3.1% (0.031)
- Clothing & Footwear: ~1.2% (0.012)
- Transportation: ~2.4% (0.024)
- Health: ~4.2% (0.042)
- General fallback: 2.5% (0.025)
"""

from __future__ import annotations

import pandas as pd

# Central baseline rates derived from DOSM projection series
SECTOR_ANNUAL_RATES: dict[str, dict[str, float]] = {
    "food": {"central": 0.031, "low": 0.020, "high": 0.045},
    "clothing": {"central": 0.012, "low": 0.005, "high": 0.022},
    "transport": {"central": 0.024, "low": 0.015, "high": 0.038},
    "healthcare": {"central": 0.042, "low": 0.028, "high": 0.060},
    "general": {"central": 0.025, "low": 0.015, "high": 0.040},
}


# ---------------------------------------------------------------------------
# Simple compound inflation
# ---------------------------------------------------------------------------

def apply_compound_inflation(
    present_value: float,
    annual_rate: float,
    years: int,
) -> float:
    """Apply compound inflation to a present-day cost.

    Parameters
    ----------
    present_value : float
        Cost in today's MYR.
    annual_rate : float
        Annual inflation rate as a decimal (e.g. 0.03 for 3 %).
    years : int
        Number of years into the future to project.

    Returns
    -------
    float
        Future value in nominal MYR, rounded to two decimal places.

    Raises
    ------
    ValueError
        If *years* is negative or *annual_rate* is below -1.
    """
    if years < 0:
        raise ValueError(f"years must be non-negative, got {years}")
    if annual_rate <= -1:
        raise ValueError(f"annual_rate must be > -1, got {annual_rate}")

    future_value = present_value * ((1 + annual_rate) ** years)
    return round(future_value, 2)


def project_costs_over_years(
    annual_cost_today: float,
    annual_rate: float,
    start_year: int,
    end_year: int,
) -> list[dict[str, float]]:
    """Project an annual cost forward year by year using compound inflation."""
    if end_year < start_year:
        raise ValueError("end_year must be >= start_year")

    results = []
    for offset, year in enumerate(range(start_year, end_year + 1)):
        inflated = apply_compound_inflation(annual_cost_today, annual_rate, offset)
        results.append({"year": year, "cost_myr": inflated})
    return results


def get_sector_inflation_rate(sector: str, scenario: str = "central") -> float:
    """Return the annual inflation rate for a specific spending sector.

    Parameters
    ----------
    sector : str
        'food', 'clothing', 'transport', 'healthcare', or 'general'.
    scenario : str
        'central', 'low', or 'high'.

    Returns
    -------
    float
        Annual inflation rate decimal (e.g. 0.042 for 4.2%).
    """
    s_clean = sector.strip().lower()
    scen_clean = scenario.strip().lower()

    sector_dict = SECTOR_ANNUAL_RATES.get(s_clean, SECTOR_ANNUAL_RATES["general"])
    return sector_dict.get(scen_clean, sector_dict["central"])


def compound_sector_cost(
    present_value: float,
    sector: str,
    years: int,
    scenario: str = "central",
) -> float:
    """Compound a present value using sector-specific inflation."""
    rate = get_sector_inflation_rate(sector, scenario=scenario)
    return apply_compound_inflation(present_value, rate, years)


# ---------------------------------------------------------------------------
# Variable-rate inflation from CSV (retained for backward compatibility)
# ---------------------------------------------------------------------------

def load_inflation_rates(csv_path: str) -> pd.DataFrame:
    """Load the historical and projected Malaysian inflation rate table."""
    required_columns = {"year", "annual_rate", "source"}
    df = pd.read_csv(csv_path)
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Inflation CSV is missing columns: {missing}")
    df["year"] = df["year"].astype(int)
    df["annual_rate"] = df["annual_rate"].astype(float)
    return df
