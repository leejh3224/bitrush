from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from lib.account.account import Account
from lib.account.account_entity import AccountEntity
from lib.account.account_entity_adapter import AccountEntityAdapter
from lib.db import session_scope


class AccountRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_all_active_accounts(self) -> List[Account]:
        db: Session
        accounts: List[AccountEntity]

        with session_scope(self.session) as db:
            start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            accounts = db.query(AccountEntity) \
                .filter(AccountEntity.enabled, AccountEntity.expired_at >= start_of_day) \
                .all()

        return [AccountEntityAdapter(account) for account in accounts]

    def get_account_by_alias(self, alias: str) -> Account:
        db: Session
        account: AccountEntity

        with session_scope(self.session) as db:
            account = db.query(AccountEntity) \
                .filter_by(enabled=True, alias=alias) \
                .first()

        return AccountEntityAdapter(account)
