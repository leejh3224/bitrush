from datetime import datetime
from typing import List, Optional, Any

from sqlalchemy.orm import Session

from lib import aes
from lib.account.account import Account
from lib.account.account_entity import AccountEntity
from lib.account.account_entity_adapter import AccountEntityAdapter
from lib.db import session_scope
from lib.kms import Kms


class AccountRepository:
    session: Session
    kms: Kms

    def __init__(self, session: Session, kms: Kms):
        self.session = session
        self.kms = kms

    def get_all_active_upbit_accounts(self, alias: Optional[str] = None) -> List[Account]:
        db: Session
        accounts: List[AccountEntity]

        with session_scope(self.session) as db:
            start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            query = db.query(AccountEntity) \
                .filter(AccountEntity.enabled, AccountEntity.expired_at >= start_of_day) \
                .filter(AccountEntity.vendor, "upbit")

            if alias:
                query.filter(AccountEntity.alias == alias)

            accounts = query.all()

        return [AccountEntityAdapter(self.__decrypt(account)) for account in accounts]

    def get_active_account(self) -> Optional[Account]:
        db: Session
        account: AccountEntity

        with session_scope(self.session) as db:
            account = db.query(AccountEntity) \
                .filter_by(enabled=True) \
                .first()

        return AccountEntityAdapter(self.__decrypt(account)) if account is not None else None

    def add_account(self, vendor: str, access_key: str, secret_key: str, expired_at: datetime, alias: str):
        db: Session
        account: AccountEntity

        data_key, plain_key = self.kms.create_data_key()
        key = plain_key.decode("utf-8")

        access_key_enc = aes.encrypt(plaintext=access_key, key=key)
        secret_key_enc = aes.encrypt(plaintext=secret_key, key=key)

        with session_scope(self.session) as db:
            account = AccountEntity(
                vendor=vendor,
                enabled=True,
                access_key=access_key_enc,
                secret_key=secret_key_enc,
                expired_at=expired_at,
                alias=alias,
                data_key=data_key
            )
            db.add(account)

    def update_credential(self, id: int, access_key: str, secret_key: str, expired_at: datetime):
        db: Session

        data_key, plain_key = self.kms.create_data_key()
        key = plain_key.decode("utf-8")

        access_key_enc = aes.encrypt(plaintext=access_key, key=key)
        secret_key_enc = aes.encrypt(plaintext=secret_key, key=key)

        with session_scope(self.session) as db:
            db.query(AccountEntity)\
                .filter(AccountEntity.id == id)\
                .update(
                    dict(
                        access_key=access_key_enc,
                        secret_key=secret_key_enc,
                        expired_at=expired_at,
                        data_key=data_key
                    )
                )

    def __decrypt(self, account: AccountEntity):
        key = self.kms.decrypt_data_key(blob=account.data_key)
        account.access_key = aes.decrypt(cipher_text=account.access_key, key=key)
        account.secret_key = aes.decrypt(cipher_text=account.secret_key, key=key)
        return account
