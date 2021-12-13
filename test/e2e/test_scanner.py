import json
from datetime import datetime

import pytest
import requests


def test_add_candles_today():
    tickers = ["BTC"]

    response = requests.post("http://scanner:8080/2015-03-31/functions/function/invocations", data=json.dumps({ "tickers": tickers }))
    res = response.json()

    body = res["body"]
    status_code = res["statusCode"]

    assert status_code == 200, body
    assert body == 1, body


def test_add_candles_between():
    start = "2021-12-08"
    end = "2021-12-10"
    tickers = ["BTC", "ETH"]

    event = json.dumps({
        "start": start,
        "end": end,
        "tickers": tickers
    })
    response = requests.post("http://scanner:8080/2015-03-31/functions/function/invocations", data=event)
    res = response.json()

    body = res["body"]
    status_code = res["statusCode"]

    assert status_code == 200, body
    assert body == 4, body
