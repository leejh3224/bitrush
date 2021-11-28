from dotenv import load_dotenv

from lib.account.account_repository import AccountRepository
from lib.asset.asset_manager import AssetManager
from lib.candle.candle import build_feed
from lib.candle.candle_repository import CandleRepository
from lib.db import get_session
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.order.open_order_repository import OpenOrderRepository
from lib.order.order_repository import OrderRepository
from lib.order.trader import Trader
from lib.sentry import init_sentry
from lib.strategy.aroon import Aroon
from lib.strategy.cci import Cci
from lib.strategy.dc_breakout import DcBreakout
from lib.strategy.rsi_bb import RsiBB
from lib.strategy.stoch_rsi import StochRSI
from sentry_sdk import capture_exception
from loguru import logger


load_dotenv()
init_sentry()


def main(event, context):
    try:
        session = get_session()

        candle_repository = CandleRepository(session)
        account_repository = AccountRepository(session)
        open_order_repository = OpenOrderRepository(session)
        order_repository = OrderRepository(session)

        accounts = account_repository.get_all_active_accounts()
        tickers = ["BTC", "ETH"]

        feeds_by_ticker = {}

        for ticker in tickers:
            exchange = UpbitExchange.build(accounts[0])

            fresh_candle = exchange.get_last_candle(ticker)
            candles = candle_repository.get_candles(ticker, 1000)
            candles.insert(0, fresh_candle)

            feed = build_feed(candles=list(reversed(candles)))
            feeds_by_ticker[ticker] = feed

        strategies_by_ticker = {
            "BTC": [DcBreakout, Aroon, Cci, RsiBB, StochRSI],
            "ETH": [DcBreakout, Aroon, Cci, RsiBB, StochRSI]
        }

        logger.info(f"accounts = {accounts}")

        for account in accounts:
            exchange = UpbitExchange.build(account)
            asset_manager = AssetManager(exchange)
            trader = Trader(asset_manager, exchange, session, account, open_order_repository, order_repository)

            for ticker, strategies in strategies_by_ticker.items():
                for strategy in strategies:
                    logger.info(f"trading with strategy = {strategy}, ticker = {ticker}")

                    trader.trade(exchange="upbit", ticker=ticker, strategy=strategy(feeds_by_ticker[ticker]))
    except Exception as e:
        capture_exception(e)


if __name__ == "__main__":
    main({}, {})
