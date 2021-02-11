from backtrader import bt
from backtest.indicators.StochRSI import StochRSI


class RsiMacd(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.macd = bt.indicators.MACD(self.data)
        self.rsi = StochRSI(self.data, period=14)
        self.macd_crossup = bt.indicators.CrossUp(self.macd, bt.LineNum(0.0))
        self.macd_crossdown = bt.indicators.CrossDown(self.macd, bt.LineNum(0.0))

    def next(self):
        cash = self.broker.get_cash()
        position = self.getposition()

        if not position and self.rsi[0] >= 0.8 or self.macd_crossup[0]:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and self.rsi[0] <= 0.3 or self.macd_crossdown[0]:
            self.close()
