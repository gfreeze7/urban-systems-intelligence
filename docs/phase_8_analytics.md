# Phase 8 — Urban Systems Analytics

## Purpose

Phase 8 evaluates whether real-world Baltimore data supports, complicates,
or contradicts selected institutional and structural hypotheses inspired by
*The Wire*.

The analysis tests hypotheses rather than attempting to prove the show's
diagnosis.

## Analytical Unit

The primary analytical unit is:

**Baltimore Community Statistical Area (CSA) × year**

The analytical dataset contains 55 non-citywide CSAs across available years.

## Core Systems

The analysis focuses on:

- economic disadvantage
- housing and residential vacancy
- education
- violent crime
- demographic geography

## Main Findings

### Economic disadvantage and violent crime

Income is consistently negatively associated with violent crime across
available yearly cross-sections, while poverty and unemployment are
consistently positively associated.

These relationships are observational and are not interpreted as causal.

### Cross-system relationships

Poverty, residential vacancy, chronic high-school absence, and violent crime
show persistent geographic overlap across Baltimore CSAs.

In 2023, chronic high-school absence has the strongest bivariate relationship
with violent crime among the core variables examined.

### Education

Chronic high-school absence is a substantially more temporally consistent
neighborhood-level correlate of violent crime than dropout/withdrawal.

Within-CSA year-to-year changes show weaker relationships than repeated
cross-sectional comparisons.

### Housing and economic disadvantage

Poverty and residential vacancy are independently associated with violent
crime.

The poverty-vacancy interaction is consistently negative across available
yearly models rather than showing a simple compounding relationship.

### Distributional lens

Across available demographic years, CSAs with larger Black population shares
show higher aggregate poverty, residential vacancy, unemployment, and chronic
high-school absence, while larger White population shares show inverse
neighborhood-level patterns.

These are ecological associations and must not be interpreted as
individual-level racial effects or causal mechanisms.

Black and White population shares are also strongly inversely related, so
their associations are not independent findings.

## Robustness Methods

Phase 8 uses:

- yearly cross-sectional correlations
- multivariable OLS regression
- standardized coefficients
- HC3 heteroskedasticity-robust standard errors
- variance inflation factors
- influence diagnostics
- sensitivity analysis
- within-CSA first differences
- yearly interaction models
- outlier sensitivity analysis

## Intervention Evidence

External intervention research is stored separately from the Baltimore
observational analysis.

This prevents observational relationships from being incorrectly treated as
causal intervention evidence.

The intervention evidence register includes research concerning:

- adaptive parent attendance messaging
- abandoned-house remediation
- Jobs-Plus
- Moving to Opportunity
- Safe Streets Baltimore

Each intervention record preserves its study design, measured outcome,
causal scope, limitations, and source provenance.

## Evidence States

The hypothesis evidence matrix uses four states:

- `SUPPORTED`
- `COMPLICATED`
- `CONTRADICTED`
- `UNRESOLVED`

These describe the state of evidence for a testable hypothesis. They are not
scores for *The Wire*.

## Reproducing the Analysis

From the project root with the virtual environment active:

```powershell
python -m src.analytics.baltimore_systems
python -m src.analytics.longitudinal_analysis
python -m src.analytics.housing_economic_analysis
python -m src.analytics.distributional_analysis
python -m src.analytics.evidence_matrix
python -m src.analytics.intervention_evidence
python -m src.analytics.visualizations
```

See [README](../README.md#reproduce) for input and database prerequisites. These modules run separately from ingestion.
