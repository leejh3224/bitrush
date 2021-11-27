from decimal import Decimal

import pytest

from lib.exchange.upbit.upbit_exchange import UpbitExchange


def test_get_day_candle(upbit_exchange: UpbitExchange):
    candle = upbit_exchange.get_day_candle("BTC")
    print(candle)


def test_get_last_candle(upbit_exchange: UpbitExchange):
    candle = upbit_exchange.get_last_candle("BTC")
    print(candle)


def test_get_all_assets(upbit_exchange: UpbitExchange):
    assets = upbit_exchange.get_all_assets()
    print(assets)


@pytest.mark.skip
def test_buy(upbit_exchange: UpbitExchange):
    order = upbit_exchange.buy("BTC", Decimal("5000"))
    print(order)


@pytest.mark.skip
def test_sell(upbit_exchange: UpbitExchange):
    order = upbit_exchange.sell("BTC", Decimal("0.000144000"))
    print(order)


def test_get_order(upbit_exchange: UpbitExchange):
    buy_order = upbit_exchange.get_order("b0c61050-450b-48e5-9854-476a431f30cb")
    sell_order = upbit_exchange.get_order("9b1a3245-2eeb-47d9-8ea8-ed59c0322e2c")
    print(buy_order)
    print(sell_order)


def test_get_order_not_found(upbit_exchange: UpbitExchange):
    order = upbit_exchange.get_order("abcd")
    assert order is None

