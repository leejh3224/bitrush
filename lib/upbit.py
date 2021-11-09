import os
import requests
import uuid
import jwt
import hashlib
from urllib.parse import urlencode
from loguru import logger
from ratelimit import limits, sleep_and_retry
import requests
import json
from decimal import Decimal


def get_hash(query_string):
    m = hashlib.sha512()
    m.update(query_string)
    return m.hexdigest()


def onError(r, *args, **kargs):
    if r.status_code >= 400:
        logger.info(
            f"error\nurl={r.url}\ndata={json.dumps(r.json(), indent=2, ensure_ascii=False)}"
        )
    r.raise_for_status()


# ref: https://docs.upbit.com/docs/user-request-guide
upbit_ratelimit = {
    "exchange": {
        "order": {"per_second": 8, "per_minute": 200},
        "others": {"per_second": 30, "per_minute": 900},
    },
    "quotation": {"per_second": 10, "per_minute": 600},
}


class Upbit:
    def __init__(self, access_key, secret_key, credential_alias) -> None:
        super().__init__()

        if not access_key or not secret_key:
            raise ValueError("access key or secret key is empty")

        self.access_key = access_key
        self.secret_key = secret_key
        self.credential_alias = credential_alias

        self.base_url = os.getenv("UPBIT_OPEN_API_SERVER_URL")

        # always throw exception for non 200 response
        self.session = requests.Session()
        self.session.hooks = {
            "response": lambda r, *args, **kargs: onError(r, args, kargs)
        }

    def __get_auth(self):
        return {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),  # nounce should unique so build this everytime
        }

    def __get_headers(self, payload):
        jwt_token = jwt.encode(payload, self.secret_key)
        return {"Authorization": f"Bearer {jwt_token}"}

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["quotation"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["quotation"]["per_second"], period=1)
    def get_ohlcv_daily(self, end, days=1, ticker="BTC"):
        url = f"{self.base_url}/v1/candles/days"
        query = {
            "market": "KRW-" + ticker,
            "count": days,
            "to": end.strftime("%Y-%m-%d %H:%M:%S"),
        }
        res = self.session.get(url, params=query)
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["quotation"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["quotation"]["per_second"], period=1)
    def get_ohlcv_now(self, ticker):
        """일봉 기준 데이터에 trade_price(종가)만 현재 가격으로 반환"""
        url = f"{self.base_url}/v1/ticker"
        query = {"markets": "KRW-" + ticker}
        res = self.session.get(url, params=query)
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["exchange"]["others"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["exchange"]["others"]["per_second"], period=1)
    def get_balance(self):
        url = f"{self.base_url}/v1/accounts"
        payload = {**self.__get_auth()}
        res = self.session.get(url, headers=self.__get_headers(payload))
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_second"], period=1)
    def buy(self, ticker, amount=Decimal(0)):
        """정해진 금액만큼 매수

        Args:
                        amount (int): 주문 총액 (원)
        """
        url = f"{self.base_url}/v1/orders"
        query = {
            "market": f"KRW-{ticker}",
            "side": "bid",
            "price": amount,
            "ord_type": "price",
        }
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.session.post(url, params=query, headers=self.__get_headers(payload))
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_second"], period=1)
    def sell(self, ticker, amount=Decimal(0)):
        """정해진 양만큼 매도

        Args:
                        amount (int): 코인양 (코인)
        """
        url = f"{self.base_url}/v1/orders"
        query = {
            "market": f"KRW-{ticker}",
            "side": "ask",
            "volume": amount,
            "ord_type": "market",
        }
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.session.post(url, params=query, headers=self.__get_headers(payload))
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_second"], period=1)
    def get_order(self, uuid):
        """개별 주문 정보 조회

        Args:
                        uuid (str): 주문 uuid
        """
        url = f"{self.base_url}/v1/order"
        query = {"uuid": uuid}
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.session.get(url, params=query, headers=self.__get_headers(payload))
        return res.json()

    @sleep_and_retry
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_minute"], period=60)
    @limits(calls=upbit_ratelimit["exchange"]["order"]["per_second"], period=1)
    def get_orders(self, ticker, state):
        """주문 목록 정보 조회

        Args:
                        ticker (str): 주문 심볼
                        state (str): 주문 상태
                                                                        - wait (default) (체결 대기)
                                                                        - done
                                                                        - cancel
        """
        url = f"{self.base_url}/v1/orders"
        query = {"market": f"KRW-{ticker}", "state": state}
        query_string = urlencode(query).encode()

        payload = {
            **self.__get_auth(),
            "query_hash": get_hash(query_string),
            "query_hash_alg": "SHA512",
        }

        res = self.session.get(url, params=query, headers=self.__get_headers(payload))
        return res.json()

    def get_credential_alias(self):
        return self.credential_alias
