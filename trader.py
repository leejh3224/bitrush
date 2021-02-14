from dotenv import load_dotenv

load_dotenv()

from lib.strategies.volatility_breakout import VolatilityBreakout
from lib.strategies.stoch_rsi import StochRSI
from lib.strategies.golden_cross import GoldenCross
from lib.strategies.aroon import Aroon
from lib.strategies.rsi_bb import RsiBB
from lib.broker import Broker
from lib.upbit import Upbit
from lib.strategies.base_strategy import BaseStrategy, StrategyParams
from decimal import *
from lib.ticker import Ticker
from lib.sqs import order_queue

api = Upbit()
broker = Broker(api, order_queue)


def main(event, context):
    strategies: list[BaseStrategy] = [
        StochRSI(broker, StrategyParams(ticker=Ticker.리플.value, ratio=Decimal(0.2))),
        GoldenCross(
            broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
        ),
        GoldenCross(
            broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.2))
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.비트코인.value,
                ratio=Decimal(0.2),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.이더리움.value,
                ratio=Decimal(0.2),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.이오스.value,
                ratio=Decimal(0.05),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.라이트코인.value,
                ratio=Decimal(0.05),
            ),
        ),
        Aroon(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))),
        Aroon(broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.2))),
        Aroon(broker, StrategyParams(ticker=Ticker.비트코인캐시.value, ratio=Decimal(0.2))),
        RsiBB(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))),
        RsiBB(broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.2))),
        RsiBB(broker, StrategyParams(ticker=Ticker.리플.value, ratio=Decimal(0.2))),
        RsiBB(broker, StrategyParams(ticker=Ticker.비트코인캐시.value, ratio=Decimal(0.2))),
        RsiBB(broker, StrategyParams(ticker=Ticker.라이트코인.value, ratio=Decimal(0.05))),
        RsiBB(broker, StrategyParams(ticker=Ticker.이오스.value, ratio=Decimal(0.05))),
    ]

    for strategy in strategies:
        strategy.trade()


if __name__ == "__main__":
    main({}, {})
