#!/usr/bin/Rscript

setwd("~/codedev/crypto_pred")

library(tomkit)
library(dplyr)
library(RJSONIO)
library(RODBC)

source("include/polo_pull.R")
dbcrypto <- odbcConnect("cryptopred")

latest <- sqlFetch(dbcrypto, "polo_last")$date[1]
all_pairs <- lapply(tracked_pairs, grabPoloCharts, latest-1)

## Deleting last line
sprintf("DELETE FROM polo_main
	WHERE date = '%s'
", latest) %>%
	sqlQuery(channel = dbcrypto) %>%
	print()

## Merging new data and pushing to DB
cat("Merging and Inserting to DB...",fill=TRUE)
Reduce(function(frame1, frame2){
		inner_join(frame1,frame2,by="date")
	}, all_pairs) %>%
	pipeMarker(text="Saving to DB. Rows = " %+% nrow(.)) %>%
	sqlSave(channel=dbcrypto, tablename="polo_main", rownames=FALSE, safer=TRUE, append=TRUE)
