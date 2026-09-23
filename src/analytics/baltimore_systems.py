import os

import pandas as pd
import psycopg
from dotenv import load_dotenv
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

load_dotenv()


INDICATORS = {
    4: "black_pct",
    5: "white_pct",
    6: "asian_pct",
    7: "two_or_more_races_pct",
    8: "other_races_pct",
    9: "hispanic_pct",
    10: "racial_diversity_index",
    20: "median_household_income",
    27: "family_poverty_pct",
    34: "vacant_abandoned_pct",
    52: "violent_crime_rate",
    75: "chronic_absence_hs",
    91: "dropout_rate",
    92: "completion_rate",
    98: "youth_school_or_employed",
    137: "unemployment_rate",
}


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


def load_bnia_observations():
    indicator_numbers = tuple(INDICATORS)

    query = """
        SELECT
            year,
            csa2010,
            source_indicator_number,
            value
        FROM bnia_observations
        WHERE source_indicator_number = ANY(%s)
          AND csa2010 <> 'Baltimore City'
        ORDER BY year, csa2010, source_indicator_number;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (list(indicator_numbers),))
            rows = cursor.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "year",
            "csa2010",
            "source_indicator_number",
            "value",
        ],
    )


def build_analytical_dataset(observations):
    dataset = observations.pivot_table(
        index=["year", "csa2010"],
        columns="source_indicator_number",
        values="value",
        aggfunc="max",
    ).reset_index()

    dataset = dataset.rename(columns=INDICATORS)
    dataset.columns.name = None

    return dataset

def summarize_missingness(dataset):
    missing = dataset.isna().sum()

    summary = pd.DataFrame(
        {
            "missing_rows": missing,
            "missing_pct": (missing / len(dataset) * 100).round(1),
        }
    )

    return summary


def run_2023_regression(dataset):
    model_data = dataset[
        [
            "year",
            "csa2010",
            "violent_crime_rate",
            "family_poverty_pct",
            "vacant_abandoned_pct",
            "chronic_absence_hs",
        ]
    ].copy()

    model_data = model_data[model_data["year"] == 2023].dropna()

    y = model_data["violent_crime_rate"]

    X = model_data[
        [
            "family_poverty_pct",
            "vacant_abandoned_pct",
            "chronic_absence_hs",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    return model, model_data


def find_influential_csas(model, model_data):
    influence = model.get_influence()

    diagnostics = model_data[["csa2010"]].copy()
    diagnostics["cooks_distance"] = influence.cooks_distance[0]
    diagnostics["studentized_residual"] = influence.resid_studentized_external

    diagnostics = diagnostics.sort_values(
        "cooks_distance",
        ascending=False,
    )

    return diagnostics.head(10)


def run_sensitivity_regression(model_data):
    sensitivity_data = model_data[
        model_data["csa2010"] != "Downtown/Seton Hill"
    ].copy()

    y = sensitivity_data["violent_crime_rate"]

    X = sensitivity_data[
        [
            "family_poverty_pct",
            "vacant_abandoned_pct",
            "chronic_absence_hs",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    return model


def run_standardized_regression(model_data):
    columns = [
        "violent_crime_rate",
        "family_poverty_pct",
        "vacant_abandoned_pct",
        "chronic_absence_hs",
    ]

    standardized = model_data[columns].copy()

    standardized = (
        standardized - standardized.mean()
    ) / standardized.std()

    y = standardized["violent_crime_rate"]

    X = standardized[
        [
            "family_poverty_pct",
            "vacant_abandoned_pct",
            "chronic_absence_hs",
        ]
    ]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    return model

def run_robust_regression(model):
    robust_model = model.get_robustcov_results(cov_type="HC3")

    return robust_model


def calculate_vif(model_data):
    predictors = model_data[
        [
            "family_poverty_pct",
            "vacant_abandoned_pct",
            "chronic_absence_hs",
        ]
    ].copy()

    predictors = sm.add_constant(predictors)

    vif = pd.DataFrame(
        {
            "variable": predictors.columns,
            "vif": [
                variance_inflation_factor(predictors.values, i)
                for i in range(predictors.shape[1])
            ],
        }
    )

    return vif



def main():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)
    missingness = summarize_missingness(dataset)
    model, model_data = run_2023_regression(dataset)
    influential_csas = find_influential_csas(model, model_data)
    sensitivity_model = run_sensitivity_regression(model_data)
    standardized_model = run_standardized_regression(model_data)
    robust_model = run_robust_regression(standardized_model)
    vif = calculate_vif(model_data)


    print("Raw observation rows:", len(observations))
    print("Analytical rows:", len(dataset))
    print()
    print(dataset.head())
    print()
    print("Columns:")
    print(dataset.columns.tolist())
    print()
    print("Missingness:")
    print(missingness)
    print()
    print("2023 multivariable regression:")
    print(model.summary())
    print()
    print("Most influential 2023 CSAs:")
    print(influential_csas.to_string(index=False))
    print()
    print("2023 sensitivity regression excluding Downtown/Seton Hill:")
    print(sensitivity_model.summary())
    print()
    print("2023 standardized regression:")
    print(standardized_model.summary())
    print()
    print("2023 predictor VIF:")
    print(vif.to_string(index=False))
    print()
    print("2023 standardized regression with HC3 robust standard errors:")
    print(robust_model.summary())

if __name__ == "__main__":
    main()
