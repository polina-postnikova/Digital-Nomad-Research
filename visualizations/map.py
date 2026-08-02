import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

file_path = 'DigitalNomadDataset.xlsx'
tourism_df = pd.read_excel(file_path, sheet_name='tourism_and_macroeconomic_data')
policy_df = pd.read_excel(file_path, sheet_name='policy_data')

tourism_2019 = tourism_df[tourism_df['year'] == 2019][['iso3', 'tourism_gdp_share']]

merged_data = pd.merge(policy_df, tourism_2019, on='iso3', how='left')

world = gpd.read_file('custom.geo-2.json')

world_merged = world.merge(merged_data, left_on='iso_a3', right_on='iso3', how='left')

world_merged['centroid'] = world_merged.geometry.representative_point()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
fig, ax = plt.subplots(figsize=(15, 10), dpi=300)

world.plot(ax=ax, color='#f0f0f0', edgecolor='#d9d9d9', linewidth=0.5)

target_countries = world_merged[world_merged['iso3'].notna()]

vmax = target_countries['tourism_gdp_share'].max()
vmin = target_countries['tourism_gdp_share'].min()

target_countries.plot(
    column='tourism_gdp_share',
    ax=ax,
    cmap='YlGnBu',
    legend=False,
    edgecolor='white',
    linewidth=0.5,
    missing_kwds={'color': '#f0f0f0'}
)

missing_in_geo = target_countries[target_countries.geometry.is_empty | target_countries.geometry.isna()]
if not missing_in_geo.empty:
    print(f"Warning: {len(missing_in_geo)} countries from policy data not found in GeoJSON.")

years = sorted([y for y in policy_df['visa_adoption_year'].unique() if not np.isnan(y)])
color_palette = plt.colormaps.get_cmap('YlOrRd')
norm_years = plt.Normalize(min(years), max(years))

for idx, row in target_countries.iterrows():
    if not np.isnan(row['visa_adoption_year']):
        ax.scatter(
            row.centroid.x, row.centroid.y,
            color=color_palette(norm_years(row['visa_adoption_year'])),
            s=80,
            edgecolor='black',
            linewidth=0.8,
            alpha=1.0,
            zorder=5
        )

sm = plt.cm.ScalarMappable(cmap='YlGnBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []
cbar = fig.colorbar(sm, ax=ax, shrink=0.4, orientation='horizontal', pad=0.02, aspect=30)
cbar.set_label('Tourism GDP Share in 2019 (%)', fontsize=11, labelpad=10)
cbar.ax.tick_params(labelsize=10)


from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label=str(int(year)),
           markerfacecolor=color_palette(norm_years(year)), markersize=10, markeredgecolor='black', markeredgewidth=0.8)
    for year in years
]
legend2 = ax.legend(
    handles=legend_elements,
    title='Visa Adoption Year',
    loc='lower left',
    fontsize=10,
    title_fontsize=11,
    frameon=True,
    edgecolor='#d9d9d9',
    bbox_to_anchor=(0.05, 0.15)
)
ax.add_artist(legend2)


ax.set_axis_off()
plt.title('Global Distribution of Digital Nomad Policies and Tourism Economic Significance',
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()

output_path = 'digital_nomad_map.png'
plt.savefig(output_path, bbox_inches='tight')
print(f"Map saved to {output_path}")
