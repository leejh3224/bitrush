from dotenv import load_dotenv

load_dotenv()

from lib.strategies.volatility_breakout import volatility_breakout
from lib.broker import Broker
from lib.upbit import Upbit
from decimal import *
from lib.strategies.golden_cross import golden_cross
from lib.ticker import Ticker


api = Upbit()
broker = Broker(api)


def main(event, context):
    # gc_params = dict(
    #     ticker=Ticker.이더리움.value,
    #     short_period=10,
    #     long_period=20,
    #     min_unit_krw=Decimal(5000),
    #     ratio=Decimal(0.2),
    # )
    # golden_cross(api, broker, gc_params)

    vb_params = dict(
        ticker=Ticker.비트코인.value,
        min_unit_krw=Decimal(5000),
        k=Decimal(0.5),
        ratio=Decimal(0.2),
    )
    volatility_breakout(api, broker, vb_params)


if __name__ == "__main__":
    main({}, {})
