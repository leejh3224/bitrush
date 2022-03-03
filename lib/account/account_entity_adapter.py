from datetime import datetime

from lib.account.account import Account
from lib.account.account_entity import AccountEntity


class AccountEntityAdapter(Account):
    account_entity: AccountEntity

    def __init__(self, account_entity: AccountEntity):
        self.account_entity = account_entity

    def get_id(self) -> int:
        return self.account_entity.id

    def get_access_key(self) -> str:
        return self.account_entity.access_key

    def get_secret_key(self) -> str:
        return self.account_entity.secret_key

    def get_alias(self) -> str:
        return self.account_entity.alias

    def get_expired_at(self) -> datetime:
        return self.account_entity.expired_at
