from sqlalchemy import BigInteger, Column, String, JSON, DateTime, func

from lib.db import Base


class OpenOrderEntity(Base):
    __tablename__ = "open_order"

    id = Column(BigInteger, primary_key=True)
    exchange = Column(String(100))
    data = Column(JSON)
    created_at = Column(DateTime, default=func.now())
