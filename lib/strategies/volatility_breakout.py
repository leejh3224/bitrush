from lib.broker import Broker
from lib.db import session
from sqlalchemy import func
from lib.models.ohlcv import Ohlcv
from datetime import datetime, timedelta
from loguru import logger
from lib.utils import get_live_feed
from decimal import *
from lib.upbit import Upbit


def volatility_breakout(api: Upbit, broker: Broker, params):

    # params
    ticker = params["ticker"]
    min_unit_krw = params["min_unit_krw"]
    k = params["k"]
    ratio = params["ratio"]

    (max_date,) = session.query(func.max(Ohlcv.date)).filter_by(ticker=ticker).first()

    yesterday = datetime.today() - timedelta(days=1)

    # Scanner가 동작하지 않아서 오늘 결과가 저장되지 않을 경우 수행 x
    if max_date.date() < yesterday.date():
        logger.info("record is stale, max date = {}", max_date)
        return

    feed = get_live_feed(api, ticker)

    cash = broker.get_cash()
    trade_amount = int(cash * ratio)
    size = broker.get_balance(ticker)

    yesterday_ohlcv = feed.iloc[-2]
    range = yesterday_ohlcv["high"] - yesterday_ohlcv["low"]
    current_ohlcv = feed.iloc[-1]

    now = datetime.now()
    when_to_sell = datetime(now.year, now.month, now.day, 23, 30, 0)

    if size > 0 and when_to_sell < now <= when_to_sell + timedelta(minutes=20):
        order = api.sell(ticker, amount=size)
        if order:
            broker.notify_order(
                order_id=order["uuid"],
                type="sell",
                ticker=ticker,
                price=current_ohlcv["close"],
                size=size,
                strategy="volatility_breakout",
            )
        return

    if size == 0 and current_ohlcv["close"] > current_ohlcv["open"] + (range * k):
        if trade_amount < min_unit_krw:
            logger.info("not enough cash")
            return
        order = api.buy(ticker, amount=trade_amount)
        if order:
            broker.notify_order(
                order_id=order["uuid"],
                type="buy",
                ticker=ticker,
                price=current_ohlcv["close"],
                size=size,
                strategy="volatility_breakout",
            )
