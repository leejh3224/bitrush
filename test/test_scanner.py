import mock

import lib.account.account_repository
import scanner_app
from lib.account.account import Account


def test_main(mock_account: Account):
    with mock.patch.object(lib.account.account_repository.AccountRepository, "get_account_by_alias", lambda *args, **kwargs: mock_account):
        scanner_app.main({}, {})
