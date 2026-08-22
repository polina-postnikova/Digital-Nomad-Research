# Stage 1 — LLM, Retrieval, and Source-Hierarchy Audit

| Item | Stage 1 value |
|---|---|
| **LLM provider** | OpenAI |
| **Model** | GPT-5.6 Luna |
| **Model version** | GPT-5.6 Luna |
| **Access date(s)** | 2026-08-09 for the principal Stage-1 adjudication/discovery work |
| **Input universe** | All 190 distinct jurisdictions in the uploaded `tourism_and_macroeconomic_data` worksheet |
| **Policy definition supplied to model** | Legally distinct immigration status/permit explicitly permitting remote work for a non-domestic employer or non-domestic clients as a basis for admission/residence, independent of a domestic job offer |
| **Number of initial primary-source adjudication runs** | 1 substantive workbook-wide adjudication pass |
| **Number of structured secondary-source discovery runs** | 1 follow-up discovery/trace pass over the unresolved jurisdictions |
| **Total substantive Stage-1 passes** | 2 |
| **Human/LLM interaction** | Interactive LLM-assisted research; not an autonomous batch API experiment |
| **Temperature / sampling settings** | Not recorded by the ChatGPT interface used for this research; therefore **not reported as a numeric setting** |
| **Top-p / seed / other generation settings** | Not recorded by the ChatGPT interface used for this research; therefore **not reported as a numeric setting** |
| **Web retrieval** | Web search/browsing through the ChatGPT web-retrieval system, supplemented by official-source URLs identified during the search |
| **File retrieval** | Uploaded Excel workbook read directly from `DigitalNomadDataset.xlsx` |
| **Source cutoff** | **2026-08-09** for the Stage-1 research pass |
| **Temporal treatment** | Policies were coded according to their operative dates; later adoption was not backdated into the 2024 panel endpoint |
| **Secondary-source role** | Discovery only; secondary evidence alone could not upgrade a jurisdiction to Qualifying Policy |
| **Primary-source requirement** | A plausible secondary claim had to be traced to a government/legal/official immigration instrument before being upgraded |
| **Unresolved rule** | Failure to establish a sufficiently probative primary source resulted in **Unresolved Status**, rather than No Qualifying Policy |
| **Tourist/workation rule** | Incidental remote work under visitor/tourist arrangements was excluded |
| **Entrepreneur/start-up rule** | Entrepreneur/start-up routes excluded unless the same instrument independently provided a qualifying remote-employment pathway |
| **Supersession rule** | Original qualifying adoption retained as adoption event; subsequent replacement/material eligibility changes treated as policy-attribute changes |
| **Multiple-tier rule** | Earliest tier establishing qualifying eligibility used for treatment; tier-specific attributes retained where available |
| **Primary-source access date** | 2026-08-09 for the Stage-1 source review |
| **Archiving** | Live source URLs were recorded. **A systematic archived-snapshot capture was not performed in Stage 1** and should not be claimed retrospectively. |

## Initial Prompt

> Using only the cited primary source(s), determine whether a jurisdiction in the 190 country panel worksheet has an immigration instrument that satisfies the study's DNV definition (ignore the policy adopters worksheet). We define a digital-nomad visa (DNV) as a legally distinct immigration status or permit whose eligibility criteria explicitly permit remote work for a non-domestic employer or non-domestic clients as a basis for admission or residence, independent of a domestic job offer.
>
> This definition is used to adjudicate the following boundary cases:
>
> - **Freelancer visas:** included only when eligibility explicitly extends to remote employees of foreign firms, not solely self-employed service providers to the local market.
> - **Remote-work residence permits:** included when the residence basis is remote work itself, even if the instrument is not branded a “digital nomad visa.”
> - **Entrepreneur / start-up visas:** excluded unless a remote-employment pathway exists within the same instrument, since the eligibility basis (founding a local business) is substantively different.
> - **Tourist-visa pathways permitting incidental remote work:** excluded from the treated set; jurisdictions relying solely on such pathways are eligible for the non-adopter comparison file, not the treated panel.
> - **Superseded programs:** coded to the currently operative instrument as of each observed year; where a program was replaced, the adoption date reflects the original qualifying instrument and any material eligibility change is logged as a policy-attribute change rather than a new adoption event.
> - **Multiple policy tiers within one jurisdiction:** coded to the tier that establishes first qualifying eligibility, with tier-level detail (e.g., income requirement by tier) retained in the field-level audit for future heterogeneity work rather than collapsed into a single value.
>
> Identify the instrument, legal basis, eligibility for remote work for foreign employers/clients, operative dates, and current status. Classify as **Qualifying Policy, No Qualifying Policy, Announced but Inactive Policy, or Unresolved Status**. Do not infer eligibility from tourism, informal tolerance, marketing language, or unrelated entrepreneur/start-up programs. Return the classification, evidence span(s), source URL, issuing authority, document date, access date, and confidence. If the evidence is insufficient, return Unresolved Status.

## Discovery-Stage Prompt

> Define the eligible universe before screening it, mirroring the systematic-review practice of pre-registering inclusion criteria ahead of the search itself [Page et al., 2021]. Run a structured, keyword-based secondary-source scan (immigration-law-firm bulletins, Big-Four mobility-practice alerts, national investment-promotion-agency announcements) for every unresolved jurisdiction, using a fixed query template per country rather than free-form search, so the discovery step itself is reproducible. For every jurisdiction returning a plausible hit, attempt to trace the claim to a primary legal instrument (gazette, statute, ministry regulation); jurisdictions where this trace fails, as with Cabo Verde and Seychelles in the pilot, remain category (iv) rather than being upgraded on secondary-source strength alone. Log every jurisdiction's category, evidence source, and access date in a discovery-audit table.

### Fixed Discovery Query

```text
"{country}" "digital nomad visa" immigration law firm remote work foreign employer
```

## Field-Specific Source Hierarchy — Stage 1

Primary-source precedence is applied independently by field.

| Field | Priority 1 | Priority 2 | Priority 3 | Secondary sources |
|---|---|---|---|---|
| **Whether DNV exists** | Statute, regulation, decree, gazette, immigration resolution | Official immigration authority / ministry | Official consular guidance | Discovery only |
| **Instrument name/type** | Legal instrument | Immigration authority | Consular authority | Discovery only |
| **Legal basis** | Gazette/statute/regulation | Official legal database | Ministry/immigration authority | Not dispositive |
| **Adoption date** | Promulgation/effective legal instrument | Official government announcement | Official immigration guidance | Not dispositive |
| **Operative dates/status** | Current statute/regulation + repeal/amendment instrument | Immigration authority | Official government programme page | Not dispositive |
| **Remote-work eligibility** | Statutory/regulatory eligibility language | Official immigration authority | Official consular guidance | **Never sufficient alone** |
| **Foreign employer/client requirement** | Statute/regulation | Immigration authority | Official consular guidance | **Never inferred from marketing language** |
| **Permit duration** | Statute/regulation | Immigration authority | Consular guidance | Discovery only |
| **Income requirement** | Statute/regulation | Immigration authority | Official consular guidance | Discovery only |
| **Visa/permit fee** | Official fee regulation/schedule | Immigration/consular authority | Official government application portal | Discovery only |
| **Tax treatment** | Tax statute/regulation + tax authority | Finance/tax ministry | Official immigration guidance where explicitly tax-specific | Never inferred from visa status |
| **Translation** | Original-language legal text | Official bilingual version | Independently checked translation | Machine translation only as discovery aid |

---

# Stage 2 — Field-Level Audit (Confirmed Adopters)

| Item | Stage 2 value |
|---|---|
| **LLM provider** | OpenAI |
| **Model** | GPT-5.6 Luna |
| **Prompt** | For every confirmed adopting jurisdiction, independently re-derive and verify all detailed policy fields (adoption timing, permit duration, income requirements, visa fees, and tax treatment) directly from primary government sources. Enforce source hierarchies: ensure primary legal texts and official immigration authority portals take absolute precedence over secondary aggregators, embassy guidance, or relocation consultancy sites. Log evidence and metadata: record exact quoted/paraphrased evidence spans, archived source snapshots (e.g., web-archive URLs), access dates, raw values, units, and explicit unit-normalization rules for every single verified cell. Process non-English sources: manage translation workflows (via professional translation, bilingual auditors, or independently checked machine translations) for non-English primary legal texts. |
| **Stage 2 scope** | Independent field-level audit of every jurisdiction coded as Qualifying Policy in Stage 1. The Stage 2 working set is the 42 jurisdictions in the Stage-1 adjudication result; historical adoption status and current operative status are kept distinct where they differ. |
| **Audit objective** | Re-derive and verify directly from primary government sources: adoption timing, permit/visa duration, income requirement, visa/permit fees, and tax treatment. Verify the underlying qualifying instrument and remote-work eligibility where necessary. |
| **Primary-source rule** | Primary legal texts and official immigration, visa, consular, finance, or tax authority sources take absolute precedence. Secondary aggregators, law-firm alerts, relocation consultancies, tourism sites, and similar material are discovery/cross-check sources only. |
| **Evidence logging** | For every verified cell, record the exact quoted or faithful paraphrase of the controlling evidence span; source title/instrument; issuing authority; source URL; access date; raw value; original unit/currency; and any normalization or derivation rule. |
| **Archive rule** | Record an archived source snapshot/web-archive URL when an independently located snapshot exists. Do not fabricate or retrospectively claim an archive capture. If none was located, record that explicitly. |
| **Access date** | The executed Stage-2 primary-source review was recorded as 2026-08-09. |
| **Raw-value rule** | Preserve the source's original value, unit, frequency, currency, and gross/net characterization. Do not silently convert or round values. |
| **Unit normalization** | If a normalized value is required, retain both raw and normalized values and state the mathematical rule explicitly. A derived value must never be represented as the legal threshold itself. |
| **Currency normalization** | Preserve the legally applicable fee in source currency. Do not collapse nationality-, consular-post-, or date-specific fee schedules into one universal amount. |
| **Duration rule** | Distinguish initial validity, maximum validity, renewal period, and total possible stay. Do not treat ordinary visitor-entry periods as DNV duration. |
| **Adoption-timing rule** | Use the controlling instrument's promulgation, approval, publication, or effective date according to the Stage-1 temporal rule. Where adoption and operational dates differ, retain both. |
| **Tax-treatment rule** | Distinguish programme-specific tax exemption/exclusion from ordinary tax-residence and source rules. Absence of tax language is not evidence of tax exemption. Tax claims require a tax statute/regulation, tax authority source, or explicitly tax-specific official guidance. |
| **Translation workflow** | For non-English primary material, retain original legal terminology where material. Prefer an official bilingual/English version; otherwise use professional translation, bilingual audit, or independently checked translation. Machine translation is a discovery aid, not dispositive evidence. |
| **Translation audit record** | For translation-dependent fields, record the original-language source, translated evidence span/paraphrase, translation method/checking method, and whether the field was independently corroborated by another official source. |
| **Field status coding** | Each field is coded as **Primary-source verified, Partially verified/conditional, or Not independently re-derived**. Missing primary evidence is not filled with a secondary value. |
| **Current-status exception** | A historical adopter may no longer have an operative programme. Retain the historical adoption event but separately record current status and the operative instrument. The executed audit identified Antigua and Barbuda as a material example: its official programme portal states that the Nomad Digital Residency programme has ended. |
| **Supersession rule** | When a qualifying instrument is replaced, link the field to the instrument operative for the relevant observation period while retaining the original adoption event and logging material policy-attribute changes. |
| **Multiple-tier rule** | Where multiple qualifying tiers/routes exist, identify the tier establishing first qualifying eligibility and retain tier-specific duration, income, fee, and tax details rather than collapsing materially different requirements. |
| **Boundary-case rule** | Continue to exclude tourist/workation arrangements that do not constitute a legally distinct qualifying immigration status, consistent with Stage 1. |
| **Quality-control rule** | A numerical field is not accepted merely because it appears repeatedly in secondary sources. It must be traceable to a primary legal/official source. Conflicting official values are retained with dates/instruments and flagged. |
| **Confidence** | Assign confidence at field/source level. Strong confidence requires a controlling legal/official source clearly supporting the field; medium indicates official but indirect/conditional evidence; low is not treated as verified. |
| **Stage 2 output** | The executed audit is documented in the Stage-2 Field-Level Audit — Confirmed Adopters report, containing the field-level verification matrix, evidence/metadata log, jurisdiction notes, source hierarchy, translation workflow, normalization rules, and QC flags. |
| **Reproducibility** | Preserve cell-level provenance: evidence span, raw value, unit, normalization rule, source hierarchy, access date, archive status, translation method, and verification status. |

## Stage 2 — Field-Specific Source Hierarchy

Primary-source precedence is applied independently to each field; an immigration source is not automatically authoritative for tax treatment or fee schedules.

| Field | Priority 1 | Priority 2 | Priority 3 | Secondary sources |
|---|---|---|---|---|
| **Adoption timing** | Statute/regulation/decree/gazette | Official government announcement | Official immigration guidance | Discovery/cross-check only |
| **Permit duration** | Statute/regulation | Official immigration authority | Official consular guidance | Discovery only |
| **Income requirement** | Statute/regulation | Official immigration authority | Official consular guidance | Discovery only |
| **Visa/permit fee** | Official fee regulation/schedule | Immigration/consular authority | Official application portal | Discovery only |
| **Tax treatment** | Tax statute/regulation + tax authority | Finance/tax ministry | Official immigration guidance if explicitly tax-specific | Never inferred |
| **Remote-work eligibility** | Statutory/regulatory eligibility language | Official immigration authority | Official consular guidance | Never sufficient alone |
| **Foreign employer/client requirement** | Statute/regulation | Immigration authority | Official consular guidance | Never inferred from marketing |
| **Translation** | Original-language legal text | Official bilingual version | Independently checked translation | Machine translation = discovery aid only |
| **Archive evidence** | Official archived government copy / reliable web archive | Government historical snapshot | Official PDF snapshot | No archive claim if none located |

## Stage 2 — Executed Audit Limitations

- The executed Stage-2 pass was deliberately conservative. Where a primary source did not expose or permit independent re-derivation of a numerical field, the field was marked unverified rather than populated from a secondary source.
- The audit recorded live primary-source URLs and explicitly marked cases where no independent archived snapshot was located; it does not claim systematic archival capture.
- The executed pass contains strong primary evidence for a subset of jurisdictions and primary-source leads for the remainder. The Stage-2 document therefore should not be read as asserting that every field in all 42 jurisdictions is fully verified.
- Later amendments, fee changes, income-index changes, or programme closures should be logged as subsequent policy-attribute changes rather than silently replacing the historical values.