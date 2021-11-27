from lib.candle.candle import Candle
from lib.candle.candle_repository import CandleRepository


def test_get_candles(candle_repository: CandleRepository):
    candles = candle_repository.get_candles(ticker="BTC", count=10)
    print(candles)
    assert len(candles) == 10


def test_add_candles(candle_repository: CandleRepository, mock_candle: Candle):
    candle_repository.add_candles(candles=[mock_candle, mock_candle])
