from typing import Tuple, List

from sqlalchemy import BigInteger
from sqlalchemy.orm import Session

from lib.db import session_scope
from lib.order.open_order_data import OpenOrderData
from lib.order.open_order_entity import OpenOrderEntity


class OpenOrderRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_open_orders(self, account_id: int, count: int) -> List[Tuple[int, OpenOrderData]]:
        db: Session
        results = []

        with session_scope(self.session) as db:
            open_orders = db.query(OpenOrderEntity.id, OpenOrderEntity.data)\
                .filter(OpenOrderEntity.data["account_id"] == account_id)\
                .limit(count)\
                .all()

            for open_order in open_orders:
                results.append((open_order[0], OpenOrderData.parse_obj(open_order[1])),)

        return results

    def remove_open_order_by_id(self, _id: int) -> None:
        db: Session

        with session_scope(self.session) as db:
            db.query(OpenOrderEntity)\
                .filter(OpenOrderEntity.id == _id)\
                .delete()

    def add_open_order(self, data: OpenOrderData) -> int:
        db: Session

        with session_scope(self.session) as db:
            open_order = OpenOrderEntity(
                exchange=data.exchange,
                data=data.dict()
            )
            db.add(open_order)
            db.flush()

            return open_order.id

    def get_last_open_order(self):
        pass

