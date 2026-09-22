from src.database.connection import get_connection


def load_census_records(records):
    connection = get_connection()

    inserted = 0
    updated = 0
    unchanged = 0

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
                    SELECT value
                    FROM census_acs_observations
                    WHERE geoid = %s
                      AND year = %s
                      AND dataset = %s
                      AND variable = %s
                    """,
                    (
                        record["geoid"],
                        record["year"],
                        record["dataset"],
                        record["variable"],
                    ),
                )

                existing_row = cursor.fetchone()

                if existing_row is None:
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
                        """,
                        (
                            record["geoid"],
                            record["year"],
                            record["dataset"],
                            record["variable"],
                            record["population"],
                        ),
                    )
                    inserted += 1

                elif existing_row[0] != record["population"]:
                    cursor.execute(
                        """
                        UPDATE census_acs_observations
                        SET value = %s
                        WHERE geoid = %s
                          AND year = %s
                          AND dataset = %s
                          AND variable = %s
                        """,
                        (
                            record["population"],
                            record["geoid"],
                            record["year"],
                            record["dataset"],
                            record["variable"],
                        ),
                    )
                    updated += 1

                else:
                    unchanged += 1

        connection.commit()

        return {
            "inserted": inserted,
            "updated": updated,
            "unchanged": unchanged,
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()