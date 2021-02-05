# pytest config file
from dotenv import load_dotenv
from lib.utils import enable_http_logging


def pytest_sessionstart(session):
    load_dotenv()
    enable_http_logging()
