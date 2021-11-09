from sqlalchemy import Column, BigInteger, String, DateTime
from lib.models.base import Base


class Credential(Base):
    __tablename__ = "credential"

    id = Column(BigInteger, primary_key=True)
    access_key = Column(String(100))
    secret_key = Column(String(100))
    expire_at = Column(DateTime)
    alias = Column(String(100))
