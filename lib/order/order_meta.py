from pydantic import BaseModel


class OrderMeta(BaseModel):
    strategy: str
    account_id: int
