from datetime import datetime
from decimal import Decimal
from typing import Optional

from lib.candle.candle import Candle
from lib.exchange.upbit.model.get_ticker_response import GetTickerResponse


class GetTickerResponseAdapter(Candle):
    response: GetTickerResponse

    def __init__(self, response: GetTickerResponse):
        self.response = GetTickerResponse(**response)

    def get_ticker(self) -> str:
        return self.response.market.replace("KRW-", "")

    def get_closed_at(self) -> datetime:
        return datetime.strptime(self.response.trade_date + self.response.trade_time, "%Y%m%d%H%M%S")

    def get_open_price(self) -> Decimal:
        return Decimal(self.response.opening_price)

    def get_high_price(self) -> Decimal:
        return Decimal(self.response.high_price)

    def get_low_price(self) -> Decimal:
        return Decimal(self.response.low_price)

    def get_close_price(self) -> Decimal:
        return Decimal(self.response.trade_price)

    def get_volume(self) -> Optional[Decimal]:
        return Decimal(self.response.trade_volume)
