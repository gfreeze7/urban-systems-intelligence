# Data Sources

[README](../README.md) · [Project Brief](PROJECT_BRIEF.md) · [Architecture](ARCHITECTURE.md) · [Decisions](DECISIONS.md)

## Source inventory

| Input | Provenance and grain | Required location / configuration |
| --- | --- | --- |
| Census ACS | Census API, 2024 `acs/acs5`, population variable `B01003_001E`; Baltimore city tracts, state `24`, county `510` | Live request configured in `src/ingestion/census_acs.py`; `CENSUS_API_KEY` |
| BNIA Vital Signs | Baltimore Neighborhood Indicators Alliance annual workbook, 2010–2023; CSA × source year × indicator | `data/raw/bnia_vital_signs/Vital Signs 2010-2023.xlsx` |
| Geographic crosswalk | BNIA-labeled 2020 tract-to-CSA2010 CSV used by the project; one row per tract | `data/raw/geography/bnia_tract2020_to_csa2010.csv` |
| Intervention research | Curated study records with source URLs, design, outcome, causal scope, and limitations | [Intervention register source](../src/analytics/intervention_evidence.py) |

The Census endpoint is specified in [the ingestion module](../src/ingestion/census_acs.py). The repository does not record an exact download URL, acquisition date, or checksum for the local BNIA workbook and crosswalk. Obtain the matching original inputs from the project owner or verify replacement exports against the contracts below; exact source-file reproduction cannot be claimed from this checkout alone.

Raw data and generated outputs are ignored by Git. Existing local copies are not evidence that a fresh clone contains them. The Dockerfile copies raw inputs from the build context, so their inclusion in an image is separate from Git tracking.

## Census contract

The loader expects `NAME`, `B01003_001E`, `state`, `county`, and `tract`. It validates row width, Baltimore geography, six-digit tract codes, unique tracts, and nonnegative integer-form population values. GEOIDs preserve leading zeros. The demonstrated run contained 199 tracts.

Geographic attributes are stored in `census_tracts`; observations retain year, dataset, and original variable identifier in `census_acs_observations`. Unsupported or nonnumeric population values are rejected rather than converted to zero.

## BNIA contract and missingness

Each year worksheet has indicator numbers in its first row, headers in its second, and 56 geography rows: 55 CSAs plus Baltimore City. `CSA2010` is the analytical geography label; `CSA2020` is retained separately when present. The recorded load contains 784 geography-year records and 104,272 observations.

The transformation retains original indicator numbers/names and raw values. Numeric cells become numeric observations; other values become missing (`None`/SQL NULL), not zero. Columns entirely empty or `--` are skipped. Empty headers and the `CSA2020` metadata column are not treated as indicators. Duplicate observation keys are rejected.

The [analytical mapping](../src/analytics/baltimore_systems.py) selects income, poverty, vacancy, violence, education, unemployment, and demographic indicators. It excludes the Baltimore City aggregate and pivots to CSA-year rows. Its current aggregation is `max` if multiple records share a pivot cell; indicator identity and definition changes therefore still require review. The 770-row BI export is a geography-year grid, not a guarantee that every measure is populated in every year. Models use available complete cases for their selected variables; sample sizes may differ.

Units, denominators, and indicator reference periods must be checked against source methodology before interpretation. No blanket imputation, harmonization of definitions, or causal adjustment is implied by the numeric cleaning rules.

## Geographic reconciliation

The [crosswalk reader](../src/ingestion/geography_crosswalk.py) requires these headers in order:

```text
STATEFP,COUNTYFP,TRACTCE2020,GEOID2020,NAME,NAMELSAD,CSA2010,ObjectId
```

It validates state/county codes, GEOID construction, unique GEOIDs, and exactly 199 records. Tract identifiers must remain strings with leading zeros. The crosswalk links 2020 tract geography to CSA2010 labels; it is not an area- or population-weighted interpolation, nor proof that historical boundaries are equivalent. Current CSA analytics read BNIA directly rather than aggregating ACS through this crosswalk.

## Temporal reconciliation

Follow [Time Reconciliation](time_reconciliation.md): **source year, observation period, and analytical comparison period are not assumed equivalent.**

BNIA retains the year supplied by each annual workbook sheet. Individual indicator measurement periods still need methodological review. Census retains the 2024 API vintage, `acs5` product, and `B01003_001E` identifier; that vintage must not be treated as a single-year measure contemporaneous with a BNIA annual record. Do not join sources on a year label alone without verifying compatible reference periods and disclosing differences.

## Evidence provenance and interpretation

[Phase 8](phase_8_analytics.md) records analytical conclusions and limitations; [Phase 9](phase_9_evidence.md) records execution counts and demonstrated capabilities. The [hypothesis matrix](../src/analytics/evidence_matrix.py) is a curated summary of those findings, not an automatically refreshed statistical result. Revise it explicitly if new analyses change the evidence.

The intervention register preserves external research separately so Baltimore correlations are not mistaken for intervention effects. CSA demographic findings are ecological, cannot establish individual-level racial effects, and do not identify causal mechanisms. Local AI synthesizes this supplied evidence; its text is not an additional source of evidence.
