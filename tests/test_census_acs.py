import pytest

from src.ingestion.census_acs import (
    transform_records,
    validate_census_response,
    validate_unique_tracts,
)


def test_unique_tracts_pass():
    records = [
        {"tract": "010100"},
        {"tract": "010200"},
    ]

    validate_unique_tracts(records)


def test_duplicate_tracts_fail():
    records = [
        {"tract": "010100"},
        {"tract": "010100"},
    ]

    with pytest.raises(ValueError):
        validate_unique_tracts(records)


def test_valid_census_response():
    data = [
        ["NAME", "B01003_001E", "state", "county", "tract"],
        ["Census Tract 101", "2706", "24", "510", "010100"],
    ]

    headers, rows = validate_census_response(data)

    assert headers == ["NAME", "B01003_001E", "state", "county", "tract"]
    assert len(rows) == 1


def test_census_response_not_list():
    data = {"NAME": "not a list"}

    with pytest.raises(ValueError):
        validate_census_response(data)


def test_census_response_missing_rows():
    data = [
        ["NAME", "B01003_001E", "state", "county", "tract"]
    ]

    with pytest.raises(ValueError):
        validate_census_response(data)


def test_census_response_bad_headers():
    data = [
        ["WRONG", "HEADERS"],
        ["Census Tract 101", "2706"],
    ]

    with pytest.raises(ValueError):
        validate_census_response(data)


def test_transform_records_valid():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "2706", "24", "510", "010100"]
    ]

    records = transform_records(headers, rows)

    assert len(records) == 1
    assert records[0]["population"] == 2706
    assert records[0]["tract"] == "010100"
    assert records[0]["geoid"] == "24510010100"


def test_transform_records_invalid_population():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "not-a-number", "24", "510", "010100"]
    ]

    with pytest.raises(ValueError):
        transform_records(headers, rows)


def test_transform_records_invalid_tract():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "2706", "24", "510", "ABC"]
    ]

    with pytest.raises(ValueError):
        transform_records(headers, rows)


def test_transform_records_wrong_row_length():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "2706", "24"]
    ]

    with pytest.raises(ValueError):
        transform_records(headers, rows)


def test_transform_records_wrong_state():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "2706", "99", "510", "010100"]
    ]

    with pytest.raises(ValueError):
        transform_records(headers, rows)


def test_transform_records_wrong_county():
    headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    rows = [
        ["Census Tract 101", "2706", "24", "999", "010100"]
    ]

    with pytest.raises(ValueError):
        transform_records(headers, rows)


