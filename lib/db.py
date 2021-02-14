import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os

sql_logging = os.getenv("SQL_LOGGING")
connection_string = os.getenv("BITRUSH_CONNECTION_STRING")

engine = db.create_engine(
    connection_string,
    pool_size=20,
    convert_unicode=True,
    echo=sql_logging == "True",
)
Session = sessionmaker(bind=engine)
session = Session()
