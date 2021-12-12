from typing import List, Dict

import pandas as pd

from lib.candle.candle import build_feed
from lib.candle.candle_repository import CandleRepository
from lib.exchange.exchange import Exchange


class DbFeed:
    exchange: Exchange
    candle_repository: CandleRepository

    def __init__(self, exchange: Exchange, candle_repository: CandleRepository):
        self.exchange = exchange
        self.candle_repository = candle_repository

    def build_feeds_by_ticker(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        feeds_by_ticker = {}

        for ticker in tickers:
            fresh_candle = self.exchange.get_last_candle(ticker)
            candles = self.candle_repository.get_candles(ticker, 1000)
            candles.insert(0, fresh_candle)

            feed = build_feed(candles=list(reversed(candles)))
            feeds_by_ticker[ticker] = feed

        return feeds_by_ticker
