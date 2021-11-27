from unittest import mock
import lib.account.account_repository
import order_syncer_app
from lib.account.account import Account
from lib.order.open_order_data import OpenOrderData


def test_main(mock_account: Account, mock_open_order_data: OpenOrderData):
    with mock.patch.object(lib.account.account_repository.AccountRepository, "get_all_active_accounts",
                           lambda *args, **kwargs: [mock_account]), \
            mock.patch.object(lib.order.open_order_repository.OpenOrderRepository, "get_open_orders", lambda *args, **kwargs: [(mock_open_order_data.order_id, mock_open_order_data)]):
        order_syncer_app.main({}, {})
