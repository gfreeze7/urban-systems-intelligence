from src.ingestion.bnia_vital_signs import (
    load_bnia_workbook,
    read_bnia_year,
)


workbook = load_bnia_workbook()

try:
    checks = [
        (2012, 175),
        (2019, 148),
    ]

    for year, target_indicator in checks:
        indicator_numbers, headers, data_rows = read_bnia_year(workbook, year)

        for column_index, indicator_number in enumerate(indicator_numbers):
            if indicator_number == target_indicator:
                print()
                print("YEAR:", year)
                print("INDICATOR:", indicator_number)
                print("HEADER:", repr(headers[column_index]))
                print("VALUES:")

                for row in data_rows:
                    value = row[column_index]

                    if value is not None:
                        print(repr(row[1]), "->", repr(value))

finally:
    workbook.close()