import pandas as pd
import matplotlib.pyplot as plt

from style_config import (
    apply_style,
    add_panel_label,
    add_source_note,
    export_svg,
    TREATED_COLOR,
    COMPARISON_COLOR,
    NEUTRAL_COLOR,
    MM_TO_IN,
)

apply_style()

bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85)


def annotate_pair(ax, years, series_a, series_b, color_a, color_b, fmt):
    for y, va, vb in zip(years, series_a, series_b):
        if pd.notna(va):
            above = pd.isna(vb) or va >= vb
            offset = (0, 12) if above else (0, -18)
            ax.annotate(
                fmt(va), (y, va), textcoords="offset points", xytext=offset,
                ha="center", va="bottom" if above else "top",
                fontsize=8, color=color_a, fontweight="bold", bbox=bbox_props, zorder=5,
            )
        if pd.notna(vb):
            above = pd.isna(va) or vb > va
            offset = (0, 12) if above else (0, -18)
            ax.annotate(
                fmt(vb), (y, vb), textcoords="offset points", xytext=offset,
                ha="center", va="bottom" if above else "top",
                fontsize=8, color=color_b, fontweight="bold", bbox=bbox_props, zorder=5,
            )


def set_headroom(ax, *series_list, top_pad=0.22, bottom_pad=0.12):
    all_vals = pd.concat([s.dropna() for s in series_list])
    lo, hi = all_vals.min(), all_vals.max()
    span = hi - lo if hi > lo else max(hi, 1) * 0.1
    ax.set_ylim(lo - span * bottom_pad, hi + span * top_pad)


df = pd.read_excel("DigitalNomadDataset.xlsx", sheet_name="tourism_and_macroeconomic_data")
years = [2019, 2020, 2021, 2022, 2023]

tha = df[(df.iso3 == "THA") & (df.year.isin(years))].set_index("year")
vnm = df[(df.iso3 == "VNM") & (df.year.isin(years))].set_index("year")

thailand_tourism = tha["tourism_gdp_share"].reindex(years)
vietnam_tourism = vnm["tourism_gdp_share"].reindex(years)
thailand_unemp = tha["unemployment_rate"].reindex(years)
vietnam_unemp = vnm["unemployment_rate"].reindex(years)

fig, axes = plt.subplots(1, 2, figsize=(160 * MM_TO_IN, 85 * MM_TO_IN), layout="constrained")

ax = axes[0]
ax.axvspan(2019.5, 2021.5, color="#f1f5f9", zorder=0, alpha=0.8)
ax.plot(years, thailand_tourism, "-o", color=TREATED_COLOR, label="Thailand (adopter)", zorder=3)
ax.plot(years, vietnam_tourism, "-o", color=COMPARISON_COLOR, label="Vietnam (non-adopter)", zorder=3)
set_headroom(ax, thailand_tourism, vietnam_tourism)
annotate_pair(ax, years, thailand_tourism, vietnam_tourism, TREATED_COLOR, COMPARISON_COLOR, lambda v: f"{v:.1f}%")
ax.set_xticks(years)
ax.set_ylabel("Tourism direct GDP share (%)")
ax.set_title("Tourism-GDP share", loc="left", pad=15)
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.14), frameon=False)

ax = axes[1]
ax.plot(years, thailand_unemp, "-o", color=TREATED_COLOR, label="Thailand (adopter)", zorder=3)
ax.plot(years, vietnam_unemp, "-o", color=COMPARISON_COLOR, label="Vietnam (non-adopter)", zorder=3)
set_headroom(ax, thailand_unemp, vietnam_unemp)
annotate_pair(ax, years, thailand_unemp, vietnam_unemp, TREATED_COLOR, COMPARISON_COLOR, lambda v: f"{v:.2f}%")
ax.set_xticks(years)
ax.set_ylabel("National unemployment (%)")
ax.set_title("Unemployment", loc="left", pad=15)
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.14), frameon=False)

export_svg(fig, "thailand_vietnam.svg")
