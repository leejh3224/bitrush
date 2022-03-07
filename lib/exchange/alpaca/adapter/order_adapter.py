from decimal import Decimal
from typing import Dict

from lib.order.order import Order
from lib.order.order_type import OrderType
from lib.exchange.alpaca.model.order import Order as AlpacaOrder
from lib.util import decimal


class OrderAdapter(Order):
    order: AlpacaOrder

    def __init__(self, order: AlpacaOrder):
        self.order = order

    def get_id(self) -> str:
        return self.order.client_order_id

    def is_filled(self) -> bool:
        return self.order.filled_at is not None

    def get_exchange(self) -> str:
        return 'alpaca'

    def get_order_type(self) -> OrderType:
        return OrderType.BUY if self.order.side == "buy" else OrderType.SELL

    def get_ticker(self) -> str:
        return self.order.symbol

    def get_avg_price(self) -> Decimal:
        return decimal(self.order.filled_avg_price) if self.order.status == "filled" else Decimal("0")

    def get_amount(self) -> Decimal:
        return decimal(self.order.notional) if self.order.notional is not None else Decimal("0")

    def get_volume(self) -> Decimal:
        return decimal(self.order.qty) if self.order.qty is not None else Decimal("0")

    def get_raw_data(self) -> Dict:
        return self.order.dict()
