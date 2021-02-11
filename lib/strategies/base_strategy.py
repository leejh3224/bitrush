from decimal import Decimal
from loguru import logger
from lib.db import session
from sqlalchemy import func
from lib.models.ohlcv import Ohlcv
from datetime import datetime, timedelta
from lib.models.trade import Trade, TradeType
from lib.broker import Broker
from typing import TypedDict


class StrategyParams(TypedDict):
    ticker: str
    ratio: Decimal


class BaseStrategy:
    def __init__(self, broker, params) -> None:
        self.params: StrategyParams = dict(
            # 최소 주문 금액
            # https://upbit.com/service_center/notice?id=1722&__cf_chl_jschl_tk__=1bc2c2a0e9ca8f59135992d502d48cb4a04550e0-1613050026-0-AQgJMP22ic2-r3TptrxI6mltzU3CNk-L_RttBhA6KcRtVxoK5idKlroV2sN-ceooTSJtbfHUfxoSngN3D_VxJdKsRuH7zY8jdaxSqJ31EL6S-Y-58K-XAhWm6rsNHdVYh98sONE6dFwBDxzSyBSzsesD_z1SCh_dSyJQ2ykd_JzyIgCfY8MlMObQTIt5wK6XpIfZ9qo-eRSN3sF5RIJVmt4SRVlKqEqrRblPgGmmkAFYJ6mDuwD29NZapxdl6dL8YEjW58RnycstPX3wzXo-62J2sI_cm-caNb1ry_Bspnpuo4ICNWAmm5j0NISGSz9VVGPFBi0gJLB783MzpgxU1T4
            min_unit_krw=Decimal(5000),
            **params,
        )
        self.broker: Broker = broker
        self.__check()

    def __check(self) -> None:
        if not self.params["ticker"]:
            raise ValueError("ticker is required")

        if not self.params["ratio"]:
            raise ValueError("ratio is required")

        if not self.name:
            raise ValueError("name is required")

    def __check_feed_staleness(self) -> None:
        (max_date,) = (
            session.query(func.max(Ohlcv.date))
            .filter_by(ticker=self.params["ticker"])
            .first()
        )

        yesterday = datetime.today() - timedelta(days=1)

        # Scanner가 동작하지 않아서 오늘 결과가 저장되지 않을 경우 수행 x
        if max_date.date() < yesterday.date():
            logger.info("record is stale, max date = {}", max_date)
            return

    # abstract properties
    name: str = None

    def should_buy(self) -> bool:
        pass

    def should_sell(self) -> bool:
        pass

    def trade(self) -> None:
        ratio = self.params["ratio"]
        name = self.name
        ticker = self.params["ticker"]
        min_unit_krw = self.params["min_unit_krw"]

        self.__check_feed_staleness()

        cash = self.broker.get_cash()
        buy_amount = int(cash * ratio)

        get_last_trade_date = (
            session.query(func.max(Trade.date))
            .filter_by(ticker=ticker, strategy=name)
            .subquery()
        )
        result = (
            session.query(Trade.type, Trade.volume)
            .filter_by(date=get_last_trade_date)
            .first()
        )
        (trade_type, volume) = result if result else (None, Decimal(0))

        if trade_type == TradeType.sell and self.should_buy():
            if buy_amount < min_unit_krw:
                logger.info("not enough cash")
                return
            order = self.broker.buy(ticker, amount=buy_amount)
            if order:
                self.broker.notify_order(
                    order_id=order["uuid"],
                    strategy=name,
                )
            return

        if trade_type == TradeType.buy and self.should_sell():
            order = self.broker.sell(ticker, amount=volume)
            if order:
                self.broker.notify_order(
                    order_id=order["uuid"],
                    strategy=name,
                )
            return
