from talib import abstract
from lib.strategies.base_strategy import BaseStrategy


class Aroon(BaseStrategy):
    name = "aroon"

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)
        aroon = abstract.AROONOSC(feed)

        self.prev_aroon_val = aroon.iloc[-2]
        self.aroon_val = aroon.iloc[-1]

    def should_buy(self) -> bool:
        return self.prev_aroon_val < 70 and self.aroon_val >= 70

    def should_sell(self) -> bool:
        return self.prev_aroon_val >= 0 and self.aroon_val < 0
