import pandas as pd

from src.analytics.baltimore_systems import build_analytical_dataset
from src.analytics.evidence_matrix import build_evidence_matrix
from src.analytics.intervention_evidence import build_intervention_evidence


def test_build_analytical_dataset_pivots_indicator_rows():
    observations = pd.DataFrame(
        [
            {
                "csa2010": "Test CSA",
                "year": 2023,
                "source_indicator_number": 27,
                "value": 12.5,
            },
            {
                "csa2010": "Test CSA",
                "year": 2023,
                "source_indicator_number": 52,
                "value": 8.0,
            },
        ]
    )

    dataset = build_analytical_dataset(observations)

    assert len(dataset) == 1
    assert dataset.loc[0, "csa2010"] == "Test CSA"
    assert dataset.loc[0, "year"] == 2023
    assert dataset.loc[0, "family_poverty_pct"] == 12.5
    assert dataset.loc[0, "violent_crime_rate"] == 8.0


def test_evidence_matrix_uses_valid_states():
    matrix = build_evidence_matrix()

    valid_states = {
        "SUPPORTED",
        "COMPLICATED",
        "CONTRADICTED",
        "UNRESOLVED",
    }

    assert set(matrix["evidence_state"]).issubset(valid_states)


def test_evidence_matrix_has_required_fields():
    matrix = build_evidence_matrix()

    required_columns = {
        "hypothesis",
        "evidence_state",
        "evidence",
        "limitation",
    }

    assert required_columns.issubset(matrix.columns)


def test_evidence_matrix_has_no_missing_interpretation():
    matrix = build_evidence_matrix()

    assert matrix["hypothesis"].notna().all()
    assert matrix["evidence"].notna().all()
    assert matrix["limitation"].notna().all()


def test_evidence_matrix_contains_all_four_evidence_states():
    matrix = build_evidence_matrix()

    expected_states = {
        "SUPPORTED",
        "COMPLICATED",
        "CONTRADICTED",
        "UNRESOLVED",
    }

    assert set(matrix["evidence_state"]) == expected_states


def test_evidence_matrix_hypotheses_are_unique():
    matrix = build_evidence_matrix()

    assert matrix["hypothesis"].is_unique


def test_analytical_dataset_preserves_multiple_csa_years():
    observations = pd.DataFrame(
        [
            {
                "csa2010": "CSA A",
                "year": 2022,
                "source_indicator_number": 27,
                "value": 10.0,
            },
            {
                "csa2010": "CSA A",
                "year": 2023,
                "source_indicator_number": 27,
                "value": 11.0,
            },
            {
                "csa2010": "CSA B",
                "year": 2023,
                "source_indicator_number": 27,
                "value": 20.0,
            },
        ]
    )

    dataset = build_analytical_dataset(observations)

    assert len(dataset) == 3

    grain = dataset[["csa2010", "year"]]

    assert not grain.duplicated().any()


def test_analytical_dataset_preserves_multiple_csa_years():
    observations = pd.DataFrame(
        [
            {
                "csa2010": "CSA A",
                "year": 2022,
                "source_indicator_number": 27,
                "value": 10.0,
            },
            {
                "csa2010": "CSA A",
                "year": 2023,
                "source_indicator_number": 27,
                "value": 11.0,
            },
            {
                "csa2010": "CSA B",
                "year": 2023,
                "source_indicator_number": 27,
                "value": 20.0,
            },
        ]
    )

    dataset = build_analytical_dataset(observations)

    assert len(dataset) == 3

    grain = dataset[["csa2010", "year"]]

    assert not grain.duplicated().any()


def test_intervention_evidence_has_required_fields():
    evidence = build_intervention_evidence()

    required_columns = {
        "intervention",
        "system",
        "geography",
        "study_design",
        "population",
        "outcome",
        "result",
        "causal_scope",
        "limitation",
        "source",
        "source_url",
    }

    assert required_columns.issubset(evidence.columns)


def test_intervention_evidence_has_unique_interventions():
    evidence = build_intervention_evidence()

    assert evidence["intervention"].is_unique


def test_intervention_evidence_has_complete_provenance():
    evidence = build_intervention_evidence()

    assert evidence["source"].notna().all()
    assert evidence["source_url"].notna().all()

    assert evidence["source"].str.strip().ne("").all()
    assert evidence["source_url"].str.strip().ne("").all()


def test_intervention_evidence_preserves_causal_limits():
    evidence = build_intervention_evidence()

    assert evidence["causal_scope"].notna().all()
    assert evidence["limitation"].notna().all()