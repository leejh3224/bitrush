import numpy as np
import pandas as pd
from talib import abstract, MA_Type

from lib.strategy.base_strategy import BaseStrategy


class RsiBb(BaseStrategy):

    # settings
    period = 7
    buy_threshold = 0.7
    sell_threshold = 0.5

    def __init__(self, feed: pd.DataFrame):
        super().__init__(feed)

        if self.has_enough_feed():
            rsi = abstract.RSI(self.feed, period=self.period)
            maxrsi = abstract.MAX(rsi, period=self.period)
            minrsi = abstract.MIN(rsi, period=self.period)
            srsi = (rsi - minrsi) / (maxrsi - minrsi)

            self.feed["srsi"] = srsi

            bb = abstract.BBANDS(self.feed, matype=MA_Type.T3, period=self.period)
            self.feed["bbh"] = bb["upperband"]
            prev_close = self.feed["close"].shift(1)
            prev_bbh = self.feed["bbh"].shift(1)
            self.feed["bbh_cross_up"] = (self.feed["close"] > self.feed["bbh"]) & (
                    prev_close <= prev_bbh
            )

    def get_name(self) -> str:
        return "rsi_bollinger_bands"

    def should_buy(self) -> bool:
        return (
                self.feed.iloc[-1]["srsi"] >= self.buy_threshold
                and self.feed.iloc[-1]["bbh_cross_up"]
        )

    def should_sell(self) -> bool:
        return self.feed.iloc[-1]["srsi"] <= self.sell_threshold

    def is_valid(self) -> bool:
        return not np.isnan(self.feed.iloc[-1]["srsi"]) and not np.isnan(self.feed.iloc[-1]["bbh"])
