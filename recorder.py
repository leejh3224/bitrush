from loguru import logger
from dotenv import load_dotenv

load_dotenv()

import json
from lib.upbit import Upbit
from lib.models.trade import Trade, TradeType
from lib.db import session
from datetime import datetime
from lib.sqs import sqs, order_queue_url, order_queue

api = Upbit()


def main(event, context):
    for record in event["Records"]:
        attributes = json.loads(record["attributes"])
        body = json.loads(record["body"])
        uuid = body["order_id"]
        order = api.get_order(uuid)

        logger.info(f"order_id = {uuid}")

        if order:
            trade_completed = (order["side"] == "ask" and order["state"] == "done") or (
                order["side"] == "bid" and order["state"] == "cancel"
            )
            if trade_completed:
                trades = []
                for trade in order["trades"]:
                    _trade = Trade(
                        id=f'upbit:{trade["uuid"]}',
                        type=TradeType.buy
                        if trade["side"] == "bid"
                        else TradeType.sell,
                        date=datetime.strptime(
                            order["created_at"], "%Y-%m-%dT%H:%M:%S+09:00"
                        ),
                        ticker=order["market"].replace("KRW-", ""),
                        price=order["price"],
                        volume=order["volume"],
                        amount=order["funds"],
                        raw_data=order,
                    )
                    trades.append(_trade)
                session.add_all(trades)
                session.commit()

                order_queue.delete_message(
                    QueueUrl=order_queue_url, ReceiptHandle=record["receiptHandle"]
                )
            else:
                retry_count = attributes["ApproximateReceiveCount"]

                logger.info(
                    f"order_id = {uuid}, retry = {retry_count}, trade not completed"
                )

                if retry_count > 3:
                    order_queue.delete_message(
                        QueueUrl=order_queue_url, ReceiptHandle=record["receiptHandle"]
                    )
                else:
                    message = sqs.Message(order_queue_url, record["receiptHandle"])
                    message.change_visibility(VisibilityTimeout=60 * 10)


if __name__ == "__main__":
    main({}, {})
