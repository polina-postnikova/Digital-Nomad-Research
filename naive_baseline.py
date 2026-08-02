import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

MACRO_PATH = "DigitalNomadDataset.xlsx"
POLICY_VALIDATION_PATH = "PolicyValidation.xlsx"

OUTCOME = "unemployment_rate"
CLUSTER = "iso3"

EXPECTED_ABSENT = {"AIA", "BHS", "CUW"}


def build_treatment_indicator(macro: pd.DataFrame, adoption_years: pd.Series) -> pd.Series:

    adopt_year = macro["iso3"].map(adoption_years)  
    treated = ((macro["year"] >= adopt_year)).astype(int)
    treated = treated.where(adopt_year.notna(), 0) 
    return treated


def naive_baseline(df: pd.DataFrame, outcome_col: str, treatment_col: str,
                    cluster_col: str = CLUSTER) -> dict:
    d = df.dropna(subset=[outcome_col, treatment_col]).copy()

    model = smf.ols(f"{outcome_col} ~ {treatment_col}", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[cluster_col]}
    )

    beta = model.params[treatment_col]
    se = model.bse[treatment_col]
    p = model.pvalues[treatment_col]
    ci_low, ci_high = model.conf_int().loc[treatment_col]

    return {
        "beta": beta,
        "se": se,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "p": p,
        "n_obs": int(d.shape[0]),
        "n_countries": int(d[cluster_col].nunique()),
        "n_treated_obs": int(d.loc[d[treatment_col] == 1].shape[0]),
    }


def main():
    macro = pd.read_excel(MACRO_PATH, sheet_name="tourism_and_macroeconomic_data")
    hand_verified = pd.read_excel(MACRO_PATH, sheet_name="policy_data")
    llm_extracted = pd.read_excel(POLICY_VALIDATION_PATH, sheet_name="AI_extraction")

    missing_from_macro = set(hand_verified["iso3"]) - set(macro["iso3"])
    assert missing_from_macro == EXPECTED_ABSENT, (
        f"Expected {EXPECTED_ABSENT} absent from macro panel, found {missing_from_macro}"
    )

    hv_years = hand_verified.set_index("iso3")["visa_adoption_year"]
    llm_years = llm_extracted.set_index("iso3")["visa_adoption_year"]
    common = hv_years.index.intersection(llm_years.index)
    mismatched = common[hv_years.loc[common] != llm_years.loc[common]]
    print(f"Adoption-year mismatches (excluded from error-aware subset): "
          f"{sorted(mismatched.tolist())}\n")

    llm_years_error_aware = llm_years.drop(index=mismatched)

    regimes = {
        "hand_verified": hv_years,
        "llm_extracted": llm_years,
        "error_aware_llm_subset": llm_years_error_aware,
    }

    results = []
    for regime_name, adoption_years in regimes.items():
        macro_regime = macro.copy()
        macro_regime["treated"] = build_treatment_indicator(macro_regime, adoption_years)

        res = naive_baseline(macro_regime, OUTCOME, "treated")
        res["data"] = regime_name
        results.append(res)

        print(f"[{regime_name}]")
        print(f"  beta        = {res['beta']:.4f}")
        print(f"  se (clust.) = {res['se']:.4f}")
        print(f"  95% CI      = [{res['ci_low']:.4f}, {res['ci_high']:.4f}]")
        print(f"  p           = {res['p']:.4f}")
        print(f"  n_obs       = {res['n_obs']}  (treated obs: {res['n_treated_obs']})")
        print(f"  n_countries = {res['n_countries']}")
        print()

    out = pd.DataFrame(results)[
        ["data", "beta", "se", "ci_low", "ci_high", "p", "n_obs", "n_countries", "n_treated_obs"]
    ]
    print(out)


if __name__ == "__main__":
    main()
