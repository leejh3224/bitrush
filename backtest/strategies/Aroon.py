import backtrader as bt
from backtest.indicators.StochRSI import StochRSI


class Aroon(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.aroon = bt.indicators.AroonOscillator(self.data)

    def next(self):
        cash = self.broker.get_cash()
        position = self.position

        if not position and self.aroon >= 70:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and self.aroon < 0:
            self.close()
