from src.database.connection import get_connection


YEARS = range(2010, 2024)
CSAS = [f"CI CSA {number:02d}" for number in range(1, 56)]

BI_INDICATORS = {
    20: "Median Household Income",
    27: "Family Poverty",
    34: "Vacant and Abandoned Housing",
    52: "Violent Crime Rate",
    75: "High School Chronic Absence",
    91: "Dropout Rate",
    92: "Completion Rate",
    98: "Youth in School or Employed",
    137: "Unemployment Rate",
}


def seed_census(cursor):
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
            'Census Tract 101; Baltimore city; Maryland',
            '24',
            '510'
        )
        ON CONFLICT (geoid) DO UPDATE
        SET tract = EXCLUDED.tract,
            name = EXCLUDED.name,
            state = EXCLUDED.state,
            county = EXCLUDED.county
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
            2706
        )
        ON CONFLICT (geoid, year, dataset, variable)
        DO UPDATE SET value = EXCLUDED.value
        """
    )


def seed_bnia(cursor):
    for year in YEARS:
        for csa_number, csa in enumerate(CSAS, start=1):
            cursor.execute(
                """
                INSERT INTO bnia_geographies (
                    year,
                    csa2010,
                    csa2020,
                    is_citywide
                )
                VALUES (%s, %s, NULL, FALSE)
                ON CONFLICT (year, csa2010) DO NOTHING
                """,
                (year, csa),
            )

            for indicator_number, indicator_name in BI_INDICATORS.items():
                value = float(
                    (year - 2000)
                    + csa_number
                    + (indicator_number / 100)
                )

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
                    DO UPDATE
                    SET raw_value = EXCLUDED.raw_value,
                        value = EXCLUDED.value
                    """,
                    (
                        year,
                        csa,
                        indicator_number,
                        indicator_name,
                        str(value),
                        value,
                    ),
                )


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            seed_census(cursor)
            seed_bnia(cursor)

        connection.commit()

    print("CI database seeded successfully.")


if __name__ == "__main__":
    main()