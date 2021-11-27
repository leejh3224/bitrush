import mock

import lib.exchange.upbit.upbit_exchange
import trader_app
from lib.account.account import Account
from lib.order.order import Order


def test_main(mock_account: Account, mock_buy_order: Order, mock_sell_order: Order):
    with mock.patch.object(lib.account.account_repository.AccountRepository, "get_all_active_accounts",
                           lambda *args, **kwargs: [mock_account]),\
            mock.patch.object(lib.exchange.upbit.upbit_exchange.UpbitExchange, "buy", lambda *args, **kwargs: mock_buy_order),\
            mock.patch.object(lib.exchange.upbit.upbit_exchange.UpbitExchange, "sell", lambda *args, **kwargs: mock_sell_order),\
            mock.patch.object(lib.order.order_repository.OrderRepository, "get_last_order", lambda *args, **kwargs: mock_sell_order):
        trader_app.main({}, {})

