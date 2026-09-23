import pandas as pd
import statsmodels.api as sm

from src.analytics.baltimore_systems import (
    build_analytical_dataset,
    load_bnia_observations,
)


def run_yearly_regressions(dataset):
    results = []

    required_columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "chronic_absence_hs",
    ]

    for year in sorted(dataset["year"].unique()):
        year_data = dataset[
            dataset["year"] == year
        ].dropna(subset=required_columns)

        if len(year_data) < 10:
            continue

        y = year_data["violent_crime_rate"]

        X = year_data[
            [
                "family_poverty_pct",
                "vacant_abandoned_pct",
                "chronic_absence_hs",
            ]
        ]

        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit(cov_type="HC3")

        results.append(
            {
                "year": year,
                "n": len(year_data),
                "poverty_coef": model.params["family_poverty_pct"],
                "vacancy_coef": model.params["vacant_abandoned_pct"],
                "absence_coef": model.params["chronic_absence_hs"],
                "absence_p": model.pvalues["chronic_absence_hs"],
                "r_squared": model.rsquared,
            }
        )

    return pd.DataFrame(results)


def build_within_csa_changes(dataset):
    columns = [
        "csa2010",
        "year",
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "chronic_absence_hs",
    ]

    changes = dataset[columns].copy()

    changes = changes.sort_values(
        ["csa2010", "year"]
    )

    changes["year_gap"] = (
        changes.groupby("csa2010")["year"].diff()
    )

    change_columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "chronic_absence_hs",
    ]

    for column in change_columns:
        changes[f"{column}_change"] = (
            changes.groupby("csa2010")[column].diff()
        )

    changes = changes[
        changes["year_gap"] == 1
    ].copy()

    return changes

def run_within_csa_change_regression(changes):
    required_columns = [
        "violent_crime_rate_change",
        "family_poverty_pct_change",
        "vacant_abandoned_pct_change",
        "chronic_absence_hs_change",
    ]

    model_data = changes.dropna(
        subset=required_columns
    ).copy()

    y = model_data["violent_crime_rate_change"]

    X = model_data[
        [
            "family_poverty_pct_change",
            "vacant_abandoned_pct_change",
            "chronic_absence_hs_change",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit(cov_type="HC3")

    return model, model_data


def compare_education_measures(dataset):
    education_data = dataset[
        [
            "year",
            "csa2010",
            "chronic_absence_hs",
            "dropout_rate",
            "completion_rate",
        ]
    ].copy()

    summary = education_data[
        [
            "chronic_absence_hs",
            "dropout_rate",
            "completion_rate",
        ]
    ].describe().T

    yearly_correlations = []

    for year in sorted(education_data["year"].unique()):
        year_data = education_data[
            education_data["year"] == year
        ]

        absence_dropout = year_data[
            [
                "chronic_absence_hs",
                "dropout_rate",
            ]
        ].dropna()

        if len(absence_dropout) < 10:
            continue

        correlation = absence_dropout[
            "chronic_absence_hs"
        ].corr(
            absence_dropout["dropout_rate"]
        )

        yearly_correlations.append(
            {
                "year": year,
                "n": len(absence_dropout),
                "absence_dropout_r": correlation,
            }
        )

    return summary, pd.DataFrame(yearly_correlations)


def test_dropout_outlier_sensitivity(dataset):
    results = []

    for year in [2022, 2023]:
        year_data = dataset[
            dataset["year"] == year
        ][
            [
                "csa2010",
                "chronic_absence_hs",
                "dropout_rate",
            ]
        ].dropna().copy()

        full_correlation = year_data[
            "chronic_absence_hs"
        ].corr(
            year_data["dropout_rate"]
        )

        highest_dropout_index = year_data[
            "dropout_rate"
        ].idxmax()

        highest_dropout_csa = year_data.loc[
            highest_dropout_index,
            "csa2010"
        ]

        highest_dropout_value = year_data.loc[
            highest_dropout_index,
            "dropout_rate"
        ]

        sensitivity_data = year_data.drop(
            index=highest_dropout_index
        )

        sensitivity_correlation = sensitivity_data[
            "chronic_absence_hs"
        ].corr(
            sensitivity_data["dropout_rate"]
        )

        results.append(
            {
                "year": year,
                "full_r": full_correlation,
                "highest_dropout_csa": highest_dropout_csa,
                "highest_dropout": highest_dropout_value,
                "without_highest_r": sensitivity_correlation,
            }
        )

    return pd.DataFrame(results)


def run_yearly_dropout_regressions(dataset):
    results = []

    required_columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "dropout_rate",
    ]

    for year in sorted(dataset["year"].unique()):
        year_data = dataset[
            dataset["year"] == year
        ].dropna(subset=required_columns)

        if len(year_data) < 10:
            continue

        y = year_data["violent_crime_rate"]

        X = year_data[
            [
                "family_poverty_pct",
                "vacant_abandoned_pct",
                "dropout_rate",
            ]
        ]

        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit(cov_type="HC3")

        results.append(
            {
                "year": year,
                "n": len(year_data),
                "poverty_coef": model.params["family_poverty_pct"],
                "vacancy_coef": model.params["vacant_abandoned_pct"],
                "dropout_coef": model.params["dropout_rate"],
                "dropout_p": model.pvalues["dropout_rate"],
                "r_squared": model.rsquared,
            }
        )

    return pd.DataFrame(results)


def main():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)

    yearly_results = run_yearly_regressions(dataset)
    within_csa_changes = build_within_csa_changes(dataset)

    change_model, change_model_data = run_within_csa_change_regression(
        within_csa_changes
    )

    education_summary, education_correlations = (
    compare_education_measures(dataset)
    )

    dropout_sensitivity = test_dropout_outlier_sensitivity(
        dataset
    )

    dropout_yearly_results = run_yearly_dropout_regressions(
        dataset
    )

    print("Yearly multivariable regressions:")
    print(yearly_results.to_string(index=False))

    print()
    print("Within-CSA consecutive-year changes:")
    print(within_csa_changes.head(10).to_string(index=False))

    print()
    print("Number of change observations:", len(within_csa_changes))

    print()
    print("Within-CSA consecutive-year change regression:")
    print("Complete change observations:", len(change_model_data))
    print(change_model.summary())

    print()
    print("Education measure summary:")
    print(education_summary.to_string())

    print()
    print("Chronic absence vs dropout by year:")
    print(education_correlations.to_string(index=False))

    print()
    print("Dropout outlier sensitivity:")
    print(dropout_sensitivity.to_string(index=False))

    print()
    print("Yearly dropout multivariable regressions:")
    print(dropout_yearly_results.to_string(index=False))


if __name__ == "__main__":
    main()