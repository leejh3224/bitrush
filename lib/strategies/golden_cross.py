from talib import abstract
from lib.strategies.base_strategy import BaseStrategy


class GoldenCross(BaseStrategy):
    name = "golden_cross"

    # settings
    short_period = 10
    long_period = 20

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        mas = abstract.SMA(feed, timeperiod=self.short_period)
        mal = abstract.SMA(feed, timeperiod=self.long_period)
        feed["mas"] = mas
        feed["mal"] = mal
        prev_mas = feed["mas"].shift(1)
        prev_mal = feed["mal"].shift(1)
        feed["cross_up"] = (feed["mas"] >= feed["mal"]) & (prev_mas <= prev_mal)
        feed["cross_down"] = (feed["mas"] <= feed["mal"]) & (prev_mas >= prev_mal)

        self.current_ohlcv = feed.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_ohlcv["cross_up"]

    def should_sell(self) -> bool:
        return self.current_ohlcv["cross_down"]
