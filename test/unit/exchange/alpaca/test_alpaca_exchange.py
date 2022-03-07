from decimal import Decimal
import pytest


def test_get_last_candle(alpaca_paper_exchange):
    candle = alpaca_paper_exchange.get_last_candle("AAPL")
    assert candle.get_ticker() == "AAPL"

def test_get_all_assets(alpaca_paper_exchange):
    assets = alpaca_paper_exchange.get_all_assets()
    assert len(assets) == 1

@pytest.mark.skip
def test_buy(alpaca_paper_exchange):
    order = alpaca_paper_exchange.buy("AAPL", Decimal("10"))
    print(order)

@pytest.mark.skip
def test_sell(alpaca_paper_exchange):
    order = alpaca_paper_exchange.sell("AAPL", volume=Decimal("0.01"))
    print(order)

def test_get_order(alpaca_paper_exchange):
    id = "cd290836-1d5f-47d0-9182-45c07d6d6d95"
    order = alpaca_paper_exchange.get_order(id)
    assert order.get_id() == id
