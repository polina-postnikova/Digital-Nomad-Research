#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
OUT="$ROOT/Reproducibility/generated"
WORK="$ROOT/Reproducibility/work"
rm -rf "$OUT" "$WORK"
mkdir -p "$OUT/results" "$OUT/figures" "$WORK"

printf '\n[1/5] Main staggered-adoption analysis\n'
"$PYTHON_BIN" "$ROOT/Scripts/Results/staggered_adoption_sensitivity.py" \
  --audit "$ROOT/Data/Intermediate/Audit_Stage1_Stage2.csv" \
  --panel "$ROOT/Data/Processed/DigitalNomadDataset.xlsx" \
  --output-dir "$OUT/results" \
  --sim-reps "${SIM_REPS:-200}" \
  --sim-beta -1.0 \
  --seed 12345

printf '\n[2/5] Tourism cross-validation\n'
mkdir -p "$WORK/cross_validation"
cp "$ROOT/Data/Processed/DigitalNomadDataset.xlsx" "$WORK/cross_validation/DigitalNomadDataset.xlsx"
(
  cd "$WORK/cross_validation"
  "$PYTHON_BIN" "$ROOT/Scripts/CrossValidation.py"
)
cp "$WORK/cross_validation/arrival_expenditure_validation.csv" "$OUT/results/arrival_expenditure_validation.csv"

printf '\n[3/5] Missingness audit\n'
mkdir -p "$WORK/missingness"
cp "$ROOT/Data/Processed/DigitalNomadDataset.xlsx" "$WORK/missingness/DigitalNomadDataset.xlsx"
(
  cd "$WORK/missingness"
  "$PYTHON_BIN" "$ROOT/Scripts/MissingnessAudit.py"
)
cp "$ROOT/Data/Processed/DigitalNomadDataset.xlsx" "$WORK/missingness/DigitalNomadDataset.xlsx"
( cd "$WORK/missingness" && PYTHONPATH="$ROOT/Figs" "$PYTHON_BIN" "$ROOT/Figs/missingness.py" )
cp "$WORK/missingness/missingness.svg" "$OUT/figures/missingness.svg"

printf '\n[4/5] Research figures\n'
cp "$OUT/results/cs_event_time_associations.csv" "$WORK/cs_event_time_associations.csv"
cp "$OUT/results/twfe_benchmark.csv" "$WORK/twfe_benchmark.csv"
cp "$ROOT/Data/Processed/DigitalNomadDataset.xlsx" "$WORK/DigitalNomadDataset.xlsx"
(
  cd "$WORK"
  PYTHONPATH="$ROOT/Figs" "$PYTHON_BIN" "$ROOT/Figs/event_study.py"
  PYTHONPATH="$ROOT/Figs" "$PYTHON_BIN" "$ROOT/Figs/twfe_vs_cs.py"
  PYTHONPATH="$ROOT/Figs" "$PYTHON_BIN" "$ROOT/Figs/thailand_vietnam.py"
)
cp "$WORK/event_study.svg" "$OUT/figures/event_study.svg"
cp "$WORK/twfe_vs_cs.svg" "$OUT/figures/twfe_vs_cs.svg"
cp "$WORK/thailand_vietnam.svg" "$OUT/figures/thailand_vietnam.svg"

printf '\n[5/5] Reproduction complete\n'
printf 'Results: %s\n' "$OUT/results"
printf 'Figures: %s\n' "$OUT/figures"
