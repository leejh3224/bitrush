from typing import Literal, Optional

from pydantic import BaseModel


class PostOrdersResponse(BaseModel):
    uuid: str
    side: Literal["bid", "ask"]
    ord_type: Literal["limit", "price", "market"]
    price: Optional[str]
    avg_price: Optional[str]
    state: Literal["wait", "done", "cancel"]
    market: str  # KRW-BTC
    created_at: str
    volume: Optional[str]
    remaining_volume: Optional[str]
    reserved_fee: str
    paid_fee: str
    locked: str
    executed_volume: str
    trades_count: int
