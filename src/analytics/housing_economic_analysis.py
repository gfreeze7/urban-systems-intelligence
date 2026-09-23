import statsmodels.api as sm

from src.analytics.baltimore_systems import (
    build_analytical_dataset,
    load_bnia_observations,
)


def run_2023_interaction_model(dataset):
    required_columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
    ]

    model_data = dataset[
        dataset["year"] == 2023
    ].dropna(
        subset=required_columns
    ).copy()

    model_data["poverty_centered"] = (
        model_data["family_poverty_pct"]
        - model_data["family_poverty_pct"].mean()
    )

    model_data["vacancy_centered"] = (
        model_data["vacant_abandoned_pct"]
        - model_data["vacant_abandoned_pct"].mean()
    )

    model_data["poverty_vacancy_interaction"] = (
        model_data["poverty_centered"]
        * model_data["vacancy_centered"]
    )

    y = model_data["violent_crime_rate"]

    X = model_data[
        [
            "poverty_centered",
            "vacancy_centered",
            "poverty_vacancy_interaction",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit(cov_type="HC3")

    return model, model_data


def run_yearly_interaction_models(dataset):
    results = []

    required_columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
    ]

    for year in sorted(dataset["year"].unique()):
        year_data = dataset[
            dataset["year"] == year
        ].dropna(
            subset=required_columns
        ).copy()

        if len(year_data) < 10:
            continue

        year_data["poverty_centered"] = (
            year_data["family_poverty_pct"]
            - year_data["family_poverty_pct"].mean()
        )

        year_data["vacancy_centered"] = (
            year_data["vacant_abandoned_pct"]
            - year_data["vacant_abandoned_pct"].mean()
        )

        year_data["poverty_vacancy_interaction"] = (
            year_data["poverty_centered"]
            * year_data["vacancy_centered"]
        )

        y = year_data["violent_crime_rate"]

        X = year_data[
            [
                "poverty_centered",
                "vacancy_centered",
                "poverty_vacancy_interaction",
            ]
        ]

        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit(cov_type="HC3")

        results.append(
            {
                "year": year,
                "n": len(year_data),
                "poverty_coef": model.params["poverty_centered"],
                "vacancy_coef": model.params["vacancy_centered"],
                "interaction_coef": model.params[
                    "poverty_vacancy_interaction"
                ],
                "interaction_p": model.pvalues[
                    "poverty_vacancy_interaction"
                ],
                "r_squared": model.rsquared,
            }
        )

    return results


def main():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)

    model, model_data = run_2023_interaction_model(
        dataset
    )

    yearly_results = run_yearly_interaction_models(
        dataset
    )


    print("2023 poverty × vacancy interaction model:")
    print("Observations:", len(model_data))
    print(model.summary())

    print()
    print("Yearly poverty × vacancy interactions:")

    for result in yearly_results:
        print(result)


if __name__ == "__main__":
    main()