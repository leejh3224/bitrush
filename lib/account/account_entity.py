from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, BLOB

from lib.db import Base


class AccountEntity(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    vendor = Column(String(100))
    enabled = Column(Boolean, default=True)
    access_key = Column(String(120))
    secret_key = Column(String(120))
    expired_at = Column(DateTime)
    alias = Column(String(100))
    data_key = Column(BLOB)
