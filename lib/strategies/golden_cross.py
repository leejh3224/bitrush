from talib import abstract
from lib.strategies.base_strategy import BaseStrategy


class GoldenCross(BaseStrategy):
    name = "golden_cross"

    # settings
    short_period = 10
    long_period = 20

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)

        mas = abstract.SMA(self.feed, timeperiod=self.short_period)
        mal = abstract.SMA(self.feed, timeperiod=self.long_period)
        self.feed["mas"] = mas
        self.feed["mal"] = mal
        prev_mas = self.feed["mas"].shift(1)
        prev_mal = self.feed["mal"].shift(1)
        self.feed["cross_up"] = (self.feed["mas"] >= self.feed["mal"]) & (
            prev_mas <= prev_mal
        )
        self.feed["cross_down"] = (self.feed["mas"] <= self.feed["mal"]) & (
            prev_mas >= prev_mal
        )

        self.current_ohlcv = self.feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cross_up"]

    def should_sell(self) -> bool:
        return self.current_ohlcv["cross_down"]
