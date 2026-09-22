from src.ingestion.bnia_vital_signs import (
    load_bnia_workbook,
    read_bnia_year,
)

workbook = load_bnia_workbook()

for year in workbook.sheetnames:
    indicator_numbers, headers, data_rows = read_bnia_year(workbook, year)

    empty_columns = 0

    for column_index in range(2, len(headers)):
        column_values = [
            row[column_index]
            for row in data_rows
        ]

        if all(
            value is None or value == "--"
            for value in column_values
        ):
            empty_columns += 1

    total_candidate_columns = len(headers) - 2
    active_columns = total_candidate_columns - empty_columns

    print(
        year,
        "EMPTY:", empty_columns,
        "ACTIVE:", active_columns,
        "TOTAL:", total_candidate_columns,
    )

workbook.close()