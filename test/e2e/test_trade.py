import json
import time

import requests


lambda_endpoint = "2015-03-31/functions/function/invocations"

order_syncer_url = f"http://order_syncer:8080/{lambda_endpoint}"
trader_url = f"http://trader:8080/{lambda_endpoint}"

def test_buy_and_sell():

    # buy
    response = requests.post(trader_url, data=json.dumps({
        "tickers": ["BTC"],
        "position-size": "5500",
        "strategy": "must_trade",
        "account-alias": "gompro-local"
    }))
    res = response.json()

    assert len(res["body"].split(",")) > 0, res["body"]

    time.sleep(3)

    # sync
    response = requests.post(order_syncer_url, data=json.dumps({
        "account-alias": "gompro-local"
    }))
    res = response.json()

    assert len(res["body"].split(",")) > 0, res["body"]

    # sell
    response = requests.post(trader_url, data=json.dumps({
        "tickers": ["BTC"],
        "position-size": "5500",
        "strategy": "must_trade",
        "account-alias": "gompro-local"
    }))
    res = response.json()

    assert len(res["body"].split(",")) > 0, res["body"]

    time.sleep(3)

    # sync
    response = requests.post(order_syncer_url, data=json.dumps({
        "account-alias": "gompro-local"
    }))
    res = response.json()

    assert len(res["body"].split(",")) > 0, res["body"]


def test_trade_with_no_params():
    response = requests.post(trader_url, data="{}")
    res = response.json()

    assert res["body"] == "", res["body"]
