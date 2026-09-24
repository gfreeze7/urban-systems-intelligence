from pathlib import Path

from src.analytics.baltimore_systems import (
    build_analytical_dataset,
    load_bnia_observations,
)


OUTPUT_DIR = Path("data/processed/bi")
OUTPUT_FILE = OUTPUT_DIR / "baltimore_csa_year.csv"


def build_bi_dataset():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)

    dataset = dataset.sort_values(
        ["year", "csa2010"]
    ).reset_index(drop=True)

    return dataset


def validate_bi_dataset(dataset):
    required_columns = {
        "year",
        "csa2010",
        "median_household_income",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "violent_crime_rate",
        "chronic_absence_hs",
        "dropout_rate",
        "completion_rate",
        "youth_school_or_employed",
        "unemployment_rate",
    }

    missing_columns = required_columns - set(dataset.columns)

    if missing_columns:
        raise ValueError(
            f"BI dataset missing required columns: {sorted(missing_columns)}"
        )

    if dataset.empty:
        raise ValueError("BI dataset contains no rows")

    if dataset.duplicated(["year", "csa2010"]).any():
        raise ValueError("Duplicate CSA-year rows found")

    return True


def export_bi_dataset(dataset):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(OUTPUT_FILE, index=False)

    return OUTPUT_FILE


def main():
    dataset = build_bi_dataset()
    validate_bi_dataset(dataset)
    output_file = export_bi_dataset(dataset)

    print("BI reporting dataset created successfully.")
    print("Rows:", len(dataset))
    print("Columns:", len(dataset.columns))
    print("Years:", f"{dataset['year'].min()}-{dataset['year'].max()}")
    print("Output:", output_file)


if __name__ == "__main__":
    main()