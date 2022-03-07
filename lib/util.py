import inspect
from decimal import Decimal
from typing import List, Tuple, Type, Union

from lib.strategy.base_strategy import BaseStrategy
import lib.strategy as lib_strategy


def snake_to_camel(text: str):
    return text.replace("_", " ").title().replace(" ", "")

def load_strategies() -> List[Tuple[str, Type[BaseStrategy]]]:
    return [(name, module) for (name, module) in inspect.getmembers(lib_strategy) if not name.startswith("__") and name not in ["base_strategy"]]

def get_strategy_by_name(name: str):
    for strategy in load_strategies():
        _name, module = strategy
        if name == _name:
            return getattr(module, snake_to_camel(name))

def float_to_decimal(val: float, decimals: int = 8) -> Decimal:
    return Decimal(val).quantize(Decimal(f"1.{'0' * decimals}"))

def decimal(val: Union[str, float], decimals: int = 8):
    return Decimal(round(Decimal(val), decimals))
