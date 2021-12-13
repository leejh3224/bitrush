from abc import ABCMeta, abstractmethod

import pandas as pd


class BaseStrategy(metaclass=ABCMeta):
    feed: pd.DataFrame

    def __init__(self, feed: pd.DataFrame):
        self.feed = feed

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def should_buy(self) -> bool:
        pass

    @abstractmethod
    def should_sell(self) -> bool:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    def has_enough_feed(self):
        return len(self.feed) >= 50
