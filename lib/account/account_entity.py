from sqlalchemy import Column, BigInteger, String, Boolean, DateTime

from lib.db import Base


class AccountEntity(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    vendor = Column(String(100))
    enabled = Column(Boolean)
    access_key = Column(String(100))
    secret_key = Column(String(100))
    expired_at = Column(DateTime)
    alias = Column(String(100))
