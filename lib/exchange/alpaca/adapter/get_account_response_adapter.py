from decimal import Decimal
from typing import Dict

from lib.asset.asset import Asset
from lib.exchange.alpaca.model.get_account_response import GetAccountResponse


class GetAccountResponseAdapter(Asset):
    response: GetAccountResponse

    def __init__(self, response: Dict):
        self.response = GetAccountResponse(**response)

    def get_net_value(self) -> Decimal:
        return Decimal(self.response.cash)

    def get_ticker(self) -> str:
        return "USD"
