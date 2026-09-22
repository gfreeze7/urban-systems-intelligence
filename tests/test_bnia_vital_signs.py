import pytest

from src.ingestion.bnia_vital_signs import (
    clean_bnia_header,
    clean_bnia_value,
    validate_bnia_year,
    validate_unique_bnia_records,
)


def test_clean_bnia_value_keeps_numbers():
    assert clean_bnia_value(25) == 25
    assert clean_bnia_value(86.25) == 86.25


def test_clean_bnia_value_rejects_non_numeric_values():
    assert clean_bnia_value("--") is None
    assert clean_bnia_value("NA") is None
    assert clean_bnia_value("<5") is None
    assert clean_bnia_value("x") is None
    assert clean_bnia_value("Cherry Hill") is None
    assert clean_bnia_value(None) is None


def test_clean_bnia_header_strips_whitespace():
    assert clean_bnia_header("  Population  ") == "Population"


def test_clean_bnia_header_preserves_non_strings():
    assert clean_bnia_header(None) is None
    assert clean_bnia_header(123) == 123


def test_validate_bnia_year_rejects_wrong_row_count():
    indicator_numbers = [None, None, 1]
    headers = ["Year", "CSA2010", "Population"]
    data_rows = [
        (2023, "Cherry Hill", 8000),
    ]

    with pytest.raises(ValueError):
        validate_bnia_year(indicator_numbers, headers, data_rows)


def test_validate_unique_bnia_records_rejects_duplicates():
    record = {
        "year": 2023,
        "csa": "Cherry Hill",
        "indicator_number": 1,
        "indicator": "Population",
    }

    records = [record, record.copy()]

    with pytest.raises(ValueError):
        validate_unique_bnia_records(records)