from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("data/processed/analytics")


INTERVENTIONS = [
    {
        "intervention": "Adaptive parent attendance messaging",
        "system": "Education",
        "geography": "Four large U.S. urban school districts",
        "study_design": "Randomized adaptive trial",
        "population": "K-5 students",
        "outcome": "Chronic absence",
        "result": (
            "All tested messaging strategies reduced chronic absence. "
            "Overall reductions were 2.4-3.6 percentage points from a "
            "20.5% comparison-group rate."
        ),
        "causal_scope": (
            "Supports a causal effect of the messaging intervention on "
            "chronic absence in the study population."
        ),
        "limitation": (
            "Does not establish that reducing chronic absence reduces "
            "violent crime or that Baltimore would experience the same effect."
        ),
        "source": "U.S. Institute of Education Sciences",
        "source_url": (
            "https://ies.ed.gov/use-work/evaluations/"
            "impact-evaluation-parent-messaging-strategies-student-attendance"
        ),
    },
    {
        "intervention": "Abandoned-house remediation",
        "system": "Housing / physical environment",
        "geography": "Philadelphia, Pennsylvania",
        "study_design": "Cluster randomized controlled trial",
        "population": "63 clusters containing 258 abandoned houses",
        "outcome": "Gun violence",
        "result": (
            "Full remediation was associated with 8.43% fewer weapons "
            "violations and 13.12% fewer gun assaults relative to control. "
            "The estimated 6.96% reduction in shootings was not statistically "
            "significant."
        ),
        "causal_scope": (
            "Random assignment provides strong evidence for effects of the "
            "tested housing remediation intervention in the study setting."
        ),
        "limitation": (
            "Philadelphia results do not establish that Baltimore would "
            "experience the same effect."
        ),
        "source": "JAMA Internal Medicine",
        "source_url": (
            "https://jamanetwork.com/journals/jamainternalmedicine/"
            "fullarticle/2799226"
        ),
    },
    {
        "intervention": "Jobs-Plus",
        "system": "Economic opportunity",
        "geography": "U.S. public housing developments including Baltimore",
        "study_design": "Place-based demonstration with comparison sites",
        "population": "Working-age public housing residents",
        "outcome": "Employment and earnings",
        "result": (
            "The original demonstration produced earnings gains in sites "
            "that fully implemented the model, while a later 24-site "
            "replication found no measurable additional employment or "
            "earnings gains."
        ),
        "causal_scope": (
            "Evidence supports potential economic effects under some "
            "implementation conditions rather than a uniform program effect."
        ),
        "limitation": (
            "Results vary substantially with implementation, site, period, "
            "and evaluation design."
        ),
        "source": "HUD / MDRC Jobs-Plus evaluations",
        "source_url": (
            "https://www.huduser.gov/portal/publications/"
            "Jobs-Plus-Long-Term-Effects.html"
        ),
    },
    {
        "intervention": "Moving to Opportunity",
        "system": "Housing mobility / economic opportunity",
        "geography": "Five U.S. cities including Baltimore",
        "study_design": "Randomized housing mobility experiment",
        "population": "Low-income families in high-poverty housing",
        "outcome": "Long-term outcomes for children",
        "result": (
            "Children who moved to lower-poverty neighborhoods before age 13 "
            "experienced higher college attendance and, among voucher users, "
            "annual income in their mid-twenties about $3,477 or 31% above "
            "the control-group mean."
        ),
        "causal_scope": (
            "Random assignment supports causal inference about the housing "
            "mobility offer; treatment-on-treated estimates describe families "
            "who used the experimental voucher."
        ),
        "limitation": (
            "Effects depend strongly on age and exposure timing and should "
            "not be generalized to all populations or housing interventions."
        ),
        "source": "Chetty, Hendren and Katz / NBER",
        "source_url": "https://www.nber.org/papers/w21156",
    },
    {
        "intervention": "Safe Streets Baltimore",
        "system": "Public safety / community violence intervention",
        "geography": "Baltimore, Maryland",
        "study_design": "Quasi-experimental augmented synthetic control",
        "population": "Neighborhoods served by 11 Safe Streets sites",
        "outcome": "Homicides and nonfatal shootings",
        "result": (
            "The five longest-running sites had an estimated 32% reduction "
            "in homicides during their first four years, while all 11 sites "
            "combined were associated with a 23% reduction in nonfatal "
            "shootings over the implementation period."
        ),
        "causal_scope": (
            "Provides quasi-experimental evidence consistent with program "
            "effects but is not a randomized trial."
        ),
        "limitation": (
            "Effects varied substantially across sites, including sites with "
            "no clear reductions and isolated adverse estimates."
        ),
        "source": "Johns Hopkins Center for Gun Violence Solutions",
        "source_url": (
            "https://publichealth.jhu.edu/2023/"
            "new-report-finds-that-baltimores-community-violence-"
            "intervention-program-safe-streets-reduced-gun-violence"
        ),
    },
]


def build_intervention_evidence():
    return pd.DataFrame(INTERVENTIONS)


def main():
    evidence = build_intervention_evidence()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "intervention_evidence.csv"

    evidence.to_csv(output_path, index=False)

    print("Intervention evidence register:")
    print(
        evidence[
            [
                "intervention",
                "system",
                "study_design",
                "outcome",
            ]
        ].to_string(index=False)
    )

    print(f"\nIntervention evidence saved to: {output_path}")


if __name__ == "__main__":
    main()