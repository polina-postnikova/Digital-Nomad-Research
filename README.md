# A Global Benchmark Dataset of Digital-Nomad Policy Adoption, Tourism Flows, and Labor-Market Indicators for Cross-Country Mobility Research
A Global Benchmark Dataset of Digital-Nomad Policy Adoption, Tourism Flows, and Labor-Market Indicators for Cross-Country Mobility Research
<p align="center"> <strong>Trustworthy AI-assisted policy curation and a human-verified benchmark for digital nomad visa research</strong><br> Paper notation: <code>\textsc{DigitalNomad}</code> </p> <p align="center"> <img alt="Trustworthy AI" src="https://img.shields.io/badge/Trustworthy%20AI-Human--Verified-4F6BED"> <img alt="Policy Benchmark" src="https://img.shields.io/badge/Policy%20Benchmark-32%20Verified%20Jurisdictions-0B7A75"> <img alt="Coverage" src="https://img.shields.io/badge/Macroeconomic%20Panel-190%20Countries-536DFE"> <img alt="Research" src="https://img.shields.io/badge/Policy-Digital%20Nomad%20Visas-7A4FB3"> <img alt="Methods" src="https://img.shields.io/badge/Methods-TWFE%20%7C%20DML-B35C00"> </p>
A Global Benchmark Dataset of Digital-Nomad Policy Adoption, Tourism Flows, and Labor-Market Indicators for Cross-Country Mobility Research is an open research benchmark for evaluating AI-assisted policy extraction through complete human verification and downstream empirical validation. The project combines a global macroeconomic panel covering approximately 190 countries with a human-verified benchmark of 32 digital nomad visa programmes, allowing researchers to measure both the reliability of large language model (LLM) policy extraction and its consequences for econometric analysis.
Unlike traditional policy datasets, every verified policy record is independently validated against official government and legal sources. The benchmark is designed to support research on trustworthy AI, reproducible policy data curation, and AI-assisted social science.
GitHub repository
https://github.com/polina-postnikova/Digital-Nomad-Research
Release Snapshot
Component	Current release
Verified policy benchmark	32 jurisdictions
Macroeconomic panel	~190 countries
Time coverage	Annual panel
Policy variables	Adoption year, visa duration, income requirement, fees, tax treatment
Verification	Human-verified against official sources
Downstream evaluation	TWFE and Doubly Robust DML
Primary contribution	Trustworthy AI-assisted policy curation
Main application	Digital nomad visa policy research
Why This Benchmark Exists
Digital Nomad Research is built around three complementary research objectives.
Trustworthy AI: evaluate the accuracy of LLM-assisted policy extraction through complete human verification.
Benchmark Construction: provide an openly documented, reproducible benchmark for digital nomad visa policies.
Downstream Evaluation: determine whether observed policy extraction errors materially influence empirical policy conclusions.
Rather than proposing a new causal estimator, the repository investigates how AI-generated policy data affect downstream econometric analyses.
Repository Structure
data/
│
├── raw/
│   Original macroeconomic and policy data
│
├── processed/
│   Cleaned panel datasets used in analysis
│
├── policy_validation/
│   Human verification records
│
├── documentation/
│   Variable definitions and coding notes
│
analysis/
│
├── figures/
│   Figure generation scripts
│
├── tables/
│   Table generation scripts
│
├── robustness/
│   Sensitivity analyses
│
└── notebooks/
│   Exploratory analyses
│
paper/
│
├── manuscript/
├── supplementary_material/
└── bibliography/
│
results/
│
├── figures/
├── tables/
└── model_outputs/
│
scripts/
│
├── preprocessing/
├── validation/
├── estimation/
└── visualization/
Main Dataset Components
Component	Description
Global macroeconomic panel	Country-level macroeconomic indicators
Verified policy benchmark	Human-validated digital nomad visa dataset
Validation annotations	Record-level verification decisions
Estimation dataset	Panel used for econometric analysis
Figure scripts	Reproduce all manuscript figures
Table scripts	Reproduce manuscript tables
Dataset Overview
The repository contains two complementary datasets.
Macroeconomic Panel
A harmonized panel of macroeconomic indicators for approximately 190 countries including variables such as
GDP per capita
unemployment
inflation
tourism dependence
price level
governance indicators
Verified Policy Benchmark
A manually verified benchmark covering 32 jurisdictions with digital nomad visa programmes.
Variables include
visa adoption year
minimum income requirement
visa duration
visa fee
tax treatment
policy documentation
Every policy record has been independently verified using official government publications or primary legal documents.
Research Workflow
Official policy sources

↓

LLM-assisted extraction

↓

Human verification

↓

Verified benchmark

↓

Panel data construction

↓

TWFE estimation

↓

Doubly Robust DML

↓

Comparison of verified vs. raw policy data
Reproducing the Paper
Install the required packages.
pip install -r requirements.txt
Run the preprocessing pipeline.
python scripts/preprocessing/build_dataset.py
Run policy validation.
python scripts/validation/validate_policy_dataset.py
Estimate the benchmark models.
python scripts/estimation/run_models.py
Generate all manuscript figures.
python scripts/visualization/build_figures.py
Generate all manuscript tables.
python scripts/tables/build_tables.py
Methodological Scope
The repository evaluates whether LLM-assisted policy extraction can support empirical policy research through transparent human verification.
The econometric analyses are intended to assess the robustness of downstream inference to policy curation errors. They should not be interpreted as definitive estimates of the causal effects of digital nomad visas.
Current Limitations
The verified benchmark currently includes 32 jurisdictions.
Policy coding requires harmonization across heterogeneous legal systems.
Some policy attributes involve interpretative decisions despite independent verification.
The empirical analyses remain observational.
Results are specific to digital nomad visa policies and should not be generalized to all AI-assisted policy extraction tasks without additional validation.
Citation
If you use this repository, please cite the accompanying paper.
