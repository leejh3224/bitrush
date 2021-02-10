from dotenv import load_dotenv

load_dotenv()

from lib.strategies.volatility_breakout import volatility_breakout
from lib.strategies.stoch_rsi import stoch_rsi
from lib.strategies.golden_cross import golden_cross
from lib.strategies.aroon import aroon
from lib.broker import Broker
from lib.upbit import Upbit
from decimal import *
from lib.ticker import Ticker
from lib.sqs import order_queue

api = Upbit()
broker = Broker(api, order_queue)


def main(event, context):
    gc_params = dict(
        ticker=Ticker.이더리움.value,
        short_period=10,
        long_period=20,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
    )
    golden_cross(api, broker, gc_params)

    vb_params = dict(
        ticker=Ticker.비트코인.value,
        min_unit_krw=Decimal(5000),
        k=Decimal(0.5),
        ratio=Decimal(0.2),
    )
    volatility_breakout(api, broker, vb_params)

    srsi_params = dict(
        ticker=Ticker.리플.value,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
        period=14,
    )
    stoch_rsi(api, broker, srsi_params)

    aroon_params = dict(
        ticker=Ticker.비트코인.value,
        min_unit_krw=Decimal(5000),
        ratio=Decimal(0.2),
    )
    aroon(api, broker, aroon_params)


if __name__ == "__main__":
    main({}, {})
