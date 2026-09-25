# Project Brief

[README](../README.md) · [Architecture](ARCHITECTURE.md) · [Data Sources](DATA_SOURCES.md) · [Decisions](DECISIONS.md)

## Question and purpose

How do economic disadvantage, housing conditions, education, and violent crime overlap across Baltimore neighborhoods, and how stable are those relationships over time?

Urban Systems Intelligence turns that question into a multi-source ingestion, storage, analysis, and reporting workflow. It demonstrates data engineering alongside careful interpretation of public urban indicators.

**Test *The Wire*, don't prove *The Wire*.** The show motivates testable institutional and structural hypotheses; it does not supply conclusions or substitute for measured evidence.

## Scope and hypotheses

The primary analytical unit is Community Statistical Area (CSA) × year: 55 non-citywide Baltimore CSAs across 2010–2023, with availability varying by indicator. Census tract data and a geographic crosswalk support the data infrastructure; the current analytical dataset is built from BNIA observations, not a contemporaneous ACS/BNIA merge.

The [curated evidence matrix](../src/analytics/evidence_matrix.py) records these interpretations of the Phase 8 work:

| Hypothesis | Recorded state |
| --- | --- |
| Economic disadvantage and violent crime cluster geographically | SUPPORTED |
| Problems overlap across institutional systems | SUPPORTED |
| Education-system dysfunction is uniformly associated with violence | COMPLICATED |
| Short-term neighborhood deterioration moves with violence | COMPLICATED |
| Housing and economic disadvantage simply compound one another | COMPLICATED |
| Structural disadvantage is evenly distributed across demographic geography | CONTRADICTED |
| Observed system relationships are causal | UNRESOLVED |

These states describe evidence for hypotheses, not scores for the television series. They are curated interpretations rather than automatically assigned statistical classifications.

## Analytical approach

[Phase 8](phase_8_analytics.md) combines yearly cross-sectional correlations, multivariable OLS, standardized coefficients, HC3 robust standard errors, variance inflation factors, influence diagnostics, outlier sensitivity, within-CSA first differences, and yearly interaction models.

The findings support persistent geographic overlap while complicating broad claims: chronic absence is more consistent than dropout as a correlate of violence, annual within-neighborhood changes are weaker than cross-sectional associations, and poverty–vacancy interactions do not show simple compounding.

External research on attendance messaging, abandoned-house remediation, Jobs-Plus, Moving to Opportunity, and Safe Streets Baltimore is maintained in a separate [intervention evidence register](../src/analytics/intervention_evidence.py). Its study designs, measured outcomes, causal scope, and limitations must remain attached to each result.

## Deliverables and boundaries

The project provides validated ingestion, PostgreSQL storage, analytical modules, figures, an evidence matrix, a BI CSV, and optional local AI briefings. [Phase 9](phase_9_evidence.md) records scheduled local and Docker execution, ACR plus managed-identity Container Apps validation, and Power BI Desktop implementation. Azure PostgreSQL and Power BI Service publication are not demonstrated. The Desktop PBIX is absent from this checkout.

Local Ollama synthesizes supplied structured evidence. It does not discover new findings or replace the analytical pipeline, and generated interpretations need review.

CSA-level associations cannot establish individual behavior, racial effects, causal direction, or intervention effectiveness. Black and White population shares are strongly inversely related and their associations are not independent findings. Missingness, indicator definitions, measurement noise, geographic boundaries, and potential lagged relationships constrain interpretation. Cross-source comparisons must follow [temporal reconciliation](time_reconciliation.md), preserving differences between ACS vintage, source year, and actual observation period.
