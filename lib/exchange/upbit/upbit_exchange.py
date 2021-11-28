import hashlib
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from urllib.parse import urlencode

import jwt
import requests
from ratelimit import sleep_and_retry, limits
from requests import Session
from loguru import logger
import json

from lib.account.account import Account
from lib.asset.asset import Asset
from lib.candle.candle import Candle
from lib.exchange.exchange import Exchange
from lib.exchange.upbit.adapter.get_accounts_response_adapter import GetAccountsResponseAdapter
from lib.exchange.upbit.adapter.get_candles_days_response_adapter import GetCandlesDaysResponseAdapter
from lib.exchange.upbit.adapter.get_order_response_adapter import GetOrderResponseAdapter
from lib.exchange.upbit.adapter.get_ticker_response_adapter import GetTickerResponseAdapter
from lib.exchange.upbit.adapter.post_orders_response_adapter import PostOrdersResponseAdapter
from lib.exchange.upbit.model.error_response import ErrorResponse
from lib.order.order import Order

# https://docs.upbit.com/docs/user-request-guide
ratelimit: Dict[str, Dict[str, int]] = {
    "exchange.order": {"per_second": 8, "per_minute": 200},
    "exchange.others": {"per_second": 30, "per_minute": 900},
    "quotation": {"per_second": 10, "per_minute": 600},
}


def get_hash(query_string):
    m = hashlib.sha512()
    m.update(query_string)
    return m.hexdigest()


class UpbitExchange(Exchange):
    client: Session

    base_url = "https://api.upbit.com"
    access_key: str
    secret_key: str
    alias: str

    @staticmethod
    def build(account: Account):

        # always throw exception for non 200 response
        def on_error(r: requests.Response):
            if r.status_code >= 400:
                logger.info(
                    f"error\nurl={r.url}\ndata={json.dumps(r.json(), indent=2, ensure_ascii=False)}"
                )
            r.raise_for_status()

        client = requests.Session()
        client.hooks = {
            "response": lambda r, *args, **kwargs: on_error(r)
        }

        return UpbitExchange(
            client=client,
            account=account
        )

    def __init__(self, client: Session, account: Account):
        super().__init__(account)
        self.client = client
        self.access_key = account.get_access_key()
        self.secret_key = account.get_secret_key()
        self.alias = account.get_alias()

    @sleep_and_retry
    @limits(calls=ratelimit["quotation"]["per_minute"], period=60)
    @limits(calls=ratelimit["quotation"]["per_second"], period=1)
    def get_day_candles(self, ticker: str, start: str, end: str) -> List[Candle]:
        delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)

        url = f"{self.base_url}/v1/candles/days"
        query = {
            "market": "KRW-" + ticker,
            "to": end + " 00:00:00",
            "count": delta.days
        }
        res_list: List[Dict] = self.client.get(url, params=query).json()
        return [GetCandlesDaysResponseAdapter(res) for res in res_list]

    @sleep_and_retry
    @limits(calls=ratelimit["quotation"]["per_minute"], period=60)
    @limits(calls=ratelimit["quotation"]["per_second"], period=1)
    def get_today_candle(self, ticker: str) -> Candle:
        url = f"{self.base_url}/v1/candles/days"
        query = {
            "market": "KRW-" + ticker,
        }
        res: List[Dict] = self.client.get(url, params=query).json()
        return GetCandlesDaysResponseAdapter(res[0])

    @sleep_and_retry
    @limits(calls=ratelimit["quotation"]["per_minute"], period=60)
    @limits(calls=ratelimit["quotation"]["per_second"], period=1)
    def get_last_candle(self, ticker: str) -> Candle:
        url = f"{self.base_url}/v1/ticker"
        query = {
            "markets": "KRW-" + ticker
        }
        res: List[Dict] = self.client.get(url, params=query).json()
        return GetTickerResponseAdapter(res[0])

    @sleep_and_retry
    @limits(calls=ratelimit["exchange.others"]["per_minute"], period=60)
    @limits(calls=ratelimit["exchange.others"]["per_second"], period=1)
    def get_all_assets(self) -> List[Asset]:
        url = f"{self.base_url}/v1/accounts"
        payload = {**self.__get_auth()}
        res_list: List[Dict] = self.client.get(url, headers=self.__get_headers(payload)).json()
        return [GetAccountsResponseAdapter(res) for res in res_list]

    @sleep_and_retry
    @limits(calls=ratelimit["exchange.order"]["per_minute"], period=60)
    @limits(calls=ratelimit["exchange.order"]["per_second"], period=1)
    def buy(self, ticker: str, amount: Decimal) -> Order:
        """

        # example
        {
           "uuid":"cd947866-91bb-43bf-bd83-71b2580e2459",
           "side":"bid",
           "ord_type":"price",
           "price":"5000.0",
           "state":"wait",
           "market":"KRW-BTC",
           "created_at":"2021-11-26T21:07:35+09:00",
           "volume":None,
           "remaining_volume":None,
           "reserved_fee":"2.5",
           "remaining_fee":"2.5",
           "paid_fee":"0.0",
           "locked":"5002.5",
           "executed_volume":"0.0",
           "trades_count":0
        }
        """
        custom_order_id = str(uuid.uuid4())

        url = f"{self.base_url}/v1/orders"
        query = {
            "market": f"KRW-{ticker}",
            "side": "bid",
            "price": amount,
            "ord_type": "price",
            "identifier": custom_order_id
        }
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.client.post(url, params=query, headers=self.__get_headers(payload)).json()
        return PostOrdersResponseAdapter(res, custom_order_id)

    @sleep_and_retry
    @limits(calls=ratelimit["exchange.order"]["per_minute"], period=60)
    @limits(calls=ratelimit["exchange.order"]["per_second"], period=1)
    def sell(self, ticker: str, volume: Decimal) -> Order:
        """

        # example
        {
           "uuid":"c06c0852-0138-42e5-883d-30a2569a4cc5",
           "side":"ask",
           "ord_type":"market",
           "price":None,
           "state":"wait",
           "market":"KRW-BTC",
           "created_at":"2021-11-26T21:12:09+09:00",
           "volume":"0.00007997",
           "remaining_volume":"0.00007997",
           "reserved_fee":"0.0",
           "remaining_fee":"0.0",
           "paid_fee":"0.0",
           "locked":"0.00007997",
           "executed_volume":"0.0",
           "trades_count":0
        }
        """
        custom_order_id = str(uuid.uuid4())

        url = f"{self.base_url}/v1/orders"
        query = {
            "market": f"KRW-{ticker}",
            "side": "ask",
            "volume": volume,
            "ord_type": "market",
            "identifier": custom_order_id
        }
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.client.post(url, params=query, headers=self.__get_headers(payload)).json()
        return PostOrdersResponseAdapter(res, custom_order_id)

    @sleep_and_retry
    @limits(calls=ratelimit["exchange.order"]["per_minute"], period=60)
    @limits(calls=ratelimit["exchange.order"]["per_second"], period=1)
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        # buy example
        {
           "uuid":"b0c61050-450b-48e5-9854-476a431f30cb",
           "side":"bid",
           "ord_type":"price",
           "price":"5000.0",
           "state":"cancel",
           "market":"KRW-BTC",
           "created_at":"2021-11-21T16:37:40+09:00",
           "volume":None,
           "remaining_volume":None,
           "reserved_fee":"2.5",
           "remaining_fee":"0.00029395",
           "paid_fee":"2.49970605",
           "locked":"0.58819395",
           "executed_volume":"0.00006827",
           "trades_count":1,
           "trades":[
              {
                 "market":"KRW-BTC",
                 "uuid":"0badef8b-0127-4667-939d-9ec27fdfbe21",
                 "price":"73230000.0",
                 "volume":"0.00006827",
                 "funds":"4999.4121",
                 "created_at":"2021-11-21T16:37:40+09:00",
                 "side":"bid"
              }
           ]
        }

        # sell example
        {
           "uuid":"9b1a3245-2eeb-47d9-8ea8-ed59c0322e2c",
           "side":"ask",
           "ord_type":"market",
           "price":None,
           "state":"done",
           "market":"KRW-BTC",
           "created_at":"2021-11-21T16:43:37+09:00",
           "volume":"0.00012827",
           "remaining_volume":"0.0",
           "reserved_fee":"0.0",
           "remaining_fee":"0.0",
           "paid_fee":"4.694233055",
           "locked":"0.0",
           "executed_volume":"0.00012827",
           "trades_count":1,
           "trades":[
              {
                 "market":"KRW-BTC",
                 "uuid":"6627a29f-6253-4fb7-bb5c-ccbc1e1f2649",
                 "price":"73193000.0",
                 "volume":"0.00012827",
                 "funds":"9388.46611",
                 "created_at":"2021-11-21T16:43:37+09:00",
                 "side":"ask"
              }
           ]
        }
        """
        url = f"{self.base_url}/v1/order"
        query = {"uuid": order_id}
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        try:
            res = self.client.get(url, params=query, headers=self.__get_headers(payload)).json()
            return GetOrderResponseAdapter(res)
        except requests.HTTPError as e:
            err: ErrorResponse = ErrorResponse.parse_raw(e.response.text)
            status_code = e.response.status_code

            if status_code == 404 and err.error.name == "order_not_found":
                return None
            raise e

    def __get_auth(self):
        return {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),  # nounce should unique so build this everytime
        }

    def __get_headers(self, payload):
        jwt_token = jwt.encode(payload, self.secret_key)
        return {"Authorization": f"Bearer {jwt_token}"}
