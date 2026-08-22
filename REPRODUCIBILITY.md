# Reproducibility checklist

## Fixed seeds and model settings

The downstream semi-synthetic analysis uses a fixed seed of `12345`, `200` simulation repetitions, and `sim-beta = -1.0` by default. These values are exposed as CLI arguments in `Scripts/Results/staggered_adoption_sensitivity.py` and recorded in `reproducibility.yml`.

The original LLM-assisted audit used GPT-5.6 Luna and was conducted on 2026-08-09. The interactive interface did not expose numeric temperature, top-p, or API-seed settings, so those values are explicitly recorded as `not_recorded` rather than inferred.

## Reproducible environment

Two environment specifications are provided:

- `environment.yml` — Conda environment with pinned Python and package versions.
- `requirements.txt` — pip requirements with pinned versions.

## One-command workflow

From the repository root:

```bash
./run_all.sh
```

This regenerates the main statistical outputs, tourism cross-validation, missingness audit, and the repository's scripted research figures under `Reproducibility/generated/`.

The default workflow uses 200 semi-synthetic repetitions. For a quick smoke test, use `SIM_REPS=2 ./run_all.sh`.

## Manifest

`MANIFEST.csv` maps the repository's reported/generated figures and result files to their generating scripts and input data. Static SVGs for which no source-generation script is included are explicitly marked as such.

## Integrity checks

`checksums.sha256` contains SHA-256 hashes for the released source inputs, documentation, scripts, and reproducibility configuration. Generated outputs are deliberately excluded because some plotting backends can embed non-semantic metadata in SVG files.

Verify with:

```bash
sha256sum -c checksums.sha256
```

## Fresh-environment test

`tests/test_fresh_environment.sh` creates a new Python virtual environment, installs the pinned requirements, runs the full workflow with `SIM_REPS=2`, and checks that the principal result and figure outputs are non-empty.

Run it with:

```bash
bash tests/test_fresh_environment.sh
```
