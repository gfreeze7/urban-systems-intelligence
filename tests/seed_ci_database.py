from src.database.connection import get_connection


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO census_tracts (
                    geoid,
                    tract,
                    name,
                    state,
                    county
                )
                VALUES (
                    '24510010100',
                    '010100',
                    'Census Tract 101, Baltimore city, Maryland',
                    '24',
                    '510'
                )
                ON CONFLICT (geoid) DO NOTHING
                """
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
                VALUES (
                    '24510010100',
                    2024,
                    'acs5',
                    'B01003_001E',
                    1000
                )
                ON CONFLICT (geoid, year, dataset, variable)
                DO NOTHING
                """
            )

        connection.commit()

    print("CI database seeded successfully.")


if __name__ == "__main__":
    main()
