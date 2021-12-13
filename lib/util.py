import inspect
from typing import List, Tuple, Type

from lib.strategy.base_strategy import BaseStrategy
import lib.strategy as lib_strategy
from lib.strategy.must_trade import MustTrade


def snake_to_camel(text: str):
    return text.replace("_", " ").title().replace(" ", "")

def load_strategies() -> List[Tuple[str, Type[BaseStrategy]]]:
    return [(name, module) for (name, module) in inspect.getmembers(lib_strategy) if not name.startswith("__") and name not in ["base_strategy"]]

def get_strategy_by_name(name: str):
    for strategy in load_strategies():
        _name, module = strategy
        if name == _name:
            return getattr(module, snake_to_camel(name))
