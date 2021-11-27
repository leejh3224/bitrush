from typing import List

from sqlalchemy.dialects.mysql import insert

from lib.candle.candle import Candle
from lib.candle.candle_entity import CandleEntity
from lib.candle.candle_entity_adapter import CandleEntityAdapter
from lib.db import session_scope
from sqlalchemy.orm.session import Session


class CandleRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_candles(self, ticker: str, count: int) -> List[Candle]:
        db: Session
        candles: List[CandleEntity]

        with session_scope(self.session) as db:
            candles = db \
                .query(CandleEntity) \
                .filter_by(ticker=ticker) \
                .limit(count) \
                .all()

        return [CandleEntityAdapter(candle) for candle in candles]

    def add_candle(self, candle: Candle):
        stmt = insert(CandleEntity).values(
            ticker=candle.get_ticker(),
            closed_at=candle.get_closed_at(),
            open=candle.get_open_price(),
            high=candle.get_high_price(),
            low=candle.get_low_price(),
            close=candle.get_close_price(),
            volume=candle.get_volume()
        ).on_duplicate_key_update(id=CandleEntity.id)  # ignore duplicate

        self.session.execute(stmt)
