from src.database.connection import get_connection


def load_census_records(records):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO census_tracts (
                        geoid,
                        tract,
                        name,
                        state,
                        county
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (geoid) DO UPDATE SET
                        tract = EXCLUDED.tract,
                        name = EXCLUDED.name,
                        state = EXCLUDED.state,
                        county = EXCLUDED.county
                    """,
                    (
                        record["geoid"],
                        record["tract"],
                        record["name"],
                        record["state"],
                        record["county"],
                    ),
                )

                cursor.execute(
                    """
                    INSERT INTO census_acs_observations (
                        geoid,
                        year,
                        dataset,
                        variable,
                        value
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (geoid, year, dataset, variable)
                    DO UPDATE SET
                        value = EXCLUDED.value
                    """,
                    (
    			record["geoid"],
    			record["year"],
    			record["dataset"],
    			record["variable"],
    			record["population"],
),
                )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()