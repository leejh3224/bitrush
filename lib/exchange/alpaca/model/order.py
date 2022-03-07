from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel


class Order(BaseModel):
    id: str
    client_order_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    submitted_at: Optional[datetime]
    filled_at: Optional[datetime]
    expired_at: Optional[datetime]
    canceled_at: Optional[datetime]
    failed_at: Optional[datetime]
    replaced_at: Optional[datetime]
    replaced_by: Optional[str]
    replaces: Optional[str]
    asset_id: str
    symbol: str
    asset_class: str
    notional: Optional[str]
    qty: Optional[str]
    filled_qty: str
    filled_avg_price: Optional[str]
    order_class: str
    type: str
    side: str
    time_in_force: str
    limit_price: Optional[str]
    stop_price: Optional[str]
    status: Literal["accepted", "pending_new", "accepted_for_bidding", "stopped", "rejected", "suspended", "calculated", "new", "partially_filled", "filled", "done_for_day", "canceled", "expired", "replaced", "pending_cancel", "pending_replace"]
    extended_hours: bool
    legs: Optional[List['Order']]
    trail_percent: Optional[str]
    trail_price: Optional[str]
    hwm: Optional[str]

Order.update_forward_refs()
