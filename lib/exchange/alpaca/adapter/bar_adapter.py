from datetime import datetime
from decimal import Decimal
from typing import Optional


from lib.candle.candle import Candle
from lib.exchange.alpaca.model.bar import Bar
from lib.util import float_to_decimal


class BarAdapter(Candle):
    ticker: str
    bar: Bar

    def __init__(self, ticker: str, bar: Bar):
        self.ticker = ticker
        self.bar = bar

    def get_ticker(self) -> str:
        return self.ticker

    def get_closed_at(self) -> datetime:
        return self.bar.t

    def get_open_price(self) -> Decimal:
        return float_to_decimal(self.bar.o, decimals=8)

    def get_high_price(self) -> Decimal:
        return float_to_decimal(self.bar.h, decimals=8)

    def get_low_price(self) -> Decimal:
        return float_to_decimal(self.bar.l, decimals=8)

    def get_close_price(self) -> Decimal:
        return float_to_decimal(self.bar.c, decimals=8)

    def get_volume(self) -> Optional[Decimal]:
        return float_to_decimal(self.bar.v, decimals=8)
