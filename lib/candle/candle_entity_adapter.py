from decimal import Decimal
from typing import Optional
from datetime import datetime

from lib.candle.candle import Candle
from lib.candle.candle_entity import CandleEntity


class CandleEntityAdapter(Candle):
    candle_entity: CandleEntity

    def __init__(self, candle_entity: CandleEntity):
        self.candle_entity = candle_entity

    def get_ticker(self) -> str:
        return self.candle_entity.ticker

    def get_closed_at(self) -> datetime:
        return self.candle_entity.closed_at

    def get_open_price(self) -> Decimal:
        return self.candle_entity.open

    def get_high_price(self) -> Decimal:
        return self.candle_entity.high

    def get_low_price(self) -> Decimal:
        return self.candle_entity.low

    def get_close_price(self) -> Decimal:
        return self.candle_entity.close

    def get_volume(self) -> Optional[Decimal]:
        return self.candle_entity.volume
