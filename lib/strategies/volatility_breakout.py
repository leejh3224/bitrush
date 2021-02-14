from lib.strategies.base_strategy import BaseStrategy
from datetime import datetime, timedelta
from decimal import *


class VolatilityBreakout(BaseStrategy):
    name = "volatility_breakout"

    # settings
    k = Decimal(0.5)
    stop_loss_threshold = Decimal(0.1)

    def __init__(self, broker, params) -> None:
        super().__init__(broker, params)
        ticker = self.params["ticker"]

        self.feed = self.broker.get_feed(ticker)

    def should_buy(self):
        yesterday_ohlcv = self.feed.iloc[-2]
        current_ohlcv = self.feed.iloc[-1]
        range = yesterday_ohlcv["high"] - yesterday_ohlcv["low"]

        return current_ohlcv["close"] > current_ohlcv["open"] + (range * self.k)

    def should_sell(self):
        now = datetime.now()
        sell_period = datetime(now.year, now.month, now.day, 6, 0, 0)

        close_when = sell_period < now <= sell_period + timedelta(minutes=20)
        stop_loss = False

        ticker = self.params["ticker"]
        last_trade = self.broker.get_last_trade(ticker=ticker, strategy=self.name)
        current_ohlcv = self.feed.iloc[-1]

        if last_trade.trade_type:
            avg_price = last_trade.avg_price
            stop_loss = (
                avg_price - current_ohlcv["close"]
                > avg_price * self.stop_loss_threshold
            )

        # 평단가 기준으로 손절하거나 다음날 포지션 청산
        return stop_loss or close_when
