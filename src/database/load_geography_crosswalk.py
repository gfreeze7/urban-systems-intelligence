from src.database.connection import get_connection


def load_geography_crosswalk(records):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO tract2020_to_csa2010 (
                        geoid2020,
                        statefp,
                        countyfp,
                        tractce2020,
                        tract_name,
                        tract_label,
                        csa2010
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (geoid2020) DO UPDATE SET
                        statefp = EXCLUDED.statefp,
                        countyfp = EXCLUDED.countyfp,
                        tractce2020 = EXCLUDED.tractce2020,
                        tract_name = EXCLUDED.tract_name,
                        tract_label = EXCLUDED.tract_label,
                        csa2010 = EXCLUDED.csa2010
                    """,
                    (
                        record["geoid2020"],
                        record["statefp"],
                        record["countyfp"],
                        record["tractce2020"],
                        record["tract_name"],
                        record["tract_label"],
                        record["csa2010"],
                    ),
                )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()