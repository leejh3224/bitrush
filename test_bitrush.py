from decimal import *
from lib.strategies.base_strategy import StrategyParams
from lib.strategies.volatility_breakout import VolatilityBreakout
from lib.strategies.stoch_rsi import StochRSI
from lib.strategies.golden_cross import GoldenCross
from lib.strategies.aroon import Aroon
from lib.strategies.rsi_bb import RsiBB
from lib.strategies.dc_breakout import DcBreakout
from lib.strategies.cci import Cci
from lib.strategies.kc_breakout import KcBreakout
from lib.ticker import Ticker
from lib.broker import Broker
from lib.upbit import Upbit
import json
from freezegun import freeze_time

api = Upbit()
broker = Broker(api)


def test_get_order():
    sell_order = api.get_order("c7ea372d-32d3-438d-9264-d923d83f591a")
    # buy_order = api.get_order("714e432e-8ccb-4d90-bc31-d00644da47a6")
    print(json.dumps(sell_order, indent=2))
    # print(json.dumps(buy_order, indent=2))


def test_notify_order():
    broker.notify_order(
        order_id="714e432e-8ccb-4d90-bc31-d00644da47a6",
        type="buy",
        ticker="BTC",
        price=Decimal("41351000.00000000"),
        size=Decimal("0.00018350"),
    )


@freeze_time("2021-02-14 06:01:00")
def test_volatility_breakout():
    strategy = VolatilityBreakout(
        broker,
        StrategyParams(ticker=Ticker.이오스.value, ratio=Decimal(0.2)),
    )
    # strategy.should_buy()
    print(strategy.should_sell())


def test_stoch_rsi():
    strategy = StochRSI(
        broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


def test_golden_cross():
    strategy = GoldenCross(
        broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


def test_aroon():
    strategy = Aroon(
        broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


def test_rsi_bb():
    strategy = RsiBB(
        broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


def test_get_orders():
    res = api.get_orders(ticker=Ticker.이더리움.value, state="cancel")
    print(res)


def test_dc_breakout():
    strategy = DcBreakout(
        broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


def test_cci():
    strategy = Cci(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2)))
    strategy.should_buy()
    strategy.should_sell()


def test_kc_breakout():
    strategy = KcBreakout(
        broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
    )
    strategy.should_buy()
    strategy.should_sell()


# 특정 수량만큼 즉시 매도
def test_sell():
    strategy = DcBreakout(
        broker, StrategyParams(ticker=Ticker.이더리움.value, volume=Decimal("0.02285347"))
    )
    strategy.trade()
