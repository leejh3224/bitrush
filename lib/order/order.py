from abc import ABCMeta, abstractmethod
from decimal import Decimal
from typing import Optional, Dict

from lib.order.order_type import OrderType


class Order(metaclass=ABCMeta):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def is_filled(self) -> bool:
        pass

    @abstractmethod
    def get_exchange(self) -> str:
        pass

    @abstractmethod
    def get_order_type(self) -> OrderType:
        pass

    @abstractmethod
    def get_ticker(self) -> str:
        pass

    @abstractmethod
    def get_avg_price(self) -> Decimal:
        pass

    @abstractmethod
    def get_amount(self) -> Decimal:
        pass

    @abstractmethod
    def get_volume(self) -> Decimal:
        pass

    @abstractmethod
    def get_raw_data(self) -> Dict:
        pass

    def __repr__(self):
        return f"""Order(id={self.get_id()}, ticker={self.get_ticker()}, is_filled={self.is_filled()}, order_type={self.get_order_type()}, avg_price={self.get_avg_price()}, amount={self.get_amount()}, volume={self.get_volume()}, raw_data={self.get_raw_data()})"""
