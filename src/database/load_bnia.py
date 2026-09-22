from src.database.connection import get_connection


def load_bnia_data(geographies, observations):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for geography in geographies:
                cursor.execute(
                    """
                    INSERT INTO bnia_geographies (
                        year,
                        csa2010,
                        csa2020,
                        is_citywide
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (year, csa2010) DO UPDATE SET
                        csa2020 = EXCLUDED.csa2020,
                        is_citywide = EXCLUDED.is_citywide
                    """,
                    (
                        geography["year"],
                        geography["csa2010"],
                        geography["csa2020"],
                        geography["is_citywide"],
                    ),
                )

            for observation in observations:
                cursor.execute(
                    """
                    INSERT INTO bnia_observations (
                        year,
                        csa2010,
                        source_indicator_number,
                        source_indicator_name,
                        raw_value,
                        value
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (
                        year,
                        csa2010,
                        source_indicator_number,
                        source_indicator_name
                    )
                    DO UPDATE SET
                        raw_value = EXCLUDED.raw_value,
                        value = EXCLUDED.value
                    """,
                    (
                        observation["year"],
                        observation["csa"],
                        observation["indicator_number"],
                        observation["indicator"],
                        observation["raw_value"],
                        observation["value"],
                    ),
                )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()