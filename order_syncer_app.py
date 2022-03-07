from os import environ

from dotenv import load_dotenv
load_dotenv()

import traceback
from lib.account.account_repository import AccountRepository
from lib.db import get_session, wait_for_db_init
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.kms import Kms
from lib.order.order_repository import OrderRepository
from lib.sentry import init_sentry
import lib.logger as logger


init_sentry()


def main(event, context):
    try:
        account_alias = event.get("account-alias")

        kms = Kms()
        session = get_session()

        if environ.get("STAGE") == "test":
            wait_for_db_init(session)

        order_repository = OrderRepository(session)
        account_repository = AccountRepository(session, kms)

        accounts = account_repository.get_all_active_upbit_accounts(alias=account_alias)

        logger.info(f"accounts = {accounts}")

        filled_order_ids = []

        for account in accounts:
            exchange = UpbitExchange.build(account)

            open_orders = order_repository.get_open_orders(account_id=account.get_id(), count=20)

            logger.info(f"alias = {account.get_alias()}, syncing open orders = {open_orders}")

            for open_order in open_orders:
                order_data = exchange.get_order(order_id=open_order.get_id())

                if not order_data or not order_data.is_filled():
                    continue

                logger.info(f"updating order data = {order_data}")

                order_repository.finish_order(id=open_order.get_id(), order=order_data)
                filled_order_ids.append(open_order.get_id())

        return {
            "statusCode": 200,
            "body": ",".join([order_id for order_id in filled_order_ids])
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
