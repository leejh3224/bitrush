from lib.order.open_order_data import OpenOrderData
from lib.order.trader import Trader


def test_get_position_size(trader: Trader):
    position_size = trader.get_position_size()
    print(position_size)


def test_on_trade_success(trader: Trader, mock_open_order_data: OpenOrderData):
    trader.on_trade_success(mock_open_order_data)
