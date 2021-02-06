from loguru import logger
from lib.utils import find
from decimal import *
from datetime import datetime
from lib.telegram_bot import send_message
import json


class Broker:
    def __init__(self, api, order_queue) -> None:
        super().__init__()
        self.api = api
        self.order_queue = order_queue
        self.assets = self.api.get_balance()

    def __get_asset(self, ticker):
        return find(self.assets, lambda asset, *args: asset.get("currency") == ticker)

    def get_cash(self):
        return self.get_balance(ticker="KRW")

    def get_balance(self, ticker):
        asset = self.__get_asset(ticker)
        return (
            Decimal(asset.get("balance", 0)) - Decimal(asset.get("locked", 0))
            if asset
            else 0
        )

    def get_price(self, ticker):
        asset = self.__get_asset(ticker)
        return Decimal(asset.get("avg_buy_price", 0)) if asset else 0

    def notify_order(self, order_id, type, ticker, price, size):
        """주문 체결 알림

        Args:
            order_id (str): 주문 uuid
            type (str): buy/sell
            ticker (str): 주문 종목
            price (Decimal): 매수/매도시 진입 가격 (실제가 x)
            size (Decimal): 주문 수량
        """
        date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        msg = json.dumps(
            {
                "date": date,
                "ticker": ticker,
                "type": type.upper(),
                "price": price,
                "size": size,
                "amount": f"{price * size:.8f}",
            },
            cls=DecimalEncoder,
            indent=2,
        )
        send_message(msg)
        logger.info(msg)
        self.order_queue.send_message(MessageBody=json.dumps({"order_id": order_id}))


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)