from sqlalchemy import Column, BigInteger, String, DateTime, JSON
from lib.models.base import Base
from sqlalchemy.sql import func


class Order(Base):
    __tablename__ = "order"

    id = Column(BigInteger, primary_key=True)
    date = Column(DateTime, default=func.now())
    exchange = Column(String(50))
    data = Column(JSON)
