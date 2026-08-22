import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

PASTEL_WB = "#1d3557"  
PASTEL_UN = "#e08e45"  
COLOR_TEXT = "#334155"  
COLOR_MUTED = "#64748b"  

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "svg.fonttype": "none",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "text.color": COLOR_TEXT,
        "axes.labelcolor": COLOR_TEXT,
        "xtick.color": COLOR_MUTED,
        "ytick.color": COLOR_TEXT,
    }
)

df = pd.read_excel(
    "DigitalNomadDataset.xlsx", sheet_name="tourism_and_macroeconomic_data"
)
N = len(df)

var_map = {
    "gdp": ("GDP (current USD)", "World Bank"),
    "exchange_rate_lcu_per_usd": ("Official exchange rate", "World Bank"),
    "price_level_index_gdp": ("Price level index", "World Bank"),
    "internet_usage_pct": ("Internet usage (% pop.)", "World Bank"),
    "inflation_annual_pct": ("Inflation (annual %)", "World Bank"),
    "unemployment_rate": ("Unemployment rate (% labor force)", "World Bank"),
    "arrivals_business": ("Inbound tourism arrivals (business)", "UN Tourism"),
    "arrivals_total": ("Inbound tourism arrivals (total)", "UN Tourism"),
    "expenditures": ("Inbound tourism expenditures", "UN Tourism"),
    "tourism_gdp_share": ("Tourism direct GDP share", "UN Tourism"),
    "tourism_employment": ("Tourism sectoral employment", "UN Tourism"),
}

rows = []
for col, (label, source) in var_map.items():
    miss = df[col].isna().sum()
    rows.append((label, source, miss, miss / N * 100))

rows.sort(key=lambda r: r[3])
variables = [r[0] for r in rows]
source_list = [r[1] for r in rows]
missing_pct = [r[3] for r in rows]

colors = [PASTEL_WB if s == "World Bank" else PASTEL_UN for s in source_list]

fig, ax = plt.subplots(figsize=(7, 5), dpi=150)

y_pos = np.arange(len(variables))
bars = ax.barh(
    y_pos, missing_pct, color=colors, edgecolor="none", height=0.8, zorder=3
)

for i, pct in enumerate(missing_pct):
    ax.text(
        pct + 1.2,
        i,
        f"{pct:.2f}%",
        va="center",
        fontsize=8.5,
        color=COLOR_TEXT,
        fontweight="semibold",
    )

ax.set_yticks(y_pos)
ax.set_yticklabels(variables, fontsize=9.5)
ax.invert_yaxis()
ax.set_xlim(0, max(missing_pct) * 1.3)

for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#cbd5e1")
ax.spines["bottom"].set_linewidth(0.8)

ax.xaxis.grid(True, linestyle="-", color="#f1f5f9", linewidth=1, zorder=0)
ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, labelsize=9)

ax.set_xlabel(
    "Missing Observations (%)", fontsize=9.5, fontweight="medium", labelpad=8
)
ax.text(
    0,
    1.025,
    f"N = {N:,} country-year observations",
    transform=ax.transAxes,
    fontsize=8.5,
    color=COLOR_MUTED,
    style="italic",
    ha="left",
    va="bottom",
)

handles = [
    Patch(facecolor=PASTEL_WB, label="World Bank Open Data"),
    Patch(facecolor=PASTEL_UN, label="UN Tourism"),
]
legend = ax.legend(
    handles=handles,
    loc="upper left",
    bbox_to_anchor=(0.7, 1.0), 
    frameon=False,
    fontsize=9,
    handlelength=1.1,
    handleheight=0.7,
)

plt.tight_layout() 
fig.savefig("fig2_missingness_pastel.svg", format="svg", bbox_inches="tight")

print("Saved SVG figure as 'fig2_missingness_pastel.svg'")
plt.show()
