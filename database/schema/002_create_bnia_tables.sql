CREATE TABLE bnia_geographies (
    year INTEGER NOT NULL,
    csa2010 TEXT NOT NULL,
    csa2020 TEXT,
    is_citywide BOOLEAN NOT NULL,
    PRIMARY KEY (year, csa2010)
);

CREATE TABLE bnia_observations (
    observation_id BIGSERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    csa2010 TEXT NOT NULL,
    source_indicator_number INTEGER,
    source_indicator_name TEXT NOT NULL,
    raw_value TEXT,
    value DOUBLE PRECISION,

    UNIQUE NULLS NOT DISTINCT (
        year,
        csa2010,
        source_indicator_number,
        source_indicator_name
    ),

    FOREIGN KEY (year, csa2010)
        REFERENCES bnia_geographies (year, csa2010)
);