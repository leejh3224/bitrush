import backtrader as bt


class BuyHold(bt.Strategy):
    def start(self):
        self.initial_cash = self.broker.get_cash()  # keep the starting cash

    def nextstart(self):
        self.order_target_percent(target=0.8)

    def stop(self):
        self.roi = (self.broker.get_value() / self.initial_cash) - 1.0
        print('ROI: {:.2f}%'.format(100.0 * self.roi))
