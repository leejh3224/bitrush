from datetime import datetime

from pydantic import BaseModel


class Bar(BaseModel):

    # ISO8601 timestamp
    t: datetime

    # open price
    o: float

    # high price
    h: float

    # low price
    l: float

    # close price
    c: float

    # volume
    v: float
