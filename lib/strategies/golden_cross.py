from decimal import *
from lib.db import session
from sqlalchemy import func
from lib.models.ohlcv import Ohlcv
from datetime import datetime, timedelta
from loguru import logger
from talib import abstract
from lib.telegram import send_message
import json
from lib.utils import get_live_feed


def golden_cross(api, broker, params):

    # params
    ticker = params["ticker"]
    short_period = params["short_period"]
    long_period = params["long_period"]
    min_unit_krw = params["min_unit_krw"]
    ratio = params["ratio"]

    (max_date,) = session.query(func.max(Ohlcv.date)).filter_by(ticker=ticker).first()

    yesterday = datetime.today() - timedelta(days=1)

    # Scanner가 동작하지 않아서 오늘 결과가 저장되지 않을 경우 수행 x
    if max_date.date() < yesterday.date():
        logger.info("record is stale, max date = {}", max_date)
        return

    feed = get_live_feed(api, ticker)

    mas = abstract.SMA(feed, timeperiod=short_period)
    mal = abstract.SMA(feed, timeperiod=long_period)
    feed["mas"] = mas
    feed["mal"] = mal
    prev_mas = feed["mas"].shift(1)
    prev_mal = feed["mal"].shift(1)
    feed["cross_up"] = (feed["mas"] >= feed["mal"]) & (prev_mas <= prev_mal)
    feed["cross_down"] = (feed["mas"] <= feed["mal"]) & (prev_mas >= prev_mal)

    today_ohlcv = feed.iloc[-1]
    cross_up = today_ohlcv["cross_up"]
    cross_down = today_ohlcv["cross_down"]

    cash = broker.get_cash()
    trade_amount = int(cash * ratio)
    size = broker.get_balance(ticker)

    if size > 0 and cross_down:
        order = api.sell(ticker, amount=size)
        if order:
            send_message(f"SELL order = {json.dumps(order, indent=2)}")
            logger.info("SELL order = {}", json.dumps(order, indent=2))
        return

    if size == 0 and cross_up:
        if trade_amount < min_unit_krw:
            logger.info("not enough cash")
            return
        order = api.buy(ticker, amount=trade_amount)
        if order:
            send_message(f"BUY order = {json.dumps(order, indent=2)}")
            logger.info("BUY order = {}", json.dumps(order, indent=2))
