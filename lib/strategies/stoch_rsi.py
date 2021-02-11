from lib.broker import Broker
from lib.strategies.base_strategy import BaseStrategy, StrategyParams
from decimal import *
from talib import abstract


class StochRSI(BaseStrategy):
    name = "stoch_rsi"

    # settings
    period = 14
    buy_threshold = 0.8
    sell_threshold = 0.3

    def __init__(self, broker: Broker, params: StrategyParams) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        rsi = abstract.RSI(feed, period=self.period)
        maxrsi = abstract.MAX(rsi, period=self.period)
        minrsi = abstract.MIN(rsi, period=self.period)
        srsi = (rsi - minrsi) / (maxrsi - minrsi)
        current_srsi = srsi.iloc[-1]

        self.current_srsi = current_srsi

    def should_buy(self) -> bool:
        return self.current_srsi >= self.buy_threshold

    def should_sell(self) -> bool:
        return self.current_srsi <= self.sell_threshold
