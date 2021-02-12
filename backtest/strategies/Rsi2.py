import backtrader as bt


class Rsi2(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.long_ema = bt.indicators.EMA(self.data.close, period=200)
        self.short_ema = bt.indicators.EMA(self.data.close, period=5)
        self.rsi = bt.indicators.RSI_Safe(self.data.close, period=2)

    def next(self):
        cash = self.broker.get_cash()
        position = self.getposition()
        close = self.data.close[0]
        long_ema = self.long_ema[0]
        short_ema = self.short_ema[0]
        rsi = self.rsi[0]

        if not position and rsi < 5 and close > long_ema:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and rsi > 95 and close < long_ema:
            self.close()
