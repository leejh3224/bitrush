from backtrader import bt


# 켈트너 채널 돌파 + 샹들리에 청산
class KcBreakout(bt.Strategy):
    params = (("ratio", 0.2), ("min_trade", 5000), ("period", 45), ("n", 2))

    def __init__(self) -> None:
        super().__init__()
        self.ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.p.period
        )
        self.atr = bt.indicators.AverageTrueRange(self.data, period=self.p.period)
        self.high = bt.indicators.Highest(self.data, period=self.p.period)

    def next(self):
        cash = self.broker.get_cash()
        position = self.getposition()
        close = self.data.close
        ma = self.ma
        atr = self.p.n * self.atr
        high = self.high

        if not position and close >= ma + atr:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and (close <= ma - atr) or (close <= high - 3 * self.atr):
            self.close()
