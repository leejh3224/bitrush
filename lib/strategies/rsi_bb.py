from lib.strategies.base_strategy import BaseStrategy
from talib import abstract, MA_Type


class RsiBB(BaseStrategy):
    name = "rsi_bollinger_bands"

    # settings
    period = 14

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)

        rsi = abstract.RSI(feed, period=self.period)
        maxrsi = abstract.MAX(rsi, period=self.period)
        minrsi = abstract.MIN(rsi, period=self.period)
        srsi = (rsi - minrsi) / (maxrsi - minrsi)

        bb = abstract.BBANDS(feed, matype=MA_Type.T3, period=self.period)
        bb_crossup = feed["close"] > bb["upperband"]

        self.current_srsi = srsi.iloc[-1]
        self.current_bb_crossup = bb_crossup.iloc[-1]

    def should_buy(self) -> bool:
        return self.current_srsi >= 0.8 and self.current_bb_crossup

    def should_sell(self) -> bool:
        return self.current_srsi <= 0.3
