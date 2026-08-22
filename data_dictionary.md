# Data Dictionary

## 1. `tourism_and_macroeconomic_data`

Source: World Bank Open Data / UN Tourism (per paper §2).

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country_name` | TODO | string | TODO | TODO |
| `iso3` | ISO 3166-1 alpha-3 country code | code | TODO | TODO |
| `year` | Calendar year | year | TODO | TODO |
| `gdp` | TODO | TODO (current USD?) | World Bank Open Data | TODO |
| `unemployment_rate` | TODO | % of labor force | World Bank Open Data | TODO |
| `expenditures` | Tourism expenditure | TODO (current USD?) | UN Tourism | TODO |
| `tourism_gdp_share` | Tourism share of GDP | % | TODO | TODO |
| `tourism_employment` | TODO | TODO | TODO | TODO |
| `arrivals_business` | International arrivals, business purpose | count | UN Tourism | TODO |
| `arrivals_total` | International arrivals, total | count | UN Tourism | TODO |
| `internet_usage_pct` | Individuals using the internet | % of population | World Bank Open Data | TODO |
| `inflation_annual_pct` | Annual inflation | % | World Bank Open Data | TODO |
| `exchange_rate_lcu_per_usd` | Local currency units per USD | ratio | World Bank Open Data | TODO |
| `price_level_index_gdp` | GDP price level index | index | World Bank Open Data | TODO |

## 2. `Policy_Data` 

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Country` | TODO | string | TODO | TODO |
| `ISO3` | ISO 3166-1 alpha-3 country code | code | TODO | TODO |
| `Adoption year` | Year of DNV policy adoption used in main-text panel | year | Derived from Stage-2 audit | TODO — confirm relation to `launch_or_effective_date` below |

## 3. Human audit 

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country` | TODO | string | Human audit | — |
| `iso3` | ISO 3166-1 alpha-3 country code | code | Human audit | — |
| `qualifying_program_found` | Whether a qualifying DNV program was identified (yes/no) | categorical | Human audit | See boundary-case adjudication rules, paper Appendix (§ Reproducible Protocol) |
| `program_name` | Name of the qualifying program | string | Primary source | — |
| `program_type` | Program category | categorical | Primary source | — |
| `program_url` | Link to program page | URL | Primary source | — |
| `legal_or_official_basis` | Statute/gazette/ministry basis | string | Primary source | — |
| `announcement_date` | Date program was publicly announced | date | Primary/secondary source | Distinct from `launch_or_effective_date` — this is the field substituted in the semi-synthetic experiment |
| `launch_or_effective_date` | Verified effective/launch date | date | Primary source | Treated as ground truth for treatment timing |
| `status_during_observation_period` | Program status as of observation window | categorical | Human audit | — |
| `discovery_evidence_span` | Quoted/paraphrased evidence supporting the call | text | Primary/secondary source | Keep short spans only — see `DATA_LICENSE.md` |
| `discovery_source_title` | Title of discovery source | string | — | — |
| `discovery_source_institution` | Issuing institution | string | — | — |
| `discovery_source_url` | URL of discovery source | URL | — | — |
| `source_publication_date` | Publication date of source | date | — | — |
| `source_access_date` | Date source was accessed by auditor | date | — | — |
| `primary_or_secondary_source` | Whether discovery source is primary or secondary | categorical | — | Primary required for "yes" adopter calls (see protocol) |

## 4. Stage-1 LLM screening (`data/intermediate/stage1_llm_screening.xlsx`)

Sheets: `190_country_adjudication`, `discovery_audit`, `screening_protocol`,
`source_register`. TODO: document each sheet's fields the same way as above.

## 5. Stage-2 LLM field audit (`data/intermediate/stage2_llm_field_audit.xlsx`)

Sheets: `field_level_audit`, `audit_protocol`, `evidence_log`,
`source_register`, `stage1_linkage`. TODO: document each sheet's fields the
same way as above. This is also the source table for Table (error taxonomy) —
see `MANIFEST.csv`.
