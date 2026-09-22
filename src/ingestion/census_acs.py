import json
import os

import requests
from dotenv import load_dotenv


from src.database.load_census import load_census_records



load_dotenv()

CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

BASE_URL = "https://api.census.gov/data/2024/acs/acs5"

params = {
    "get": "NAME,B01003_001E",
    "for": "tract:*",
    "in": "state:24 county:510",
    "key": CENSUS_API_KEY,
}

def get_census_data():
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def save_json(contents, filepath):
    with open(filepath, "w") as file:
        json.dump(contents, file, indent=4)

def validate_census_response(data):
    if not isinstance(data, list):
        raise ValueError("Census response is not a list")

    if len(data) < 2:
        raise ValueError("Census response does not contain headers and data rows")

    headers = data[0]
    rows = data[1:]

    expected_headers = ["NAME", "B01003_001E", "state", "county", "tract"]

    if headers != expected_headers:
        raise ValueError(f"Unexpected Census headers: {headers}")

    return headers, rows

def validate_unique_tracts(records):
    tract_ids = [record["tract"] for record in records]

    if len(tract_ids) != len(set(tract_ids)):
        raise ValueError("Duplicate tract codes found")

def transform_records(headers, rows):
    records = []

    for row in rows:
        if len(row) != len(headers):
            raise ValueError(f"Unexpected row length: {len(row)}")
        
        raw_record = dict(zip(headers, row))

        population_raw = raw_record["B01003_001E"]
        
        tract = raw_record["tract"]
        geoid = raw_record["state"] + raw_record["county"] + tract
        
        if len(tract) != 6 or not tract.isdigit():
            raise ValueError(f"Invalid tract code: {tract}")
        
        if not population_raw.isdigit():
            raise ValueError(f"Invalid population value: {population_raw}")
        
        if raw_record["state"] != "24":
            raise ValueError(f"Unexpected state code: {raw_record['state']}")
        
        if raw_record["county"] != "510":
            raise ValueError(f"Unexpected county code: {raw_record['county']}")
        
        record = {
    "geoid": geoid,
    "name": raw_record["NAME"],
    "population": int(population_raw),
    "state": raw_record["state"],
    "county": raw_record["county"],
    "tract": tract,
}

        records.append(record)

    return records

def main():
    data = get_census_data()

    headers, rows = validate_census_response(data)

    save_json(data, "data/raw/census_acs_2024_baltimore.json")

    print("Headers:", headers)
    print("Number of rows:", len(rows))
    print("First data row:", rows[0])
    
    records = transform_records(headers, rows)

    validate_unique_tracts(records)

    load_census_records(records)

    save_json(records, "data/processed/census_acs_2024_baltimore.json")

    print("Number of records:", len(records))
    print("First record:", records[0])

if __name__ == "__main__":
    main()