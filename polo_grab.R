library(tomkit)
library(dplyr)
library(RJSONIO)


## Pairs
tracked_pairs <- c("USDT_BTC", "USDT_ETH", "USDT_LTC", "USDT_XMR", "BTC_ETH", "BTC_LTC", "BTC_XMR", "XMR_LTC")


## Grabs data from Polo API for training
grabPriceAPI <- function(symbol){
	cat("Grabbing ",symbol, " prices from Poloniex", fill=TRUE)
	"https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=1405699200&end=9999999999&period=300" %>%
		sprintf(symbol) %>%
		fromJSON() %>%
		lapply(function(y){
			y %>%
				t() %>%
				as.data.frame()
			}) %>%
		bind_rows() %>%
		mutate(date = as.character(date)) %>%
		select(date, weightedAverage, high, low, quoteVolume) %>%
		setNames(tolower(c("date",
			symbol %+% "_price",
			symbol %+% "_high",
			symbol %+% "_low",
			symbol %+% "_qvol")))
	}

all_pairs <- lapply(tracked_pairs, grabPriceAPI)

Reduce(function(frame1, frame2){
		inner_join(frame1,frame2,by="date")
	}, all_pairs) %>%
	write.csv("data/polo_prices.csv", row.names=FALSE)
