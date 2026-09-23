from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("data/processed/analytics")


EVIDENCE = [
    {
        "hypothesis": "Economic disadvantage and violent crime cluster geographically",
        "evidence_state": "SUPPORTED",
        "evidence": (
            "Across Baltimore CSA cross-sections, income is consistently negatively "
            "associated with violent crime, while poverty and unemployment are "
            "consistently positively associated with violent crime."
        ),
        "limitation": (
            "The relationships are observational and do not establish that economic "
            "disadvantage causes violent crime."
        ),
    },
    {
        "hypothesis": "Urban problems overlap across institutional systems",
        "evidence_state": "SUPPORTED",
        "evidence": (
            "Poverty, residential vacancy, chronic high-school absence, and violent "
            "crime show persistent geographic overlap across Baltimore CSAs."
        ),
        "limitation": (
            "Geographic clustering does not establish the causal direction or mechanism "
            "connecting the systems."
        ),
    },
    {
        "hypothesis": "Education-system dysfunction is uniformly associated with violence",
        "evidence_state": "COMPLICATED",
        "evidence": (
            "Chronic high-school absence is a persistent correlate of violent crime, "
            "including after accounting for poverty and vacancy, while dropout/withdrawal "
            "is substantially less temporally consistent."
        ),
        "limitation": (
            "Different education indicators measure different processes and may have "
            "different denominators, timing, and sensitivity to extreme observations."
        ),
    },
    {
        "hypothesis": "Short-term deterioration within a neighborhood moves with violence",
        "evidence_state": "COMPLICATED",
        "evidence": (
            "Within-CSA year-to-year changes show substantially weaker relationships "
            "than repeated cross-sectional comparisons, including a much weaker "
            "chronic-absence relationship."
        ),
        "limitation": (
            "Annual first differences may miss lagged relationships and may amplify "
            "measurement noise."
        ),
    },
    {
        "hypothesis": "Housing and economic disadvantage compound one another",
        "evidence_state": "COMPLICATED",
        "evidence": (
            "Poverty and vacancy are each positively associated with violent crime, "
            "but the poverty-vacancy interaction is consistently negative across "
            "available yearly models rather than showing simple compounding."
        ),
        "limitation": (
            "Interaction estimates vary in statistical precision and do not identify "
            "a causal mechanism."
        ),
    },
    {
        "hypothesis": "Structural disadvantage is distributed evenly across demographic geography",
        "evidence_state": "CONTRADICTED",
        "evidence": (
            "Across available demographic years, Baltimore CSAs with larger Black "
            "population shares consistently show higher poverty, vacancy, unemployment, "
            "and chronic high-school absence, while larger White population shares show "
            "the inverse neighborhood-level pattern."
        ),
        "limitation": (
            "These are ecological associations. Black and White population shares are "
            "also strongly inversely related, so their results are not independent and "
            "cannot be interpreted as individual-level racial effects."
        ),
    },
    {
        "hypothesis": "The observed system relationships are causal",
        "evidence_state": "UNRESOLVED",
        "evidence": (
            "The current analyses establish repeated associations, robustness patterns, "
            "and important complications but do not identify causal effects."
        ),
        "limitation": (
            "Causal claims would require stronger identification strategies and evidence "
            "than the current observational CSA-level design provides."
        ),
    },
]


def build_evidence_matrix():
    return pd.DataFrame(EVIDENCE)


def main():
    matrix = build_evidence_matrix()

    print("The Wire hypothesis evidence matrix:")
    print(matrix.to_string(index=False))

    print("\nEvidence-state counts:")
    print(matrix["evidence_state"].value_counts().to_string())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "the_wire_evidence_matrix.csv"

    matrix.to_csv(output_path, index=False)

    print(f"\nEvidence matrix saved to: {output_path}")


if __name__ == "__main__":
    main()