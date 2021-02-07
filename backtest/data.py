from sqlalchemy import create_engine
import pandas as pd
import os

db_url = os.getenv("BITRUSH_CONNECTION_STRING")
engine = create_engine(db_url, convert_unicode=True)
db = engine.connect()


def get_ohlcv(ticker="BTC"):
    data = pd.read_sql_query(
        f"""
	select date, open, high, low, close, volume
	from ohlcv
	where ticker = '{ticker}';
	""",
        db,
    ).fillna(0)
    data["date"] = pd.to_datetime(data["date"])
    data.set_index("date", inplace=True)
    return data
