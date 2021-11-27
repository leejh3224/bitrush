from dotenv import load_dotenv

from lib.account.account_repository import AccountRepository
from lib.db import get_session
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.order.open_order_repository import OpenOrderRepository
from lib.order.order_repository import OrderRepository
from lib.sentry import init_sentry
from sentry_sdk import capture_exception
import logging as logger


load_dotenv()
init_sentry()


def main(event, context):
    try:
        session = get_session()
        open_order_repository = OpenOrderRepository(session)
        order_repository = OrderRepository(session)
        account_repository = AccountRepository(session)

        accounts = account_repository.get_all_active_accounts()

        for account in accounts:
            exchange = UpbitExchange.build(account)

            open_orders = open_order_repository.get_open_orders(account_id=account.get_id(), count=20)

            logger.info(f"syncing open orders = {open_orders}")

            for open_order in open_orders:
                _id = open_order[0]
                data = open_order[1]

                order = exchange.get_order(order_id=_id)

                if not order or not order.is_filled():
                    continue

                logger.info(f"adding order = {order}, data = {data}")
                order_repository.add_order(order, data)
    except Exception as e:
        capture_exception(e)


if __name__ == "__main__":
    main({}, {})
