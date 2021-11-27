# pytest config file
import pathlib
import uuid
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv
from os import path, environ
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from lib.account.account import Account
from lib.account.account_repository import AccountRepository
from lib.asset.asset_manager import AssetManager
from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository
from lib.db import get_session
from lib.exchange.upbit.upbit_exchange import UpbitExchange
from lib.order.open_order_data import OpenOrderData
from lib.order.open_order_repository import OpenOrderRepository
from lib.order.order import Order
from lib.order.order_repository import OrderRepository
from lib.order.order_type import OrderType
from lib.order.trader import Trader


def pytest_sessionstart(session):
    dotenv_path = path.join(pathlib.Path().parent.resolve(), ".env.test")
    load_dotenv(dotenv_path=dotenv_path)


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
def mock_candle():
    candle = Mock(spec=Candle)
    candle.get_ticker.return_value = "BTC"
    candle.get_closed_at.return_value = datetime.strptime("2021-11-26 00:00:00", "%Y-%m-%d %H:%M:%S")
    candle.get_open_price.return_value = Decimal("10")
    candle.get_high_price.return_value = Decimal("20")
    candle.get_low_price.return_value = Decimal("5")
    candle.get_close_price.return_value = Decimal("15")
    candle.get_volume.return_value = Decimal("0.00001")
    return candle


@pytest.fixture
def mock_buy_order():
    order = Mock(spec=Order)
    order.get_id.return_value = str(uuid.uuid4())
    order.is_filled.return_value = True
    order.get_order_type.return_value = OrderType.BUY
    order.get_ticker.return_value = "BTC"
    order.get_avg_price.return_value = Decimal("5000")
    order.get_amount.return_value = Decimal("4999.2221")
    order.get_volume.return_value = Decimal("0.00001")
    order.get_raw_data.return_value = "{}"
    return order


@pytest.fixture
def mock_sell_order():
    order = Mock(spec=Order)
    order.get_id.return_value = str(uuid.uuid4())
    order.is_filled.return_value = True
    order.get_order_type.return_value = OrderType.SELL
    order.get_ticker.return_value = "BTC"
    order.get_avg_price.return_value = Decimal("5000")
    order.get_amount.return_value = Decimal("4999.2221")
    order.get_volume.return_value = Decimal("0.00001")
    order.get_raw_data.return_value = "{}"
    return order


@pytest.fixture
def mock_open_order_data():
    return OpenOrderData.parse_obj(
        dict(
            exchange="test",
            order_id="b0c61050-450b-48e5-9854-476a431f30cb",
            strategy="test",
            account_id=0
        )
    )


@pytest.fixture
def session():
    return get_session()


@pytest.fixture
def candle_repository(session: Session):
    return CandleRepository(session)


@pytest.fixture
def open_order_repository(session: Session):
    return OpenOrderRepository(session)


@pytest.fixture
def account_repository(session: Session):
    return AccountRepository(session)


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
def trader(asset_manager: AssetManager, upbit_exchange: UpbitExchange, session: Session, mock_account: Account, open_order_repository: OpenOrderRepository, order_repository: OrderRepository):
    return Trader(
        asset_manager,
        exchange=upbit_exchange,
        sess=session,
        account=mock_account,
        open_order_repository=open_order_repository,
        order_repository=order_repository
    )
