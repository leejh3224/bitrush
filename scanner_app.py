from typing import List

from dotenv import load_dotenv

from lib.account.account_repository import AccountRepository
from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.db import get_session
from lib.sentry import init_sentry
from sentry_sdk import capture_exception
import lib.logger as logger


load_dotenv()
init_sentry()


def main(event, context) -> None:
    try:
        sess = get_session()
        account_repository = AccountRepository(sess)
        candle_repository = CandleRepository(sess)

        alias = "sternwarret-prod"
        account = account_repository.get_account_by_alias(alias)

        if not account:
            raise ValueError(f"cannot find account with alias = {alias}")

        exchange = UpbitExchange.build(account)

        tickers = ["BTC", "ETH"]

        candles: List[Candle] = []

        for ticker in tickers:
            candles.append(exchange.get_today_candle(ticker))

        logger.error(f"candles = {candles}")
        candle_repository.add_candles(candles)
    except Exception as e:
        capture_exception(e)


if __name__ == "__main__":
    main({}, {})
