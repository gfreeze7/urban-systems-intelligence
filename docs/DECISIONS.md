# Decisions

[README](../README.md) · [Project Brief](PROJECT_BRIEF.md) · [Architecture](ARCHITECTURE.md) · [Data Sources](DATA_SOURCES.md)

## 1. Test hypotheses rather than confirm a narrative

*The Wire* supplies questions about interconnected systems. The evidence matrix preserves `SUPPORTED`, `COMPLICATED`, `CONTRADICTED`, and `UNRESOLVED` outcomes, with a limitation for every hypothesis. This makes mixed evidence visible instead of forcing agreement with the show's diagnosis. States are curated interpretations and need explicit review when analyses change.

## 2. Separate geography from observations in PostgreSQL

Census tract identity is stored separately from observations keyed by GEOID, vintage, dataset, and variable. BNIA keeps geography-year records and long-form indicator observations. This preserves time and source identity instead of overwriting a geography row with a single timeless measure. The tradeoff is joins and an explicit schema/migration sequence; apply that sequence to an empty database as documented in the README.

## 3. Preserve raw values and missingness

BNIA stores raw and cleaned values; nonnumeric cells become missing rather than fabricated zeros. Entirely empty/sentinel columns are skipped. Analyses use available data and model-specific complete cases, so coverage and sample sizes require interpretation. A 770-row BI export does not imply 770 valid observations for every variable.

## 4. Make repeat loading and failures observable

Census observation loading distinguishes inserts, changes, and unchanged values. BNIA and the crosswalk use upserts. Per-loader transactions, failure records, and stale-run handling support recovery, but the master run is not atomic across stages and does not remove records deleted upstream. Master record-count metrics currently cover Census only. These limits matter when interpreting operational success.

## 5. Keep spatial and temporal reconciliation explicit

A tract2020-to-CSA2010 crosswalk preserves geography labels without inventing interpolation weights. ACS source vintage and BNIA annual year are retained separately; a matching label is not proof of contemporaneous measurement. The current CSA models use BNIA rather than a silently aligned cross-source merge. See [Data Sources](DATA_SOURCES.md) and [Time Reconciliation](time_reconciliation.md).

## 6. Use several observational checks without claiming causality

Yearly correlations, OLS, standardized coefficients, HC3 errors, VIF, influence diagnostics, sensitivity tests, first differences, and interactions examine stability and complications. None identifies causal effects by itself. Ecological demographic relationships cannot establish individual racial effects, and strongly inversely related population shares are not independent evidence. External intervention studies remain a separate register with their own causal scope and limitations.

## 7. Make CI deterministic without treating fixtures as evidence

The [workflow](../.github/workflows/ci.yml) provisions PostgreSQL 17 and applies schema/migrations before tests. The [seed](../tests/seed_ci_database.py) supplies a fixed Census observation and 55 synthetic CSAs across 14 years with the nine required BI indicators. Running it as `python -m tests.seed_ci_database` uses the repository's module context. This removes dependence on a developer's populated database while retaining integration assertions.

Synthetic values verify behavior and BI shape, not Baltimore findings. Seed only a separate test database; never mix fixtures with the analytical source data. CI performs automated testing, not continuous deployment. Phase 9's 46/46 result is historical evidence, not a guarantee of current execution everywhere.

## 8. Limit cloud and BI claims to demonstrated execution

[Phase 9](phase_9_evidence.md) records private ACR storage and managed-identity Container Apps Job validation with a runtime Census secret. Azure PostgreSQL was not deployed, so this is ingestion/validation evidence rather than an end-to-end cloud database deployment. Cloud provisioning configuration is not included.

Power BI Desktop was completed; Service publication was attempted but not demonstrated. The recorded PBIX is absent from this checkout. The CSV export can be regenerated with the required inputs and database; reproducing the original report requires the separate PBIX.

## 9. Use local AI for evidence-aware communication

Ollama with `llama3.2:3b` receives the curated hypothesis matrix and prompt constraints. This permits local synthesis without a paid model API. It does not generate analytical evidence, automatically update evidence states, or verify its own statements; human review remains necessary. The model is an optional reporting component outside the ingestion Docker image.

## 10. Keep credentials and bulky data out of Git

`.env`, virtual environments, caches, and raw/processed data are ignored; placeholders preserve directory structure. Runtime configuration supplies secrets. Docker separately excludes secrets and development artifacts but copies raw source files, so its build context needs review. Missing source download metadata/checksums and the absent PBIX limit clone-only reproducibility; the documentation discloses those gaps rather than claiming a self-contained deployment.
