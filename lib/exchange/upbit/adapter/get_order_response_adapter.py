import json
from decimal import Decimal
from typing import Optional, Dict

from lib.exchange.upbit.model.get_order_response import GetOrderResponse
from lib.order.order import Order
from lib.order.order_type import OrderType
from lib.type import JsonString


class GetOrderResponseAdapter(Order):
    response: GetOrderResponse

    def __init__(self, response: GetOrderResponse):
        self.response = GetOrderResponse(**response)

    def get_id(self) -> str:
        return self.response.uuid

    def is_filled(self) -> bool:
        return self.response.state != "wait"

    def get_order_type(self) -> OrderType:
        return OrderType.BUY if self.response.side == "bid" else OrderType.SELL

    def get_ticker(self) -> str:
        return self.response.market.replace("KRW-", "")

    def get_volume(self) -> Optional[Decimal]:
        trades = self.response.trades
        return sum([Decimal(trade.volume) for trade in trades])

    def get_avg_price(self) -> Optional[Decimal]:
        trades = self.response.trades
        sum_price = Decimal("0")

        for trade in trades:
            sum_price += Decimal(trade.price)

        return sum_price / len(trades)

    def get_amount(self) -> Decimal:
        trades = self.response.trades
        return sum([Decimal(trade.funds) for trade in trades])

    def get_raw_data(self) -> Dict:
        return self.response.dict()
