from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict

from lib.candle.candle import Candle
from lib.exchange.upbit.model.get_candles_days_response import GetCandlesDaysResponse


class GetCandlesDaysResponseAdapter(Candle):
    response: GetCandlesDaysResponse

    def __init__(self, response: Dict):
        self.response = GetCandlesDaysResponse(**response)

    def get_ticker(self) -> str:
        return self.response.market.replace("KRW-", "")

    def get_closed_at(self) -> datetime:
        return datetime.strptime(self.response.candle_date_time_utc, "%Y-%m-%dT%H:%M:%S")

    def get_open_price(self) -> Decimal:
        return Decimal(self.response.opening_price)

    def get_high_price(self) -> Decimal:
        return Decimal(self.response.high_price)

    def get_low_price(self) -> Decimal:
        return Decimal(self.response.low_price)

    def get_close_price(self) -> Decimal:
        return Decimal(self.response.trade_price)

    def get_volume(self) -> Optional[Decimal]:
        return Decimal(self.response.candle_acc_trade_volume)
