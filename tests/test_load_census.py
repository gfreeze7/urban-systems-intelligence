from src.database.connection import get_connection
from src.database.load_census import load_census_records


def delete_test_record(geoid):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM census_acs_observations
                WHERE geoid = %s
                """,
                (geoid,),
            )

            cursor.execute(
                """
                DELETE FROM census_tracts
                WHERE geoid = %s
                """,
                (geoid,),
            )

        connection.commit()

    finally:
        connection.close()


def test_load_census_records_unchanged():
    record = {
        "geoid": "24510010100",
        "tract": "010100",
        "name": "Census Tract 101; Baltimore city; Maryland",
        "state": "24",
        "county": "510",
        "population": 2706,
        "year": 2024,
        "dataset": "acs5",
        "variable": "B01003_001E",
    }

    result = load_census_records([record])

    assert result["inserted"] == 0
    assert result["updated"] == 0
    assert result["unchanged"] == 1


def test_load_census_records_new():
    record = {
        "geoid": "99999999999",
        "tract": "999999",
        "name": "Test Census Tract",
        "state": "99",
        "county": "999",
        "population": 1234,
        "year": 2024,
        "dataset": "acs5",
        "variable": "B01003_001E",
    }

    try:
        result = load_census_records([record])

        assert result["inserted"] == 1
        assert result["updated"] == 0
        assert result["unchanged"] == 0

    finally:
        delete_test_record(record["geoid"])


def test_load_census_records_changed():
    record = {
        "geoid": "99999999998",
        "tract": "999998",
        "name": "Test Census Tract Changed",
        "state": "99",
        "county": "999",
        "population": 1234,
        "year": 2024,
        "dataset": "acs5",
        "variable": "B01003_001E",
    }

    try:
        load_census_records([record])

        changed_record = record.copy()
        changed_record["population"] = 5678

        result = load_census_records([changed_record])

        assert result["inserted"] == 0
        assert result["updated"] == 1
        assert result["unchanged"] == 0

    finally:
        delete_test_record(record["geoid"])