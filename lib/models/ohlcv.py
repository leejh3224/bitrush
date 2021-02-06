from sqlalchemy import Column, String, BigInteger, DateTime, Numeric
from lib.models.base import Base


class Ohlcv(Base):
    __tablename__ = "ohlcv"

    id = Column(BigInteger, primary_key=True)
    ticker = Column(String(100))
    date = Column(DateTime)
    open = Column(Numeric(precision=19, scale=8))
    high = Column(Numeric(precision=19, scale=8))
    low = Column(Numeric(precision=19, scale=8))
    close = Column(Numeric(precision=19, scale=8))
    volume = Column(Numeric(precision=21, scale=8))
