from decimal import Decimal
from typing import Union
from lib.strategy import strategies


def get_strategy_by_name(name: str):
    found = list(filter(lambda str: str[0] == name, strategies))
    return found[0][1] if len(found) == 1 else None

def float_to_decimal(val: float, decimals: int = 8) -> Decimal:
    return Decimal(val).quantize(Decimal(f"1.{'0' * decimals}"))

def decimal(val: Union[str, float], decimals: int = 8):
    return Decimal(round(Decimal(val), decimals))
