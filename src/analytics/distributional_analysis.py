import pandas as pd

from src.analytics.baltimore_systems import (
    build_analytical_dataset,
    load_bnia_observations,
)


DEMOGRAPHIC_COLUMNS = [
    "black_pct",
    "white_pct",
    "asian_pct",
    "two_or_more_races_pct",
    "other_races_pct",
    "hispanic_pct",
]

OUTCOME_COLUMNS = [
    "family_poverty_pct",
    "vacant_abandoned_pct",
    "violent_crime_rate",
    "chronic_absence_hs",
    "unemployment_rate",
]


def calculate_2023_correlations(dataset):
    data_2023 = dataset[
        dataset["year"] == 2023
    ].copy()

    results = []

    for demographic in DEMOGRAPHIC_COLUMNS:
        for outcome in OUTCOME_COLUMNS:
            pair = data_2023[
                [demographic, outcome]
            ].dropna()

            correlation = pair[demographic].corr(
                pair[outcome]
            )

            results.append(
                {
                    "demographic": demographic,
                    "outcome": outcome,
                    "n": len(pair),
                    "correlation": correlation,
                }
            )

    return pd.DataFrame(results)


def calculate_yearly_distributional_correlations(dataset):
    demographics = [
        "black_pct",
        "white_pct",
    ]

    results = []

    for year in sorted(dataset["year"].unique()):
        year_data = dataset[
            dataset["year"] == year
        ]

        for demographic in demographics:
            if year_data[demographic].notna().sum() == 0:
                continue

            result = {
                "year": year,
                "demographic": demographic,
            }

            for outcome in OUTCOME_COLUMNS:
                pair = year_data[
                    [demographic, outcome]
                ].dropna()

                result[outcome] = (
                    pair[demographic].corr(pair[outcome])
                    if len(pair) >= 10
                    else None
                )

            results.append(result)

    return pd.DataFrame(results)


def calculate_demographic_composition_relationship(dataset):
    data_2023 = dataset[
        dataset["year"] == 2023
    ][
        ["black_pct", "white_pct"]
    ].dropna()

    return data_2023["black_pct"].corr(
        data_2023["white_pct"]
    )


def main():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)

    correlations = calculate_2023_correlations(
        dataset
    )

    print("2023 demographic × structural outcome correlations:")
    print(
        correlations.to_string(
            index=False
        )
    )

    yearly_results = calculate_yearly_distributional_correlations(
        dataset
    )

    print("\nYearly Black/White composition × structural outcome correlations:")
    print(
        yearly_results.to_string(
            index=False
        )
    )

    black_white_correlation = (
        calculate_demographic_composition_relationship(
            dataset
        )
    )

    print(
        "\n2023 Black % × White % correlation:",
        round(black_white_correlation, 3),
    )


if __name__ == "__main__":
    main()