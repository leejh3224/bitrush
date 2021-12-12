from decimal import Decimal

from sqlalchemy import Column, String, DateTime, Numeric, JSON, Enum, BigInteger, func

from lib.db import Base
from lib.order.order_type import OrderType


class OrderEntity(Base):
    __tablename__ = "order"

    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    exchange = Column(String(100))
    type = Column(Enum(OrderType))
    ticker = Column(String(100))
    strategy = Column(String(100))
    avg_price: Decimal = Column(Numeric(precision=19, scale=8))
    volume: Decimal = Column(Numeric(precision=19, scale=8))
    amount: Decimal = Column(Numeric(precision=19, scale=8))
    raw_data = Column(JSON)
    account_id = Column(BigInteger)

    """
    enum
        - wait
        - filled
    """
    status = Column(String(20))
