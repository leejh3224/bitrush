from lib.order.open_order_data import OpenOrderData
from lib.order.order import Order
from lib.order.order_repository import OrderRepository


def test_add_order(order_repository: OrderRepository, mock_buy_order, mock_open_order_data: OpenOrderData):
    order_repository.add_order(order=mock_buy_order, data=mock_open_order_data)


def test_get_last_order(order_repository: OrderRepository):
    order = order_repository.get_last_order(ticker="BTC", strategy="test", account_id=0)
    print(order)

