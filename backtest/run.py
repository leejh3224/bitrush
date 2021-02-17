from __future__ import absolute_import, division, print_function, unicode_literals
from backtest.strategies.DcBreakout import DcBreakout
from dotenv import load_dotenv

load_dotenv()

from backtest.strategies.RSI import CRSI, SRSI
from backtest.strategies.VollatilityBreakout import VolatilityBreakout
from backtest.strategies.Turtle import Turtle
from backtest.strategies.GoldenCross import GoldenCross
from backtest.strategies.KVO import Kvo
from backtest.strategies.Aroon import Aroon
from backtest.strategies.RsiBollingerBands import RsiBollingerBands
from backtest.commission import CommInfoFractional
from backtest.strategies.BuyHold import BuyHold
from backtest.strategies.Rsi2 import Rsi2
from backtest.data import get_ohlcv

import backtrader as bt
import backtrader.analyzers as btanalyzers
import math
import tableprint as tp

strategies = {
    "buy_hold": BuyHold,
    "golden_cross": GoldenCross,
    "turtle": Turtle,
    "volatility_breakout": VolatilityBreakout,
    "crsi": CRSI,  # ConnorsRSI
    "srsi": SRSI,  # StochRSI
    "kvo": Kvo,
    "aroon": Aroon,
    "rsi_bb": RsiBollingerBands,
}

cerebro = bt.Cerebro()
cerebro.addstrategy(DcBreakout)

cerebro.broker = bt.brokers.BackBroker(slip_perc=0.02)
cerebro.broker.setcash(130_0000)
cerebro.broker.addcommissioninfo(CommInfoFractional())

data = get_ohlcv(ticker="BTC")
feed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(feed)

cerebro.addanalyzer(btanalyzers.TimeDrawDown, _name="drawdown")
cerebro.addanalyzer(btanalyzers.AnnualReturn, _name="annualreturn")
cerebro.addanalyzer(btanalyzers.Returns, _name="returns")
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(btanalyzers.SQN, _name="sqn")

cerebro.addobserver(bt.observers.DrawDown)

result = cerebro.run()

sqn = result[0].analyzers.sqn.get_analysis()
ta = result[0].analyzers.ta.get_analysis()
drawdown = result[0].analyzers.drawdown.get_analysis()
annualreturn = result[0].analyzers.annualreturn.get_analysis()
returns = result[0].analyzers.returns.get_analysis()

sqn_score = sqn.get("sqn", 0)
mdd = drawdown.get("maxdrawdown", 0)
mdd_period = drawdown.get("maxdrawdownperiod", 0)
total_compound_return = returns.get("rtot", 0)
num_trades = ta.get("total", {}).get("total", 0)
num_win = ta.get("won", {}).get("total", 0)
win_pnl = ta.get("won", {}).get("pnl", {}).get("average", 0)
lose_pnl = ta.get("lost", {}).get("pnl", {}).get("average", 0)
net_pnl = ta.get("pnl", {}).get("net", {}).get("average", 0)

win_rate = num_win / num_trades if num_trades > 0 else 0

data = [
    [
        f"{math.floor(cerebro.broker.get_value()):,} ({total_compound_return:.2%})",
        f"{sqn_score:.2f}",
        f"{mdd:.2f}%",
        mdd_period,
    ],
]

headers = [
    # final porfolio value
    # rate of return
    "fpv/ror",
    # Van Tharp's SQN
    # ref: https://indextrader.com.au/van-tharps-sqn/
    # 1.6 - 1.9 Below average
    # 2.0 - 2.4 Average
    # 2.5 - 2.9 Good
    # 3.0 - 5.0 Excellent
    # 5.1 - 6.9 Superb
    # 7.0 - Holy Grail?
    "sqn",
    # max drawdown
    "mdd",
    "mdd period",
]
tp.table(data, headers, align="center")

pnl_headers = [
    "trades",
    "win rate",
    # profit & loss
    "win pnl",
    "lose pnl",
    "net pnl",
]
pnl_data = [
    [
        f"{num_trades} ({num_win})",
        f"{win_rate:.2%}",
        f"{win_pnl:.2f}",
        f"{lose_pnl:.2f}",
        f"{net_pnl:.2f}",
    ]
]
tp.table(data=pnl_data, headers=pnl_headers, align="center")

tp.table(
    data=[["CAGR"] + list(map(lambda n: f"{n:.2%}", annualreturn.values()))],
    headers=[""] + list(map(lambda n: str(n), annualreturn.keys())),
    align="center",
)

cerebro.plot()
