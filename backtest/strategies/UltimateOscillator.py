from backtrader import bt


class UltimateOscillator(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.ult_osc = bt.talib.ULTOSC(self.data.high, self.data.low, self.data.close)

    def next(self):
        cash = self.broker.get_cash()
        position = self.getposition()
        ult_osc = self.ult_osc[0]

        if not position and ult_osc >= 60:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and ult_osc <= 30:
            self.close()
