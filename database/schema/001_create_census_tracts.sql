CREATE TABLE census_tracts (
    geoid CHAR(11) PRIMARY KEY,
    tract VARCHAR(6) NOT NULL,
    name TEXT NOT NULL,
    population INTEGER NOT NULL,
    state CHAR(2) NOT NULL,
    county CHAR(3) NOT NULL
);