from backtest.indicators.KlingerVolumeOscillator import KlingerVolumeOscillator
import backtrader as bt


class Kvo(bt.Strategy):
    params = (
        ("ratio", 0.2),
        ("min_trade", 5000),
    )

    def __init__(self) -> None:
        super().__init__()
        self.kvo = KlingerVolumeOscillator(self.data)
        self.crossover = bt.indicators.CrossOver(self.kvo.kvo, self.kvo.sig)

    def next(self):
        cash = self.broker.get_cash()
        position = self.position

        if not position and self.crossover > 0:
            if cash * self.p.ratio > self.p.min_trade:
                self.order_target_percent(target=self.p.ratio)
        elif position and self.crossover < 0:
            self.close()
