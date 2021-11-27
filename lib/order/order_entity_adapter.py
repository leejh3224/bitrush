from decimal import Decimal
from typing import Optional, Dict

from lib.order.order import Order
from lib.order.order_entity import OrderEntity
from lib.order.order_type import OrderType
from lib.type import JsonString


class OrderEntityAdapter(Order):
    order_entity: OrderEntity

    def __init__(self, order_entity: OrderEntity):
        self.order_entity = order_entity

    def get_id(self) -> str:
        return self.order_entity.id

    # only filled orders are store
    def is_filled(self) -> bool:
        return True

    def get_order_type(self) -> OrderType:
        return OrderType.BUY if self.order_entity.type == OrderType.BUY else OrderType.SELL

    def get_ticker(self) -> str:
        return self.order_entity.ticker

    def get_volume(self) -> Optional[Decimal]:
        return self.order_entity.volume

    def get_avg_price(self) -> Optional[Decimal]:
        return self.order_entity.avg_price

    def get_amount(self) -> Decimal:
        return self.order_entity.amount

    def get_raw_data(self) -> Dict:
        return self.order_entity.raw_data
