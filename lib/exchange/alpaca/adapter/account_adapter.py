from decimal import Decimal
from typing import Dict

from lib.asset.asset import Asset
from lib.exchange.alpaca.model.account import Account
from lib.util import decimal


class AccountAdapter(Asset):
    account: Account

    def __init__(self, account: Dict):
        self.account = Account(**account)

    def get_net_value(self) -> Decimal:
        return decimal(self.account.cash)

    def get_ticker(self) -> str:
        return "USD"
