from typing import Optional

from pydantic import BaseModel


class GetCandlesDaysResponse(BaseModel):
    market: str
    candle_date_time_utc: str
    candle_date_time_kst: str
    opening_price: str
    high_price: str
    low_price: str
    trade_price: str
    timestamp: int
    candle_acc_trade_price: str
    candle_acc_trade_volume: str
    prev_closing_price: str
    change_price: str
    change_rate: str
    converted_trade_price: Optional[str]
