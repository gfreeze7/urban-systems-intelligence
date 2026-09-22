CREATE TABLE tract2020_to_csa2010 (
    geoid2020 CHAR(11) PRIMARY KEY,
    statefp CHAR(2) NOT NULL,
    countyfp CHAR(3) NOT NULL,
    tractce2020 CHAR(6) NOT NULL,
    tract_name TEXT NOT NULL,
    tract_label TEXT NOT NULL,
    csa2010 TEXT NOT NULL,

    FOREIGN KEY (geoid2020)
        REFERENCES census_tracts (geoid)
);