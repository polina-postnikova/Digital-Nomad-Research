# Trustworthy AI for Global Policy Evidence

## Auditing LLM-Curated Digital-Nomad Visa Data and Evaluating Downstream Causal Consequences

> Anonymous research repository for a study of LLM-assisted policy-data curation, human verification, and downstream causal analysis of digital-nomad visa adoption.

[![Trustworthy AI](https://img.shields.io/badge/Trustworthy%20AI-Human--Verified-4F6BED)](#research-overview)
[![Policy benchmark](https://img.shields.io/badge/Policy%20Benchmark-190%20Jurisdictions-0B7A75)](#data)
[![Macroeconomic panel](https://img.shields.io/badge/Macroeconomic%20Panel-190%20Countries-536DFE)](#data)
[![Methods](https://img.shields.io/badge/Methods-TWFE%20%7C%20CS--style%20DID-B35C00)](#analysis)

---

## Research overview

Large language models can turn unstructured legal and policy material into structured datasets, but errors in policy definitions and treatment dates can affect the results of subsequent empirical analysis.

This repository studies that problem using digital-nomad visa (DNV) policy data. The workflow combines:

1. **LLM-assisted Stage 1 screening** of 190 jurisdictions.
2. **Primary-source verification** of qualifying policies and policy attributes.
3. **A structured field-level audit** of adoption timing, duration, income requirements, fees, and tax treatment.
4. **A country-year macroeconomic and tourism panel** linked to the policy data.
5. **Data-quality and missingness checks.**
6. **Cross-validation of tourism arrivals and expenditure measures.**
7. **Staggered-adoption analysis**, including a conventional two-way fixed-effects (TWFE) benchmark and a Callaway–Sant'Anna-style group-time/event-time analysis.
8. **A semi-synthetic error-propagation experiment** examining the consequences of using different treatment-date definitions.

The central research question is:

> **How trustworthy are LLM-curated global policy data for consequential comparative and causal analysis?**

The repository is designed to make the data, audit trail, analysis scripts, and generated research outputs inspectable and reproducible.

---

## Key design principles

### Primary sources take precedence

The audit treats statutes, regulations, decrees, gazettes, official immigration authorities, consular guidance, and other government sources as the controlling evidence for policy fields.

Secondary sources are used for discovery and cross-checking, but a secondary source alone does not establish that a jurisdiction has a qualifying DNV.

### Explicit DNV definition

A qualifying digital-nomad visa is defined as a legally distinct immigration status or permit whose eligibility explicitly permits remote work for a non-domestic employer or non-domestic clients as a basis for admission or residence, independently of a domestic job offer.

The audit therefore excludes, among other cases:

- ordinary tourist or visitor arrangements that merely tolerate incidental remote work;
- entrepreneur/start-up routes unless the same instrument independently provides a qualifying remote-employment pathway;
- policies inferred solely from marketing language or secondary aggregators.

### Preserve raw evidence

The audit records source evidence, source metadata, access dates, raw values, original units/currencies, and normalization rules. Derived or normalized values are not treated as if they were the underlying legal threshold.

### Separate historical adoption from current status

A country can have a historical DNV adoption event while no longer operating the same programme. The dataset therefore distinguishes adoption timing from operative/current status and records policy changes separately where possible.

---

## Repository structure

```text
Digital-Nomad-Research-main/
├── README.md
├── LICENSE
│
├── Data/
│   ├── Raw/
│   │   ├── GDP.xls
│   │   ├── Unemployment.xls
│   │   ├── Inflation, consumer prices (annual %).csv
│   │   ├── Official exchange rate (LCU per US$, period average).csv
│   │   ├── internet penetration data.csv
│   │   ├── price level index (GDP).csv
│   │   ├── UN Tourism inbound arrivals.xlsx
│   │   ├── UN Tourism inbound expenditure.xlsx
│   │   ├── UN Tourism employed persons.xlsx
│   │   └── Tourism direct GDP as a proportion of total GDP (%).xlsx
│   │
│   ├── Intermediate/
│   │   ├── LLM_Stage1.xlsx
│   │   ├── LLM_Stage2.xlsx
│   │   └── Audit_Stage1_Stage2.csv
│   │
│   └── Processed/
│       └── DigitalNomadDataset.xlsx
│
├── Docs/
│   ├── data_dictionary.md
│   └── Stage 1 and Stage 2: LLM, Retrieval, Source-Hierarchy, and Field-Level Audit.md
│
├── Scripts/
│   ├── sample_loader.py
│   ├── CrossValidation.py
│   ├── MissingnessAudit.py
│   └── Results/
│       ├── staggered_adoption_sensitivity.py
│       └── *.csv
│
└── Figs/
    ├── digital_nomad_map.svg
    ├── event_study.svg
    ├── twfe_vs_cs.svg
    ├── thailand_vietnam.svg
    ├── missingness.svg
    └── *.py
```

The repository also contains the source files used to generate several figures in `Figs/` and analysis outputs in `Scripts/Results/`.

---

## Data

### Processed analysis dataset

`Data/Processed/DigitalNomadDataset.xlsx` contains two linked worksheets:

| Worksheet | Rows | Columns | Description |
|---|---:|---:|---|
| `tourism_and_macroeconomic_data` | 2,464 | 14 | Country-year macroeconomic and tourism panel |
| `policy_data` | 33 | 3 | Policy-adoption information for the countries represented in the processed policy table |

The macro/tourism panel contains, among other variables:

- country name and ISO3 code;
- year;
- GDP;
- unemployment rate;
- tourism expenditure;
- tourism GDP share;
- tourism employment;
- business and total tourism arrivals;
- internet usage;
- inflation;
- exchange rate;
- GDP price-level index.

The complete field definitions and harmonization rules are documented in [`Docs/data_dictionary.md`](Docs/data_dictionary.md).

### Intermediate audit data

`Data/Intermediate/` contains the policy-curation and verification artifacts:

- `LLM_Stage1.xlsx` — Stage 1 LLM-assisted screening/discovery output;
- `LLM_Stage2.xlsx` — Stage 2 field-level audit material;
- `Audit_Stage1_Stage2.csv` — consolidated audit data used by the analysis.

The Stage 1/Stage 2 methodology, source hierarchy, inclusion criteria, evidence rules, and translation/normalization procedures are documented in [`Docs/Stage 1 and Stage 2: LLM, Retrieval, Source-Hierarchy, and Field-Level Audit.md`](Docs/Stage%201%20and%20Stage%202%3A%20LLM%2C%20Retrieval%2C%20Source-Hierarchy%2C%20and%20Field-Level%20Audit.md).

### Raw data

`Data/Raw/` contains the source macroeconomic and tourism files used to construct the processed panel, including World Bank-style indicators and UN Tourism measures.

Raw files should be treated as source inputs rather than edited analysis files.

---

## Audit methodology

### Stage 1 — jurisdiction-level screening

Stage 1 covers all **190 jurisdictions** in the macro/tourism panel.

The screening process:

1. applies a predefined DNV definition;
2. identifies plausible policy instruments;
3. uses structured secondary-source discovery for unresolved cases;
4. traces plausible claims back to primary legal or official sources;
5. records classification, evidence, source metadata, and confidence.

The protocol distinguishes:

- Qualifying Policy;
- No Qualifying Policy;
- Announced but Inactive Policy;
- Unresolved Status.

The audit was conducted as an interactive LLM-assisted research process rather than as a deterministic batch API experiment. Consequently, the repository preserves the resulting audit artifacts and protocol rather than claiming that the original LLM browsing session can be replayed exactly.

### Stage 2 — field-level verification

Stage 2 independently audits confirmed adopters and focuses on detailed policy fields such as:

- adoption timing;
- permit/visa duration;
- income requirements;
- visa or permit fees;
- tax treatment;
- remote-work eligibility and the underlying qualifying instrument.

For each field, the methodology prioritizes primary legal and official sources and records evidence and provenance where available.

The documented Stage 2 review date is **2026-08-09**.

---

## Analysis workflow

The repository contains four main analysis components.

### 1. Sample inspection

`Scripts/sample_loader.py` loads the processed Excel workbook and prints the first rows of its worksheets.

```bash
python Scripts/sample_loader.py
```

**Note:** the script currently expects `DigitalNomadDataset.xlsx` in its working directory. If you run it from the repository root, either place/copy the processed workbook there or update the `file_path` in the script to:

```text
Data/Processed/DigitalNomadDataset.xlsx
```

### 2. Tourism cross-validation

`Scripts/CrossValidation.py` compares year-over-year growth in tourism arrivals and tourism expenditure.

For countries with sufficient observations, it calculates Pearson correlations between arrivals growth and expenditure growth, and it also reports the pooled correlation.

```bash
python Scripts/CrossValidation.py
```

The script currently writes `arrival_expenditure_validation.csv` to its working directory and likewise expects `DigitalNomadDataset.xlsx` to be available there.

### 3. Missingness audit

`Scripts/MissingnessAudit.py` evaluates missing data at several levels:

- variable level;
- country level;
- year level;
- dataset level.

It also produces missingness summaries, yearly plots, heatmaps, and Excel audit tables.

```bash
python Scripts/MissingnessAudit.py
```

As with the sample loader and cross-validation script, the current implementation expects `DigitalNomadDataset.xlsx` in the working directory.

### 4. Staggered-adoption sensitivity analysis

The main empirical analysis is implemented in:

```text
Scripts/Results/staggered_adoption_sensitivity.py
```

It performs the following steps:

1. loads the audit and macroeconomic panel;
2. parses announcement and effective dates;
3. distinguishes calendar-year adoption from first full exposure;
4. constructs the main treatment sample;
5. estimates group-time treatment associations using never-treated countries;
6. aggregates results by event time;
7. estimates a conventional TWFE benchmark;
8. produces treatment-date sensitivity data;
9. runs the semi-synthetic error-propagation experiment;
10. generates descriptive/event-time figures;
11. saves the analysis-ready panel and result tables.

The default simulation settings in the script are:

```text
--sim-reps 200
--sim-beta -1.0
--seed 12345
```

A reproducible run from the repository root can be made explicit by supplying the files that are actually present in this repository:

```bash
python Scripts/Results/staggered_adoption_sensitivity.py \
  --audit Data/Intermediate/Audit_Stage1_Stage2.csv \
  --panel Data/Processed/DigitalNomadDataset.xlsx \
  --output-dir Scripts/Results/dnm_sensitivity \
  --sim-reps 200 \
  --sim-beta -1.0 \
  --seed 12345
```

The analysis script writes outputs including:

```text
Scripts/Results/dnm_sensitivity/
├── audit_with_treatment_dates.csv
├── sample_flow.csv
├── cs_group_time_associations.csv
├── cs_event_time_associations.csv
├── twfe_benchmark.csv
├── treatment_date_sensitivity_country_level.csv
├── semi_synthetic_summary.csv
├── semi_synthetic_metadata.csv
├── analysis_panel_main.csv
├── event_time_associations.svg
└── descriptive_unemployment_trajectories.svg
```

---

## Statistical approach

### TWFE benchmark

The analysis includes a conventional two-way fixed-effects benchmark with:

- country fixed effects;
- year fixed effects;
- a treatment indicator based on first full exposure;
- lagged covariates including log GDP, inflation, and internet usage.

### Callaway–Sant'Anna-style group-time analysis

The repository implements a never-treated-control group-time DID estimator.

For treatment cohort \(g\) and year \(t\), the estimator compares the change from the pre-treatment base year \(g-1\) to year \(t\) for the treated cohort against the corresponding change among never-treated countries.

The repository then aggregates these group-time estimates by event time.

This implementation should be understood as a **CS-style group-time association estimator using never-treated controls**, not as a general solution to endogenous treatment adoption.

### Treatment-date sensitivity

The analysis explicitly distinguishes:

- the policy's calendar-year adoption date; and
- the first year of full exposure.

This distinction is central to the error-propagation experiment because announcement dates can precede the date on which a policy becomes legally or practically operative.

### Semi-synthetic experiment

The semi-synthetic component introduces a controlled treatment-date error and evaluates how that error affects downstream estimates.

The experiment is designed to isolate the consequences of curation/timing error rather than to claim that the simulated effect represents the true causal effect of DNV adoption.

---

## Figures

The `Figs/` directory contains existing visual outputs and their source scripts, including:

- `digital_nomad_map.svg`
- `event_study.svg`
- `twfe_vs_cs.svg`
- `thailand_vietnam.svg`
- `missingness.svg`

Associated Python scripts include:

- `Figs/event_study.py`
- `Figs/twfe_vs_cs.py`
- `Figs/thailand_vietnam.py`
- `Figs/missingness.py`

These files provide the figure-generation code and the corresponding rendered SVG outputs included in the repository.

---

## Reproducibility and current repository limitations

This repository contains the data and scripts used for the analysis, but it does **not** currently include some of the automation files described in earlier versions of the README, such as:

- `requirements.txt`;
- `environment.yml`;
- `run_all.sh`;
- a `tests/` directory;
- GitHub Actions reproduction workflow;
- `MANIFEST.csv`;
- `checksums.sha256`;
- `CITATION.cff`.

Accordingly, reproduction should currently be performed script-by-script using the files and paths present in the repository.

The Python scripts import the following main packages:

```text
pandas
numpy
scipy
statsmodels
matplotlib
seaborn
openpyxl
```

Install them in your preferred Python environment before running the analysis.

For example:

```bash
python -m pip install pandas numpy scipy statsmodels matplotlib seaborn openpyxl
```

The original LLM screening/audit session itself is not deterministically replayable. What is reproducible from this repository is the downstream analysis performed on the released audit and processed datasets.

---

## Data provenance and evidence

The audit documentation emphasizes field-level provenance. Where populated, audit records preserve information such as:

- evidence span or paraphrase;
- primary-source URL;
- source title;
- issuing authority;
- access date;
- raw value;
- original unit or currency;
- normalization rule;
- confidence/verification status.

The repository therefore separates **source evidence** from **derived analytical variables** rather than treating a transformed value as the original legal requirement.

For detailed provenance and field definitions, see:

- [`Docs/data_dictionary.md`](Docs/data_dictionary.md)
- [`Docs/Stage 1 and Stage 2: LLM, Retrieval, Source-Hierarchy, and Field-Level Audit.md`](Docs/Stage%201%20and%20Stage%202%3A%20LLM%2C%20Retrieval%2C%20Source-Hierarchy%2C%20and%20Field-Level%20Audit.md)

---

## Licensing

The repository's code is released under the **MIT License**. See [`LICENSE`](LICENSE) for the complete license text.

The raw data files retain the licensing and redistribution conditions of their underlying sources. Users should verify the applicable terms for any third-party World Bank and UN Tourism data before redistributing them independently.

---

## Research status

The repository is structured as an **anonymous research/replication repository**. The accompanying audit documentation records the methodology and the date of the LLM-assisted research pass.

The repository should therefore be read as a research artifact: the audited policy data, provenance records, statistical scripts, and generated figures are intended to support inspection and replication of the reported analysis, while the original interactive LLM browsing session is not itself replayable.

---

## Citation

Citation information is not provided as a separate `CITATION.cff` file in the current repository. Until a final bibliographic record is added, please cite the associated paper/research project and identify this repository as the replication data and analysis repository.
