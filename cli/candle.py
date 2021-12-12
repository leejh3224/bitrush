from typing import List

import typer

from lib.account.account_repository import AccountRepository
from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository
from lib.db import get_session
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.kms import Kms
from lib.order.trader import get_trading_tickers

candle_app = typer.Typer()


@candle_app.command()
def add(start: str, end: str):
    """add candles between `start` and `end`

    Args:
        start (str): start date in format YYYY-MM-DD (inclusive)
        end (str): end date in format YYYY-MM-DD (exclusive)
    """
    pass
