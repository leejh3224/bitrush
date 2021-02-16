from lib.broker import Broker
from lib.strategies.base_strategy import BaseStrategy, StrategyParams
from decimal import *
from talib import abstract


class StochRSI(BaseStrategy):
    name = "stoch_rsi"

    # settings
    period = 30
    buy_threshold = 0.7
    sell_threshold = 0.3

    def __init__(self, broker: Broker, params: StrategyParams) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        rsi = abstract.RSI(feed, period=self.period)
        maxrsi = abstract.MAX(rsi, period=self.period)
        minrsi = abstract.MIN(rsi, period=self.period)
        srsi = (rsi - minrsi) / (maxrsi - minrsi)

        feed["srsi"] = srsi
        prev_srsi = feed["srsi"].shift(1)
        feed["cross_up"] = (feed["srsi"] > self.buy_threshold) & (
            prev_srsi <= self.buy_threshold
        )
        feed["cross_down"] = (feed["srsi"] < self.sell_threshold) & (
            prev_srsi >= self.sell_threshold
        )

        self.current_ohlcv = feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cross_up"]

    def should_sell(self) -> bool:
        return self.current_ohlcv["cross_down"]
