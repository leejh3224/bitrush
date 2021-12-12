import pathlib
from os import path

from dotenv import load_dotenv


def pytest_sessionstart():
    dotenv_path = path.join(pathlib.Path().parent.resolve(), "../.env.test")
    load_dotenv(dotenv_path=dotenv_path)

