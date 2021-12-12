import json

import pytest
import requests


def test_add_candles_today():
    response = requests.post("http://scanner:8080/2015-03-31/functions/function/invocations", data="{}")
    res = response.json()

    body = res["body"]
    status_code = res["statusCode"]

    assert status_code == 200, body
    assert body == 1, body


def test_add_candles_between():
    event = json.dumps({
        "start": "2021-12-08",
        "end": "2021-12-10"
    })
    response = requests.post("http://scanner:8080/2015-03-31/functions/function/invocations", data=event)
    res = response.json()

    body = res["body"]
    status_code = res["statusCode"]

    assert status_code == 200, body
    assert body == 2, body
