from typing import Optional, List, Dict

from sqlalchemy import func
from sqlalchemy.orm import Session

from lib.db import session_scope
from lib.order.order_meta import OrderMeta
from lib.order.order import Order
from lib.order.order_entity import OrderEntity
from lib.order.order_entity_adapter import OrderEntityAdapter


class OrderRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add_order(self, order: Order, meta: OrderMeta) -> None:
        db: Session

        with session_scope(self.session) as db:
            order = OrderEntity(
                id=order.get_id(),
                exchange=order.get_exchange(),
                type=order.get_order_type(),
                ticker=order.get_ticker(),
                strategy=meta.strategy,
                avg_price=order.get_avg_price(),
                volume=order.get_volume(),
                amount=order.get_amount(),
                raw_data=order.get_raw_data(),
                account_id=meta.account_id,
                status="wait"
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

        return OrderEntityAdapter(order_entity) if order_entity else None

    def get_open_orders(self, account_id: int, count: int) -> List[Order]:
        db: Session

        with session_scope(self.session) as db:
            open_orders = db.query(OrderEntity)\
                .filter(OrderEntity.account_id == account_id, OrderEntity.status == "wait")\
                .limit(count)\
                .all()

        return [OrderEntityAdapter(order) for order in open_orders]

    def finish_order(self, id: str, order: Order) -> None:
        db: Session

        with session_scope(self.session) as db:
            db.query(OrderEntity)\
                .filter(OrderEntity.id == id)\
                .update(
                    dict(
                        avg_price=order.get_avg_price(),
                        volume=order.get_volume(),
                        amount=order.get_amount(),
                        raw_data=order.get_raw_data(),
                        status="filled"
                    )
                )
