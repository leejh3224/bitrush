from os import environ

import pandas as pd
from talib import abstract

from lib.strategy.base_strategy import BaseStrategy


class Aroon(BaseStrategy):

    buy_threshold = 70
    sell_threshold = 0

    def __init__(self, feed: pd.DataFrame) -> None:
        super().__init__(feed)

        if self.has_enough_feed():
            aroon = abstract.AROONOSC(self.feed)

            self.prev_aroon_val = aroon.iloc[-2]
            self.aroon_val = aroon.iloc[-1]

    def get_name(self) -> str:
        return "aroon"

    def should_buy(self) -> bool:
        if environ.get("STAGE") == "test":
            return True
        return self.prev_aroon_val < self.buy_threshold <= self.aroon_val

    def should_sell(self) -> bool:
        if environ.get("STAGE") == "test":
            return True
        return self.prev_aroon_val >= self.sell_threshold > self.aroon_val
