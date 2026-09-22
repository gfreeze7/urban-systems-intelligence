BEGIN;

ALTER TABLE census_tracts
DROP COLUMN population;

COMMIT;