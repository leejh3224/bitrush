from decimal import Decimal
import pytest


def test_get_last_candle(alpaca_paper_exchange):
    candle = alpaca_paper_exchange.get_last_candle("AAPL")
    assert candle.get_ticker() == "AAPL"

def test_get_all_assets(alpaca_paper_exchange):
    assets = alpaca_paper_exchange.get_all_assets()
    assert len(assets) == 2

@pytest.mark.skip
def test_buy(alpaca_paper_exchange):
    order = alpaca_paper_exchange.buy("AAPL", Decimal("20"))
    print(order)

@pytest.mark.skip
def test_sell(alpaca_paper_exchange):
    order = alpaca_paper_exchange.sell("AAPL", volume=Decimal("0.1"))
    print(order)

def test_get_order(alpaca_paper_exchange):
    selling_order_id = "d272a4e8-d20b-490b-a864-9c46e884eb64"
    # buying_order_id = "fe8305b1-bbf4-4059-bc63-49d07c8b9b7e"
    order = alpaca_paper_exchange.get_order(selling_order_id)
    assert order.get_id() == selling_order_id
