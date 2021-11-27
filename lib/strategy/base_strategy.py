from abc import ABCMeta, abstractmethod

import pandas as pd


class BaseStrategy(metaclass=ABCMeta):
    feed: pd.DataFrame

    def __init__(self, feed: pd.DataFrame):
        if len(feed) < 1000:
            raise ValueError("not enough data in feed")

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
