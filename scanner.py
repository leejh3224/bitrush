from dotenv import load_dotenv

load_dotenv()

from typing import Any, Dict
from lib.db import session
from lib.models.ohlcv import Ohlcv
from lib.ticker import Ticker
from lib.upbit import Upbit
from datetime import datetime, timedelta


def main(event: Dict[str, Any], context) -> None:
    """명시된 ticker의 일봉 정보를 저장

    Args:
        event (dict): 람다 이벤트
            - end (str): yyyy-mm-dd 09:00:00 형식의 날짜
            - days (int): end를 포함한, 일봉 데이터를 저장할 기간
        context (dict): 람다 컨텍스트
    """
    upbit = Upbit()

    yesterday = datetime.today() - timedelta(days=1)
    end = (
        datetime.strptime(event.get("end"), "%Y-%m-%d %H:%M:%S")
        if event.get("end")
        else yesterday
    )

    end = end.replace(hour=9, minute=0, second=0)
    days = event.get("days", 1)
    tickers = [ticker.value for ticker in Ticker]

    for ticker in tickers:
        ohlcvs = []
        candles = upbit.get_ohlcv_daily(ticker=ticker, end=end, days=days)

        for candle in candles:
            ohlcv = Ohlcv(
                ticker=candle["market"].replace("KRW-", ""),
                date=datetime.strptime(
                    candle["candle_date_time_kst"], "%Y-%m-%dT%H:%M:%S"
                ),
                open=candle["opening_price"],
                high=candle["high_price"],
                low=candle["low_price"],
                close=candle["trade_price"],
                volume=candle["candle_acc_trade_volume"],
            )
            ohlcvs.append(ohlcv)
        ohlcvs.reverse()

        session.add_all(ohlcvs)
        session.commit()


if __name__ == "__main__":
    # main({"end": "2021-01-24 09:00:00", "days": 1}, "")
    main({}, {})
