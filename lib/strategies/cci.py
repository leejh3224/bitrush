from lib.strategies.base_strategy import BaseStrategy
from talib import abstract


class Cci(BaseStrategy):
    name = "cci"

    # settings
    period = 7
    high = 100
    low = 75

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        cci = abstract.CCI(
            self.feed["high"], self.feed["low"], self.feed["close"], period=self.period
        )

        self.feed["cci"] = cci

        self.current_ohlcv = self.feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cci"] >= self.high

    def should_sell(self) -> bool:
        return self.current_ohlcv["cci"] < self.low
