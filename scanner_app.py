import datetime
from os import environ

from dotenv import load_dotenv
load_dotenv()

from typing import List
from datetime import date

from lib.account.account_repository import AccountRepository
from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.db import get_session, wait_for_db_init
from lib.kms import Kms
from lib.order.trader import get_trading_tickers
from lib.sentry import init_sentry
import lib.logger as logger
from lib.type import LambdaResponse
import traceback


init_sentry()


def main(event, context) -> LambdaResponse:
    try:
        _tickers = event.get("tickers")
        _start = event.get("start")
        _end = event.get("end")

        kms = Kms()
        session = get_session()

        if environ.get("STAGE") == "test":
            wait_for_db_init(session)

        account_repository = AccountRepository(session, kms)
        candle_repository = CandleRepository(session)

        account = account_repository.get_active_account()

        if account is None:
            raise ValueError(f"active account doesn't exists")

        exchange = UpbitExchange.build(account)

        tickers = _tickers or get_trading_tickers()

        today = date.today()
        tomorrow = today + datetime.timedelta(days=1)

        start = _start if _start is not None else today.strftime("%Y-%m-%d")
        end = _end if _end is not None else tomorrow.strftime("%Y-%m-%d")

        candles: List[Candle] = []

        for ticker in tickers:
            for candle_info in exchange.get_day_candles(ticker, start, end):
                candles.append(candle_info)

        candle_repository.add_candles(candles)

        return {
            "statusCode": 200,
            "body": len(candles)
        }
    except Exception as e:
        stack = traceback.format_exc()
        logger.error(e)

        return {
            "statusCode": 500,
            "body": stack
        }


if __name__ == "__main__":
    event = {
        "start": "2021-12-11",
        "end": "2021-12-12"
    }
    main(event, {})
