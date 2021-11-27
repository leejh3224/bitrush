from os import environ

import sqlalchemy
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base

# sqlalchemy model base class
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
def session_scope(sess: Session):
    """Provide a transactional scope around a series of operations."""
    try:
        yield sess
        sess.commit()
    except Exception:
        sess.rollback()
        raise
    finally:
        sess.close()
