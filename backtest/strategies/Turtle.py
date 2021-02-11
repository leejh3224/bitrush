import backtrader as bt
from backtest.indicators.DonchianChannel import DonchianChannels


class Turtle(bt.Strategy):

    # S1: (10, 20)
    # S2: (20, 55)
    params = (
        ("ratio", 0.2),
        ("unit", 0.05),
        ("low_period", 20),
        ("high_period", 55),
        ("fractional", False),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.dc = DonchianChannels(
            self.data, low_period=self.p.low_period, high_period=self.p.high_period
        )
        self.high_crossup = bt.indicators.CrossUp(self.data.close, self.dc.dch)
        self.low_crossdown = bt.indicators.CrossDown(self.data.close, self.dc.dcl)
        self.atr = bt.indicators.AverageTrueRange(self.data)

    def next(self):
        position = self.getposition()
        new_high_updated = self.high_crossup == 1
        new_low_updated = self.low_crossdown == 1
        close = self.data.close[0]
        n = self.atr[0]
        gap = 2 * n
        cash = self.broker.get_cash()
        size = (cash * self.p.unit) / gap

        # entry rule
        if not self.position and new_high_updated:
            if cash * self.p.unit > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)

        if self.position:
            position_value = position.price * position.size
            can_buy_more = position_value < cash * self.p.ratio

            # pyramiding
            if can_buy_more and close >= position.price + gap:
                self.buy(size=size)

            # exit rule
            stop_loss = close <= position.price - gap or new_low_updated
            if stop_loss:
                self.close()
