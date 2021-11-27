import pandas as pd
from talib import abstract

from lib.strategy.base_strategy import BaseStrategy


class DcBreakout(BaseStrategy):

    # settings
    low_period = 10
    high_period = 20

    def __init__(self, feed: pd.DataFrame):
        super().__init__(feed)

        dch = abstract.MAX(self.feed["close"], timeperiod=self.high_period)
        dcl = abstract.MIN(self.feed["close"], timeperiod=self.low_period)

        self.feed["dch"] = dch
        self.feed["dcl"] = dcl
        prev_close = self.feed["close"].shift(1)
        prev_dch = self.feed["dch"].shift(1)
        prev_dcl = self.feed["dcl"].shift(1)

        self.feed["cross_up"] = (self.feed["close"] >= self.feed["dch"]) & (
                prev_close < prev_dch
        )
        self.feed["cross_down"] = (self.feed["close"] <= self.feed["dcl"]) & (
                prev_close > prev_dcl
        )

    def get_name(self) -> str:
        return "dc_breakout"

    def should_buy(self) -> bool:
        return self.feed.iloc[-1]["cross_up"]

    def should_sell(self) -> bool:
        return self.feed.iloc[-1]["cross_down"]
