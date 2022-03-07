import importlib
import os


base_path = "lib.strategy"

path = os.path.dirname(os.path.abspath(__file__))
paths = [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py' and f not in ['base_strategy.py']]

def snake_to_camel(text: str):
    return text.replace("_", " ").title().replace(" ", "")

def import_class(file_name: str):
    return (file_name, getattr(importlib.import_module(f"{base_path}.{file_name}"), snake_to_camel(file_name)))

strategies = list(map(import_class, paths))
