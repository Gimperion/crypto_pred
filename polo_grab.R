library(tomkit)
library(dplyr)
library(RJSONIO)
library(RODBC)

source("include/polo_pull.R")
dbcrypto <- odbcConnect("cryptopred")

all_pairs <- lapply(tracked_pairs, grabPoloCharts)

cat("Merging and saving to database...",fill=TRUE)
Reduce(function(frame1, frame2){
		inner_join(frame1,frame2,by="date")
	}, all_pairs) %>%
	pipeMarker(text="Saving to DB. Rows = " %+% nrow(.)) %>%
	sqlSave(channel=dbcrypto, tablename="polo_main", rownames=FALSE, safer=FALSE)

polo_rows <- sqlQuery(dbcrypto, "SELECT count(*) as count FROM polo_main;")
cat("Operations finished. ", polo_rows$count[1] %+% "rows", fill=TRUE)
