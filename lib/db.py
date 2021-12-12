from os import environ

import sqlalchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy model base class
from sqlalchemy.sql import Insert
import time

Base = declarative_base()


def get_session(connection_string=None, sql_logging=None) -> Session:
    if not connection_string:
        connection_string = environ.get("BITRUSH_CONNECTION_STRING")

    if not sql_logging:
        sql_logging = environ.get("SQL_LOGGING") == "True"

    engine = sqlalchemy.create_engine(
        connection_string,
        pool_size=20,
        echo=sql_logging,
    )
    return Session(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope(session: Session):
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@compiles(Insert)
def on_duplicate_key_update(insert, compiler, **kwargs):
    sql = compiler.visit_insert(insert, **kwargs)
    if "on_duplicate_key_update" in insert.kwargs:
        compares = insert.kwargs["on_duplicate_key_update"]
        return sql + " ON DUPLICATE KEY UPDATE " + ",".join([compare[0] + " = " + compare[1] for compare in compares.items()])
    return sql


def wait_for_db_init(session: Session):
    """wait for docker mysql init script"""
    tables = ["account", "candle", "order"]
    max_tries = 10
    num_tries = 0

    while True:
        time.sleep(0.5)
        result = session.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'bitrush' AND TABLE_NAME IN :tables", params={'tables': tables})
        count_tables = result.first()[0]
        num_tries += 1

        if num_tries >= max_tries or count_tables == len(tables):
            break
