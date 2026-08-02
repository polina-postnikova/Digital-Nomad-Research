import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
import warnings
warnings.filterwarnings("ignore")


matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7,
    "axes.labelsize": 7,
    "axes.titlesize": 8,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5,
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "lines.linewidth": 1.1,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "grid.linewidth": 0.4,
    "grid.alpha": 0.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

NAT_BLUE   = "#2166AC"
NAT_RED    = "#D6604D"
NAT_GREEN  = "#4DAC26"
NAT_ORANGE = "#F4A582"
NAT_PURPLE = "#762A83"
NAT_GRAY   = "#878787"
NAT_LTBLUE = "#92C5DE"
NAT_LTRED  = "#F7F7F7"

macro = pd.read_excel(
    "DigitalNomadDataset.xlsx",
    sheet_name="tourism_and_macroeconomic_data"
)
policy = pd.read_excel(
    "DigitalNomadDataset.xlsx",
    sheet_name="policy_data"
)

adopters = set(policy["iso3"].tolist())
adoption_map = dict(zip(policy["iso3"], policy["visa_adoption_year"]))

macro = macro.copy()
macro["is_adopter"] = macro["iso3"].isin(adopters)
macro["adoption_year"] = macro["iso3"].map(adoption_map)
macro["event_time"] = macro["year"] - macro["adoption_year"]

# Business share
macro["biz_share"] = macro["arrivals_business"] / macro["arrivals_total"].replace(0, np.nan)
macro["biz_leisure_ratio"] = macro["arrivals_business"] / (
    macro["arrivals_total"] - macro["arrivals_business"].fillna(0)
).replace(0, np.nan)

# Tourism dependence: top quartile of tourism_gdp_share
tgdp_q75 = macro.groupby("iso3")["tourism_gdp_share"].mean().quantile(0.75)
tourism_dep = set(
    macro.groupby("iso3")["tourism_gdp_share"].mean()
    .pipe(lambda s: s[s >= tgdp_q75]).index
)

print(f"Adopters: {len(adopters)} | Tourism-dependent: {len(tourism_dep)}")
print(f"Overlap (adopter & tourism-dep): {len(adopters & tourism_dep)}")

def panel_label(ax, letter, x=-0.14, y=1.05):
    ax.text(x, y, letter, transform=ax.transAxes,
            fontsize=10, fontweight="bold", va="top", ha="left")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 – Q1: Business-arrival share DiD (event study)
# ══════════════════════════════════════════════════════════════════════════════
fig1, axes1 = plt.subplots(1, 2, figsize=(7.2, 2.9))
fig1.subplots_adjust(wspace=0.38)

# ── 1a. Event-study: mean business share relative to adoption year ────────────
ax = axes1[0]

ev_df = macro[macro["is_adopter"] & macro["biz_share"].notna()].copy()
ev_grp = (
    ev_df.groupby("event_time")["biz_share"]
    .agg(["mean", "sem", "count"])
    .reset_index()
)
ev_grp = ev_grp[(ev_grp["event_time"] >= -5) & (ev_grp["event_time"] <= 4)]
ev_grp = ev_grp[ev_grp["count"] >= 3]

ci95 = 1.96 * ev_grp["sem"]
pre_mean = ev_grp[ev_grp["event_time"] < 0]["mean"].mean()

ax.axhline(pre_mean, color=NAT_GRAY, lw=0.7, ls="--", alpha=0.7)
ax.axvline(0, color=NAT_RED, lw=0.8, ls=":", alpha=0.8)
ax.fill_between(ev_grp["event_time"],
                ev_grp["mean"] - ci95,
                ev_grp["mean"] + ci95,
                alpha=0.18, color=NAT_BLUE)
ax.plot(ev_grp["event_time"], ev_grp["mean"],
        "o-", color=NAT_BLUE, ms=4, lw=1.2, zorder=5)

# shade post-adoption
ax.axvspan(0, ev_grp["event_time"].max(), alpha=0.06, color=NAT_RED)

ax.set_xlabel("Years relative to visa adoption")
ax.set_ylabel("Business arrivals / total arrivals")
ax.set_title("Event study: business-arrival share\naround digital nomad visa adoption", pad=4)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_xlim(-5.5, 4.5)

# annotation
post = ev_grp[ev_grp["event_time"] >= 0]["mean"].mean()
delta = post - pre_mean
ax.annotate(
    f"Δ = {delta:+.3f}\n(post − pre mean)",
    xy=(2, post), xytext=(1.8, post + 0.04),
    fontsize=6, color=NAT_BLUE,
    arrowprops=dict(arrowstyle="-", color=NAT_GRAY, lw=0.6)
)

panel_label(ax, "a")

# ── 1b. Adopters vs non-adopters: business share 2019–2022 ───────────────────
ax = axes1[1]

years_panel = [2019, 2020, 2021, 2022]
records = []
for yr in years_panel:
    sub = macro[(macro["year"] == yr) & macro["biz_share"].notna()]
    for grp, label, col in [
        (True, "Adopters", NAT_BLUE),
        (False, "Non-adopters", NAT_GRAY)
    ]:
        s = sub[sub["is_adopter"] == grp]["biz_share"]
        if len(s) > 1:
            records.append({
                "year": yr, "label": label,
                "mean": s.mean(), "sem": s.sem(), "color": col
            })
r = pd.DataFrame(records)

x = np.arange(len(years_panel))
w = 0.35
for i, (label, col) in enumerate([("Adopters", NAT_BLUE), ("Non-adopters", NAT_GRAY)]):
    sub_r = r[r["label"] == label]
    offset = (i - 0.5) * w
    bars = ax.bar(x + offset, sub_r["mean"], w * 0.9,
                  color=col, alpha=0.85, zorder=3)
    ax.errorbar(x + offset, sub_r["mean"], yerr=1.96 * sub_r["sem"],
                fmt="none", color="black", capsize=2, lw=0.8, zorder=5)

ax.set_xticks(x)
ax.set_xticklabels(years_panel)
ax.set_xlabel("Year")
ax.set_ylabel("Mean business-arrival share")
ax.set_title("Business-arrival share:\nadopters vs. non-adopters", pad=4)

legend_patches = [
    mpatches.Patch(color=NAT_BLUE, alpha=0.85, label="Visa adopters"),
    mpatches.Patch(color=NAT_GRAY, alpha=0.85, label="Non-adopters"),
]
ax.legend(handles=legend_patches, frameon=False, loc="upper right")
panel_label(ax, "b")

fig1.savefig("Fig1_Q1_visa_arbitrage.pdf", dpi=300, bbox_inches="tight")
fig1.savefig("Fig1_Q1_visa_arbitrage.png", dpi=300, bbox_inches="tight")
print("Figure 1 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 – Q2: Unemployment recovery in tourism-dependent economies
# ══════════════════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 2, figsize=(7.2, 2.9))
fig2.subplots_adjust(wspace=0.38)

# Filter to tourism-dependent countries
td_macro = macro[macro["iso3"].isin(tourism_dep)].copy()

# ── 2a. Mean unemployment: adopters vs non-adopters, 2019-2023, tourism-dep ──
ax = axes2[0]
years_u = list(range(2019, 2024))
records2 = []
for yr in years_u:
    sub = td_macro[(td_macro["year"] == yr) & td_macro["unemployment_rate"].notna()]
    for grp, label, col in [(True, "Adopter", NAT_BLUE), (False, "Non-adopter", NAT_GRAY)]:
        s = sub[sub["is_adopter"] == grp]["unemployment_rate"]
        if len(s) > 1:
            records2.append({"year": yr, "label": label, "mean": s.mean(), "sem": s.sem(), "color": col})
r2 = pd.DataFrame(records2)

for label, col, ls, mk in [("Adopter", NAT_BLUE, "-", "o"), ("Non-adopter", NAT_GRAY, "--", "s")]:
    sub_r = r2[r2["label"] == label]
    ax.fill_between(sub_r["year"],
                    sub_r["mean"] - 1.96 * sub_r["sem"],
                    sub_r["mean"] + 1.96 * sub_r["sem"],
                    alpha=0.15, color=col)
    ax.plot(sub_r["year"], sub_r["mean"], ls, color=col, marker=mk, ms=4,
            label=f"{label} (n≥{sub_r['mean'].notna().sum()})")

ax.axvline(2020, color="black", lw=0.7, ls=":", alpha=0.6)
ax.axvspan(2021, 2023, alpha=0.05, color=NAT_GREEN)
ax.set_xlabel("Year")
ax.set_ylabel("Mean unemployment rate (%)")
ax.set_title("Unemployment recovery:\ntourism-dependent economies", pad=4)
ax.legend(frameon=False)
ax.text(2020.1, ax.get_ylim()[1]*0.97, "COVID shock", fontsize=5.5, color="#555", va="top")
ax.text(2021.1, ax.get_ylim()[1]*0.88, "Recovery\nwindow", fontsize=5.5, color=NAT_GREEN, va="top")
panel_label(ax, "a")

# ── 2b. Δ unemployment 2019→2022 by tourism dependence & adoption status ─────
ax = axes2[1]

base_yr, end_yr = 2019, 2022
base = macro[macro["year"] == base_yr][["iso3", "unemployment_rate"]].rename(columns={"unemployment_rate": "u_base"})
end  = macro[macro["year"] == end_yr][["iso3", "unemployment_rate"]].rename(columns={"unemployment_rate": "u_end"})
delta_df = base.merge(end, on="iso3").dropna()
delta_df["delta_u"] = delta_df["u_end"] - delta_df["u_base"]
delta_df["is_adopter"] = delta_df["iso3"].isin(adopters)
delta_df["is_td"] = delta_df["iso3"].isin(tourism_dep)
delta_df["group"] = delta_df.apply(
    lambda r: ("TD+Adopter" if r["is_td"] and r["is_adopter"]
               else "TD+Non-adopter" if r["is_td"]
               else "Non-TD+Adopter" if r["is_adopter"]
               else "Non-TD+Non-adopter"), axis=1
)

order   = ["TD+Adopter", "TD+Non-adopter", "Non-TD+Adopter", "Non-TD+Non-adopter"]
colors  = [NAT_BLUE, NAT_LTBLUE, NAT_RED, NAT_ORANGE]
labels  = ["TD\nAdopter", "TD\nNon-adopter", "Non-TD\nAdopter", "Non-TD\nNon-adopter"]

positions = np.arange(len(order))
for i, (grp, col, lbl) in enumerate(zip(order, colors, labels)):
    vals = delta_df[delta_df["group"] == grp]["delta_u"].dropna()
    if len(vals) > 0:
        bp = ax.boxplot(vals, positions=[i], widths=0.55,
                        patch_artist=True,
                        boxprops=dict(facecolor=col, alpha=0.75, linewidth=0.6),
                        medianprops=dict(color="black", linewidth=1.2),
                        whiskerprops=dict(linewidth=0.6),
                        capprops=dict(linewidth=0.6),
                        flierprops=dict(marker=".", ms=2.5, alpha=0.5, color=col))
        n = len(vals)
        ax.text(i, ax.get_ylim()[0] if ax.get_ylim()[0] > -20 else -12,
                f"n={n}", ha="center", fontsize=5.5, color="#555")

ax.axhline(0, color="black", lw=0.6, ls="--", alpha=0.5)
ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=5.5)
ax.set_ylabel("Δ Unemployment rate 2019→2022 (pp)")
ax.set_title("Unemployment change 2019→2022\nby tourism-dependence & adoption status", pad=4)

td_patch   = mpatches.Patch(color=NAT_BLUE, alpha=0.75, label="Tourism-dependent (TD)")
ntd_patch  = mpatches.Patch(color=NAT_RED,  alpha=0.75, label="Non-TD")
ax.legend(handles=[td_patch, ntd_patch], frameon=False, fontsize=6)
panel_label(ax, "b")


fig2.savefig("Fig2_Q2_unemployment_recovery.pdf", dpi=300, bbox_inches="tight")
fig2.savefig("Fig2_Q2_unemployment_recovery.png", dpi=300, bbox_inches="tight")
print("Figure 2 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – Q3: Business-to-leisure ratio structural break
# ══════════════════════════════════════════════════════════════════════════════
fig3, axes3 = plt.subplots(1, 2, figsize=(7.2, 2.9))
fig3.subplots_adjust(wspace=0.42)

macro["leisure"] = macro["arrivals_total"] - macro["arrivals_business"].fillna(0)
macro["biz_leisure"] = macro["arrivals_business"] / macro["leisure"].replace(0, np.nan)

# ── 3a. Global trend: mean B/L ratio, adopters vs non-adopters ───────────────
ax = axes3[0]
years_r = list(range(2010, 2023))
rec3 = []
for yr in years_r:
    sub = macro[(macro["year"] == yr) & macro["biz_leisure"].notna() & (macro["biz_leisure"] < 10)]
    for grp, lbl, col in [(True, "Adopter", NAT_BLUE), (False, "Non-adopter", NAT_GRAY)]:
        s = sub[sub["is_adopter"] == grp]["biz_leisure"]
        if len(s) > 2:
            rec3.append({"year": yr, "label": lbl, "mean": s.mean(), "sem": s.sem()})
r3 = pd.DataFrame(rec3)

for lbl, col, ls, mk in [("Adopter", NAT_BLUE, "-", "o"), ("Non-adopter", NAT_GRAY, "--", "s")]:
    sub_r = r3[r3["label"] == lbl]
    ax.fill_between(sub_r["year"],
                    sub_r["mean"] - 1.96*sub_r["sem"],
                    sub_r["mean"] + 1.96*sub_r["sem"],
                    alpha=0.15, color=col)
    ax.plot(sub_r["year"], sub_r["mean"], ls, color=col, marker=mk, ms=3.5,
            label=lbl, lw=1.1)

# shade adoption wave
ax.axvspan(2020, 2022, alpha=0.08, color=NAT_RED)
ax.text(2020.1, ax.get_ylim()[1] * 0.98 if len(r3) > 0 else 0.3,
        "Adoption\nwave", fontsize=5.5, color=NAT_RED, va="top")
ax.set_xlabel("Year")
ax.set_ylabel("Business / leisure arrivals ratio")
ax.set_title("Business-to-leisure arrival ratio\nover time", pad=4)
ax.legend(frameon=False)
panel_label(ax, "a")

# ── 3b. Radar / scatter: adoption year vs ratio change per country ────────────
ax = axes3[1]

# Compute pre/post B/L ratio change for each adopter
ratio_changes = []
for iso, yr in adoption_map.items():
    pre  = macro[(macro["iso3"] == iso) & (macro["year"].between(yr-3, yr-1)) & macro["biz_leisure"].notna()]["biz_leisure"]
    post = macro[(macro["iso3"] == iso) & (macro["year"].between(yr, yr+3))  & macro["biz_leisure"].notna()]["biz_leisure"]
    col_row = policy[policy["iso3"] == iso]
    if len(pre) >= 1 and len(post) >= 1:
        ratio_changes.append({
            "iso3": iso,
            "country": col_row["country_name"].values[0] if len(col_row) else iso,
            "pre_mean": pre.mean(),
            "post_mean": post.mean(),
            "delta": post.mean() - pre.mean(),
            "adoption_year": yr,
            "min_income": col_row["min_income_to_apply_per_month"].values[0] if len(col_row) else np.nan,
        })

rc_df = pd.DataFrame(ratio_changes)
if len(rc_df) > 0:
    colors_rc = [NAT_BLUE if d > 0 else NAT_RED for d in rc_df["delta"]]
    scatter = ax.scatter(rc_df["adoption_year"] + np.random.uniform(-0.2, 0.2, len(rc_df)),
                         rc_df["delta"],
                         c=colors_rc, s=40, alpha=0.85, edgecolors="white", lw=0.4, zorder=5)
    ax.axhline(0, color="black", lw=0.6, ls="--", alpha=0.5)

    # annotate a few notable ones
    top_pos = rc_df.nlargest(2, "delta")
    top_neg = rc_df.nsmallest(2, "delta")
    for _, row in pd.concat([top_pos, top_neg]).iterrows():
        ax.annotate(row["country"], (row["adoption_year"], row["delta"]),
                    fontsize=5, xytext=(4, 3), textcoords="offset points", color="#333")

    ax.set_xlabel("Visa adoption year")
    ax.set_ylabel("Δ Business/leisure ratio (post − pre)")
    ax.set_title("Per-country change in B/L ratio\naround visa adoption", pad=4)

    pos_patch = mpatches.Patch(color=NAT_BLUE, alpha=0.85, label="Ratio increased post-adoption")
    neg_patch = mpatches.Patch(color=NAT_RED,  alpha=0.85, label="Ratio decreased post-adoption")
    ax.legend(handles=[pos_patch, neg_patch], frameon=False, fontsize=6)

panel_label(ax, "b")


fig3.savefig("Fig3_Q3_biz_leisure_ratio.pdf", dpi=300, bbox_inches="tight")
fig3.savefig("Fig3_Q3_biz_leisure_ratio.png", dpi=300, bbox_inches="tight")
print("Figure 3 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 – Q4: Structural reliance – tourism GDP share persistence
# ══════════════════════════════════════════════════════════════════════════════
fig4, axes4 = plt.subplots(1, 2, figsize=(7.2, 2.9))
fig4.subplots_adjust(wspace=0.42)

# ── 4a. Tourism GDP share recovery trajectory, 2019-2023 ─────────────────────
ax = axes4[0]
years_g = list(range(2019, 2024))
rec4 = []
for yr in years_g:
    sub = macro[(macro["year"] == yr) & macro["tourism_gdp_share"].notna()]
    for grp, lbl, col in [(True, "Adopter", NAT_BLUE), (False, "Non-adopter", NAT_GRAY)]:
        s = sub[sub["is_adopter"] == grp]["tourism_gdp_share"]
        if len(s) > 2:
            rec4.append({"year": yr, "label": lbl, "mean": s.mean(), "sem": s.sem(), "n": len(s)})
r4 = pd.DataFrame(rec4)

for lbl, col, ls, mk in [("Adopter", NAT_BLUE, "-", "o"), ("Non-adopter", NAT_GRAY, "--", "s")]:
    sub_r = r4[r4["label"] == lbl]
    if len(sub_r) > 0:
        ax.fill_between(sub_r["year"],
                        sub_r["mean"] - 1.96*sub_r["sem"],
                        sub_r["mean"] + 1.96*sub_r["sem"],
                        alpha=0.18, color=col)
        ax.plot(sub_r["year"], sub_r["mean"], ls, color=col, marker=mk,
                ms=4, label=lbl, lw=1.1)

ax.axvline(2020, color="black", lw=0.7, ls=":", alpha=0.5)
ax.set_xlabel("Year")
ax.set_ylabel("Tourism / GDP share (%)")
ax.set_title("Tourism-GDP share recovery\n(2019–2023)", pad=4)
ax.legend(frameon=False)
ax.text(2020.05, ax.get_ylim()[1]*0.97 if len(r4) > 0 else 5, "COVID", fontsize=5.5, color="#555", va="top")
panel_label(ax, "a")

# ── 4b. Tourism GDP share: level and 2019-base index, 2021-23 adopters ───────
ax = axes4[1]

# Normalise to 2019 = 100 for each country
tgdp_pivot = macro.pivot_table(index="iso3", columns="year", values="tourism_gdp_share")
base_vals  = tgdp_pivot.get(2019, pd.Series(dtype=float))
normed = tgdp_pivot.div(base_vals, axis=0) * 100

# Select countries with good 2019 data & multiple post years
good_isos = base_vals.dropna().index
years_idx = [yr for yr in [2020, 2021, 2022, 2023] if yr in normed.columns]

rec4b = []
for yr in years_idx:
    col_data = normed[yr].dropna()
    col_data = col_data[col_data.index.isin(good_isos)]
    for grp, lbl, col in [(adopters, "Adopter", NAT_BLUE), (set(macro["iso3"]) - adopters, "Non-adopter", NAT_GRAY)]:
        s = col_data[col_data.index.isin(grp)]
        if len(s) > 2:
            rec4b.append({"year": yr, "label": lbl, "mean": s.mean(), "sem": s.sem(), "n": len(s)})
r4b = pd.DataFrame(rec4b)

for lbl, col, ls, mk in [("Adopter", NAT_BLUE, "-", "o"), ("Non-adopter", NAT_GRAY, "--", "s")]:
    sub_r = r4b[r4b["label"] == lbl]
    if len(sub_r) > 0:
        ax.fill_between(sub_r["year"],
                        sub_r["mean"] - 1.96*sub_r["sem"],
                        sub_r["mean"] + 1.96*sub_r["sem"],
                        alpha=0.18, color=col)
        ax.plot(sub_r["year"], sub_r["mean"], ls, color=col, marker=mk,
                ms=4, label=lbl, lw=1.1)
        for _, row in sub_r.iterrows():
            ax.text(row["year"], row["mean"] + 1.5, f"n={int(row['n'])}", ha="center", fontsize=5, color=col)

ax.axhline(100, color="black", lw=0.7, ls="--", alpha=0.5)
ax.text(years_idx[0] + 0.05, 101, "2019 baseline", fontsize=5.5, color="#555")
ax.set_xlabel("Year")
ax.set_ylabel("Tourism/GDP index (2019 = 100)")
ax.set_title("Post-COVID tourism-GDP index:\nadopters vs. non-adopters", pad=4)
ax.legend(frameon=False)
panel_label(ax, "b")

fig4.savefig("Fig4_Q4_structural_reliance.pdf", dpi=300, bbox_inches="tight")
fig4.savefig("Fig4_Q4_structural_reliance.png", dpi=300, bbox_inches="tight")
print("Figure 4 saved.")
