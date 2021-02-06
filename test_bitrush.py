from decimal import *
from lib.broker import Broker
from lib.upbit import Upbit
import json
from lib.sqs import order_queue

api = Upbit()
broker = Broker(api, order_queue)


def test_get_order():
    sell_order = api.get_order("fbd50fdf-9f6c-4d11-98f7-554cca2dc946")
    buy_order = api.get_order("714e432e-8ccb-4d90-bc31-d00644da47a6")
    print(json.dumps(sell_order, indent=2))
    print(json.dumps(buy_order, indent=2))


def test_notify_order():
    broker.notify_order(
        order_id="714e432e-8ccb-4d90-bc31-d00644da47a6",
        type="buy",
        ticker="BTC",
        price=Decimal("41351000.00000000"),
        size=Decimal("0.00018350"),
    )
