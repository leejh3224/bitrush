import json
from decimal import Decimal
from typing import Optional, Dict

from lib.exchange.upbit.model.post_orders_response import PostOrdersResponse
from lib.order.order import Order
from lib.order.order_type import OrderType
from lib.type import JsonString


class PostOrdersResponseAdapter(Order):
    response: PostOrdersResponse
    custom_order_id: str

    def __init__(self, response: Dict, custom_order_id: str):
        """
        Args:
            custom_order_id (str): custom order id to group each order items
        """
        self.response = PostOrdersResponse(**response)
        self.custom_order_id = custom_order_id

    def get_id(self) -> str:
        return self.custom_order_id

    def is_filled(self) -> bool:
        return self.response.state != "wait"

    def get_order_type(self) -> OrderType:
        return OrderType.BUY if self.response.side == "bid" else OrderType.SELL

    def get_ticker(self) -> str:
        return self.response.market.replace("KRW-", "")

    def get_volume(self) -> Optional[Decimal]:
        return Decimal(self.response.volume) if self.response.volume else None

    def get_avg_price(self):
        return Decimal(self.response.price) if self.response.price else None

    def get_amount(self):

        # order is just placed
        return Decimal("0")

    def get_raw_data(self) -> Dict:
        return self.response.dict()
