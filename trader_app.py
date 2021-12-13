from os import environ

from dotenv import load_dotenv
load_dotenv()

from lib.util import get_strategy_by_name

import traceback
from lib.account.account_repository import AccountRepository
from lib.asset.asset_manager import AssetManager
from lib.candle.candle_repository import CandleRepository
from lib.db import get_session, wait_for_db_init
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.feed.db_feed import DbFeed
from lib.kms import Kms
from lib.order.order_repository import OrderRepository
from lib.order.trader import Trader, get_trading_tickers, get_trading_strategies_by_ticker
from lib.sentry import init_sentry
import lib.logger as logger


init_sentry()


def main(event, context):
    try:
        _tickers = event.get("tickers")
        _position_size = event.get("position-size")
        _strategy = event.get("strategy")
        account_alias = event.get("account-alias")

        kms = Kms()
        session = get_session()

        if environ.get("STAGE") == "test":
            wait_for_db_init(session)

        candle_repository = CandleRepository(session)
        account_repository = AccountRepository(session, kms)
        order_repository = OrderRepository(session)

        accounts = account_repository.get_all_active_accounts(alias=account_alias)
        db_feed = DbFeed(exchange=UpbitExchange.build(accounts[0]), candle_repository=candle_repository)

        tickers = _tickers or get_trading_tickers()
        strategy = get_strategy_by_name(name=_strategy)

        feeds_by_ticker = db_feed.build_feeds_by_ticker(tickers=tickers)
        strategies_by_ticker = get_trading_strategies_by_ticker(tickers=tickers, override_strategy=strategy)

        logger.info(f"accounts = {accounts}")
        orders = []

        for account in accounts:
            exchange = UpbitExchange.build(account)
            asset_manager = AssetManager(exchange)
            trader = Trader(asset_manager, exchange, session, account, order_repository)

            for ticker, strategies in strategies_by_ticker.items():
                for strategy in strategies:
                    logger.info(f"trading with strategy = {strategy}, ticker = {ticker}")

                    wait_order = trader.trade(ticker=ticker, strategy=strategy(feeds_by_ticker[ticker]), position_size=_position_size)

                    if wait_order is not None:
                        orders.append(wait_order)

        return {
            "statusCode": 200,
            "body": ",".join([order.get_id() for order in orders])
        }
    except Exception as e:
        stack = traceback.format_exc()
        logger.error(e)

        return {
            "statusCode": 500,
            "body": stack
        }


if __name__ == "__main__":
    main({}, {})
