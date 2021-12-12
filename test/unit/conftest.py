# pytest config file
import pathlib
from dotenv import load_dotenv
from os import path, environ
from unittest.mock import Mock

dotenv_path = path.join(pathlib.Path().resolve(), "test/.env.test")
load_dotenv(dotenv_path=dotenv_path)

import pytest
from sqlalchemy.orm import Session

from lib.account.account import Account
from lib.asset.asset_manager import AssetManager
from lib.db import get_session
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.kms import Kms
from lib.order.order_repository import OrderRepository
from lib.order.trader import Trader


@pytest.fixture
def mock_account():
    test_access_key = environ.get("UPBIT_LOCAL_ACCESS_KEY")
    test_secret_key = environ.get("UPBIT_LOCAL_SECRET_KEY")

    account = Mock(spec=Account)
    account.get_id.return_value = 0
    account.get_access_key.return_value = test_access_key
    account.get_secret_key.return_value = test_secret_key
    account.get_alias.return_value = "test"
    return account


@pytest.fixture
def kms():
    return Kms()


@pytest.fixture
def session():
    return get_session()


@pytest.fixture
def order_repository(session: Session):
    return OrderRepository(session)


@pytest.fixture
def upbit_exchange(mock_account):
    return UpbitExchange.build(account=mock_account)


@pytest.fixture
def asset_manager(upbit_exchange: UpbitExchange):
    return AssetManager(exchange=upbit_exchange)


@pytest.fixture
def trader(asset_manager: AssetManager, upbit_exchange: UpbitExchange, session: Session, mock_account: Account, order_repository: OrderRepository):
    return Trader(
        asset_manager,
        exchange=upbit_exchange,
        sess=session,
        account=mock_account,
        order_repository=order_repository
    )
