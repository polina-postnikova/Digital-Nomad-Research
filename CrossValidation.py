import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import seaborn as sns

file_path = "DigitalNomadPolicyDataset.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="tourism_and_macroeconomic_data"
)

validation_df = df[
    ["iso3", "country_name", "year",
     "arrivals_total", "expenditures"]
].copy()

validation_df = validation_df.dropna(
    subset=["arrivals_total", "expenditures"]
)



validation_df = validation_df.sort_values(
    ["iso3", "year"]
)

validation_df["arrivals_growth"] = (
    validation_df.groupby("iso3")["arrivals_total"]
    .pct_change() * 100
)

validation_df["expenditure_growth"] = (
    validation_df.groupby("iso3")["expenditures"]
    .pct_change() * 100
)

validation_df = validation_df.dropna(
    subset=["arrivals_growth", "expenditure_growth"]
)


results = []

for iso3, group in validation_df.groupby("iso3"):

    if len(group) >= 5:

        r, p = pearsonr(
            group["arrivals_growth"],
            group["expenditure_growth"]
        )

        results.append({
            "iso3": iso3,
            "country_name": group["country_name"].iloc[0],
            "n_years": len(group),
            "correlation": r,
            "p_value": p
        })

corr_df = pd.DataFrame(results)


print(
    f"Countries analysed: {len(corr_df)}"
)

print(
    f"Mean correlation: "
    f"{corr_df['correlation'].mean():.3f}"
)

print(
    f"Median correlation: "
    f"{corr_df['correlation'].median():.3f}"
)

print(
    f"Countries with positive correlation: "
    f"{(corr_df['correlation'] > 0).sum()}"
)


anomalies = corr_df[
    corr_df["correlation"] < 0
].sort_values("correlation")

print("\nPotential anomalies:")
print(
    anomalies[
        ["iso3", "country_name", "correlation"]
    ].head(20)
)

corr_df.to_csv(
    "arrival_expenditure_validation.csv",
    index=False
)

# Overall pooled correlation

overall_r, overall_p = pearsonr(
    validation_df["arrivals_growth"],
    validation_df["expenditure_growth"]
)

print("\nOverall pooled correlation")
print(f"r = {overall_r:.3f}")
print(f"p = {overall_p:.5f}")
