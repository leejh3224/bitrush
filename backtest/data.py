from sqlalchemy import create_engine
import backtrader as bt
import pandas as pd

db_name = 'bitrush'
engine = create_engine(
    f'mysql://root:@localhost:3306/{db_name}', convert_unicode=True)
db = engine.connect()


def get_ohlcv(ticker='BTC'):
    data = pd.read_sql_query(f'''
	select date, open, high, low, close, volume
	from ohlcv
	where ticker = '{ticker}';
	''', db).fillna(0)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    return data
