import csv

from src.database.load_geography_crosswalk import load_geography_crosswalk


CROSSWALK_FILEPATH = "data/raw/geography/bnia_tract2020_to_csa2010.csv"

EXPECTED_HEADERS = [
    "STATEFP",
    "COUNTYFP",
    "TRACTCE2020",
    "GEOID2020",
    "NAME",
    "NAMELSAD",
    "CSA2010",
    "ObjectId",
]


def read_crosswalk(filepath=CROSSWALK_FILEPATH):
    with open(filepath, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_HEADERS:
            raise ValueError(f"Unexpected crosswalk headers: {reader.fieldnames}")

        rows = list(reader)

    return rows


def transform_crosswalk(rows):
    records = []

    for row in rows:
        geoid = row["GEOID2020"]
        tract = row["TRACTCE2020"]

        if row["STATEFP"] != "24":
            raise ValueError(f"Unexpected state code: {row['STATEFP']}")

        if row["COUNTYFP"] != "510":
            raise ValueError(f"Unexpected county code: {row['COUNTYFP']}")

        if len(geoid) != 11 or not geoid.isdigit():
            raise ValueError(f"Invalid GEOID: {geoid}")

        if len(tract) != 6 or not tract.isdigit():
            raise ValueError(f"Invalid tract code: {tract}")

        expected_geoid = row["STATEFP"] + row["COUNTYFP"] + tract

        if geoid != expected_geoid:
            raise ValueError(
                f"GEOID does not match state + county + tract: {geoid}"
            )

        record = {
            "geoid2020": geoid,
            "statefp": row["STATEFP"],
            "countyfp": row["COUNTYFP"],
            "tractce2020": tract,
            "tract_name": row["NAME"],
            "tract_label": row["NAMELSAD"],
            "csa2010": row["CSA2010"],
        }

        records.append(record)

    return records


def validate_crosswalk(records):
    if len(records) != 199:
        raise ValueError(f"Expected 199 crosswalk records, found {len(records)}")

    geoids = [record["geoid2020"] for record in records]

    if len(geoids) != len(set(geoids)):
        raise ValueError("Duplicate GEOIDs found in crosswalk")


def main():
    rows = read_crosswalk()
    records = transform_crosswalk(rows)
    validate_crosswalk(records)

    load_geography_crosswalk(records)

    print("Raw rows:", len(rows))
    print("Validated records:", len(records))
    print("First record:", records[0])
    print("Crosswalk load complete")


if __name__ == "__main__":
    main()