# DATA AUDIT & HANDOVER REPORT
## The Cost of Waiting — Malaysian Childhood Obesity Lifetime Cost Calculator

**Prepared:** 2026-10-10  
**Auditor:** Kiro (pre-handover to Antigravity)  
**Scope:** Full inspection of all project files, CSV datasets, calculation code, and tests.  
**Files changed by this audit:** None. All original files are untouched.

---

## 1. Project Structure Reviewed

```
Cost of Waiting/
├── app.py                          ← Streamlit landing page (under development stub)
├── requirements.txt                ← streamlit≥1.35, pandas≥2.2, numpy≥1.26, plotly≥5.22
├── README.md                       ← Setup and overview documentation
├── .gitignore                      ← Standard Python/Streamlit exclusions
├── DATA_AUDIT_HANDOVER.md          ← This file (created by audit)
│
├── calculator/                     ← Pure Python calculation engine (no Streamlit imports)
│   ├── __init__.py
│   ├── bmi.py                      ← IMPLEMENTED: adult BMI calc + classification
│   ├── inflation.py                ← IMPLEMENTED: compound inflation, year-by-year projection
│   ├── food.py                     ← SKELETON: data loader stub + zero-returning placeholder
│   ├── clothing.py                 ← SKELETON: data loader stub + zero-returning placeholder
│   ├── transport.py                ← SKELETON: data loader stub + zero-returning placeholder
│   └── healthcare.py               ← SKELETON: data loader stub + zero-returning placeholder
│
├── ui/
│   ├── __init__.py
│   ├── inputs.py                   ← Widget stubs (not yet wired to calculator)
│   ├── charts.py                   ← Three Plotly chart builders (line, bar, waterfall)
│   └── summary.py                  ← Results layout (placeholder mode when results=None)
│
├── tests/
│   ├── test_bmi.py                 ← 11 tests (see §11)
│   ├── test_inflation.py           ← 13 tests (see §11)
│   └── test_food.py                ← 1 live test + 2 skipped (see §11)
│
└── data/                           ← 13 CSV files (see §2 for full inventory)
```

**Python installation status:** Python is not yet installed on this machine. The Microsoft Store stub is present but non-functional. Tests have NOT been executed. See §11.

---

## 2. Complete CSV Inventory

### 2.1 Template files (no data rows)

| # | Filename | Lines | Purpose | Status |
|---|---|---|---|---|
| T1 | `food_prices_malaysia.csv` | 1 header + 15 comment lines | Food price reference for caloric cost model | BLOCKED — empty |
| T2 | `clothing_prices.csv` | 1 header + 14 comment lines | Clothing price reference (old schema) | SUPERSEDED — empty |
| T3 | `transport_costs.csv` | 1 header + 14 comment lines | Transport cost reference (old schema) | SUPERSEDED — empty |
| T4 | `healthcare_costs.csv` | 1 header + 21 comment lines | Healthcare cost reference (old schema) | SUPERSEDED — empty |
| T5 | `inflation_rates.csv` | 1 header + 19 comment lines | Simple inflation reference (old schema) | SUPERSEDED — empty |

**Action required:** T2–T5 are superseded by richer datasets (see §2.2). T1 (`food_prices_malaysia.csv`) is the only critical missing dataset. The old template files should be retained to preserve schema documentation but must not be passed to calculation functions as if they contained data.

---

### 2.2 Substantive datasets

#### D1 — `malaysia_obesity_cost_person_year.csv`

| Property | Value |
|---|---|
| **File size** | 4,864.8 KB |
| **Rows (data)** | 18,000 |
| **Columns** | 44 |
| **Encoding** | UTF-8 (no BOM) |

**Column names:**
`person_id, year, age, age_group, sex, region, area_type, healthcare_sector_payer, household_income_group, employment_status, smoker, weight_status, bmi_kg_m2, treatment_pathway` + 17 binary comorbidity flags (`type2_diabetes, prediabetes, hypertension, dyslipidemia, nafld, sleep_apnea, cvd, osteoarthritis, ckd, gerd, depression_anxiety, asthma, pcos, cancer_obesity_related, gout, vit_d_deficiency, orthopedic_child`) + `n_comorbidities, days_lost` + 8 cost columns: `medication_cost_myr, clinic_visit_cost_myr, treatment_program_cost_myr, lab_diagnostic_device_cost_myr, surgery_cost_myr, hospital_er_cost_myr, complication_care_cost_myr, total_direct_cost_myr, out_of_pocket_cost_myr, indirect_cost_myr, total_cost_myr` + `fx_rate_myr_per_usd, total_cost_usd_equiv`

**Key facts (sampled from first 200 rows, confirmed against full file header):**
- **Weight status values:** Obesity Class 1, Obesity Class 2, Obesity Class 3, Overweight (control), Normal weight (control)
- **Years:** 2024, 2025, 2026 only
- **Age range:** 5–85 (sampled)
- **Sex:** Male, Female
- **Payer types:** Public (MOH), Private - insured (medical card/takaful), Private - self-pay
- **Structure:** ~6,000 unique persons × 3 years = 18,000 rows
- **Missing values:** None observed in cost or key demographic columns in sampled rows
- **Exact duplicates:** None observed

**Units:** All costs in Malaysian Ringgit (MYR). `fx_rate_myr_per_usd` = 4.08 throughout (fixed exchange rate assumption).

**Date/geographic coverage:** 2024–2026 reference period. 6 Malaysian regions: Central (KL/Selangor/Putrajaya), Northern (Penang/Kedah/Perak/Perlis), Southern (Johor/Melaka/N.Sembilan), East Coast (Kelantan/Terengganu/Pahang), Sabah/Labuan, Sarawak.

**Source provenance:** Not documented within the file. No source URL, publication date, or methodology note present in the data itself. The file appears to be a synthetic/modelled cohort.

**Data quality flags:**
- Some individuals change `weight_status` between years (e.g. a person classified as Obesity Class 2 in 2024 appears as Obesity Class 1 in 2025). This is consistent with a synthetic cohort but would be unusual in a real longitudinal clinical dataset.
- `fx_rate_myr_per_usd = 4.08` is fixed across all rows and years. This is an assumption, not a live exchange rate.
- `total_cost_usd_equiv` is a mechanical conversion; it adds no independent information.

**Fitness for purpose:** PASS WITH LIMITATIONS — usable for computing mean annual costs by weight status group, but the synthetic origin must be prominently disclosed. Do not present outputs as measured patient costs. Projecting 2024–2026 unit costs forward to age 80 requires explicit inflation adjustment.

---

#### D2 — `malaysia_obesity_cost_line_items.csv`

| Property | Value |
|---|---|
| **File size** | 21,968.5 KB (~22 MB) |
| **Rows (data)** | 130,345 |
| **Columns** | 14 |
| **Encoding** | UTF-8 (no BOM) |

**Column names:** `person_id, year, age, age_group, healthcare_sector_payer, region, weight_status, cost_category, item, care_setting, unit_cost_myr, units_per_year, total_cost_myr, patient_out_of_pocket_myr`

**Purpose:** Line-item cost breakdown behind D1. One row per cost item per person per year. Provides the itemised evidence for the evidence/drill-down panel.

**Key facts:**
- Cost categories observed: `Clinic visit, Treatment program, Lab / diagnostic, Medication, Hospital / ER, Device, Indirect cost`
- Care settings: Outpatient, Lab, Pharmacy, DME, Emergency, Sleep lab, Imaging, Non-medical
- Rows with `units_per_year = 0` produce `total_cost_myr = 0` — intentional (represents eligibility without utilisation in that year, e.g. zero work-days lost), not a data error.
- `patient_out_of_pocket_myr` is consistently a fixed fraction of `total_cost_myr` per payer type — consistent with a modelled cost-sharing assumption, not individually measured.

**Source provenance:** Not documented. Linked to D1 via `person_id`.

**Fitness for purpose:** PASS WITH LIMITATIONS — useful for the evidence panel and category breakdowns. Not required for the primary Scenario A vs B calculation. Same synthetic-origin caveat as D1.

---

#### D3 — `malaysia_obesity_healthcare_costs.csv`

| Property | Value |
|---|---|
| **File size** | 18.8 KB |
| **Rows (data)** | 53 |
| **Columns** | 15 |
| **Encoding** | UTF-8 with BOM (use `encoding="utf-8-sig"` on load) |

**Column names:** `bmi_group, bmi_range_kg_m2, setting, cost_component, perspective, scenario_and_assumptions, unit, unit_cost_low_RM, unit_cost_high_RM, units_per_year, annual_cost_low_RM, annual_cost_high_RM, ratio_vs_nonobese_midpoint, evidence_basis, source_urls`

**Purpose:** Summary cost-range table by BMI class × care setting × cost component. Provides ranges (low/high) rather than point estimates.

**Key facts:**
- BMI groups: Non-obese (18.5–24.9), Obese class I (30.0–34.9), Obese class II (35.0–39.9), Obese class III (≥40.0)
- Settings: Private, Public (MOH), Both (out-of-pocket)
- Cost components: Consultation, Medication (anti-obesity drugs, chronic comorbidity), Admission (ward charge), Surgery (bariatric), TOTALs (A and B scenarios)
- Cross-check row: "Overall medical expenses ratio" — IPH finding of 2.5× for obese vs healthy weight (secondary source; underlying study not located)

**Data quality flags:**
- **Explicit ASSUMED flags:** Multiple rows in `scenario_and_assumptions` and `evidence_basis` state "ASSUMED" or "Visit counts ASSUMED". These must not be presented as evidence-based.
- **Explicit DATA GAP:** Private sector chronic medication costs have no price source. Three rows explicitly say "DATA GAP".
- **GLP-1 anti-obesity medications:** RM 800–1,800/month. Wide range; flagged as optional/patient-funded. No class-specific dosing cited.
- **Bariatric surgery:** Two conflicting price ranges from different sources: RM 15,000–35,000 (news article, 2020) and RM 25,000–50,000 (commercial site, undated). Low reliability.
- **`ratio_vs_nonobese_midpoint`:** Some cells contain strings like "1.0 (baseline)" — column is mixed string/numeric.
- **`unit_cost_low_RM`** and **`unit_cost_high_RM`:** Three DATA GAP rows have blank numeric cells — confirmed missing values.

**Source provenance:** Source URLs documented within the file. Includes Malaysian Medical Association fee guide, MOH Sarawak charges, CodeBlue article, PubMed, ScienceDirect, and JMDH. Not all URLs were independently verified during this audit. The IPH 2.5× figure is cited as secondary; the original study was not located.

**Fitness for purpose:** NEEDS CLEANING — useful as a supplementary evidence/cross-check table, but multiple ASSUMED rows and DATA GAPs prevent it from being the primary cost source. Requires explicit flagging of assumed vs. sourced values before display. Do not use the TOTAL rows for calculation without first confirming their derivation is correct (they are self-described as "Derived (sum of rows above)").

---

#### D4 — `Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv`

| Property | Value |
|---|---|
| **File size** | 820 KB |
| **Rows (data)** | 1,144 |
| **Columns** | 21 |
| **Encoding** | UTF-8 (no BOM) |

**Column names:** `country, sector, subcategory, year, data_type, scenario, cpi_index, annual_inflation_rate_percent, cumulative_price_change_percent, estimated_price_multiplier, source_organisation, source_title, source_url, publication_date, retrieval_date, unit, cpi_base_year, methodology, verification_status, projection_assumptions, notes`

**Sectors present:** Food & Non-Alcoholic Beverages | Clothing & Footwear | Transportation | Health (Medicines & Healthcare-Related Products)

**Year range:** 1980–2105 (historical: 1980–2025; modelled projection: 2026–2105)

**Data types:** `historical`, `modelled_projection`

**Key facts:**
- Source: DOSM (Department of Statistics Malaysia), officially published CPI series (Laspeyres, base year 2010=100)
- Verification status column present — confirmed "Officially published" for historical rows
- `annual_inflation_rate_percent` is blank for the first year of each sector series (1980), since YoY requires a prior-year baseline. This is expected and documented in the `notes` column.
- Projections extend to 2105 — an 80-year horizon covering childhood-to-age-80 projections.

**Data quality flags:**
- The first-row blank in `annual_inflation_rate_percent` per sector must be handled on load (skip or use next year's value).
- Projection years (2026–2105) are modelled estimates, not observed data. The `projection_assumptions` column documents the methodology.
- All four sectors needed by the application are present: food inflation ✓, clothing inflation ✓, health inflation ✓, transport inflation ✓.

**Source provenance:** Fully documented. Source URL: `https://storage.dosm.gov.my/cpi/cpi_2d_annual.csv`. Retrieval date: 2026-10-10. Organisation: DOSM.

**Fitness for purpose:** PASS — this is the best-quality dataset in the project. Sector-specific rates are directly applicable to each cost category. Projections must be disclosed as modelled, not historical.

---

#### D5 — `malaysia_transport_costs_obese_vs_non_obese.csv`

| Property | Value |
|---|---|
| **File size** | 1.1 KB |
| **Rows (data)** | 8 (including TOTAL row) |
| **Columns** | 8 |
| **Encoding** | UTF-8 with BOM |

**Column names:** `Category, Item, Non_Obese_MYR_per_Month, Obese_MYR_per_Month, Difference_MYR_per_Month, Non_Obese_MYR_per_Year, Obese_MYR_per_Year, Assumption_Notes`

**Key finding:** TOTAL row: obese annual = MYR 9,180; non-obese annual = MYR 4,800; difference = MYR 4,380.

**Coverage:** Adults only (driving age). No child transport costs.

**Source provenance:** No source URL or publication cited. `Assumption_Notes` column describes the rationale for each row but these are stated as assumptions, not measured survey values.

**Fitness for purpose:** PASS WITH LIMITATIONS — usable as a reasonable illustrative estimate for adults. Must be disclosed as assumption-based, not survey-measured. Superseded for child transport by D6.

---

#### D6 — `malaysia_transport_costs_adult_obese_nonobese_child.csv`

| Property | Value |
|---|---|
| **File size** | 1.6 KB |
| **Rows (data)** | 9 (including TOTAL row) |
| **Columns** | 9 |
| **Encoding** | UTF-8 with BOM |

**Column names:** `Category, Item, Adult_Non_Obese_MYR_per_Month, Adult_Obese_MYR_per_Month, Child_MYR_per_Month, Adult_Obese_minus_Non_Obese_MYR_per_Month, Adult_Non_Obese_MYR_per_Year, Adult_Obese_MYR_per_Year, Child_MYR_per_Year, Assumption_Notes`

**Key finding:** TOTAL row: Adult Obese annual = MYR 9,660; Adult Non-Obese = MYR 4,920; Child = MYR 600.  
Annual adult difference = MYR 4,740 (slightly higher than D5's 4,380 — the two files use slightly different assumptions).

**Note:** D6 supersedes D5 for any use case that needs child or adult transport costs in one place. D5 should be deprecated in favour of D6, but both are retained.

**Source provenance:** Same limitation as D5 — assumption-based, no survey citation.

**Fitness for purpose:** PASS WITH LIMITATIONS — preferred over D5 because it covers children. Same disclosure requirement. The ≈MYR 360 discrepancy between D5 and D6 adult totals should be reconciled before finalising the model.

---

#### D7 — `SizeCost_Malaysia_Granular_Size_Observations.csv`

| Property | Value |
|---|---|
| **File size** | 439.8 KB |
| **Rows (data)** | 1,337 |
| **Columns** | 17 |
| **Encoding** | UTF-8 with BOM |

**Column names:** `Observation ID, Product ID, Retailer, Brand, Product Name, Category, Material, Displayed Size, Size Classification, Current Selling Price (RM), Original Price (RM), Discount Status, Availability, Date Collected, Product URL, Verification Status, Extraction Method`

**Retailers (18):** Oxwhite Malaysia, Whimsigirl Malaysia, Pestle & Mortar Clothing, Al-Ikhsan Sports Malaysia, Siti Khadijah, Uniqlo Malaysia, Padini, Zalora Malaysia, Marks & Spencer Malaysia, Cotton On Malaysia, Doublewoot Malaysia, Petit Moi Malaysia, Shein Malaysia, Poplook, Behati Malaysia, CalaQisya Malaysia, Decathlon Malaysia, and duplicate "Oxwhite" entry.

**Categories:** T-shirts and tops, Shirts, Everyday clothing, Sportswear, Dresses, Trousers and jeans

**Size Classifications (observed values):** `Standard`, `Extended / Plus` — plus contamination (see below)

**Price range:** 0–2,000 MYR

**Date collected:** 2026-10-10 (single snapshot date — no longitudinal price history)

**Data quality flags — CRITICAL:**

1. **Column shift / parsing contamination in `Size Classification`:** The profiling run detected values like `"UK M"`, `" 2% Elastane"`, `"UK 8"`, `"30"`, `"36"`, `"Default Title"` in the `Size Classification` column. The expected values are only `"Standard"` and `"Extended / Plus"`. This indicates that for some rows (likely M&S jeans with waist sizes like "30R", "32R"), the CSV columns are not aligned — either a missing quote causes a comma inside a field to be parsed as a delimiter, shifting all subsequent columns one position right. **This must be fixed before any analysis.** Rows with malformed `Size Classification` values will produce incorrect premium calculations.

2. **Exact duplicate product+size records:** 35 duplicate (Product ID + Displayed Size + Size Classification) combinations were detected. These must be deduplicated before computing mean prices.

3. **Price = 0 entries:** Some rows have a price of 0, which is not a valid retail price. These require investigation — they may represent scraping failures where the price field was not captured.

4. **"Default Title" size value:** Some rows have `Displayed Size = "Default Title"` — a scraping artefact from products that don't have size variants. These rows cannot be classified as Standard or Extended/Plus and should be excluded from premium calculations.

5. **Key finding on premium:** Based on the data visible during review, the majority of retailers (Uniqlo, Padini, Siti Khadijah) price identically across standard and plus sizes. The observed premium comes primarily from a small number of items at Zalora Curve (+MYR 14–30) and Marks & Spencer (+MYR 10). The computed annual clothing premium is likely small (estimated MYR 50–200/year for a full clothing basket) and may be near zero at many retailers. **Do not assume a large premium before computing it from clean data.**

**Source provenance:** Extraction method and product URLs documented per row. Verification status column present. Single-date snapshot (2026-10-10) — prices may change.

**Fitness for purpose:** NEEDS CLEANING — column-shift contamination for waist-size products must be resolved before use. After cleaning, usable for estimating a size premium with appropriate caveats (small sample, single date, not all clothing categories covered).

---

#### D8 — `bmi_meal_spending.csv`

| Property | Value |
|---|---|
| **File size** | 1.5 KB |
| **Rows (data)** | 40 (20 male + 20 female, ages 1–20+) |
| **Columns** | 6 |
| **Encoding** | UTF-8 (no BOM) |

**Column names:** `Sex, Age (years), Normal BMI, Obese BMI, Average annual meal spending (MYR), Obese annual meal spending (MYR)`

**Purpose:** Annual meal spending by age and sex for normal-weight vs obese individuals. This is the **food cost dataset** — the only substantive food cost data in the project.

**Key facts:**
- Age coverage: 1–19, then "20+" bucket
- Sex: Male, Female
- `Normal BMI` and `Obese BMI`: reference BMI values at the boundary of each category for each age/sex combination
- `Average annual meal spending (MYR)`: spending for a normal-weight individual. Ranges from MYR 3,600 (ages 1–6) to MYR 5,760 (age 20+).
- `Obese annual meal spending (MYR)`: spending for an obese individual. Ranges from MYR ~4,095 (male age 3) to MYR ~8,078 (female age 19). Values marked with "+" for age 20+ (e.g. "7513.04+") indicating the value continues to increase beyond this age.

**Calculated annual difference (male):**
- Age 1: MYR 4,216 − MYR 3,600 = MYR 616
- Age 10: MYR 5,742 − MYR 4,313 = MYR 1,429
- Age 18: MYR 7,487 − MYR 5,628 = MYR 1,859
- Age 20+: MYR 7,513 − MYR 5,760 = MYR 1,753

**Data quality flags:**
- **"20+" in the `Age (years)` column** is a string, not an integer. The `Obese annual meal spending (MYR)` value for age 20+ also has a "+" suffix (e.g. `7513.04+`). Both must be cleaned before numeric parsing.
- **Source provenance is not documented.** There is no source column, URL, publication date, or methodology note in the file. It is unclear whether these figures are: (a) derived from published Malaysian dietary surveys, (b) calculated from caloric intake differences applied to market food prices, or (c) modelled assumptions. **This is the most significant provenance gap in the project.**
- **`Normal BMI` and `Obese BMI` column names are misleading.** For children, BMI cut-offs are age- and sex-specific percentile-based thresholds, not fixed values. The values in these columns appear to be reference BMI values at the weight-status boundary for each age/sex group, but the reference population and methodology are undocumented.
- **The spending figures imply obese individuals spend 17–43% more on food** (varying by age and sex). This is plausible but the evidence basis needs to be established before it can be used in a decision-support tool.
- **Age 20+ is a catch-all bucket**, not a specific age. For projections to age 80, a single adult value will be applied across a 60-year span unless more granular adult data is obtained.

**Fitness for purpose:** SOURCE VERIFICATION REQUIRED — the data appears complete and plausible, and directly unblocks the food cost calculation. However, the absence of any source citation makes it unsuitable for use in a tool presented to users without first establishing its provenance. If the source is a published Malaysian dietary study or a calculation from DOSM food expenditure data, documenting it transforms this from "unknown" to "usable."

---

## 3. Data-Quality Findings and Severity

| Severity | Finding | Affected File(s) |
|---|---|---|
| 🔴 Critical | `Size Classification` column contamination — column shift for waist-size products | D7 |
| 🔴 Critical | `bmi_meal_spending.csv` has no source, URL, methodology, or date — provenance unknown | D8 |
| 🟠 High | "20+" string in age column and "7513.04+" in spending column require pre-processing | D8 |
| 🟠 High | D5 and D6 adult transport totals disagree by MYR 360/year — two inconsistent assumption sets | D5, D6 |
| 🟠 High | `food_prices_malaysia.csv` is empty — the template schema requires food item–level data | T1 |
| 🟠 High | D3 contains explicit ASSUMED rows and DATA GAP cells — mixing sourced and invented values | D3 |
| 🟡 Medium | 35 duplicate product+size records in SizeCost require deduplication before analysis | D7 |
| 🟡 Medium | Price = 0 entries in SizeCost require investigation — likely scraping failures | D7 |
| 🟡 Medium | `bmi_meal_spending.csv` age 20+ is a coarse bucket — insufficient for age-graded lifetime projections | D8 |
| 🟡 Medium | D1 weight_status changes between years for some persons — synthetic artefact, not biological change | D1 |
| 🟡 Medium | `fx_rate_myr_per_usd = 4.08` fixed across all rows — stated assumption, not live rate | D1, D2 |
| 🟡 Medium | D4 projections extend to 2105 — 80-year modelled projection requires disclosure | D4 |
| 🟢 Low | `annual_inflation_rate_percent` blank for first year of each sector (1980) — expected, documented | D4 |
| 🟢 Low | `ratio_vs_nonobese_midpoint` in D3 is mixed string/numeric (e.g. "1.0 (baseline)") | D3 |
| 🟢 Low | "Default Title" appears as a size value in D7 — scraping artefact, needs exclusion | D7 |
| 🟢 Low | Five original template CSVs are superseded but retained — no action needed | T1–T5 |

---

## 4. Dataset Fitness-for-Purpose Assessment

| ID | Filename | Assessment | Rationale |
|---|---|---|---|
| D1 | `malaysia_obesity_cost_person_year.csv` | **PASS WITH LIMITATIONS** | Rich, usable for mean cost by weight status. Synthetic origin must be disclosed. |
| D2 | `malaysia_obesity_cost_line_items.csv` | **PASS WITH LIMITATIONS** | Useful for evidence panel. Synthetic origin. Not required for primary calculation. |
| D3 | `malaysia_obesity_healthcare_costs.csv` | **NEEDS CLEANING** | Multiple ASSUMED rows and DATA GAPs. Requires flagging before display. |
| D4 | `Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv` | **PASS** | Best-quality dataset. DOSM official source, fully documented, all four needed sectors present. |
| D5 | `malaysia_transport_costs_obese_vs_non_obese.csv` | **PASS WITH LIMITATIONS** | Adults only. Assumption-based. Superseded by D6. |
| D6 | `malaysia_transport_costs_adult_obese_nonobese_child.csv` | **PASS WITH LIMITATIONS** | Preferred over D5. Covers children. Assumption-based. Discrepancy with D5 needs reconciliation. |
| D7 | `SizeCost_Malaysia_Granular_Size_Observations.csv` | **NEEDS CLEANING** | Column-shift contamination must be resolved. After cleaning, usable with caveats. |
| D8 | `bmi_meal_spending.csv` | **SOURCE VERIFICATION REQUIRED** | Data appears complete and usable but has no documented source. Provenance must be established before publication. |
| T1 | `food_prices_malaysia.csv` | **BLOCKED** | Empty. No data. |
| T2–T5 | Template CSVs | **BLOCKED** | Empty. Superseded. Retain for schema reference only. |

---

## 5. Data Dependencies for Each Application Feature

| Feature | Required Datasets | Currently Available? | Blocker |
|---|---|---|---|
| Adult BMI calculation | None (formula only) | ✅ Yes | — |
| Child BMI classification (percentile) | WHO/CDC growth reference table (not in project) | ❌ No | Missing reference table |
| Food cost estimation | D8 (+ source verification) | ⚠️ Partial | Provenance undocumented |
| Clothing cost estimation | D7 (after cleaning) | ⚠️ Partial | Column-shift contamination |
| Transport cost estimation — adults | D6 | ✅ Yes | Disclose assumption basis |
| Transport cost estimation — children | D6 (child column) | ✅ Yes | Disclose assumption basis |
| Healthcare cost estimation (mean) | D1 | ✅ Yes | Disclose synthetic origin |
| Healthcare cost estimation (range) | D3 | ⚠️ Partial | Flag ASSUMED rows |
| Inflation adjustment (sector-specific) | D4 | ✅ Yes | — |
| Inflation adjustment (simple fallback) | Built into inflation.py | ✅ Yes | — |
| Scenario A: Cost of Waiting (projection) | D1, D6, D7 (clean), D8 (sourced), D4 | ⚠️ Partial | Food provenance; clothing cleaning |
| Scenario B: Cost of Acting Early | Same as Scenario A | ⚠️ Partial | Same blockers |
| Uncertainty ranges / sensitivity | D3 (low/high), D4 (sector rates) | ⚠️ Partial | D3 ASSUMED rows limit reliability |
| Budget-aware recommendations | Not yet designed | ❌ No | Feature not yet scoped |
| Paediatric BMI interpretation | WHO/CDC reference table | ❌ No | Missing dataset |

**Important distinction — descriptive vs causal claims:**
The datasets in this project describe *current observed costs* associated with obesity status. They do **not** constitute evidence that early intervention *causes* cost reduction, prevents specific diseases, or guarantees weight normalisation. Scenario B ("Cost of Acting Early") should be framed as: "estimated costs if obesity is resolved by age X" — not as "savings guaranteed by intervention." No dataset in this project supports a causal effectiveness claim.

---

## 6. Unverified Sources and Missing Documentation

| Dataset | Missing Information |
|---|---|
| D8 `bmi_meal_spending.csv` | Source, URL, methodology, date, reference population — **all absent** |
| D1 `malaysia_obesity_cost_person_year.csv` | No source note in file; synthetic vs real cohort not stated in data |
| D2 `malaysia_obesity_cost_line_items.csv` | Same as D1 |
| D3 `malaysia_obesity_healthcare_costs.csv` | IPH 2.5× ratio: secondary citation, original study not located |
| D5/D6 transport CSVs | No survey source; assumption-based |
| D7 SizeCost | Single-date snapshot; no longitudinal pricing; Shein/Doublewoot prices may not be representative |

**Action before Antigravity handover:**
1. For D8: identify the author/source. If it was generated from a calculation, document the inputs (e.g. "derived from MOH Malaysia dietary guidelines × DOSM household food expenditure survey, accessed [date]").
2. For D1/D2: add a provenance note (e.g. "synthetic cohort generated using [tool/model] based on [reference population] parameters").
3. For D3: locate the underlying IPH study for the 2.5× ratio.

---

## 7. Calculations Safe to Implement Now

The following can be implemented without additional data or source resolution:

1. **Adult BMI calculation** (`calculate_bmi`) — already implemented and tested.
2. **Adult BMI classification** (`classify_bmi_adult`, `is_obese_adult`) — already implemented and tested.
3. **Compound inflation (fixed rate)** (`apply_compound_inflation`, `project_costs_over_years`) — already implemented and tested.
4. **Sector-specific inflation adjustment** using D4 — data is complete, DOSM-sourced. Implement `get_sector_rate()` in `inflation.py`.
5. **Healthcare mean annual cost by weight status** using D1 — compute mean `total_direct_cost_myr` grouped by `weight_status`, with optional filter by `age_group`, `sex`, `payer`. Disclose synthetic origin and n_observations.
6. **Transport annual difference (adults)** using D6 TOTAL row — MYR 4,740 adult obese − non-obese difference. Disclose assumption basis.
7. **Transport cost for children** using D6 child column — MYR 600/year. Disclose assumption basis.
8. **Lifetime cost projection** for healthcare + transport categories — uses D1 + D6 + D4, with clear labelling that food and clothing are pending.

---

## 8. Calculations That Must Remain Blocked

| Calculation | Reason | What Would Unblock It |
|---|---|---|
| **Food cost (full)** | `food_prices_malaysia.csv` is empty | Populate T1 with food item prices |
| **Food cost (alternative)** | D8 `bmi_meal_spending.csv` has no documented source | Establish and document D8 provenance |
| **Clothing size premium** | D7 has column-shift contamination | Fix CSV parsing for waist-size products |
| **Paediatric BMI classification** | WHO/CDC growth reference table absent | Add `data/who_bmi_for_age_reference.csv` |
| **Healthcare cost ranges** | D3 has ASSUMED/DATA GAP rows | Flag rows in UI; only present sourced rows as evidence |
| **Causal savings claims** | No intervention effectiveness data exists in the project | Would require a separate evidence base (RCT, intervention study) |

---

## 9. Prioritised List of Missing Datasets and Evidence

Ordered by impact on completeness:

1. **🔴 `bmi_meal_spending.csv` source documentation** — establishes food cost calculation. Zero development effort; pure documentation task. Highest priority.

2. **🔴 Fix `SizeCost_Malaysia_Granular_Size_Observations.csv` column-shift contamination** — required before any clothing premium calculation. Data cleaning task, not a new dataset.

3. **🟠 Reconcile D5 vs D6 transport totals** — adult difference of MYR 4,380 (D5) vs MYR 4,740 (D6). Choose one canonical source and remove the other from active use.

4. **🟠 WHO/CDC BMI-for-age growth reference CSV** — required for paediatric BMI classification, which is the core use case (childhood obesity). Without it, the app cannot classify children's weight status correctly. Available free from WHO: https://www.who.int/tools/child-growth-standards

5. **🟠 Adult age-graded food spending data** — D8 uses a single "20+" bucket for all adults. A table covering ages 20–80 by sex would allow accurate lifetime food cost projection.

6. **🟡 Private-sector chronic medication prices** — D3 has three DATA GAP rows for this. MOH Malaysian Pharmaceutical Price List or DUOPHARMA/KPJ published prices would fill this.

7. **🟡 Additional clothing retailers or categories** — D7 covers 6 categories across 18 retailers but the plus-size premium is near-zero at most. Verifying against specialist plus-size retailers (FashionValet Plus, Pomelo Curve) would strengthen or contradict the current finding.

8. **🟢 `food_prices_malaysia.csv` population** — if D8 provenance cannot be established, T1 provides an alternative path (item-level prices + caloric model).

---

## 10. Recommended Next Steps for Antigravity

**Before writing any new calculation code:**

1. **Establish D8 provenance.** Ask the project owner: where did `bmi_meal_spending.csv` come from? A one-sentence source note transforms it from unusable to usable.

2. **Fix D7 column-shift contamination.** The standard CSV parser in pandas will misparse rows where a field contains an unescaped comma (e.g. M&S jeans sizes "30R"). Read the file and identify which rows have `Size Classification` values other than `"Standard"` or `"Extended / Plus"`. Either fix the source CSV or implement a row-level validation filter that rejects malformed rows before analysis.

3. **Download and add the WHO BMI-for-age reference table.** This is freely available and takes minutes to add. Without it, the app cannot do its stated core function for children.

4. **Implement `calculator/data_loader.py`** as a central loading module. Each loader should: strip BOM (`encoding="utf-8-sig"`), validate required columns, raise informative errors, and never mutate the input file. See the workflow agent's brief from the previous session for a detailed specification.

5. **Implement transport and healthcare calculations** using D1 and D6 — these are ready with no blockers. Document limitations in the UI.

6. **Implement sector-specific inflation** using D4. This replaces the single-rate `project_costs_over_years` for category-appropriate projections.

7. **Implement food cost calculation only after D8 provenance is documented.** Use D8 as the primary source if sourced; fall back to the `food_prices_malaysia.csv` caloric model once that file is populated.

8. **Never present the Scenario A vs B delta as a causal "savings" figure.** The correct framing is: "estimated lifetime cost difference between an obese trajectory and a healthy-weight trajectory." The datasets support this framing. They do not support the claim that any specific intervention achieves the healthy-weight trajectory.

---

## 11. Existing Tests and Their Actual Status

**Python is not installed on this machine.** The Microsoft Store stub (`WindowsApps/python.exe`) is present but non-functional. No test run was possible during this audit.

**Tests were not executed. The following status reflects code inspection only.**

| File | Tests | Inspected Status | Notes |
|---|---|---|---|
| `tests/test_bmi.py` | 11 tests across 3 classes | Code is correct based on inspection | Tests `calculate_bmi`, `classify_bmi_adult`, `is_obese_adult`. Boundary conditions covered. Expected to pass once Python is installed. |
| `tests/test_inflation.py` | 13 tests across 2 classes | Code is correct based on inspection | Tests `apply_compound_inflation` and `project_costs_over_years`. Expected to pass. |
| `tests/test_food.py` | 1 live test + 2 skipped | Code is correct based on inspection | The live test (`test_normal_weight_returns_zero`) passes `food_prices_df=None` and expects `0.0` — valid because the function returns 0.0 unconditionally in skeleton state. The two skipped tests are correctly marked `@pytest.mark.skip`. |

**No tests exist** for: clothing, transport, healthcare, data loading, inflation sector lookup, or the new datasets. These must be written alongside any new calculator implementations.

**Action required before first test run:** Install Python ≥3.10 from https://www.python.org/downloads/ with "Add python.exe to PATH" checked, then run:
```powershell
cd "C:\Users\Matthias\OneDrive\Desktop\Cost of Waiting"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests/ -v
```

---

## 12. Files Inspected and Files Changed

**Files inspected (read-only):**

| File | How Inspected |
|---|---|
| `app.py` | Full read |
| `calculator/bmi.py` | Full read |
| `calculator/inflation.py` | Full read |
| `calculator/food.py` | Full read |
| `calculator/clothing.py` | Full read |
| `calculator/transport.py` | Full read |
| `calculator/healthcare.py` | Full read |
| `ui/inputs.py`, `charts.py`, `summary.py`, `__init__.py` | Full read (previous session) |
| `tests/test_bmi.py` | Full read |
| `tests/test_inflation.py` | Full read |
| `tests/test_food.py` | Full read |
| `requirements.txt` | Full read (previous session) |
| `README.md` | Full read (previous session) |
| `data/food_prices_malaysia.csv` | Full read — confirmed empty (template only) |
| `data/clothing_prices.csv` | Full read — confirmed empty (template only) |
| `data/transport_costs.csv` | Full read — confirmed empty (template only) |
| `data/healthcare_costs.csv` | Full read — confirmed empty (template only) |
| `data/inflation_rates.csv` | Full read — confirmed empty (template only) |
| `data/bmi_meal_spending.csv` | Full read — 40 data rows confirmed |
| `data/malaysia_transport_costs_adult_obese_nonobese_child.csv` | Full read — 9 data rows confirmed |
| `data/malaysia_transport_costs_obese_vs_non_obese.csv` | Full read — 8 data rows confirmed |
| `data/malaysia_obesity_cost_person_year.csv` | Header + 200-row sample + line count (18,000 rows) |
| `data/malaysia_obesity_cost_line_items.csv` | Header + partial read + line count (130,345 rows) |
| `data/malaysia_obesity_healthcare_costs.csv` | Full read — 53 data rows |
| `data/Malaysia_Sector_Inflation_Complete_Dataset_Historical_and_Projections.csv` | Header + sector/year profiling (1,144 rows) |
| `data/SizeCost_Malaysia_Granular_Size_Observations.csv` | Header + full profiling (1,337 rows) |

**Files created by this audit:**
- `DATA_AUDIT_HANDOVER.md` (this file)

**Files modified:** None.  
**Files deleted:** None.  
**Files renamed or moved:** None.

---

## 13. Most Important Issues to Resolve Before Transferring to Antigravity

In priority order:

1. **Install Python.** Nothing can be tested or run without it. This is a prerequisite for everything else.

2. **Document the source of `bmi_meal_spending.csv`.** One sentence — "derived from [X], published by [Y] in [year]" — transforms the food cost module from blocked to implementable. This is the single highest-leverage action.

3. **Fix the `SizeCost` column-shift contamination.** The Size Classification column has incorrect values for waist-size products. Any clothing premium computed from uncleaned data will be wrong. Either fix the source CSV or implement a strict row-validation filter.

4. **Reconcile the D5/D6 transport total discrepancy** (MYR 4,380 vs MYR 4,740 annual adult difference). Decide which file is canonical and document why.

5. **Add the WHO BMI-for-age reference table.** The application is described as a childhood obesity calculator. Without age-sex-specific BMI cut-offs for children, it cannot classify the target population correctly. An adult BMI threshold applied to a 10-year-old will produce medically incorrect results.

6. **Add the `calculator/data_loader.py` module** before Antigravity begins writing new calculation code. Central loading with validation, BOM handling, and informative errors prevents silent failures when files are missing or malformed.

7. **Write a brief scope note clarifying Scenario B.** The project currently says Scenario B is "The Cost of Acting Early." That framing implies an intervention guarantee. Before Antigravity builds the comparison, agree on the correct framing: is Scenario B (a) costs for a person who maintains healthy weight throughout life, (b) costs after a specific intervention with documented effectiveness, or (c) something else? The available datasets only support option (a).

---

*End of audit report. No files were modified, deleted, or renamed.*
