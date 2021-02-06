from lib.utils import find
from decimal import *


class Broker:
    def __init__(self, api) -> None:
        super().__init__()
        self.api = api
        self.assets = self.api.get_balance()

    def get_cash(self):
        return self.get_balance(ticker="KRW")

    def get_balance(self, ticker):
        asset = self.__get_asset(ticker)
        return (
            Decimal(asset.get("balance", 0)) - Decimal(asset.get("locked", 0))
            if asset
            else 0
        )

    def get_price(self, ticker):
        asset = self.__get_asset(ticker)
        return Decimal(asset.get("avg_buy_price", 0)) if asset else 0

    def __get_asset(self, ticker):
        return find(self.assets, lambda asset, *args: asset.get("currency") == ticker)
