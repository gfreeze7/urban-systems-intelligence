# Architecture

[README](../README.md) · [Project Brief](PROJECT_BRIEF.md) · [Data Sources](DATA_SOURCES.md) · [Decisions](DECISIONS.md)

## Data and execution flow

```text
Census ACS API ───────┐
BNIA workbook ────────┼→ ingestion validation / transformation → PostgreSQL
Tract–CSA crosswalk ──┘                                         │
                                      separately invoked BNIA analytics
                                              ├→ terminal model summaries
                                              ├→ figures
                                              └→ CSA-year CSV → Power BI Desktop

Curated hypothesis evidence → matrix CSV / local Ollama briefing
External intervention studies → separate intervention register CSV
```

The current analytics query BNIA observations. Census and crosswalk storage do not imply that ACS measurements have been joined into the CSA-year models. The evidence matrix encodes recorded interpretations; exporting it does not rerun regressions.

## Components and storage

| Component | Responsibility |
| --- | --- |
| `src/ingestion/` | Fetch Census data; read BNIA workbook/crosswalk; validate schemas, keys, geography, and values |
| `src/database/` | Database connections, transactional loads, and pipeline status tracking |
| `src/orchestration/pipeline.py` | Census → BNIA → crosswalk stages; database or cloud-validation mode |
| `src/analytics/` | Analytical datasets, models, figures, BI export, and curated evidence registers |
| `ai/ai_briefing.py` | Supply hypothesis/evidence/state/limitation fields to local Ollama |
| `.github/workflows/ci.yml` | PostgreSQL-backed automated tests with deterministic seed data |

The [schema](../database/schema/001_create_census_tracts.sql) and subsequent files/migrations separate geographic identity from time-varying observations:

| Table | Grain/key |
| --- | --- |
| `census_tracts` | Tract GEOID |
| `census_acs_observations` | GEOID × year × dataset × variable |
| `bnia_geographies` | Year × CSA2010, with CSA2020 label when supplied and citywide flag |
| `bnia_observations` | Year × CSA2010 × source indicator number × source indicator name |
| `tract2020_to_csa2010` | 2020 tract GEOID mapped to a CSA2010 label |
| `pipeline_runs` | Run identifier, timestamps, status, errors, and record metrics |

Census observation loading distinguishes inserted, updated, and unchanged values. BNIA and crosswalk loaders use conflict upserts. Each loader commits or rolls back its own transaction; the entire orchestration is not one atomic transaction, so earlier successful stages remain committed after a later failure. Source deletions are not reconciled by these upserts.

The orchestrator marks stale runs and records overall success/failure. Its record-count metrics currently describe **Census observations only**, not total work across all three stages.

## Runtime modes

Default database mode (`python -m src.orchestration.pipeline`) uses `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `CENSUS_API_KEY`, loaded from the environment/`.env`. The [PowerShell launcher](../run_pipeline.ps1) invokes the repository's virtual-environment Python and propagates failure status. Daily Windows Task Scheduler execution is recorded in Phase 9; task registration is not included as deployable configuration.

`PIPELINE_MODE=cloud_validation` fetches Census data and validates it alongside the packaged workbook and crosswalk. This mode does not load PostgreSQL or write database run records. Reset the variable to `database` before a database-mode run.

The [Dockerfile](../Dockerfile) uses Python 3.14, installs pinned dependencies, and copies `src/` and `data/`. CI uses Python 3.13. Raw input files must exist in the build context; `.dockerignore` excludes processed outputs, secrets, tests, and docs. The image does not include `ai/`, so the AI briefing runs separately. A successful image build alone does not prove source availability or database connectivity.

Phase 9 records a private ACR image pulled by an Azure Container Apps Job using managed identity and `AcrPull`, with the Census key supplied through a runtime secret reference. Validation reported 199 Census records, 104,272 BNIA observations, 784 geography-year records, and 199 crosswalk records. **No Azure PostgreSQL deployment or cloud database write was demonstrated.** Azure provisioning configuration is not present in this repository.

## Analytics, BI, and AI

Run analytical modules separately after loading real source data, following the [README sequence](../README.md#reproduce). BI export writes `data/processed/bi/baltimore_csa_year.csv`; evidence exports use `data/processed/analytics/`; plots use `data/processed/figures/`. Model modules print their summaries.

Phase 9 records Power BI Desktop transformations, DAX measures, filters, KPIs, and visualizations. The saved PBIX is absent from this checkout, and Service publication was not completed.

Ollama receives the curated hypothesis matrix through a constrained prompt. The prompt requests evidence-state preservation and avoidance of unsupported causality; it is not a factual verification mechanism. External intervention research remains a separate register and is not automatically part of the AI context.

## Verification boundary

CI creates an isolated PostgreSQL 17 database, applies SQL in a fixed order, seeds synthetic records, and runs pytest. This tests code behavior and contracts; it is not a deployment workflow or a re-estimation of real-world findings. Full-suite local reproduction must use a separate test database because seeding and some tests write data. See [README](../README.md#tests-and-repository-hygiene) and the [Phase 9 record](phase_9_evidence.md).
