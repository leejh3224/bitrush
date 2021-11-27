from decimal import Decimal
from typing import Dict

from lib.asset.asset import Asset
from lib.exchange.upbit.model.get_accounts_response import GetAccountsResponse
from lib.ticker import Ticker


class GetAccountsResponseAdapter(Asset):
    response: GetAccountsResponse

    def __init__(self, response: Dict):
        self.response = GetAccountsResponse(**response)

    def get_net_value(self) -> Decimal:
        if self.response.currency == "KRW":
            return Decimal(self.response.balance) - Decimal(self.response.locked)
        return Decimal(self.response.avg_buy_price) * Decimal(self.response.balance)

    def get_ticker(self) -> str:
        return self.response.currency
