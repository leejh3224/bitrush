from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from lib.db import session_scope
from lib.order.open_order_data import OpenOrderData
from lib.order.order import Order
from lib.order.order_entity import OrderEntity
from lib.order.order_entity_adapter import OrderEntityAdapter


class OrderRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add_order(self, order: Order, data: OpenOrderData) -> None:
        db: Session

        with session_scope(self.session) as db:
            order = OrderEntity(
                id=order.get_id(),
                exchange=data.exchange,
                type=order.get_order_type(),
                ticker=order.get_ticker(),
                strategy=data.strategy,
                avg_price=order.get_avg_price(),
                volume=order.get_volume(),
                amount=order.get_amount(),
                raw_data=order.get_raw_data(),
                account_id=data.account_id
            )
            db.add(order)

    def get_last_order(self, ticker: str, strategy: str, account_id: int) -> Optional[Order]:
        db: Session

        with session_scope(self.session) as db:
            max_created_at = (
                db.query(func.max(OrderEntity.created_at))
                .filter_by(ticker=ticker, strategy=strategy, account_id=account_id)
                .subquery()
            )
            order_entity = db.query(OrderEntity) \
                .filter_by(created_at=max_created_at, ticker=ticker, strategy=strategy,
                           account_id=account_id) \
                .first()

            if not order_entity:
                return None

        return OrderEntityAdapter(order_entity)
