from lib.account.account_repository import AccountRepository


def test_get_all_active_account(account_repository: AccountRepository):
    accounts = account_repository.get_all_active_accounts()

    assert len(accounts) == 2


def test_get_account_by_alias(account_repository: AccountRepository):
    account = account_repository.get_account_by_alias("gompro-prod")

    assert account.get_alias() == "gompro-prod"

