import pandas as pd

from lib.strategy.base_strategy import BaseStrategy


class MustTrade(BaseStrategy):

    def __init__(self, feed: pd.DataFrame):
        super().__init__(feed)

    def get_name(self) -> str:
        return "must_trade"

    def should_buy(self) -> bool:
        return True

    def should_sell(self) -> bool:
        return True

    def is_valid(self) -> bool:
        return True
