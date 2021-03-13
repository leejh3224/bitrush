from dotenv import load_dotenv

load_dotenv()

from lib.strategies.volatility_breakout import VolatilityBreakout
from lib.strategies.stoch_rsi import StochRSI
from lib.strategies.golden_cross import GoldenCross
from lib.strategies.aroon import Aroon
from lib.strategies.rsi_bb import RsiBB
from lib.strategies.dc_breakout import DcBreakout
from lib.strategies.cci import Cci
from lib.strategies.kc_breakout import KcBreakout
from lib.broker import Broker
from lib.upbit import Upbit
from lib.strategies.base_strategy import BaseStrategy, StrategyParams
from decimal import *
from lib.ticker import Ticker

api = Upbit()
broker = Broker(api)


def main(event, context):

    # todo: 즉시 매매 by trade id 구현
    strategies: list[BaseStrategy] = [
        GoldenCross(
            broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.15))
        ),
        GoldenCross(
            broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.15))
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.비트코인.value,
                ratio=Decimal(0.05),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.이더리움.value,
                ratio=Decimal(0.05),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.이오스.value,
                ratio=Decimal(0.03),
            ),
        ),
        VolatilityBreakout(
            broker,
            StrategyParams(
                ticker=Ticker.라이트코인.value,
                ratio=Decimal(0.03),
            ),
        ),
        Aroon(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.1))),
        Aroon(broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.1))),
        Aroon(broker, StrategyParams(ticker=Ticker.비트코인캐시.value, ratio=Decimal(0.1))),
        RsiBB(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.3))),
        RsiBB(broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.1))),
        RsiBB(broker, StrategyParams(ticker=Ticker.리플.value, ratio=Decimal(0.03))),
        RsiBB(broker, StrategyParams(ticker=Ticker.비트코인캐시.value, ratio=Decimal(0.1))),
        RsiBB(broker, StrategyParams(ticker=Ticker.라이트코인.value, ratio=Decimal(0.03))),
        RsiBB(broker, StrategyParams(ticker=Ticker.이오스.value, ratio=Decimal(0.03))),
        DcBreakout(
            broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.1))
        ),
        DcBreakout(
            broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.05))
        ),
        DcBreakout(broker, StrategyParams(ticker=Ticker.리플.value, ratio=Decimal(0.03))),
        DcBreakout(
            broker, StrategyParams(ticker=Ticker.라이트코인.value, ratio=Decimal(0.02))
        ),
        DcBreakout(
            broker, StrategyParams(ticker=Ticker.이오스.value, ratio=Decimal(0.02))
        ),
        Cci(broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.05))),
        Cci(broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.05))),
        Cci(broker, StrategyParams(ticker=Ticker.이오스.value, ratio=Decimal(0.02))),
        KcBreakout(
            broker, StrategyParams(ticker=Ticker.비트코인.value, ratio=Decimal(0.2))
        ),
        KcBreakout(
            broker, StrategyParams(ticker=Ticker.이더리움.value, ratio=Decimal(0.2))
        ),
    ]

    for strategy in strategies:
        strategy.trade()


if __name__ == "__main__":
    main({}, {})
