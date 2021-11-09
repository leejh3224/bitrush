from decimal import *
from loguru import logger
from lib.db import session_scope
from sqlalchemy import func
from lib.models.ohlcv import Ohlcv
from datetime import datetime, timedelta
from lib.models.trade import TradeType
from lib.broker import Broker
from typing import TypedDict, Optional


class StrategyParams(TypedDict):
    ticker: str
    ratio: Optional[Decimal]

    # 지정수량 매도
    # ex) ticker='BTC', volume=Decimal("0.01")
    volume: Optional[Decimal]

    # 지정가 매수
    # ex) ticker='BTC', amount=Decimal("10000.0")
    amount: Optional[Decimal]


class BaseStrategy:
    def __init__(self, broker, params) -> None:
        self.params: StrategyParams = dict(
            # 최소 주문 금액
            # https://upbit.com/service_center/notice?id=1722&__cf_chl_jschl_tk__=1bc2c2a0e9ca8f59135992d502d48cb4a04550e0-1613050026-0-AQgJMP22ic2-r3TptrxI6mltzU3CNk-L_RttBhA6KcRtVxoK5idKlroV2sN-ceooTSJtbfHUfxoSngN3D_VxJdKsRuH7zY8jdaxSqJ31EL6S-Y-58K-XAhWm6rsNHdVYh98sONE6dFwBDxzSyBSzsesD_z1SCh_dSyJQ2ykd_JzyIgCfY8MlMObQTIt5wK6XpIfZ9qo-eRSN3sF5RIJVmt4SRVlKqEqrRblPgGmmkAFYJ6mDuwD29NZapxdl6dL8YEjW58RnycstPX3wzXo-62J2sI_cm-caNb1ry_Bspnpuo4ICNWAmm5j0NISGSz9VVGPFBi0gJLB783MzpgxU1T4
            min_unit_krw=Decimal(5000),
            **params,
        )
        self.__check()
        self.broker: Broker = broker
        self.feed = self.broker.get_feed(self.params["ticker"])

    def __check(self) -> None:
        if not self.params["ticker"]:
            raise ValueError("ticker is required")

        if (
            not self.params.get("ratio")
            and not self.params.get("amount")
            and not self.params.get("volume")
        ):
            raise ValueError("ratio or amount/volume is required")

        if not self.name:
            raise ValueError("name is required")

    def __check_feed_staleness(self) -> None:
        with session_scope() as session:
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

    def __buy(self, amount):
        name = self.name
        ticker = self.params["ticker"]
        min_unit_krw = self.params["min_unit_krw"]

        if amount < min_unit_krw:
            logger.info("not enough cash")
            return

        order = self.broker.buy(ticker, amount=amount)
        credential_alias = self.broker.api.get_credential_alias()

        logger.info(f"order = {order}, credential_alias = {credential_alias}")

        if order:
            self.broker.notify_order(
                order_id=order["uuid"], strategy=name, credential_alias=credential_alias
            )

    def __sell(self, volume):
        ticker = self.params["ticker"]
        name = self.name

        order = self.broker.sell(ticker, amount=volume)
        credential_alias = self.broker.api.get_credential_alias()

        logger.info(f"order = {order}")

        if order:
            self.broker.notify_order(
                order_id=order["uuid"], strategy=name, credential_alias=credential_alias
            )

    def trade(self) -> None:
        """매매

        Args:
                volume (Decimal): 지정 수량 매도
                amount (Decimal): 지정 수량 매수
        """
        try:
            ratio = self.params.get("ratio")
            name = self.name
            ticker = self.params["ticker"]
            volume = self.params.get("volume")
            amount = self.params.get("amount")

            if volume and amount:
                raise Exception("can't specify both volume and amount")

            if volume:
                self.__sell(volume=volume)
                return

            if amount:
                self.__buy(amount=amount)
                return

            self.__check_feed_staleness()

            cash = self.broker.get_cash()
            buy_amount = int(cash * ratio)

            last_trade = self.broker.get_last_trade(ticker=ticker, strategy=name)
            trade_type = last_trade.trade_type
            total_volume = last_trade.total_volume

            logger.info(f"name = {name}, ticker = {ticker}, last_trade = {last_trade}")

            if (
                trade_type == None or trade_type == TradeType.sell
            ) and self.should_buy():
                self.__buy(amount=buy_amount)
                return

            if trade_type == TradeType.buy and self.should_sell():
                self.__sell(volume=total_volume)
                return
        except Exception as e:
            logger.error(e)
