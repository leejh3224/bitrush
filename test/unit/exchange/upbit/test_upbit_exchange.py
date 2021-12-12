from datetime import datetime
from decimal import Decimal

import pytest

from lib.exchange.upbit.upbit_exchange import UpbitExchange


def test_get_day_candles_candle_at_2021_11_27(upbit_exchange: UpbitExchange):
    candles = upbit_exchange.get_day_candles("BTC", start="2021-11-27", end="2021-11-28")

    assert candles[0].get_ticker() == "BTC"
    assert len(candles) == 1


def test_get_today_candle(upbit_exchange: UpbitExchange):
    candle = upbit_exchange.get_today_candle("BTC")

    assert candle.get_ticker() == "BTC"
    assert candle.get_closed_at() == datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def test_get_last_candle(upbit_exchange: UpbitExchange):
    candle = upbit_exchange.get_last_candle("BTC")
    print(candle)


def test_get_all_assets(upbit_exchange: UpbitExchange):
    assets = upbit_exchange.get_all_assets()
    print(assets)


@pytest.mark.skip
def test_buy(upbit_exchange: UpbitExchange):
    order = upbit_exchange.buy("BTC", Decimal("6000"))

    assert order.get_id() != order.get_raw_data()["uuid"]
    print(order)


def test_buy_less_than_min_required_amount(upbit_exchange: UpbitExchange):
    order = upbit_exchange.buy("BTC", Decimal("0.1"))
    assert order is None


@pytest.mark.skip
def test_sell(upbit_exchange: UpbitExchange):
    order = upbit_exchange.sell("ETH", Decimal("0.07775381"))

    assert order.get_id() != order.get_raw_data()["uuid"]
    print(order)


def test_sell_less_than_min_required_amount(upbit_exchange: UpbitExchange):
    order = upbit_exchange.sell("BTC", Decimal("0.000000010"))
    assert order is None


def test_get_order(upbit_exchange: UpbitExchange):
    buy_order = upbit_exchange.get_order("b0c61050-450b-48e5-9854-476a431f30cb")
    sell_order = upbit_exchange.get_order("9b1a3245-2eeb-47d9-8ea8-ed59c0322e2c")
    print(buy_order)
    print(sell_order)


def test_get_order_not_found(upbit_exchange: UpbitExchange):
    order = upbit_exchange.get_order("abcd")
    assert order is None

