# ANTIGRAVITY PROJECT AUDIT & HANDOVER ASSESSMENT
## The Cost of Waiting — Malaysian Childhood Obesity Lifetime Cost Calculator

**Date:** 2026-10-10  
**Assessor:** Antigravity (Pair Programming AI Assistant)  
**Project:** The Cost of Waiting (Malaysian Childhood Obesity Financial Decision-Support Tool)  
**Status:** Initial Assessment & Architecture Audit (No project files altered, all raw datasets preserved)

---

## Executive Summary for the Project Owner

Welcome to the initial audit report. You have built a solid foundation and collected rich datasets. However, the project is currently in an early **transition phase**:

1. **The application frontend (`app.py`) is currently a static landing page.** It does not yet connect the input widgets (`ui/inputs.py`), the charts (`ui/charts.py`), or the summary displays (`ui/summary.py`) to the calculation engine.
2. **The calculation modules (`calculator/`) are mostly skeleton functions returning `0.0`.** Only adult BMI math and basic compound inflation math are currently implemented.
3. **The data files collected are far richer than the original templates**, but the existing code still references the old, empty template files.
4. **Environment check:** Git and Python are not currently available in the system `PATH`. As a result, automated unit tests could not be executed in this session.
5. **Future Google Stitch UI:** The Google Stitch design has **not** been imported or inspected. The architecture is cleanly decoupled so that once you provide Stitch templates (HTML/CSS or components), they can be smoothly integrated without rewriting the calculation engine.

Below is the complete, evidence-based audit.

---

## 1. Current Project Architecture

### 1.1 Architecture Pattern
The project is organized into a clean **three-tier architecture**:

```
┌────────────────────────────────────────────────────────┐
│                   UI Layer (`ui/` + `app.py`)          │
│   Streamlit widgets, Plotly visualisations, layouts    │
└───────────────────────────┬────────────────────────────┘
                            │ (passes clean dicts/primitives)
┌───────────────────────────▼────────────────────────────┐
│              Calculation Engine (`calculator/`)         │
│   Pure Python logic (Zero Streamlit imports)            │
│   BMI, Inflation, Food, Clothing, Transport, Health     │
└───────────────────────────┬────────────────────────────┘
                            │ (loads DataFrames via pandas)
┌───────────────────────────▼────────────────────────────┐
│                   Data Layer (`data/`)                 │
│   13 CSV files: Government stats, surveys, models      │
└────────────────────────────────────────────────────────┘
```

- **Framework:** Streamlit (>= 1.35.0).
- **Visualization:** Plotly (>= 5.22.0).
- **Data Manipulation:** Pandas (>= 2.2.0), NumPy (>= 1.26.0).
- **Testing:** Pytest.
- **Entry Point:** `app.py`.

### 1.2 Component Breakdown
- **`app.py` (Entry point):** Displays informational text about the five expense categories and an expander previewing future fields. It does **not** yet import or run `ui/inputs.py` or `ui/summary.py`.
- **`calculator/`:**
  - `bmi.py`: Fully implements adult BMI and adult classification. Contains a stub for paediatric BMI-for-age percentiles.
  - `inflation.py`: Implements compound inflation calculations (`apply_compound_inflation` and `project_costs_over_years`). Contains a stub for CSV rate loading.
  - `food.py`, `clothing.py`, `transport.py`, `healthcare.py`: Skeletons where estimation functions return `0.0`. Loaders expect old template schemas.
- **`ui/`:**
  - `inputs.py`: Renders inputs for Age (2–17), Sex, Height, Weight, and Projection End Age (slider 20–80). Missing: Optional monthly lifestyle budget (RM) and Page 1 / Page 2 navigation.
  - `charts.py`: Implements Plotly line chart, horizontal bar chart, and waterfall chart functions.
  - `summary.py`: Renders total metrics, a percentage breakdown table, and charts. Currently accepts a generic single-scenario dictionary.
- **`tests/`:** Contains unit test files for BMI, inflation, and food.

---

## 2. Comprehensive Dataset Audit

The workspace contains **13 CSV files** in the `data/` directory. Each file was inspected directly:

### 2.1 Substantive Datasets

| File & Path | Rows × Cols | Size | Key Variables & Inferred Types | Coverage & Dates | Provenance & Source | Quality Assessment & Suitability |
|---|---|---|---|---|---|---|
| `data/Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv` | 1,144 rows × 21 cols | ~820 KB | `sector` (string), `year` (int), `data_type` (str), `scenario` (str), `annual_inflation_rate_percent` (float), `cpi_index` (float) | 1980–2105 (Historical: 1980–2025; Projections: 2026–2105). Malaysia national. 4 sectors: Food, Clothing, Health, Transport. | **DOSM** (Department of Statistics Malaysia) CPI series. URL: `https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv`. Retrieval: 2026-10-10. | **EXCELLENT / PASS**. Highest-quality dataset in the repo. Contains 3 projection scenarios (`central`, `low`, `high`). First historical year (1980) has blank YoY rate as expected. |
| `data/SizeCost_Malaysia_Granular_Size_Observations.csv` | 1,337 rows × 17 cols | ~440 KB | `Retailer` (str), `Product Name` (str), `Displayed Size` (str), `Size Classification` (str), `Current Selling Price (RM)` (float) | Snapshot collected 2026-10-10. 18 Malaysian retailers (Uniqlo, Padini, Zalora, M&S, Oxwhite, etc.). | Scraped retail observations with URLs and verification status. | **PASS (Resolved Parser Non-Issue)**. Prior handover suspected "column shift contamination". RFC 4180 parsing confirms 1,172 "Standard" and 165 "Extended / Plus". 2 items have RM 0.00 (1 free promotional oil, 1 test item). 26 duplicate IDs. Premium is small/zero for most mass retailers. |
| `data/bmi_meal_spending.csv` | 40 rows × 6 cols | ~1.5 KB | `Sex` (str), `Age (years)` (str/int), `Normal BMI` (float), `Obese BMI` (str/float), `Average annual meal spending (MYR)` (float), `Obese annual meal spending (MYR)` (str/float) | Ages 1–19, plus "20+". Male & Female. | **UNKNOWN / UNDOCUMENTED**. No source URL or citations. | **NEEDS PROVENANCE & CLEANING**. Mathematical discovery: Obese spending was derived directly by multiplying Baseline Spending × (Obese BMI / Normal BMI). Age "20+" and spending "7513.04+" contain trailing "+" symbols that break float conversion. |
| `data/malaysia_transport_costs_adult_obese_nonobese_child.csv` | 10 rows × 10 cols | ~1.6 KB | `Category`, `Item`, `Adult_Non_Obese_MYR_per_Month`, `Adult_Obese_MYR_per_Month`, `Child_MYR_per_Month`, `Child_MYR_per_Year` | Monthly & annual costs. Adults and children. Includes UTF-8 BOM. | Stated as: *"Illustrative scenario estimates, not survey data"*. | **PASS WITH LIMITATIONS**. Useful for adult differential (RM 4,740/year). **Critical limitation:** Child transport is RM 600/yr for all children with no obese vs. non-obese difference modelled. |
| `data/malaysia_transport_costs_obese_vs_non_obese.csv` | 9 rows × 8 cols | ~1.1 KB | `Category`, `Item`, `Non_Obese_MYR_per_Month`, `Obese_MYR_per_Month`, `Difference_MYR_per_Year` | Adults only. Includes UTF-8 BOM. | Stated as assumptions in notes. | **SUPERSEDED**. Superseded by the adult+child dataset above. Uses slightly different assumptions (RM 4,380 adult diff vs RM 4,740). |
| `data/malaysia_obesity_healthcare_costs.csv` | 53 rows × 15 cols | ~18.8 KB | `bmi_group`, `setting`, `cost_component`, `annual_cost_low_RM`, `annual_cost_high_RM`, `ratio_vs_nonobese_midpoint`, `source_urls` | Non-obese, Obese Classes I, II, III. Public (MOH) and Private. Includes UTF-8 BOM. | MMA fee guide, MOH Sarawak, CodeBlue, PubMed, ScienceDirect, JMDH. | **USE WITH FLAGS**. Sourced ranges for GP visits, ward fees, GLP-1 drugs (RM 800–1,800/mo), bariatric surgery (RM 15k–50k). Contains 3 explicit "DATA GAP" rows and multiple "ASSUMED" visit frequencies. |
| `data/malaysia_obesity_cost_person_year.csv` | 18,000 rows × 44 cols | ~4.86 MB | `person_id`, `age` (5–85), `sex`, `region`, `healthcare_sector_payer`, `weight_status`, 17 comorbidity flags, cost columns in MYR | 2024–2026. 6 Malaysian regions. 6,000 synthetic individuals × 3 years. | Synthetic micro-simulation cohort. Fixed exchange rate 4.08 MYR/USD. | **PASS WITH DISCLOSURE**. Rich dataset for mean healthcare costs by age and weight status: Normal = RM 2,520; Obese Class 1 = RM 5,596 (2.22×); Obese Class 2 = RM 7,523; Obese Class 3 = RM 10,156. Must be disclosed as synthetic. |
| `data/malaysia_obesity_cost_line_items.csv` | 130,345 rows × 14 cols | ~22 MB | `person_id`, `year`, `age`, `cost_category`, `item`, `unit_cost_myr`, `units_per_year`, `total_cost_myr`, `patient_out_of_pocket_myr` | Links to `person_year.csv`. Covers outpatient, pharmacy, lab, ER, DME. | Synthetic micro-simulation line items. | **PASS WITH DISCLOSURE**. Supports granular evidence drill-downs. Not needed for top-level projections. |

### 2.2 Template Files (0 Data Rows)
The following 5 files contain only commented headers and instructions. They should remain in `data/` as historical schema records but must **not** be loaded by the active calculator:
- `data/food_prices_malaysia.csv` (16 lines, 0 data rows)
- `data/clothing_prices.csv` (15 lines, 0 data rows)
- `data/transport_costs.csv` (16 lines, 0 data rows)
- `data/healthcare_costs.csv` (22 lines, 0 data rows)
- `data/inflation_rates.csv` (20 lines, 0 data rows)

### 2.3 Crucial Missing Dataset: Child Growth Reference
- **Missing File:** WHO BMI-for-age Growth Reference (Ages 5–19) and WHO Child Growth Standards (Ages 0–5).
- **Impact:** For adults, BMI ≥ 30 is obese. For children, BMI thresholds change with every month of age and differ by sex. Currently, the application **cannot** accurately determine if a child is overweight or obese without this reference table.

---

## 3. Calculation & Evidence Audit

### 3.1 Data Flow Trace
1. **User Input:** User enters age, sex, height, weight, and end age in `ui/inputs.py`. (Currently not connected to `app.py`).
2. **BMI Interpretation:** `calculator/bmi.py` calculates $BMI = weight / (height/100)^2$. If age < 18, `classify_bmi_child()` returns `"Classification pending"`.
3. **Cost Categories:**
   - **Food:** `estimate_annual_food_cost_difference()` returns `0.0`.
   - **Clothing:** `estimate_annual_clothing_cost_difference()` returns `0.0`.
   - **Transport:** `estimate_annual_transport_cost_difference()` returns `0.0`.
   - **Healthcare:** `estimate_annual_healthcare_cost_difference()` returns `0.0`.
4. **Inflation:** Functions exist in `calculator/inflation.py` to compound values forward, but they are not hooked to the sector-specific inflation dataset (`D4`).
5. **Scenario Comparison:** There is currently **no logic** for Scenario A ("The Cost of Waiting") versus Scenario B ("The Cost of Acting Early").

### 3.2 Audit of Causal Assumptions & Methodological Risks
- **No Direct Causal Evidence in Datasets:** The datasets document cross-sectional cost differences between obese and healthy individuals. They **do not prove** that an intervention at age 10 causes an exact financial saving by age 40.
- **Scenario Framing:** 
  - **Scenario A (Waiting / Unchanged Trajectory):** Cumulative projected costs if the child remains on an obese trajectory through the chosen end age.
  - **Scenario B (Early Action / Healthy Trajectory):** Cumulative projected costs if the child transitions to and maintains a healthy weight trajectory, plus any user-specified lifestyle/intervention budget.
  - **Difference:** Must be clearly described as an *estimated lifetime expenditure difference between two potential trajectories*, not a guaranteed financial return or clinical promise.
- **Child Transport Difference:** `malaysia_transport_costs_adult_obese_nonobese_child.csv` shows RM 0 difference for children. Transport differences only manifest in adult driving years.
- **Food Cost Scaling:** `bmi_meal_spending.csv` mathematically assumes food spending scales linearly with BMI. This assumption must be disclosed to users.

---

## 4. Target User Experience Gap Analysis

| Required Feature | Current Implementation Status | Gap / Required Action |
|---|---|---|
| **Two-Page Workflow** | Single landing page stub in `app.py` | Need clean multi-step/two-page navigation (e.g. Page 1: Input & Configuration → Page 2: Report & Evidence). |
| **Page 1: Child Information** | `ui/inputs.py` has Age, Sex, Height, Weight | Working widgets exist, but need validation logic, DOB support if desired, and integration with paediatric BMI cutoffs. |
| **Page 1: Projection End Age** | Slider (20 to 80, default 80) in `ui/inputs.py` | Implemented, but needs validation ensuring `end_age > current_age` and capping at 80. |
| **Page 1: Optional Monthly Lifestyle Budget** | Not present | Add numeric input: "Optional monthly lifestyle / intervention budget (RM)". |
| **Page 2: Scenario A vs Scenario B** | Not implemented | Build calculation comparing cumulative trajectory A (inaction) vs trajectory B (early action + intervention budget). |
| **Page 2: Cumulative Comparison Chart** | Line chart in `ui/charts.py` supports single series | Extend Plotly chart to show both Scenario A and Scenario B lines on the same axes. |
| **Page 2: Budget-Respecting Recommendation** | Not implemented | Add recommendation logic comparing user budget against evidence-backed lifestyle programs (e.g. dietitian sessions in D1/D2). |
| **Page 2: Expandable Evidence & Uncertainty** | Generic table in `ui/summary.py` | Add collapsible expanders showing data sources, assumptions, and limitations. |

---

## 5. Google Stitch UI Integration Strategy

You indicated that a Google Stitch UI design has been designed or is intended, but **has not yet been imported or inspected**.

### 5.1 Our Approach
- **Zero Guesswork:** We have not created or assumed any layout, CSS class names, or components from Stitch.
- **Architectural Preservation:** The pure calculation engine in `calculator/` is 100% independent of UI libraries. This guarantees that whether Stitch exports HTML/CSS, React, or standard web components:
  1. If Stitch generates **HTML/CSS/JS**: We can wrap or render it via Streamlit components (`st.components.v1.html`) or convert the styles into Streamlit-compatible CSS.
  2. If Stitch generates **design mockups/tokens**: We can implement the color palette, typography, and card layouts directly in Streamlit using custom CSS injection (`st.markdown('<style>...</style>')`).
  3. The core math, data loading, and projection logic will remain intact and directly reusable.

---

## 6. Testing & Environment Status

### 6.1 Environment Findings
- **Git:** The `git` command was not recognized in PowerShell. Uncommitted changes are safe, and all file operations will be strictly non-destructive.
- **Python Runtime:** Executing `python` returned:
  > *"Python was not found; run without arguments to install from the Microsoft Store..."*  
  The Microsoft Store stub exists, but a working Python installation or active virtual environment is not configured in the active PATH.

### 6.2 Unit Test Execution Status
- **Actual Status:** **Tests were NOT executed** due to the absence of a functional Python runtime in the environment PATH.
- **Inspected Test Code:**
  - `tests/test_bmi.py` (11 tests): Correctly validates formulas, boundary classifications, zero/negative exceptions.
  - `tests/test_inflation.py` (13 tests): Correctly validates compound formulas, year sequencing, zero rate handling.
  - `tests/test_food.py` (1 active, 2 skipped): 1 placeholder test checks normal weight returns `0.0`.
  - **Missing Tests:** No tests exist for data loading, sector-specific inflation, transport, clothing, healthcare, or Scenario A vs B comparison.

---

## 7. Prioritised Implementation Plan

```
Stage 1: Environment & Paediatric Foundation (Immediate)
├── 1.1 Verify/configure Python environment so pytest can run
├── 1.2 Add WHO BMI-for-age reference dataset (clean CSV)
└── 1.3 Complete paediatric classification in `calculator/bmi.py`

Stage 2: Centralized Data Loader & Cleaning
├── 2.1 Create `calculator/data_loader.py` with UTF-8-BOM handling
├── 2.2 Clean non-numeric symbols ("20+", "+") in `bmi_meal_spending.csv`
└── 2.3 Connect substantive datasets (D1, D4, D6, D7, D8)

Stage 3: Financial Engine & Scenario Comparison
├── 3.1 Implement sector-specific inflation compounding (using D4)
├── 3.2 Implement annual cost modules (Food, Clothing, Transport, Healthcare)
├── 3.3 Build Scenario A (Waiting) vs Scenario B (Acting Early + Budget) engine
└── 3.4 Expand unit test coverage to 100% across all calculation modules

Stage 4: Two-Page Workflow & UI Wiring
├── 4.1 Page 1: Inputs with validation, DOB/age, and optional monthly budget
├── 4.2 Page 2: Comparative report, dual-line cumulative chart, and recommendation
└── 4.3 Prepare design integration hooks for the future Google Stitch UI
```

---

## 8. Decisions & Information Requested From You

1. **Python Environment:** Can you confirm if you have a specific Python installation or virtual environment on your computer that we should point to?
2. **`bmi_meal_spending.csv` Source:** Do you have notes or a link on where this table was collected from, so we can document its official citation?
3. **WHO Growth Reference:** May we download and place the standard WHO 2007 BMI-for-age lookup table (`data/who_bmi_for_age_reference.csv`) into the project?
4. **Google Stitch UI Assets:** Whenever you are ready, you can share the Stitch screenshots, exported HTML/CSS, or design specifications.

---

*Report prepared autonomously by Antigravity. No raw data files or code files have been modified or deleted.*


