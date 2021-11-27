from abc import ABCMeta, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

import pandas as pd


class Candle(metaclass=ABCMeta):

    @abstractmethod
    def get_ticker(self) -> str:
        pass

    @abstractmethod
    def get_closed_at(self) -> datetime:
        pass

    @abstractmethod
    def get_open_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_high_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_low_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_close_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_volume(self) -> Optional[Decimal]:
        pass

    def to_df_row(self):
        return [
            self.get_closed_at(),
            self.get_open_price(),
            self.get_high_price(),
            self.get_low_price(),
            self.get_close_price()
        ]

    def __repr__(self):
        return f"""Candle(closed_at={self.get_closed_at()}, open={self.get_open_price()}, high={self.get_high_price()}, low={self.get_low_price()}, close={self.get_close_price()}, volume={self.get_volume()})"""


def build_feed(candles: List[Candle]):
    return pd.DataFrame([c.to_df_row() for c in candles],
                        columns=["closed_at", "open", "high", "low", "close"])

