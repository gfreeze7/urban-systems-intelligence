from pathlib import Path

import matplotlib.pyplot as plt

from src.analytics.baltimore_systems import (
    build_analytical_dataset,
    load_bnia_observations,
)


OUTPUT_DIR = Path("data/processed/figures")


def build_2023_absence_violence_plot(dataset):
    plot_data = dataset[
        dataset["year"].eq(2023)
        & dataset["chronic_absence_hs"].notna()
        & dataset["violent_crime_rate"].notna()
    ].copy()

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        plot_data["chronic_absence_hs"],
        plot_data["violent_crime_rate"],
        alpha=0.75,
    )

    ax.set_title(
        "Chronic High-School Absence and Violent Crime\n"
        "Baltimore Community Statistical Areas, 2023"
    )
    ax.set_xlabel("Chronic high-school absence (%)")
    ax.set_ylabel("Violent crime rate")

    ax.grid(alpha=0.2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "2023_chronic_absence_vs_violent_crime.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    return output_path, len(plot_data)


def build_absence_violence_correlation_plot(dataset):
    yearly_correlations = (
        dataset.groupby("year")
        .apply(
            lambda group: group["chronic_absence_hs"].corr(
                group["violent_crime_rate"]
            ),
            include_groups=False,
        )
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        yearly_correlations.index,
        yearly_correlations.values,
        marker="o",
        linewidth=2,
    )

    ax.axhline(0, linewidth=1, linestyle="--")

    ax.set_title(
        "Chronic High-School Absence and Violent Crime\n"
        "Yearly CSA-Level Correlations in Baltimore"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Pearson correlation")

    ax.set_ylim(-1, 1)
    ax.grid(alpha=0.2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "yearly_absence_violence_correlation.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    return output_path, yearly_correlations


def build_2023_system_correlation_plot(dataset):
    columns = {
        "family_poverty_pct": "Family poverty",
        "vacant_abandoned_pct": "Vacancy",
        "chronic_absence_hs": "Chronic absence",
        "violent_crime_rate": "Violent crime",
    }

    plot_data = (
        dataset.loc[dataset["year"].eq(2023), list(columns)]
        .rename(columns=columns)
    )

    correlation_matrix = plot_data.corr()

    fig, ax = plt.subplots(figsize=(8, 7))

    image = ax.imshow(
        correlation_matrix,
        vmin=-1,
        vmax=1,
    )

    labels = correlation_matrix.columns

    ax.set_xticks(range(len(labels)), labels=labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels)), labels=labels)

    for row in range(len(labels)):
        for column in range(len(labels)):
            value = correlation_matrix.iloc[row, column]

            ax.text(
                column,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
            )

    ax.set_title(
        "Cross-System Relationships Across Baltimore CSAs, 2023"
    )

    fig.colorbar(image, ax=ax, label="Pearson correlation")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "2023_system_correlation_matrix.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    return output_path, correlation_matrix


def build_2023_distributional_correlation_plot(dataset):
    outcome_columns = {
        "family_poverty_pct": "Family poverty",
        "vacant_abandoned_pct": "Vacancy",
        "unemployment_rate": "Unemployment",
        "chronic_absence_hs": "Chronic absence",
        "violent_crime_rate": "Violent crime",
    }

    plot_data = dataset.loc[
        dataset["year"].eq(2023),
        ["black_pct", *outcome_columns],
    ]

    correlations = (
        plot_data.corr()["black_pct"]
        .drop("black_pct")
        .rename(index=outcome_columns)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        correlations.index,
        correlations.values,
    )

    ax.axvline(0, linewidth=1, linestyle="--")

    for index, value in enumerate(correlations.values):
        ax.text(
            value + 0.015,
            index,
            f"{value:.2f}",
            va="center",
        )

    ax.set_title(
        "Black Population Share and Aggregate Neighborhood Conditions\n"
        "Baltimore Community Statistical Areas, 2023"
    )
    ax.set_xlabel("Pearson correlation with Black population share")
    ax.set_xlim(-1, 1)

    ax.text(
        0.5,
        -0.18,
        "Neighborhood-level ecological associations; not individual effects or causal estimates.",
        transform=ax.transAxes,
        ha="center",
        fontsize=9,
    )

    ax.grid(axis="x", alpha=0.2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "2023_distributional_correlations.png"

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return output_path, correlations


def main():
    observations = load_bnia_observations()
    dataset = build_analytical_dataset(observations)

    scatter_path, observation_count = build_2023_absence_violence_plot(dataset)

    print(f"Observations plotted: {observation_count}")
    print(f"Figure saved to: {scatter_path}")

    correlation_path, yearly_correlations = (
        build_absence_violence_correlation_plot(dataset)
    )

    print("\nYearly chronic-absence / violent-crime correlations:")
    print(yearly_correlations.to_string())

    print(f"\nFigure saved to: {correlation_path}")

    matrix_path, correlation_matrix = (
        build_2023_system_correlation_plot(dataset)
    )

    print("\n2023 cross-system correlation matrix:")
    print(correlation_matrix.to_string())

    print(f"\nFigure saved to: {matrix_path}")

    distributional_path, distributional_correlations = (
        build_2023_distributional_correlation_plot(dataset)
    )

    print("\n2023 distributional correlations:")
    print(distributional_correlations.to_string())

    print(f"\nFigure saved to: {distributional_path}")


if __name__ == "__main__":
    main()