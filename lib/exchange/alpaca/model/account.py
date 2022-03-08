from datetime import datetime
from pydantic import BaseModel


class Account(BaseModel):
    account_blocked: bool
    account_number: str
    accrued_fees: str
    buying_power: str
    cash: str
    created_at: datetime
    crypto_status: str
    currency: str
    daytrade_count: int
    daytrading_buying_power: str
    equity: str
    id: str
    initial_margin: str
    last_equity: str
    last_maintenance_margin: str
    long_market_value: str
    maintenance_margin: str
    multiplier: str
    non_marginable_buying_power: str
    pattern_day_trader: bool
    pending_transfer_in: str
    portfolio_value: str
    regt_buying_power: str
    short_market_value: str
    shorting_enabled: bool
    sma: str
    status: str
    trade_suspended_by_user: bool
    trading_blocked: bool
    transfers_blocked: bool
