from lib.utils import find
from decimal import *
import json
from lib.models.ohlcv import Ohlcv
import pandas as pd
from datetime import datetime
from lib.db import session


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
            else Decimal(0)
        )

    def get_price(self, ticker):
        asset = self.__get_asset(ticker)
        return Decimal(asset.get("avg_buy_price", 0)) if asset else 0

    def notify_order(self, order_id, strategy):
        """주문 체결 알림

        Args:
            order_id (str): 주문 uuid
            strategy (str): 전략
        """
        self.order_queue.send_message(
            MessageBody=json.dumps({"order_id": order_id, "strategy": strategy})
        )

    def buy(self, ticker, amount=0):
        self.api.buy(ticker, amount)

    def sell(self, ticker, amount=0):
        self.api.sell(ticker, amount)

    def get_feed(self, ticker):
        """디비에 있는 어제까지의 데이터 + 현재 데이터"""
        [json_result] = self.api.get_ohlcv_now(ticker)
        ohlcv = Ohlcv(
            ticker=ticker,
            date=datetime.strptime(
                json_result["trade_date_kst"] + json_result["trade_time_kst"],
                "%Y%m%d%H%M%S",
            ),
            open=Decimal(json_result["opening_price"]),
            high=Decimal(json_result["high_price"]),
            low=Decimal(json_result["low_price"]),
            close=Decimal(json_result["trade_price"]),
        )
        ohlcvs = session.query(Ohlcv).filter_by(ticker=ticker).all() + [ohlcv]

        feed = pd.DataFrame(
            [vars(s) for s in ohlcvs], columns=["date", "open", "high", "low", "close"]
        )
        return feed


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)