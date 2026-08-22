# Data Dictionary

## 1. `tourism_and_macroeconomic_data`

Source: World Bank Open Data / UN Tourism (per paper §2).

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country_name` | Official country name as used in World Bank/UN Tourism data | string | World Bank Open Data / UN Tourism | Standardized to ISO country name format; matches `iso3` codes |
| `iso3` | ISO 3166-1 alpha-3 country code | code | World Bank Open Data / UN Tourism | Three-letter country code; primary key for linking policy data |
| `year` | Calendar year | year | World Bank Open Data / UN Tourism | Four-digit year; panel spans 2008-2024 |
| `gdp` | Gross Domestic Product, current US dollars | current USD | World Bank Open Data | Converted to USD using annual average exchange rates where needed |
| `unemployment_rate` | Unemployment as percentage of total labor force | % of labor force | World Bank Open Data | ILO estimate; modeled ILO estimate used where available |
| `expenditures` | Tourism expenditure (inbound tourism spending) | current USD | UN Tourism | Inbound tourism expenditure in current USD; converted using annual average exchange rates |
| `tourism_gdp_share` | Tourism share of GDP | % | UN Tourism | Direct tourism contribution as percentage of GDP |
| `tourism_employment` | Tourism sector employment | count (persons) | UN Tourism / World Bank | Direct tourism employment in persons; values may be estimated for some countries |
| `arrivals_business` | International arrivals for business purposes | count | UN Tourism | Number of international tourist arrivals with business as primary purpose |
| `arrivals_total` | International arrivals, total | count | UN Tourism | Total international tourist arrivals (all purposes) |
| `internet_usage_pct` | Individuals using the internet | % of population | World Bank Open Data | Percentage of population with access to the internet; ITU estimate |
| `inflation_annual_pct` | Annual inflation (consumer prices) | % | World Bank Open Data | Annual percentage change in consumer price index |
| `exchange_rate_lcu_per_usd` | Local currency units per USD | ratio | World Bank Open Data | Annual average exchange rate; national currency per USD |
| `price_level_index_gdp` | GDP price level index | index (USA=100) | World Bank Open Data | Price level index relative to USA; PPP-based |

---

## 2. `policy_data`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Country` | Official country name | string | Derived from Stage-2 audit | Matches `country_name` in main dataset; standardize to ISO format |
| `ISO3` | ISO 3166-1 alpha-3 country code | code | Derived from Stage-2 audit | Three-letter country code; primary key for merging |
| `Adoption year` | Year of DNV policy adoption used in main-text panel | year | Derived from Stage-2 audit | Uses `launch_or_effective_date` from human audit; year when policy became operative; for announced-but-not-implemented policies, uses announcement year with status flag |

---

## 3. Human audit

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country` | Official country name | string | Human audit | Standardized to ISO country name; matches `country_name` in main dataset |
| `iso3` | ISO 3166-1 alpha-3 country code | code | Human audit | Three-letter country code; primary key |
| `qualifying_program_found` | Whether a qualifying DNV program was identified (yes/no) | categorical | Human audit | "Yes" only if primary source confirms distinct immigration status/permit; "No" for tourism workation programs or no program |
| `program_name` | Name of the qualifying program | string | Primary source | Official program name from government/legal source; use original language with English translation in notes where helpful |
| `program_type` | Program category | categorical | Primary source | Classified as: Digital Nomad Visa, Digital Nomad Residence Permit, Temporary Residence Permit, Long-term Visa, Residence Permit Pathway |
| `program_url` | Link to program page | URL | Primary source | Official government URL where available; use archive.org snapshot if original page changes |
| `legal_or_official_basis` | Statute/gazette/ministry basis | string | Primary source | Specific law, regulation, decree, or official policy document; include citation |
| `announcement_date` | Date program was publicly announced | date | Primary/secondary source | Date of official announcement or first public disclosure; distinct from `launch_or_effective_date`; used in semi-synthetic experiment |
| `launch_or_effective_date` | Verified effective/launch date | date | Primary source | Treated as ground truth for treatment timing; date when program became operative for applicants |
| `status_during_observation_period` | Program status as of observation window | categorical | Human audit | Active, Ended, Announced but Inactive, or Excluded (for tourism workation programs); observation window is 2008-2024 |
| `discovery_evidence_span` | Quoted/paraphrased evidence supporting the call | text | Primary/secondary source | Short verbatim quote or paraphrase from primary source showing remote work eligibility; keep concise |
| `discovery_source_title` | Title of discovery source | string | — | Title of the document/webpage where evidence was found |
| `discovery_source_institution` | Issuing institution | string | — | Government ministry, agency, or official body that published the source |
| `discovery_source_url` | URL of discovery source | URL | — | Direct link to source; use archive.org if original URL is unstable |
| `source_publication_date` | Publication date of source | date | — | Date when the discovery source was published or last updated |
| `source_access_date` | Date source was accessed by auditor | date | — | Date when the auditor retrieved the source (YYYY-MM-DD format) |
| `primary_or_secondary_source` | Whether discovery source is primary or secondary | categorical | — | Primary required for "yes" adopter calls; Primary = official government/legal source; Secondary = law firm bulletin, blog, news article, or third-party summary |

---

## 4. Stage-1 LLM screening

### Sheet: `190_country_adjudication`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country_name` | Official country name | string | Country list | Standardized to ISO format; matches `country_name` in main dataset |
| `iso3` | ISO 3166-1 alpha-3 country code | code | Country list | Three-letter country code |
| `classification` | Initial classification from LLM screening | categorical | LLM screening | Qualifying Policy, No Qualifying Policy, Unresolved Status |
| `instrument` | Name of the identified instrument | string | LLM screening | Program name if Qualifying Policy; empty otherwise |
| `legal_basis` | Legal or regulatory basis for the instrument | string | LLM screening | Citation of law/regulation if identified |
| `remote_work_eligibility` | Eligibility requirement for remote work | text | LLM screening | Description of who qualifies for the program |
| `operative_dates` | Date range or effective date | text | LLM screening | When the program is/was operational |
| `current_status` | Current operational status | categorical | LLM screening | Operative, Ended, Excluded, Announced |
| `evidence_spans` | Quoted evidence supporting classification | text | LLM screening | Key phrases from discovery |
| `source_url` | URL of discovery source | URL | LLM screening | Link to source document |
| `issuing_authority` | Institution that issued the instrument | string | LLM screening | Government ministry or agency |
| `document_date` | Date of legal instrument or announcement | date | LLM screening | Date of official document |
| `access_date` | Date source was accessed | date | LLM screening | Retrieval date (YYYY-MM-DD format) |
| `confidence` | Confidence level in classification | categorical | LLM screening | High, Medium, Low |
| `notes` | Additional notes on screening decision | text | LLM screening | Justification and caveats |

### Sheet: `discovery_audit`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country_name` | Official country name | string | Country list | Standardized to ISO format |
| `discovery_query` | Query string used for discovery | string | Screening protocol | Fixed template: `"{country}" "digital nomad visa" immigration law firm remote work foreign employer` |
| `secondary_hit` | Whether a secondary source was found | boolean | LLM screening | Yes/No based on query results |
| `secondary_source` | Name of secondary source document | string | LLM screening | Title of secondary source if found |
| `secondary_source_url` | URL of secondary source | URL | LLM screening | Link to secondary source |
| `plausible_hit` | Whether a plausible claim was identified | boolean | LLM screening | Yes if secondary source suggests a program exists |
| `primary_trace_status` | Whether primary source was located | categorical | LLM screening | Successful/sufficient, Failed/not established, Not triggered |
| `final_category` | Final classification | categorical | LLM screening | Qualifying Policy, No Qualifying Policy, Unresolved Status |
| `instrument_or_claim` | Name of instrument or claim description | string | LLM screening | Program name or description of claim |
| `screening_rationale` | Explanation of classification decision | text | LLM screening | Reasoning for final classification |
| `access_date` | Date source was accessed | date | LLM screening | Retrieval date |
| `confidence` | Confidence level in classification | categorical | LLM screening | High, Medium, Low |

### Sheet: `screening_protocol`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `field` | Name of protocol parameter | string | Protocol definition | Fixed field names per protocol |
| `value` | Value of protocol parameter | text | Protocol definition | Specific rule or value |

### Sheet: `source_register`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `issuer` | Institution that published the source | string | Source metadata | Government agency or organization |
| `document` | Title of the source document | string | Source metadata | Official title of the document |
| `url` | URL of the source | URL | Source metadata | Link to the document |
| `source_role` | Role of the source in screening | categorical | Source metadata | Primary legal instrument, Primary official immigration source, Primary government programme source, Secondary discovery, Exclusion evidence |
| `document_date` | Date of the source document | date | Source metadata | Publication or effective date |

---

## 5. Stage-2 LLM field audit 

### Sheet: `field_level_audit`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Jurisdiction` | Official country name | string | Stage-1 screening | Standardized to ISO format |
| `Verification Status` | Whether primary source was verified | categorical | Field audit | Field-level verification complete, Field-level verification incomplete |
| `Adoption Timing` | Policy adoption date and details | text | Primary source | Enactment/approval/publication date; separately identify operative date where available |
| `Permit Duration` | Maximum validity of the permit | duration | Primary source | Initial term and renewal options; preserve source unit (months/years) |
| `Income Requirement` | Minimum income threshold | currency/period | Primary source | Preserve gross/net and original time unit; no silent conversions |
| `Visa/Permit Fee` | Application and issuance fees | currency | Primary source | Preserve currency and each component; do not merge charges without source support |
| `Tax Treatment` | Tax status of program participants | categorical | Primary source | No DNV-specific income-tax exemption established; may include program exemptions |
| `Evidence / Paraphrase` | Quoted evidence from primary source | text | Primary source | Direct quote or precise paraphrase; short span only |
| `Primary Source URL` | URL of the primary source | URL | Primary source | Official government/legal source |
| `Access Date` | Date source was accessed | date | Field audit | YYYY-MM-DD format |
| `Archive Snapshot` | Archive.org URL if available | URL | Field audit | Not located in this pass, or archive URL |
| `Translation Method` | Approach to non-English sources | text | Field audit | Official English/bilingual source preferred; otherwise checked paraphrase |
| `Normalization / Unit Rule` | Rules for standardizing values | text | Field audit | Preserve source unit/currency; no silent conversion; distinguish fee components |
| `Confidence` | Confidence in recorded values | categorical | Field audit | High, Medium-High, Medium, Low, Low/pending |
| `Notes` | Additional context or caveats | text | Field audit | Special considerations, missing data, or pending verification |

### Sheet: `audit_protocol`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Item` | Name of protocol parameter | string | Protocol definition | Fixed field names per protocol |
| `Rule` | Value of protocol parameter | text | Protocol definition | Specific auditing rule |

### Sheet: `evidence_log`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Jurisdiction` | Official country name | string | Stage-1 screening | Standardized to ISO format |
| `Evidence Span / Paraphrase` | Quoted or paraphrased evidence | text | Primary source | Direct evidence supporting the field values |
| `Primary Source URL` | URL of the primary source | URL | Primary source | Official government/legal source |
| `Access Date` | Date source was accessed | date | Field audit | YYYY-MM-DD format |
| `Archive Snapshot` | Archive.org URL if available | URL | Field audit | Not located in this pass, or archive URL |
| `Verification Status` | Whether primary source was verified | categorical | Field audit | Verified where populated, Pending |
| `Confidence` | Confidence in recorded values | categorical | Field audit | High, Medium-High, Medium, Low, Low/pending |

### Sheet: `source_register`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `Jurisdiction` | Official country name | string | Stage-1 screening | Standardized to ISO format |
| `Primary Source` | URL or citation of primary source | URL | Field audit | Official government/legal source |
| `Role` | Role of the source | categorical | Field audit | Controlling/lead primary source |
| `Access Date` | Date source was accessed | date | Field audit | YYYY-MM-DD format |

### Sheet: `stage1_linkage`

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country_name` | Official country name | string | Stage-1 screening | Standardized to ISO format |
| `iso3` | ISO 3166-1 alpha-3 country code | code | Stage-1 screening | Three-letter country code |
| `classification` | Classification from Stage 1 | categorical | Stage-1 screening | Qualifying Policy, No Qualifying Policy, Unresolved Status |
| `instrument` | Name of the identified instrument | string | Stage-1 screening | Program name if Qualifying Policy; empty otherwise |
| `legal_basis` | Legal or regulatory basis | string | Stage-1 screening | Citation of law/regulation if identified |
| `remote_work_eligibility` | Eligibility requirement for remote work | text | Stage-1 screening | Description of who qualifies |
| `operative_dates` | Date range or effective date | text | Stage-1 screening | When the program is/was operational |
| `current_status` | Current operational status | categorical | Stage-1 screening | Operative, Ended, Excluded, Announced |
| `evidence_spans` | Quoted evidence supporting classification | text | Stage-1 screening | Key phrases from discovery |
| `source_url` | URL of discovery source | URL | Stage-1 screening | Link to source document |
| `issuing_authority` | Institution that issued the instrument | string | Stage-1 screening | Government ministry or agency |
| `document_date` | Date of legal instrument or announcement | date | Stage-1 screening | Date of official document |
| `access_date` | Date source was accessed | date | Stage-1 screening | Retrieval date |
| `confidence` | Confidence level in classification | categorical | Stage-1 screening | High, Medium, Low |
| `notes` | Additional notes on screening decision | text | Stage-1 screening | Justification and caveats |

---

## 6. Completed Audit 

| Field | Definition | Unit | Source | Harmonization rule |
|---|---|---|---|---|
| `country` | Official country name | string | Human audit | Standardized to ISO country name |
| `iso3` | ISO 3166-1 alpha-3 country code | code | Human audit | Three-letter country code |
| `qualifying_program_found` | Whether a qualifying DNV program was identified (yes/no) | categorical | Human audit | Yes only if primary source confirms distinct immigration status/permit |
| `program_name` | Name of the qualifying program | string | Primary source | Official program name; empty if no program |
| `program_type` | Program category | categorical | Primary source | Digital Nomad Visa, Digital Nomad Residence Permit, Temporary Residence Permit, Long-term Visa, Residence Permit Pathway |
| `program_url` | Link to program page | URL | Primary source | Official government URL where available |
| `legal_or_official_basis` | Statute/gazette/ministry basis | string | Primary source | Specific law, regulation, decree, or official policy document |
| `announcement_date` | Date program was publicly announced | date | Primary/secondary source | Date of official announcement; distinct from launch date |
| `launch_or_effective_date` | Verified effective/launch date | date | Primary source | Date when program became operative |
| `status_during_observation_period` | Program status as of observation window | categorical | Human audit | Active, Ended, Announced but Inactive; observation window 2008-2024 |
| `discovery_evidence_span` | Quoted/paraphrased evidence supporting the call | text | Primary/secondary source | Short verbatim quote or paraphrase showing remote work eligibility |
| `discovery_source_title` | Title of discovery source | string | — | Title of the document/webpage where evidence was found |
| `discovery_source_institution` | Issuing institution | string | — | Government ministry or agency that published the source |
| `discovery_source_url` | URL of discovery source | URL | — | Direct link to source; use archive.org if unstable |
| `source_publication_date` | Publication date of source | date | — | Date when source was published or last updated |
| `source_access_date` | Date source was accessed by auditor | date | — | Retrieval date (YYYY-MM-DD format) |
| `primary_or_secondary_source` | Whether discovery source is primary or secondary | categorical | — | Primary = official government/legal source; Secondary = third-party summary |
