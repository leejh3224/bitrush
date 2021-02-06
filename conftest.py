# pytest config file
from dotenv import load_dotenv


def pytest_sessionstart(session):
    load_dotenv()
