from loguru import logger
from dotenv import load_dotenv

load_dotenv()

from lib.db import session_scope
from lib.upbit import Upbit
from lib.models.order import Order
from lib.utils import is_trade_completed
from lib.models.trade import Trade, TradeType
from lib.models.credential import Credential
from datetime import datetime


def main(event, context):
    with session_scope() as session:
        credentials = session.query(
            Credential.access_key, Credential.secret_key, Credential.alias
        ).all()

        for credential in credentials:
            access_key = credential[0]
            secret_key = credential[1]
            alias = credential[2]

            api = Upbit(access_key, secret_key, credential_alias=alias)

            db_orders = (
                session.query(Order.id, Order.exchange, Order.data).limit(10).all()
            )

            logger.info(f"orders = {db_orders}")

            for db_order in db_orders:
                logger.info(f"order = {db_order}")

                id = db_order[0]
                exchange = db_order[1]
                data = db_order[2]

                if exchange == "upbit":
                    uuid = data["order_id"]
                    strategy = data["strategy"]
                    credential_alias = data["credential_alias"]

                    order = api.get_order(uuid)

                    if order:
                        trade_completed = is_trade_completed(order)
                        if trade_completed:
                            trades = []
                            for trade in order["trades"]:
                                _trade = Trade(
                                    id=f'upbit:{trade["uuid"]}',
                                    strategy=strategy,
                                    type=TradeType.buy
                                    if trade["side"] == "bid"
                                    else TradeType.sell,
                                    date=datetime.strptime(
                                        trade["created_at"], "%Y-%m-%dT%H:%M:%S+09:00"
                                    ),
                                    ticker=trade["market"].replace("KRW-", ""),
                                    price=trade["price"],
                                    volume=trade["volume"],
                                    amount=trade["funds"],
                                    raw_data=trade,
                                    credential_alias=credential_alias,
                                )
                                trades.append(_trade)

                            session.add_all(trades)
                            session.query(Order).filter(Order.id == id).delete()
                            session.commit()


if __name__ == "__main__":
    main({}, {})
