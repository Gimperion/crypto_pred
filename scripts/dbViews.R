library(RODBC)
dbcrypto <- odbcConnect("cryptopred")


### Most Recent 144 Rows ###
sqlQuery(dbcrypto, "
    CREATE or REPLACE VIEW polo_current AS
    SELECT *
    FROM (
        SELECT *
        FROM polo_main
        ORDER BY date DESC
        LIMIT 144
    ) A
    ORDER BY date;"
)


### Last Date Stamp ###
sqlQuery(dbcrypto, "
    CREATE OR REPLACE VIEW polo_last AS
    SELECT max(date) as date
    FROM polo_main;
")
