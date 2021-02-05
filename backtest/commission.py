import backtrader as bt


# enable fractional size trading for bitcoin
class CommInfoFractional(bt.CommissionInfo):
    params = (
        ('commission', 0.005),
        ('interest', 0.005),
    )

    def getsize(self, price, cash):
        if cash < 5000:
            return 0
        return cash / price
