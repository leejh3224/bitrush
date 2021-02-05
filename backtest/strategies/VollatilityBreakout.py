import backtrader as bt


class VolatilityBreakout(bt.Strategy):
    params = {
        ('ratio', 0.2),
        ('min_trade', 5000),
        ('k', 0.5)
    }

    def __init__(self) -> None:
        super().__init__()

    def next(self):
        range = self.data.high[-1] - self.data.low[-1]
        position = self.getposition()
        cash = self.broker.get_cash()

        if position:
            self.close()

        if not position and self.data.close[0] > self.data.open[0] + (range * self.p.k):
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
