# A Global Benchmark Dataset of Digital-Nomad Policy Adoption, Tourism Flows, and Labor-Market Indicators for Cross-Country Mobility Research

<p align="center">
  <strong>Trustworthy AI-assisted policy curation and a human-verified benchmark for digital nomad visa research</strong><br>
</p>

<p align="center">
  <img alt="Trustworthy AI" src="https://img.shields.io/badge/Trustworthy%20AI-Human--Verified-4F6BED">
  <img alt="Policy Benchmark" src="https://img.shields.io/badge/Policy%20Benchmark-32%20Verified%20Jurisdictions-0B7A75">
  <img alt="Coverage" src="https://img.shields.io/badge/Macroeconomic%20Panel-190%20Countries-536DFE">
  <img alt="Research" src="https://img.shields.io/badge/Policy-Digital%20Nomad%20Visas-7A4FB3">
  <img alt="Methods" src="https://img.shields.io/badge/Methods-TWFE%20%7C%20DML-B35C00">
</p>

**A Global Benchmark Dataset of Digital-Nomad Policy Adoption, Tourism Flows, and Labor-Market Indicators for Cross-Country Mobility Research** is an open research benchmark for evaluating **AI-assisted policy extraction** through complete human verification and downstream empirical validation. The project combines a global macroeconomic panel covering approximately **190 countries** with a **human-verified benchmark of 32 digital nomad visa programmes**, allowing researchers to evaluate the reliability of large language model (LLM) policy extraction and assess how policy curation errors affect downstream econometric analysis.

Unlike conventional policy datasets, every verified policy record has been independently validated against official government websites and primary legal sources. The benchmark is intended to support reproducible research in trustworthy AI, policy analytics, and computational social science.

---

# Release Snapshot

| Component | Current Release |
|------------|-----------------|
| Verified policy benchmark | 32 adopter jurisdictions |
| Non-adopter reference set | 11 jurisdictions |
| Macroeconomic panel | 190 countries |
| Time coverage | Annual country panel, 2008–2024 |
| Policy variables | Adoption year, visa duration, income requirement, visa fees, tax treatment |
| Verification | Human-verified against official sources |
| Downstream evaluation | TWFE and Doubly Robust DML |
| Primary contribution | Trustworthy AI-assisted policy curation |
| Application domain | Digital nomad visa policy |

---

# Why This Benchmark Exists

Digital Nomad Research is designed around three complementary research objectives.

- **Trustworthy AI:** Evaluate the reliability of LLM-assisted policy extraction through complete human verification.
- **Benchmark Construction:** Provide a transparent, reproducible benchmark for digital nomad visa policies.
- **Downstream Evaluation:** Measure whether observed policy extraction errors materially influence empirical policy conclusions.

Rather than proposing a new causal inference method, the repository evaluates how AI-generated policy datasets affect downstream statistical analyses.

---

# Repository Structure

```text
Digital-Nomad-Research/
│
├── visualizations/
│   ├── custom.geo-2.json         # Custom geography file for map visualizations
│   ├── differenceindifference.py # Difference-in-differences visualization
│   └── map.py                    # Choropleth / geographic visualization
│
├── DigitalNomadDataset.xlsx       # Core dataset (3 sheets, see Dataset Overview)
├── sample_loader.py               # Loads and merges macroeconomic + policy data
├── naive_baseline.py              # Naive (unverified) policy baseline estimation
├── MissingnessAudit.py            # Missing-data audit across panel variables
├── CrossValidation.py             # Cross-validation of AI-extracted vs. verified policy data
├── twfe_dml.py                    # TWFE and Doubly Robust DML estimation
│
├── LICENSE
└── README.md
```

---

# Main Repository Components

| File / Folder | Description |
|------------|-------------|
| `DigitalNomadDataset.xlsx` | Core dataset: macroeconomic panel, verified policy benchmark, and non-adopter reference set |
| `sample_loader.py` | Loads and merges the macroeconomic panel with the verified policy benchmark |
| `naive_baseline.py` | Constructs a naive baseline using unverified, AI-extracted policy data |
| `MissingnessAudit.py` | Audits missingness patterns across macroeconomic and policy variables |
| `CrossValidation.py` | Cross-validates AI-extracted policy records against the human-verified benchmark |
| `twfe_dml.py` | Runs Two-Way Fixed Effects (TWFE) and Doubly Robust DML estimation |
| `visualizations/map.py` | Produces geographic/choropleth visualizations of policy adoption |
| `visualizations/differenceindifference.py` | Produces difference-in-differences event-study figures |
| `visualizations/custom.geo-2.json` | Custom geography file used by the mapping script |

---

# Dataset Overview

`DigitalNomadDataset.xlsx` contains three sheets that together form the benchmark.

## `tourism_and_macroeconomic_data`

A harmonized annual country panel covering **190 countries** from **2008–2024**, with columns:

- `country_name`, `iso3`, `year`
- `gdp`
- `unemployment_rate`
- `expenditures` (tourism expenditure)
- `tourism_gdp_share`
- `tourism_employment`
- `arrivals_business`, `arrivals_total`
- `internet_usage_pct`
- `inflation_annual_pct`
- `exchange_rate_lcu_per_usd`
- `price_level_index_gdp`

Coverage is unbalanced: not every country reports every variable in every year, which is why `MissingnessAudit.py` exists.

## `policy_data` — Verified Digital Nomad Policy Benchmark

A human-verified benchmark covering **32 adopter jurisdictions**, with columns:

- `iso3`, `country_name`
- `visa_adoption_year`
- `coarse_tax_treatment`
- `min_income_to_apply_per_month`
- `visa_duration_months`
- `min_visa_fee`

Every policy record has been independently verified against primary legal documents or official government sources.

## `non_adopters` — Non-Adopter Reference Set

A reference set of **11 jurisdictions** without a formal, standalone digital nomad visa, with columns:

- `iso3`, `country_name`
- `primary_remote_work_visa`
- `supplementary_alternative_visas`
- `opc_corporate_setup_policy` (own-personal-company / corporate-setup workaround policy)
- `digital_nomad_community_policies`

This sheet supports comparison and robustness checks (e.g. treated-vs-control framing) alongside the 32 verified adopters.

---

# Research Workflow

```text
Official Government Sources
            │
            ▼
LLM-Assisted Policy Extraction
            │
            ▼
Independent Human Verification
            │
            ▼
Verified Policy Benchmark
            │
            ▼
Merged Macroeconomic Panel
            │
            ▼
Econometric Evaluation
(TWFE & Doubly Robust DML)
            │
            ▼
Comparison of Raw vs. Verified Policy Data
```

---

# Reproducing the Paper

Load and merge the macroeconomic panel with the policy benchmark.

```bash
python sample_loader.py
```

Construct the naive (unverified) policy baseline.

```bash
python naive_baseline.py
```

Audit missingness across the merged panel.

```bash
python MissingnessAudit.py
```

Cross-validate AI-extracted policy data against the verified benchmark.

```bash
python CrossValidation.py
```

Estimate the TWFE and Doubly Robust DML models.

```bash
python twfe_dml.py
```

Generate the difference-in-differences figures.

```bash
python visualizations/differenceindifference.py
```

Generate the geographic policy-adoption map.

```bash
python visualizations/map.py
```

---

# Methodological Scope

This repository evaluates whether AI-assisted policy extraction can support empirical policy research through transparent human verification.

The econometric analyses are intended to assess the robustness of downstream inference to policy curation errors. They should not be interpreted as definitive estimates of the causal effects of digital nomad visa adoption.

---

# Current Limitations

- The verified benchmark currently includes **32 jurisdictions**.
- Policy coding requires harmonization across heterogeneous legal systems.
- Some policy variables require interpretative coding despite independent verification.
- The empirical analyses remain observational.
- Findings are specific to digital nomad visa policies and should not be generalized to other policy domains without additional validation.

---

# License

The repository code, documentation, and analysis scripts are released under the **MIT License**.

The benchmark dataset is released for academic research and reproducibility. Users should consult the terms of use of the original government data sources when redistributing derived policy information.
