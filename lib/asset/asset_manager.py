from typing import Optional

from lib.asset.asset import Asset
from lib.exchange.exchange import Exchange


class AssetManager:
    exchange: Exchange

    def __init__(self, exchange: Exchange):
        self.exchange = exchange

    def get_cash(self):
        asset = self.get_asset("KRW")
        if asset:
            return asset.get_net_value()
        return 0

    def get_account_size(self):
        assets = self.exchange.get_all_assets()
        total_value = 0
        for asset in assets:
            total_value += asset.get_net_value()
        return total_value

    def get_asset(self, ticker: str) -> Optional[Asset]:
        assets = self.exchange.get_all_assets()
        for asset in assets:
            if asset.get_ticker() == ticker:
                return asset
        return None
