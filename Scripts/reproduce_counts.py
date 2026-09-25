"""Regenerates every count in Sections 3-4 that comes from the jurisdiction-level records.
Usage: python reproduce_counts.py [path/to/jurisdiction_reconciliation.csv] [path/to/LLM_Stage2.xlsx]
Only the LLM adoption-year coding in LLM_YEAR (Stage-2 free text -> year) is manual; everything else is computed."""
import re, sys, math
import pandas as pd

REC = sys.argv[1] if len(sys.argv) > 1 else "jurisdiction_reconciliation.csv"
S2 = sys.argv[2] if len(sys.argv) > 2 else "LLM_Stage2.xlsx"
r = pd.read_csv(REC)

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * (c - h), 1), round(100 * (c + h), 1)

print("Stage-1 labels:", r.llm_stage1_label.value_counts().to_dict())
print("Stage-2 status (Stage-1 qualifying):", r.llm_stage2_status.value_counts().to_dict())

det = r[r.llm_stage1_label != "Unresolved Status"].copy()
det["llm_yes"] = det.llm_stage1_label == "Qualifying Policy"
det["hum_yes"] = det.human_label == "yes"
n = len(det); k = int((det.llm_yes == det.hum_yes).sum())
po = k / n
pe = det.llm_yes.mean() * det.hum_yes.mean() + (1 - det.llm_yes.mean()) * (1 - det.hum_yes.mean())
print(f"Determinate calls n={n}; agree={k} ({100*po:.1f}%); Wilson95={wilson(k,n)}; kappa={(po-pe)/(1-pe):.3f}")
print("Disagreement status:", r.disagreement_status.value_counts().to_dict())
print("LLM-missed adopters (Unresolved but human yes):", int(((r.llm_stage1_label == "Unresolved Status") & (r.human_label == "yes")).sum()))

ad = r[r.human_label == "yes"].copy()
st = ad.human_status.fillna("none").str.lower()
print("Adopters:", len(ad), "| active-equivalent:", int(st.str.startswith("active").sum()),
      "| announced-not-active:", int((st == "announced_but_inactive").sum()), "| no status:", int((st == "none").sum()))

def parse(s):
    if pd.isna(s): return None
    s = str(s).strip()
    if re.fullmatch(r"\d{4}", s): return (int(s), None, None)
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m: return (int(m[1]), int(m[2]), None)
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s)
    if m:
        y = int(m[3]); y = y + 2000 if y < 100 else y
        return (y, int(m[1]), int(m[2]))
ad["e"] = ad.human_effective_date.map(parse); ad["a"] = ad.human_announcement_date.map(parse)
gran = ad.e.map(lambda t: "missing" if not isinstance(t, tuple) else "year" if t[1] is None else "month" if t[2] is None else "day")
print("Effective-date granularity:", gran.value_counts().to_dict())

rows = []
for _, x in ad.iterrows():
    if not (isinstance(x.e, tuple) and isinstance(x.a, tuple)) or x.e[1] is None: continue
    true_c = x.e[0] if x.e[1] == 1 else x.e[0] + 1
    rows.append(dict(jurisdiction=x.jurisdiction, announcement=x.human_announcement_date, effective=x.human_effective_date,
                     verified_cohort=true_c, announcement_year_cohort=x.a[0],
                     identical_dates=(x.a == x.e), first_full_year_observed=true_c <= 2024))
m = pd.DataFrame(rows)
o = m[m.first_full_year_observed].copy(); o["shifted"] = o.verified_cohort != o.announcement_year_cohort
print("Cohort sizes (first full exposure year <= 2024):", o.verified_cohort.value_counts().sort_index().to_dict())
print(f"Adopters with month-level+ effective date: {len(m)}; cohort <=2024: {len(o)}; cohorts shifted by announcement-year rule: {int(o.shifted.sum())}"
      f"; of those with identical announcement/effective dates: {int((o.shifted & o.identical_dates).sum())}")
o.to_csv("treatment_year_mapping.csv", index=False)

LLM_YEAR = {"Antigua and Barbuda": 2020, "Argentina": 2022, "Barbados": 2020, "Brazil": 2021, "Estonia": 2020, "Japan": 2024,
            "Bermuda": None, "Croatia": None, "Hungary": None}
s2 = pd.read_excel(S2, sheet_name="field_level_audit").set_index("Jurisdiction")
t = []
for j, y in LLM_YEAR.items():
    h = ad[ad.jurisdiction == j].iloc[0]
    t.append(dict(jurisdiction=j, llm_text=s2.loc[j, "Adoption Timing"], llm_year=y,
                  human_effective=h.human_effective_date, human_effective_year=h.e[0],
                  year_match=None if y is None else y == h.e[0]))
t = pd.DataFrame(t); t.to_csv("adoption_year_check.csv", index=False)
ev = t.dropna(subset=["year_match"]); kk = int(ev.year_match.sum())
print(f"Adoption-year (same calendar year): {kk}/{len(ev)}; Wilson95={wilson(kk, len(ev))}; overlap rows without a usable LLM year: {int(t.llm_year.isna().sum())}")
