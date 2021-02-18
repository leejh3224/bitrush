from lib.strategies.base_strategy import BaseStrategy
from talib import abstract


class Cci(BaseStrategy):
    name = "cci"

    # settings
    period = 7
    high = 100
    low = 60

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        cci = abstract.CCI(feed["high"], feed["low"], feed["close"], period=self.period)

        feed["cci"] = cci

        print(feed.tail(55))

        self.current_ohlcv = feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cci"] >= self.high

    def should_sell(self) -> bool:
        return self.current_ohlcv["cci"] < self.low
