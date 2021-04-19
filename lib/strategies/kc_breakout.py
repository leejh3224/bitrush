from lib.strategies.base_strategy import BaseStrategy
from talib import abstract


class KcBreakout(BaseStrategy):
    name = "kc_breakout"

    # settings
    period = 45
    n = 2
    stop_n = 3

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        self.ma = abstract.SMA(self.feed, timeperiod=self.period)
        self.high = abstract.MAX(self.feed["close"], timeperiod=self.period)
        self.atr = abstract.ATR(
            self.feed["high"],
            self.feed["low"],
            self.feed["close"],
            timeperiod=self.period,
        )
        self.close = self.feed["close"]

    def should_buy(self) -> bool:
        return (self.close >= self.ma + self.n * self.atr).iloc[-1]

    def should_sell(self) -> bool:
        return (
            (self.close <= self.ma - self.n * self.atr)
            | (self.close <= self.high - self.stop_n * self.atr)
        ).iloc[-1]
