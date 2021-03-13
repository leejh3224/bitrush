from loguru import logger
from dotenv import load_dotenv

load_dotenv()

from lib.db import session
from lib.upbit import Upbit
from lib.models.order import Order
from lib.utils import is_trade_completed
from lib.models.trade import Trade, TradeType
from datetime import datetime

api = Upbit()


def main(event, context):
    db_orders = session.query(Order.id, Order.exchange, Order.data).all()

    for db_order in db_orders:
        logger.info(f"order = {db_order}")

        id = db_order[0]
        exchange = db_order[1]
        data = db_order[2]

        if exchange == "upbit":
            uuid = data["order_id"]
            strategy = data["strategy"]

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
                        )
                        trades.append(_trade)

                    try:
                        session.add_all(trades)
                        session.delete(Order(id))
                        session.commit()
                    except:
                        session.rollback()
                        raise


if __name__ == "__main__":
    main({}, {})
