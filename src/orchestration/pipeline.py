import os
from src.database.load_census import load_census_records
from src.ingestion.census_acs import (
    get_census_data,
    transform_records,
    validate_census_response,
    validate_unique_tracts,
)


def run_census_stage():
    data = get_census_data()

    validate_census_response(data)

    headers = data[0]
    rows = data[1:]

    records = transform_records(headers, rows)

    validate_unique_tracts(records)

    result = load_census_records(records)

    return result


from src.database.load_bnia import load_bnia_data
from src.ingestion.bnia_vital_signs import (
    load_bnia_workbook,
    transform_bnia_geographies,
    transform_bnia_workbook,
    validate_unique_bnia_geographies,
)

from src.database.load_geography_crosswalk import load_geography_crosswalk
from src.ingestion.geography_crosswalk import (
    read_crosswalk,
    transform_crosswalk,
    validate_crosswalk,
)

from src.database.pipeline_runs import (
    finish_pipeline_run,
    mark_stale_pipeline_runs,
    start_pipeline_run,
)


def run_bnia_stage():
    workbook = load_bnia_workbook()

    try:
        observations = transform_bnia_workbook(workbook)
        geographies = transform_bnia_geographies(workbook)

        validate_unique_bnia_geographies(geographies)

        result = load_bnia_data(geographies, observations)

        return result
    finally:
        workbook.close()


def run_geography_stage():
    rows = read_crosswalk()

    records = transform_crosswalk(rows)

    validate_crosswalk(records)

    result = load_geography_crosswalk(records)

    return result


def run_pipeline():
    mark_stale_pipeline_runs()

    run_id = start_pipeline_run("urban_systems_master")
    results = {}

    try:
        results["census"] = run_census_stage()
        results["bnia"] = run_bnia_stage()
        results["geography"] = run_geography_stage()

        census_metrics = results["census"]

        finish_pipeline_run(
            run_id,
            status="success",
            records_processed=(
                census_metrics["inserted"]
                + census_metrics["updated"]
            ),
            records_received=(
                census_metrics["inserted"]
                + census_metrics["updated"]
                + census_metrics["unchanged"]
            ),
            records_inserted=census_metrics["inserted"],
            records_updated=census_metrics["updated"],
            records_unchanged=census_metrics["unchanged"],
        )

        return results

    except Exception as error:
        finish_pipeline_run(
            run_id,
            status="failed",
            error_message=str(error),
        )

        raise


def main():
    pipeline_mode = os.getenv("PIPELINE_MODE", "database")

    if pipeline_mode == "cloud_validation":
        results = run_cloud_validation()
        print("Cloud validation completed successfully.")
    else:
        results = run_pipeline()
        print("Pipeline completed successfully.")

    for stage, result in results.items():
        print(f"{stage}: {result}")


def run_cloud_validation():
    results = {}

    census_data = get_census_data()
    validate_census_response(census_data)

    census_headers = census_data[0]
    census_rows = census_data[1:]

    census_records = transform_records(
        census_headers,
        census_rows,
    )
    validate_unique_tracts(census_records)

    results["census_records"] = len(census_records)

    workbook = load_bnia_workbook()

    try:
        bnia_observations = transform_bnia_workbook(workbook)
        bnia_geographies = transform_bnia_geographies(workbook)

        validate_unique_bnia_geographies(bnia_geographies)

        results["bnia_observations"] = len(bnia_observations)
        results["bnia_geographies"] = len(bnia_geographies)

    finally:
        workbook.close()

    geography_rows = read_crosswalk()
    geography_records = transform_crosswalk(geography_rows)
    validate_crosswalk(geography_records)

    results["geography_records"] = len(geography_records)

    return results


if __name__ == "__main__":
    main()