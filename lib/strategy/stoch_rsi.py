import pandas as pd
from talib import abstract

from lib.strategy.base_strategy import BaseStrategy


class StochRSI(BaseStrategy):

    # settings
    period = 30
    buy_threshold = 0.7
    sell_threshold = 0.3

    def __init__(self, feed: pd.DataFrame):
        super().__init__(feed)

        if self.has_enough_feed():
            rsi = abstract.RSI(self.feed, period=self.period)
            maxrsi = abstract.MAX(rsi, period=self.period)
            minrsi = abstract.MIN(rsi, period=self.period)
            srsi = (rsi - minrsi) / (maxrsi - minrsi)

            self.feed["srsi"] = srsi
            prev_srsi = self.feed["srsi"].shift(1)
            self.feed["cross_up"] = (self.feed["srsi"] > self.buy_threshold) & (
                    prev_srsi <= self.buy_threshold
            )
            self.feed["cross_down"] = (self.feed["srsi"] < self.sell_threshold) & (
                    prev_srsi >= self.sell_threshold
            )

    def get_name(self) -> str:
        return "stoch_rsi"

    def should_buy(self) -> bool:
        return self.feed.iloc[-1]["cross_up"]

    def should_sell(self) -> bool:
        return self.feed.iloc[-1]["cross_down"]
