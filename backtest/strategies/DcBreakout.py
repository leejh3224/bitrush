import backtrader as bt
from backtest.indicators.DonchianChannel import DonchianChannels


class DcBreakout(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
        ("low_period", 2),
        ("high_period", 4),
    )

    def __init__(self) -> None:
        super().__init__()
        self.dc = DonchianChannels(
            self.data, low_period=self.p.low_period, high_period=self.p.high_period
        )
        self.high_crossup = bt.indicators.CrossUp(self.data.close, self.dc.dch)
        self.low_crossdown = bt.indicators.CrossDown(self.data.close, self.dc.dcl)

    def next(self):
        position = self.getposition()
        cash = self.broker.get_cash()
        new_high = self.high_crossup[0] == 1
        new_low = self.low_crossdown[0] == 1

        if not position and new_high:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and new_low:
            self.close()
