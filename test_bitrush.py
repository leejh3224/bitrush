from decimal import *
from lib.strategies.rsi_bb import rsi_bb
from lib.ticker import Ticker
from lib.strategies.golden_cross import golden_cross
from lib.strategies.aroon import aroon
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


def test_golden_cross():
    gc_params = dict(
        ticker=Ticker.이더리움.value,
        short_period=10,
        long_period=20,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
    )
    golden_cross(api, broker, gc_params)


def test_aroon():
    aroon_params = dict(
        ticker=Ticker.비트코인.value,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
    )
    aroon(api, broker, aroon_params)


def test_rsi_bb():
    rsi_bb_params = dict(
        ticker=Ticker.비트코인.value,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
        period=14,
    )
    rsi_bb(api, broker, rsi_bb_params)
