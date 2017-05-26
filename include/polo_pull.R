require(tomkit)
require(RJSONIO)
require(dplyr)

## Price Pairs
tracked_pairs <- c("USDT_BTC", "USDT_ETH", "USDT_LTC", "USDT_XMR", "BTC_ETH", "BTC_LTC", "BTC_XMR", "XMR_LTC")

## Grabs data from Polo Charts API for training
## start date can be updated for smaller data chunks
grabPoloCharts <- function(symbol, start="1405699200"){
	cat("Grabbing ",symbol, " prices from Poloniex", fill=TRUE)
	"https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=%s&end=9999999999&period=300" %>%
		sprintf(symbol, as.character(start)) %>%
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
