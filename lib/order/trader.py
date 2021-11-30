import math
from decimal import Decimal

from sqlalchemy.orm import Session

from lib.account.account import Account
from lib.asset.asset_manager import AssetManager
from lib.exchange.exchange import Exchange
from lib.order.open_order_data import OpenOrderData
from lib.order.open_order_repository import OpenOrderRepository
from lib.order.order_repository import OrderRepository
from lib.order.order_type import OrderType
from lib.strategy.base_strategy import BaseStrategy
import lib.logger as logger


class Trader:
    asset_manager: AssetManager
    exchange: Exchange
    sess: Session
    account: Account
    open_order_repository: OpenOrderRepository
    order_repository: OrderRepository

    account_risk_ratio = Decimal("0.01")
    stoploss_ratio = Decimal("0.1")

    def __init__(self,
                 asset_manager: AssetManager,
                 exchange: Exchange,
                 sess: Session,
                 account: Account,
                 open_order_repository: OpenOrderRepository,
                 order_repository: OrderRepository):
        self.asset_manager = asset_manager
        self.exchange = exchange
        self.sess = sess
        self.account = account
        self.open_order_repository = open_order_repository
        self.order_repository = order_repository

    def trade(self, exchange: str, ticker: str, strategy: BaseStrategy):
        amount = self.get_position_size()

        last_order = self.order_repository.get_last_order(
            ticker=ticker,
            strategy=strategy.get_name(),
            account_id=self.account.get_id()
        )

        # TODO read from open_order as well to check if pending order exists

        should_buy = (not last_order or last_order.get_order_type() == OrderType.SELL) and strategy.should_buy() and amount > Decimal("0")
        should_sell = last_order and last_order.get_order_type() == OrderType.BUY and strategy.should_sell()

        logger.info(f"last order = {last_order}, should buy = {should_buy}, should sell = {should_sell}")

        order = None

        if should_buy:
            order = self.exchange.buy(ticker=ticker, amount=amount)

        if should_sell:
            order = self.exchange.sell(ticker=ticker, volume=last_order.get_volume())

        if order:
            data = OpenOrderData.parse_obj(
                dict(
                    exchange=exchange,
                    order_id=order.get_id(),
                    strategy=strategy.get_name(),
                    account_id=self.account.get_id()
                )
            )

            logger.info(f"order placed, order = {order}, data = {data}")
            self.on_trade_success(data)

    def get_position_size(self) -> Decimal:
        cash = self.asset_manager.get_cash()
        position_size = Decimal(math.floor(((self.asset_manager.get_account_size() * self.account_risk_ratio) / self.stoploss_ratio)))
        return position_size if cash >= position_size else Decimal("0")

    def on_trade_success(self, data: OpenOrderData) -> None:
        self.open_order_repository.add_open_order(data)

