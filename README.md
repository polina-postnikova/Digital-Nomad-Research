# Digital Nomad Research

<p align="center">
  <strong>Trustworthy AI-assisted policy curation and a human-verified benchmark for digital nomad visa research</strong><br>
  Paper notation: <code>\textsc{DigitalNomad}</code>
</p>

<p align="center">
  <img alt="Trustworthy AI" src="https://img.shields.io/badge/Trustworthy%20AI-Human--Verified-4F6BED">
  <img alt="Policy Benchmark" src="https://img.shields.io/badge/Policy%20Benchmark-32%20Verified%20Jurisdictions-0B7A75">
  <img alt="Coverage" src="https://img.shields.io/badge/Macroeconomic%20Panel-190%20Countries-536DFE">
  <img alt="Research" src="https://img.shields.io/badge/Policy-Digital%20Nomad%20Visas-7A4FB3">
  <img alt="Methods" src="https://img.shields.io/badge/Methods-TWFE%20%7C%20DML-B35C00">
</p>

**Digital Nomad Research** is an open research benchmark for evaluating **AI-assisted policy extraction** through complete human verification and downstream empirical validation. The project combines a global macroeconomic panel covering approximately **190 countries** with a **human-verified benchmark of 32 digital nomad visa programmes**, allowing researchers to evaluate the reliability of large language model (LLM) policy extraction and assess how policy curation errors affect downstream econometric analysis.

Unlike conventional policy datasets, every verified policy record has been independently validated against official government websites and primary legal sources. The benchmark is intended to support reproducible research in trustworthy AI, policy analytics, and computational social science.

---

# Release Snapshot

| Component | Current Release |
|------------|-----------------|
| Verified policy benchmark | 32 jurisdictions |
| Macroeconomic panel | ~190 countries |
| Time coverage | Annual country panel |
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
├── data/
│   ├── raw/
│   ├── processed/
│   ├── policy_validation/
│   └── documentation/
│
├── scripts/
│   ├── preprocessing/
│   ├── validation/
│   ├── estimation/
│   └── visualization/
│
├── analysis/
│   ├── figures/
│   ├── tables/
│   ├── robustness/
│   └── notebooks/
│
├── paper/
│   ├── manuscript/
│   ├── supplementary_material/
│   └── bibliography/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── model_outputs/
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Main Repository Components

| Component | Description |
|------------|-------------|
| Global macroeconomic panel | Country-level macroeconomic indicators |
| Verified policy benchmark | Human-validated digital nomad visa dataset |
| Policy validation records | Verification decisions and supporting sources |
| Estimation dataset | Panel used for empirical analyses |
| Figure scripts | Reproduce all manuscript figures |
| Table scripts | Reproduce manuscript tables |

---

# Dataset Overview

The repository contains two complementary datasets.

## Global Macroeconomic Panel

A harmonized panel of approximately **190 countries**, including indicators such as:

- GDP per capita
- Unemployment
- Inflation
- Tourism dependence
- Price level index
- Governance indicators

## Verified Digital Nomad Policy Benchmark

A human-verified benchmark covering **32 jurisdictions** with digital nomad visa programmes.

Policy variables include:

- Visa adoption year
- Minimum monthly income requirement
- Visa duration
- Visa application fee
- Tax treatment
- Official policy references

Every policy record has been independently verified against primary legal documents or official government sources.

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

Install the required Python packages.

```bash
pip install -r requirements.txt
```

Build the processed dataset.

```bash
python scripts/preprocessing/build_dataset.py
```

Run policy validation.

```bash
python scripts/validation/validate_policy_dataset.py
```

Estimate the empirical models.

```bash
python scripts/estimation/run_models.py
```

Generate all manuscript figures.

```bash
python scripts/visualization/build_figures.py
```

Generate all manuscript tables.

```bash
python scripts/tables/build_tables.py
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

The repository code, documentation, and analysis scripts are released under the **MIT License** (or replace with your preferred license).

The benchmark dataset is released for academic research and reproducibility. Users should consult the terms of use of the original government data sources when redistributing derived policy information.
