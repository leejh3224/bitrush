from dotenv import load_dotenv

from lib.account.account_repository import AccountRepository
from lib.candle.candle_repository import CandleRepository
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.db import get_session
from lib.sentry import init_sentry

load_dotenv()
init_sentry()


def main(event, context) -> None:
    sess = get_session()
    account_repository = AccountRepository(sess)
    candle_repository = CandleRepository(sess)

    account = account_repository.get_account_by_alias(alias="gompro-prod")

    exchange = UpbitExchange.build(account)

    tickers = ["BTC", "ETH"]

    for ticker in tickers:
        candle = exchange.get_day_candle(ticker)
        candle_repository.add_candle(candle)


if __name__ == "__main__":
    main({}, {})
