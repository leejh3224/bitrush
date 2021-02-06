from datetime import timedelta
import logging
import http.client
from lib.models.ohlcv import Ohlcv
from decimal import *
from datetime import datetime, timedelta
import pandas as pd
from lib.db import session


def find(list, func):
    return ([item for idx, item in enumerate(list) if func(item, idx, list)] or [None])[
        0
    ]


def missing_days(days):
    """API에서 받아온 데이터에 구멍이 있을 경우 디비와 대조해서 빠진 날짜를 계산"""
    date_set = set(days[0] + timedelta(x) for x in range((days[-1] - days[0]).days))
    return sorted(date_set - set(days))


def get_live_feed(api, ticker):
    """디비에 있는 어제까지의 데이터 + 현재 데이터"""
    [json_result] = api.get_ohlcv_now(ticker)
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