from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository
from lib.ticker import Ticker


def test_get_candles(candle_repository: CandleRepository):
    candles = candle_repository.get_candles(ticker="BTC", count=10)
    print(candles)
    assert len(candles) == 10


def test_add_candle(candle_repository: CandleRepository, mock_candle: Candle):
    candle_repository.add_candle(candle=mock_candle)
