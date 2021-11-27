from typing import Literal, List, Optional

from pydantic import BaseModel


class Trade(BaseModel):
    market: str
    uuid: str
    price: str
    volume: str
    funds: str
    side: Literal["bid", "ask"]
    created_at: str


class GetOrderResponse(BaseModel):
    uuid: str
    side: Literal["bid", "ask"]
    ord_type: Literal["limit", "price", "market"]
    price: Optional[str]
    state: Literal["wait", "done", "cancel"]
    market: str
    created_at: str
    volume: Optional[str]
    remaining_volume: Optional[str]
    reserved_fee: str
    remaining_fee: str
    paid_fee: str
    locked: str
    executed_volume: str
    trades_count: int
    trades: List[Trade]
