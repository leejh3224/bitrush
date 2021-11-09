from sqlalchemy import Column, String, DateTime, Numeric, Enum, JSON
from lib.models.base import Base
import enum


class TradeType(enum.Enum):
    buy = "buy"
    sell = "sell"


class Trade(Base):
    __tablename__ = "trade"

    id = Column(String(60), primary_key=True)
    strategy = Column(String(100))
    type = Column(Enum(TradeType))
    date = Column(DateTime)
    ticker = Column(String(100))
    price = Column(Numeric(precision=19, scale=8))
    volume = Column(Numeric(precision=19, scale=8))
    amount = Column(Numeric(precision=19, scale=8))
    raw_data = Column(JSON)
    credential_alias = Column(String(100))
