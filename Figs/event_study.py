import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from style_config import (
    apply_style,
    add_panel_label,
    add_source_note,
    export_svg,
    CS_COLOR,
    NEUTRAL_COLOR,
    CI_LINEWIDTH,
    CAP_SIZE,
    MM_TO_IN,
)

apply_style()

df = pd.read_csv("cs_event_time_associations.csv").sort_values("event_time")

fig, ax = plt.subplots(figsize=(150 * MM_TO_IN, 100 * MM_TO_IN), layout="constrained")

x = df["event_time"].to_numpy()
y = df["estimate"].to_numpy()
lo = df["ci_low"].to_numpy()
hi = df["ci_high"].to_numpy()
n_obs = df["n_treated_country_observations"].to_numpy()
n_coh = df["n_cohorts"].to_numpy()

size_ref = 260
sizes = size_ref * (n_obs / n_obs.max())

ax.axhline(0, color=NEUTRAL_COLOR, lw=0.9, ls="--", alpha=0.6, zorder=1)

ax.errorbar(
    x, y, yerr=[y - lo, hi - y],
    fmt="none", ecolor=CS_COLOR, elinewidth=CI_LINEWIDTH, capsize=CAP_SIZE,
    capthick=CI_LINEWIDTH, zorder=2,
)
ax.plot(x, y, color=CS_COLOR, lw=1.4, alpha=0.55, zorder=2)
ax.scatter(
    x, y, s=sizes, color=CS_COLOR, edgecolor="white", linewidth=0.9,
    zorder=3, label="CS estimate (95% CI)",
)

for xi, yi, hii, nc, no in zip(x, y, hi, n_coh, n_obs):
    ax.annotate(
        f"n$_{{cohorts}}$={nc}\nn$_{{obs}}$={no}",
        (xi, hii),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        va="bottom",
        fontsize=6.6,
        color="#333333",
    )

ax.set_xticks(x)
ax.set_xlim(-0.6, x.max() + 0.6)
ax.set_xlabel("Event time (years since treatment start; 0 = first full exposure year)")
ax.set_ylabel("ATT on log GDP (Callaway-Sant'Anna)")
ax.text(
    0.015, 0.03,
    "No pre-treatment (event_time < 0) estimates are available in this specification;\n"
    "the plot begins at event_time = 0 by construction, not by omission.",
    transform=ax.transAxes, fontsize=6.8, style="italic", color="#555555", va="bottom",
)


export_svg(fig, "event_study.svg")
