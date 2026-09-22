import pytest

from src.ingestion.geography_crosswalk import (
    transform_crosswalk,
    validate_crosswalk,
)


def make_row():
    return {
        "STATEFP": "24",
        "COUNTYFP": "510",
        "TRACTCE2020": "120202",
        "GEOID2020": "24510120202",
        "NAME": "1202.02",
        "NAMELSAD": "Census Tract 1202.02",
        "CSA2010": "Greater Charles Village/Barclay",
        "ObjectId": "1",
    }


def test_transform_valid_row():
    records = transform_crosswalk([make_row()])

    assert records[0]["geoid2020"] == "24510120202"
    assert records[0]["tractce2020"] == "120202"
    assert records[0]["csa2010"] == "Greater Charles Village/Barclay"


def test_reject_wrong_state():
    row = make_row()
    row["STATEFP"] = "99"

    with pytest.raises(ValueError):
        transform_crosswalk([row])


def test_reject_wrong_county():
    row = make_row()
    row["COUNTYFP"] = "999"

    with pytest.raises(ValueError):
        transform_crosswalk([row])


def test_reject_invalid_geoid():
    row = make_row()
    row["GEOID2020"] = "ABC"

    with pytest.raises(ValueError):
        transform_crosswalk([row])


def test_reject_invalid_tract():
    row = make_row()
    row["TRACTCE2020"] = "ABC"

    with pytest.raises(ValueError):
        transform_crosswalk([row])


def test_reject_duplicate_geoids():
    record = transform_crosswalk([make_row()])[0]

    records = [record.copy() for _ in range(199)]
    records[1]["tractce2020"] = "999999"

    with pytest.raises(ValueError):
        validate_crosswalk(records)


def test_reject_geoid_component_mismatch():
    row = make_row()
    row["GEOID2020"] = "24510120203"

    with pytest.raises(ValueError):
        transform_crosswalk([row])