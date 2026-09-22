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
                        population,
                        state,
                        county
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (geoid) DO UPDATE SET
                    tract = EXCLUDED.tract,
                    name = EXCLUDED.name,
                    population = EXCLUDED.population,
                    state = EXCLUDED.state,
                    county = EXCLUDED.county
                    """,
                    (
                        record["geoid"],
                        record["tract"],
                        record["name"],
                        record["population"],
                        record["state"],
                        record["county"],
                    ),
                )

            connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()