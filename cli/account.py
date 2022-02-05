import typer
from datetime import datetime

from lib.account.account_repository import AccountRepository
from lib.db import get_session
from lib.kms import Kms

account_app = typer.Typer()


@account_app.command()
def add(vendor: str, access_key: str, secret_key: str, expired_at: str, alias: str):
    session = get_session()
    kms = Kms()
    account_repository = AccountRepository(session, kms)

    account_repository.add_account(
        vendor=vendor,
        access_key=access_key,
        secret_key=secret_key,
        expired_at=datetime.fromisoformat(expired_at),
        alias=alias
    )

@account_app.command()
def update_credential(id: int, access_key: str, secret_key: str, expired_at: str):
    session = get_session()
    kms = Kms()
    account_repository = AccountRepository(session, kms)

    account_repository.update_credential(
        id=id,
        access_key=access_key,
        secret_key=secret_key,
        expired_at=datetime.fromisoformat(expired_at)
    )
