from lib.order.open_order_data import OpenOrderData
from lib.order.open_order_repository import OpenOrderRepository


def test_get_open_orders(open_order_repository: OpenOrderRepository):
    open_orders = open_order_repository.get_open_orders(account_id=0, count=10)
    print(open_orders)

    first = open_orders[0]
    assert type(first[0]) == int
    assert type(first[1]) == OpenOrderData


def test_add_open_order_remove_open_order_by_id(open_order_repository: OpenOrderRepository, mock_open_order_data: OpenOrderData):
    inserted_id = open_order_repository.add_open_order(mock_open_order_data)
    open_order_repository.remove_open_order_by_id(inserted_id)
