import csv

from src.database.connection import get_connection


filepath = "data/raw/geography/bnia_tract2020_to_csa2010.csv"

with open(filepath, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    crosswalk_rows = list(reader)

crosswalk_geoids = {row["GEOID2020"] for row in crosswalk_rows}

connection = get_connection()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT geoid FROM census_tracts")
        census_geoids = {row[0].strip() for row in cursor.fetchall()}
finally:
    connection.close()

print("Census GEOIDs:", len(census_geoids))
print("Crosswalk GEOIDs:", len(crosswalk_geoids))
print("Missing from crosswalk:", census_geoids - crosswalk_geoids)
print("Missing from Census:", crosswalk_geoids - census_geoids)


connection = get_connection()

try:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT csa2010
            FROM bnia_geographies
            WHERE NOT is_citywide
            """
        )
        bnia_csas = {row[0] for row in cursor.fetchall()}
finally:
    connection.close()

crosswalk_csas = {row["CSA2010"] for row in crosswalk_rows}

print("BNIA CSAs:", len(bnia_csas))
print("Crosswalk CSAs:", len(crosswalk_csas))
print("Missing from crosswalk:", bnia_csas - crosswalk_csas)
print("Missing from BNIA:", crosswalk_csas - bnia_csas)


unassigned_rows = [
    row
    for row in crosswalk_rows
    if row["CSA2010"] == "Unassigned -- Jail"
]

print("Unassigned rows:", len(unassigned_rows))

for row in unassigned_rows:
    print(
        row["GEOID2020"],
        row["NAMELSAD"],
        row["CSA2010"],
    )


assigned_rows = [
    row
    for row in crosswalk_rows
    if row["CSA2010"] != "Unassigned -- Jail"
]

print("Assigned tract rows:", len(assigned_rows))
print("Unassigned tract rows:", len(unassigned_rows))
print("Total tract rows:", len(assigned_rows) + len(unassigned_rows))


with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                SUM(o.value) AS total_population,
                SUM(
                    CASE
                        WHEN x.csa2010 <> 'Unassigned -- Jail'
                        THEN o.value
                        ELSE 0
                    END
                ) AS assigned_population,
                SUM(
                    CASE
                        WHEN x.csa2010 = 'Unassigned -- Jail'
                        THEN o.value
                        ELSE 0
                    END
                ) AS unassigned_population
            FROM census_acs_observations o
            JOIN tract2020_to_csa2010 x
                ON o.geoid = x.geoid2020
            WHERE o.year = 2024
                AND o.dataset = 'acs5'
                AND o.variable = 'B01003_001E'
            """
        )

        total_population, assigned_population, unassigned_population = cursor.fetchone()

if total_population != assigned_population + unassigned_population:
    raise ValueError("Population reconciliation failed")

print("Total population:", total_population)
print("Assigned population:", assigned_population)
print("Unassigned population:", unassigned_population)
print("Population reconciliation: PASS")