from sqlalchemy import Column, BigInteger, String, JSON
from lib.models.base import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(BigInteger, primary_key=True)
    exchange = Column(String(50))
    data = Column(JSON)
