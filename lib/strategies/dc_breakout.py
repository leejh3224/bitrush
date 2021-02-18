from lib.strategies.base_strategy import BaseStrategy
from talib import abstract, MA_Type


class DcBreakout(BaseStrategy):
    name = "dc_breakout"

    # settings
    low_period = 2
    high_period = 4

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)

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

        self.current_ohlcv = self.feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cross_up"]

    def should_sell(self) -> bool:
        return self.current_ohlcv["cross_down"]
