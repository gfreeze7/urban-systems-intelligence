from src.ingestion.bnia_vital_signs import (
    load_bnia_workbook,
    read_bnia_year,
)


workbook = load_bnia_workbook()

try:
    indicator_numbers, headers, data_rows = read_bnia_year(workbook, 2017)

    for column_index, indicator_number in enumerate(indicator_numbers):
        if indicator_number in (112, 113, 114):
            print()
            print("COLUMN INDEX:", column_index)
            print("INDICATOR NUMBER:", repr(indicator_number))
            print("HEADER:", repr(headers[column_index]))
            print("FIRST 3 VALUES:")

            for row in data_rows[:3]:
                print(repr(row[column_index]))

finally:
    workbook.close()