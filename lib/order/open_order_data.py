from pydantic import BaseModel


class OpenOrderData(BaseModel):
    exchange: str
    order_id: str
    strategy: str
    account_id: int
