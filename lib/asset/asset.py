from abc import ABCMeta, abstractmethod
from decimal import Decimal


class Asset(metaclass=ABCMeta):

    @abstractmethod
    def get_net_value(self) -> Decimal:
        pass

    @abstractmethod
    def get_ticker(self) -> str:
        pass

    def __repr__(self):
        return f"""Asset(ticker={self.get_ticker()}, net_value={self.get_net_value()})"""
