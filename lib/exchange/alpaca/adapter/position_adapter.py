from decimal import Decimal
from typing import Dict

from lib.asset.asset import Asset
from lib.exchange.alpaca.model.position import Position
from lib.util import decimal


class PositionAdapter(Asset):
    position: Position

    def __init__(self, position: Dict):
        self.position = Position(**position)

    def get_net_value(self) -> Decimal:
        return decimal(Decimal(self.position.current_price) * Decimal(self.position.qty))

    def get_ticker(self) -> str:
        return self.position.symbol
