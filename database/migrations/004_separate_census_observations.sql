BEGIN;

CREATE TABLE census_acs_observations (
    geoid CHAR(11) NOT NULL,
    year INTEGER NOT NULL,
    dataset TEXT NOT NULL,
    variable TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,

    PRIMARY KEY (geoid, year, dataset, variable),

    FOREIGN KEY (geoid)
        REFERENCES census_tracts (geoid)
);

INSERT INTO census_acs_observations (
    geoid,
    year,
    dataset,
    variable,
    value
)
SELECT
    geoid,
    2024,
    'acs5',
    'B01003_001E',
    population
FROM census_tracts;

COMMIT;