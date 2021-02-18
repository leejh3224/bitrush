from lib.strategies.base_strategy import BaseStrategy
from talib import abstract, MA_Type


class RsiBB(BaseStrategy):
    name = "rsi_bollinger_bands"

    # settings
    period = 7
    buy_threshold = 0.7
    sell_threshold = 0.3

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        rsi = abstract.RSI(feed, period=self.period)
        maxrsi = abstract.MAX(rsi, period=self.period)
        minrsi = abstract.MIN(rsi, period=self.period)
        srsi = (rsi - minrsi) / (maxrsi - minrsi)

        feed["srsi"] = srsi

        bb = abstract.BBANDS(feed, matype=MA_Type.T3, period=self.period)
        feed["bbh"] = bb["upperband"]
        prev_close = feed["close"].shift(1)
        prev_bbh = feed["bbh"].shift(1)
        feed["bbh_cross_up"] = (feed["close"] > feed["bbh"]) & (prev_close <= prev_bbh)

        self.current_ohlcv = feed.iloc[-1]

    def should_buy(self) -> bool:
        return (
            self.current_ohlcv["srsi"] >= self.buy_threshold
            and self.current_ohlcv["bbh_cross_up"]
        )

    def should_sell(self) -> bool:
        return self.current_ohlcv["srsi"] <= self.sell_threshold
