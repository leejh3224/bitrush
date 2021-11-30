import pandas as pd
from talib import abstract

from lib.strategy.base_strategy import BaseStrategy


class Cci(BaseStrategy):

    # settings
    period = 7
    high = 100
    low = 75

    def __init__(self, feed: pd.DataFrame):
        super().__init__(feed)
        cci = abstract.CCI(
            self.feed["high"], self.feed["low"], self.feed["close"], period=self.period
        )
        self.feed["cci"] = cci

    def get_name(self) -> str:
        return "cci"

    def should_buy(self) -> bool:
        return self.feed.iloc[-1]["cci"] >= self.high

    def should_sell(self) -> bool:
        return self.feed.iloc[-1]["cci"] < self.low