import backtrader as bt


class GoldenCross(bt.Strategy):
    params = (
        ('fast', 10),
        ('slow', 20),
        ('ratio', 0.2),
        ('min_trade', 5000),
    )

    def __init__(self) -> None:
        super().__init__()

        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.fast,
            plotname='fast ma'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.slow,
            plotname='slow ma'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma,
            self.slowma
        )

    def next(self):
        cash = self.broker.get_cash()

        if self.position.size == 0 and self.crossover > 0:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif self.position.size > 0 and self.crossover < 0:
            self.close()
