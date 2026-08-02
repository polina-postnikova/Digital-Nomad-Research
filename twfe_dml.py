import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
import statsmodels.api as sm

np.random.seed(42)

macro = pd.read_excel('DigitalNomadDataset.xlsx', sheet_name='tourism_and_macroeconomic_data')
hv = pd.read_excel('PolicyValidation.xlsx', sheet_name='verified')
ai = pd.read_excel('PolicyValidation.xlsx', sheet_name='AI_extraction').dropna(how='all', axis=1)
ai = ai.rename(columns={'min_income_month':'min_income_to_apply_per_month'})

macro_countries = set(macro['iso3'])
hv = hv[hv['iso3'].isin(macro_countries)].copy()
ai = ai[ai['iso3'].isin(macro_countries)].copy()

mismatch_iso3 = set(hv.merge(ai[['iso3','visa_adoption_year']], on='iso3', suffixes=('_hv','_ai'))
                     .query('visa_adoption_year_hv != visa_adoption_year_ai')['iso3'])

def build_panel(policy_df):
    df = macro.copy()
    pol = policy_df.set_index('iso3')
    adopt_year = pol['visa_adoption_year'].to_dict()
    df['adopt_year'] = df['iso3'].map(adopt_year)
    df['D'] = ((df['adopt_year'].notna()) & (df['year'] >= df['adopt_year'])).astype(int)
    return df

panel_hv = build_panel(hv)
panel_ai = build_panel(ai)
panel_ea = build_panel(ai[~ai['iso3'].isin(mismatch_iso3)])
panel_ea.loc[panel_ea['iso3'].isin(mismatch_iso3), 'D'] = 0  # excluded from treated set, kept as controls

MACRO_COVS = ['internet_usage_pct', 'inflation_annual_pct', 'exchange_rate_lcu_per_usd', 'price_level_index_gdp']

def prep(df):
    df = df.copy()
    df['log_gdp'] = np.log(df['gdp'])
    for c in MACRO_COVS + ['log_gdp']:
        df[c] = df[c].fillna(df[c].median())
    return df

panel_hv, panel_ai, panel_ea = prep(panel_hv), prep(panel_ai), prep(panel_ea)

def within_demean(df, cols):
    out = {}
    for c in cols:
        gi = df.groupby('iso3')[c].transform('mean')
        gt = df.groupby('year')[c].transform('mean')
        grand = df[c].mean()
        out[c + '_tilde'] = df[c] - gi - gt + grand
    return pd.DataFrame(out, index=df.index)

def dml_estimate(df, outcome, cov_cols, n_splits=5, n_estimators=400):
    df = df.dropna(subset=[outcome]).copy()
    covs = [c for c in cov_cols if c != outcome]
    tilde = within_demean(df, [outcome, 'D'] + covs)
    X = tilde[[c + '_tilde' for c in covs]].values
    Y = tilde[outcome + '_tilde'].values
    Dv = tilde['D_tilde'].values
    groups = df['iso3'].values

    gkf = GroupKFold(n_splits=n_splits)
    resid_Y = np.zeros_like(Y); resid_D = np.zeros_like(Dv)
    for train_idx, test_idx in gkf.split(X, Y, groups):
        m_y = RandomForestRegressor(n_estimators=n_estimators, max_depth=4, min_samples_leaf=20, random_state=0)
        m_d = RandomForestRegressor(n_estimators=n_estimators, max_depth=4, min_samples_leaf=20, random_state=1)
        m_y.fit(X[train_idx], Y[train_idx]); m_d.fit(X[train_idx], Dv[train_idx])
        resid_Y[test_idx] = Y[test_idx] - m_y.predict(X[test_idx])
        resid_D[test_idx] = Dv[test_idx] - m_d.predict(X[test_idx])

    Xfinal = sm.add_constant(resid_D)
    model = sm.OLS(resid_Y, Xfinal).fit(cov_type='cluster', cov_kwds={'groups': df['iso3'].values})
    ci = model.conf_int()[1]
    return dict(beta=model.params[1], se=model.bse[1], ci_low=ci[0], ci_high=ci[1], p=model.pvalues[1],
                n_obs=len(df), n_countries=df['iso3'].nunique())

def twfe_estimate(df, outcome, cov_cols=None):
    df = df.dropna(subset=[outcome]).copy()
    cov_cols = [c for c in (cov_cols or []) if c != outcome]
    tilde = within_demean(df, [outcome, 'D'] + cov_cols)
    X = tilde[['D_tilde'] + [c+'_tilde' for c in cov_cols]]
    X = sm.add_constant(X)
    Y = tilde[outcome + '_tilde']
    model = sm.OLS(Y, X).fit(cov_type='cluster', cov_kwds={'groups': df['iso3'].values})
    ci = model.conf_int().loc['D_tilde']
    return dict(beta=model.params['D_tilde'], se=model.bse['D_tilde'], ci_low=ci[0], ci_high=ci[1],
                p=model.pvalues['D_tilde'], n_obs=len(df), n_countries=df['iso3'].nunique())

results = []
outcomes = [('unemployment_rate', ['log_gdp']+MACRO_COVS),
            ('log_gdp', MACRO_COVS),
            ('tourism_gdp_share', ['log_gdp']+MACRO_COVS)]
for name, panel in [('hand_verified', panel_hv), ('llm_extracted', panel_ai), ('error_aware_llm_subset', panel_ea)]:
    for outcome, covs in outcomes:
        r_twfe_bivar = twfe_estimate(panel, outcome, cov_cols=[])
        r_twfe_cov = twfe_estimate(panel, outcome, cov_cols=covs)
        r_dml = dml_estimate(panel, outcome, covs)
        results.append(dict(data=name, outcome=outcome, method='TWFE (bivariate, as in original Table 4)', **r_twfe_bivar))
        results.append(dict(data=name, outcome=outcome, method='TWFE + macro controls', **r_twfe_cov))
        results.append(dict(data=name, outcome=outcome, method='DML (RF nuisances, macro controls)', **r_dml))

res_df = pd.DataFrame(results)
pd.set_option('display.width', 220)
print(res_df.round(4).to_string())
