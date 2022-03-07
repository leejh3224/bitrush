import math
from decimal import Decimal
from os import environ
from typing import Optional, List, Dict, Type

from sqlalchemy.orm import Session

from lib.account.account import Account
from lib.asset.asset_manager import AssetManager
from lib.exchange.exchange import Exchange
from lib.order.order_meta import OrderMeta
from lib.order.order import Order
from lib.order.order_repository import OrderRepository
from lib.order.order_type import OrderType
from lib.strategy.base_strategy import BaseStrategy
import lib.logger as logger
from lib.strategy import strategies as default_strategies


def get_trading_tickers() -> List[str]:
    """get tickers open for trade"""
    return ["BTC", "ETH"]


def get_trading_strategies_by_ticker(tickers: List[str], override_strategy: Optional[Type[BaseStrategy]] = None) -> Dict[str, List[Type[BaseStrategy]]]:
    strategies = [override_strategy] if override_strategy is not None else [clazz for (name, clazz) in default_strategies if name != "must_trade"]
    return { ticker: strategies for ticker in tickers }


class Trader:
    asset_manager: AssetManager
    exchange: Exchange
    sess: Session
    account: Account
    order_repository: OrderRepository

    account_risk_ratio = Decimal("0.01")
    stoploss_ratio = Decimal("0.1")

    def __init__(self,
                 asset_manager: AssetManager,
                 exchange: Exchange,
                 sess: Session,
                 account: Account,
                 order_repository: OrderRepository):
        self.asset_manager = asset_manager
        self.exchange = exchange
        self.sess = sess
        self.account = account
        self.order_repository = order_repository

    def trade(self, ticker: str, strategy: BaseStrategy, position_size: Optional[str] = None) -> Optional[Order]:
        amount = Decimal(position_size) if position_size else self.get_position_size()

        last_order = self.order_repository.get_last_order(
            ticker=ticker,
            strategy=strategy.get_name(),
            account_id=self.account.get_id()
        )

        should_buy = (not last_order or (last_order.get_order_type() == OrderType.SELL and last_order.is_filled())) and strategy.should_buy() and amount > Decimal("0")
        should_sell = last_order and last_order.is_filled() and last_order.get_order_type() == OrderType.BUY and strategy.should_sell()

        logger.info(f"last order = {last_order}, should buy = {should_buy}, should sell = {should_sell}")

        order = None

        if should_buy:
            order = self.exchange.buy(ticker=ticker, amount=amount)

        if should_sell:
            order = self.exchange.sell(ticker=ticker, volume=last_order.get_volume())

        if order:
            meta = OrderMeta.parse_obj(
                dict(
                    strategy=strategy.get_name(),
                    account_id=self.account.get_id()
                )
            )

            logger.info(f"order placed, order = {order}, meta = {meta}")
            self.on_trade_success(order, meta)

        return order

    def get_position_size(self) -> Decimal:
        cash = self.asset_manager.get_cash()
        position_size = Decimal(math.floor(((self.asset_manager.get_account_size() * self.account_risk_ratio) / self.stoploss_ratio)))
        return position_size if cash >= position_size else Decimal("0")

    def on_trade_success(self, order: Order, meta: OrderMeta) -> None:
        self.order_repository.add_order(order, meta)
