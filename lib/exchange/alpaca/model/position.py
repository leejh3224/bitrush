from typing import Literal
from pydantic import BaseModel


class Position(BaseModel):
    asset_id: str
    symbol: str
    exchange: str
    asset_class: str
    asset_marginable: bool
    qty: str
    side: Literal['long']
    market_value: str
    cost_basis: str
    unrealized_pl: str
    unrealized_plpc: str
    unrealized_intraday_pl: str
    unrealized_intraday_plpc: str
    current_price: str
    lastday_price: str
    change_today: str
