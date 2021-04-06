from backtest.indicators.StochRSI import StochRSI
from backtrader import bt


class Cci(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.cci = bt.indicators.CommodityChannelIndex(self.data, period=7)

    def next(self):
        cash = self.broker.get_cash()
        position = self.getposition()

        if not position and self.cci >= 100:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and self.cci < 60:
            self.close()