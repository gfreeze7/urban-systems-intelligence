# Urban Systems Intelligence

A Python and PostgreSQL urban analytics project examining how economic disadvantage, housing, education, and violent crime overlap across Baltimore neighborhoods.

**Test *The Wire*, don't prove *The Wire*.** The show supplies hypotheses; observed data can support, complicate, contradict, or leave them unresolved. The analysis concerns neighborhood associations, not individual behavior or causal effects.

## What the project demonstrates

- Validated ingestion of Census ACS, BNIA Vital Signs, and a tract-to-CSA geographic crosswalk into PostgreSQL.
- CSA-year analytics: correlations, multivariable regression, robust standard errors, influence checks, first differences, and interaction models.
- A BI export covering 55 Community Statistical Areas (CSAs), 2010–2023: 770 CSA-year rows in the recorded run, with indicator-specific missingness.
- Local orchestration, scheduled Windows execution, Docker execution against local PostgreSQL, and GitHub Actions testing with deterministic fixtures.
- Azure Container Registry plus managed-identity Container Apps Job **ingestion/validation**. Azure PostgreSQL was not deployed.
- A completed Power BI Desktop report, as recorded in Phase 9; Power BI Service publication was attempted but not demonstrated. The PBIX is not included in this checkout.
- Local Ollama (`llama3.2:3b`) synthesis of a structured, curated evidence matrix. The model communicates evidence; it does not generate or validate it.

The stack includes Python, pandas, statsmodels, psycopg, PostgreSQL, pytest, Docker, Azure, Power BI, and Ollama. Demonstrated capabilities and counts are documented in the [Phase 9 evidence record](docs/phase_9_evidence.md); they are not claims of continuously running services.

## Findings and limits

The [Phase 8 analytical record](docs/phase_8_analytics.md) reports persistent geographic overlap between poverty, vacancy, chronic high-school absence, and violent crime. Income is negatively associated with violent crime; poverty and unemployment are positively associated across available yearly cross-sections.

Chronic absence is more temporally consistent than dropout/withdrawal as a correlate of violence. Within-CSA annual changes have weaker relationships than cross-sectional comparisons. The poverty–vacancy interaction is negative across available yearly models, complicating a simple compounding hypothesis.

These are observational, ecological results. Demographic associations cannot be read as individual-level racial effects; correlated population shares are not independent findings. External intervention studies are kept separate. ACS vintage and BNIA source year are not silently treated as equivalent measurement periods; see [temporal reconciliation](docs/time_reconciliation.md).

## System flow

```text
Census API + BNIA workbook + geographic crosswalk
  → validation / transformation → PostgreSQL
  → separately invoked analytics → figures and BI CSV → Power BI Desktop
Curated analytical evidence matrix → local Ollama briefing
External intervention research → separate evidence register
```

The ingestion orchestrator does not automatically run analytics, BI, or AI. Cloud-validation mode validates source data without database writes.

## Reproduce

Start from the repository root. Use Python 3.13 and PostgreSQL 17 to match CI; the Dockerfile currently uses Python 3.14. Dependencies are pinned in [requirements.txt](requirements.txt).

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

For a new setup, edit `.env` with your database connection and Census API key. Preserve an existing `.env` rather than replacing it. Provision an empty database and a role that owns it, using the names configured in `.env`. Install `psql` and add it to your PATH.

Apply the SQL files in the exact order below **once to the empty database**; these are not rerunnable bootstrap migrations. The example uses the template's local database/user names and prompts for a password on each call. `psql` does not load `.env`.

```powershell
$schemaFiles = @(
    'database/schema/001_create_census_tracts.sql'
    'database/schema/002_create_bnia_tables.sql'
    'database/schema/003_create_geography_crosswalk.sql'
    'database/schema/004_create_pipeline_runs.sql'
    'database/schema/005_add_pipeline_run_metrics.sql'
    'database/migrations/004_separate_census_observations.sql'
    'database/migrations/005_remove_population_from_census_tracts.sql'
)
foreach ($schemaFile in $schemaFiles) {
    psql -h localhost -p 5432 -U project3_app -d project3_db -W -v ON_ERROR_STOP=1 -f $schemaFile
    if ($LASTEXITCODE -ne 0) { throw "Schema setup failed: $schemaFile" }
}
```

Obtain the BNIA workbook and crosswalk described in [Data Sources](docs/DATA_SOURCES.md) and place them at their required paths. Git contains directory placeholders, not these inputs; a clone alone cannot reproduce the live pipeline or analytical findings.

```powershell
python -m src.orchestration.pipeline
python -m src.analytics.baltimore_systems
python -m src.analytics.longitudinal_analysis
python -m src.analytics.housing_economic_analysis
python -m src.analytics.distributional_analysis
python -m src.analytics.evidence_matrix
python -m src.analytics.intervention_evidence
python -m src.analytics.visualizations
python -m src.analytics.bi_reporting
```

Run each command only after the preceding command succeeds. Analytics read the populated database; figures and CSVs are written under `data/processed/`. The evidence matrix and intervention register export curated records and do not recompute their interpretations from regression results.

For Power BI Desktop, import `data/processed/bi/baltimore_csa_year.csv` and configure its source path. The recorded report was saved as `docs/Urban_Systems_Intelligence.pbix`, but that file must be obtained separately to reproduce the original report rather than build a new one.

Optional AI briefing requires a running local Ollama installation:

```powershell
ollama pull llama3.2:3b
python -m ai.ai_briefing
```

Review generated text against the supplied evidence. Prompt restrictions are not a guarantee of factual accuracy.

## Tests and repository hygiene

[CI](.github/workflows/ci.yml) provisions PostgreSQL 17, applies the schema and migrations, seeds a synthetic database, and runs `python -m pytest -q`. Phase 9 records 46/46 passing; that is a historical result, not an assertion that every environment has been retested.

To reproduce the full suite locally, use a **separate empty test database**, apply the same SQL sequence, and set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in the test shell to target it. Then run:

```powershell
python -m tests.seed_ci_database
python -m pytest -q
```

The seed inserts synthetic CSA data and fixes a Census observation used by an unchanged-record test. Database tests perform writes and stale-run updates. Never seed the analytical database: synthetic rows would contaminate the findings. CI tests behavior and data contracts; it does not independently reproduce the real-data findings, Azure execution, Desktop report, or Ollama generation.

`.gitignore` excludes `.env`, `.venv`, Python/pytest caches, and raw/processed data, retaining `.gitkeep` placeholders. `.dockerignore` excludes secrets and development files, but raw inputs are copied into the image; inspect the build context before building or sharing an image.

## Documentation

| Document | Purpose |
| --- | --- |
| [Project Brief](docs/PROJECT_BRIEF.md) | Question, hypotheses, scope, and analytical limits |
| [Architecture](docs/ARCHITECTURE.md) | Components, storage, execution modes, and operational limits |
| [Data Sources](docs/DATA_SOURCES.md) | Input provenance, geography, missingness, and reproduction requirements |
| [Decisions](docs/DECISIONS.md) | Engineering and analytical choices with tradeoffs |
| [Phase 8](docs/phase_8_analytics.md) | Recorded analytical findings and methods |
| [Phase 9](docs/phase_9_evidence.md) | Recorded operational, cloud, BI, and AI demonstrations |
| [Time Reconciliation](docs/time_reconciliation.md) | Rules for comparing source periods |
