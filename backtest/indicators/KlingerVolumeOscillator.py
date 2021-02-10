import backtrader as bt


class KlingerVolumeOscillator(bt.Indicator):
    lines = ("sig", "kvo")

    # 34, 55, 13
    params = (("kvoFast", 34), ("kvoSlow", 55), ("sigPeriod", 13))

    def __init__(self):
        self.plotinfo.plotyhlines = [0]
        self.addminperiod(self.p.kvoSlow)

        self.data.hlc3 = (self.data.high + self.data.low + self.data.close) / 3
        # This works - Note indexing should be () rather than []
        # See: https://www.backtrader.com/docu/concepts.html#lines-delayed-indexing
        self.data.sv = bt.If(
            (self.data.hlc3(0) - self.data.hlc3(-1)) / self.data.hlc3(-1) >= 0,
            self.data.volume,
            -self.data.volume,
        )
        self.lines.kvo = bt.indicators.EMA(
            self.data.sv, period=self.p.kvoFast
        ) - bt.indicators.EMA(self.data.sv, period=self.p.kvoSlow)
        self.lines.sig = bt.indicators.EMA(self.lines.kvo, period=self.p.sigPeriod)
