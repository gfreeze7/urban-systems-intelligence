from src.ingestion.bnia_vital_signs import (
    load_bnia_workbook,
    transform_bnia_workbook,
)


workbook = load_bnia_workbook()

try:
    records = transform_bnia_workbook(workbook)

    for record in records:
        value = record["value"]

        if value is not None and not isinstance(value, (int, float)):
            print(
                record["year"],
                "|",
                record["csa"],
                "|",
                record["indicator_number"],
                "|",
                repr(record["indicator"]),
                "|",
                repr(value),
            )

finally:
    workbook.close()