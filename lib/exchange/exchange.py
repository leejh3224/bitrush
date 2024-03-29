from abc import *
from decimal import *
from typing import List, Optional

from lib.asset.asset import Asset
from lib.candle.candle import Candle
from lib.order.order import Order


class Exchange(metaclass=ABCMeta):

    @abstractmethod
    def get_day_candles(self, ticker: str, start: str, end: str) -> List[Candle]:
        """get day candles between `start` and `end`

        Args:
            ticker (str): symbol for a ticker, ex) BTC
            start (str): start date in format YYYY-MM-DD (inclusive)
            end (str): end date in format YYYY-MM-DD (exclusive)
        """
        pass

    @abstractmethod
    def get_last_candle(self, ticker: str) -> Candle:
        pass

    @abstractmethod
    def get_all_assets(self) -> List[Asset]:
        pass

    @abstractmethod
    def buy(self, ticker: str, amount: Decimal) -> Optional[Order]:
        pass

    @abstractmethod
    def sell(self, ticker: str, volume: Decimal) -> Optional[Order]:
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        pass
