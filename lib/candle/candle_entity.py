from decimal import Decimal

from sqlalchemy import Column, String, BigInteger, DateTime, Numeric, DECIMAL
from lib.db import Base


class CandleEntity(Base):
    __tablename__ = "candle"

    id = Column(BigInteger, primary_key=True)
    ticker = Column(String(100))
    closed_at = Column(DateTime)
    open: Decimal = Column(DECIMAL(precision=19, scale=8))
    high: Decimal = Column(Numeric(precision=19, scale=8))
    low: Decimal = Column(Numeric(precision=19, scale=8))
    close: Decimal = Column(Numeric(precision=19, scale=8))
    volume: Decimal = Column(Numeric(precision=21, scale=8))

    def __repr__(self):
        return f"""CandleEntity(ticker={self.ticker}, closed_at={self.closed_at}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})"""
