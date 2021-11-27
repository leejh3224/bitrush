from abc import *
from decimal import *
from typing import List, Optional

from lib.account.account import Account
from lib.asset.asset import Asset
from lib.candle.candle import Candle
from lib.order.order import Order


class Exchange(metaclass=ABCMeta):
    account: Account

    def __init__(self, account: Account):
        self.account = account

    @abstractmethod
    def get_day_candle(self, ticker: str) -> Candle:
        pass

    @abstractmethod
    def get_last_candle(self, ticker: str) -> Candle:
        pass

    @abstractmethod
    def get_all_assets(self) -> List[Asset]:
        pass

    @abstractmethod
    def buy(self, ticker: str, amount: Decimal) -> Order:
        pass

    @abstractmethod
    def sell(self, ticker: str, volume: Decimal) -> Order:
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        pass
