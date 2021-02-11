from lib.strategies.base_strategy import BaseStrategy
from datetime import datetime, timedelta
from decimal import *


class VolatilityBreakout(BaseStrategy):
    name = "volatility_breakout"

    # settings
    k = Decimal(0.5)

    def should_buy(self):
        ticker = self.params["ticker"]

        feed = self.broker.get_feed(ticker)
        yesterday_ohlcv = feed.iloc[-2]
        current_ohlcv = feed.iloc[-1]
        range = yesterday_ohlcv["high"] - yesterday_ohlcv["low"]

        return current_ohlcv["close"] > current_ohlcv["open"] + (range * self.k)

    def should_sell(self):
        now = datetime.now()
        sell_period = datetime(now.year, now.month, now.day, 6, 0, 0)

        return sell_period < now <= sell_period + timedelta(minutes=20)
