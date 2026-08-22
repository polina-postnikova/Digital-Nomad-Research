import pandas as pd
import matplotlib.pyplot as plt

from style_config import (
    apply_style,
    add_panel_label,
    add_source_note,
    export_svg,
    CS_COLOR,
    TWFE_COLOR,
    NEUTRAL_COLOR,
    CI_LINEWIDTH,
    CAP_SIZE,
    MM_TO_IN,
)

apply_style()

twfe = pd.read_csv("twfe_benchmark.csv").iloc[0]
cs = pd.read_csv("cs_event_time_associations.csv").sort_values("event_time")

rows = []
rows.append({
    "label": f"TWFE - pooled\n(n={int(twfe.n_obs)} obs, {int(twfe.n_countries)} countries)",
    "estimate": twfe.estimate, "lo": twfe.ci_low, "hi": twfe.ci_high,
    "color": TWFE_COLOR, "group": "TWFE",
})
for _, r in cs.iterrows():
    rows.append({
        "label": f"CS - event time {int(r.event_time)}\n"
                 f"(n={int(r.n_cohorts)} cohorts, {int(r.n_treated_country_observations)} obs)",
        "estimate": r.estimate, "lo": r.ci_low, "hi": r.ci_high,
        "color": CS_COLOR, "group": "CS",
    })

fig, ax = plt.subplots(figsize=(150 * MM_TO_IN, 100 * MM_TO_IN), layout="constrained")

y_positions = list(range(len(rows)))[::-1]
ax.axvline(0, color=NEUTRAL_COLOR, lw=0.9, ls="--", alpha=0.6, zorder=1)

for ypos, row in zip(y_positions, rows):
    ax.errorbar(
        row["estimate"], ypos, xerr=[[row["estimate"] - row["lo"]], [row["hi"] - row["estimate"]]],
        fmt="o", color=row["color"], elinewidth=CI_LINEWIDTH, capsize=CAP_SIZE,
        capthick=CI_LINEWIDTH, markeredgecolor="white", markeredgewidth=0.9,
        markersize=7, zorder=3,
    )

divider_y = y_positions[0] - 0.5  
ax.axhline(divider_y, color="#BBBBBB", lw=0.8, zorder=0)
ax.axhspan(divider_y, max(y_positions) + 0.6, color=TWFE_COLOR, alpha=0.06, zorder=0)
ax.axhspan(min(y_positions) - 0.6, divider_y, color=CS_COLOR, alpha=0.06, zorder=0)

ax.set_yticks(y_positions)
ax.set_yticklabels([r["label"] for r in rows], fontsize=7.6)
ax.set_xlabel("Estimated effect on log GDP")

export_svg(fig, "twfe_vs_cs.svg")
