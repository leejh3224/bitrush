import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager

sql_logging = os.getenv("SQL_LOGGING")
connection_string = os.getenv("BITRUSH_CONNECTION_STRING")

engine = db.create_engine(
    connection_string,
    pool_size=20,
    convert_unicode=True,
    echo=sql_logging == "True",
)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
