# E2E

## Trade

The goal of the trade test is to check if trader can place buy/sell order.

In order to do that without hassle, following conditions are mocked.

    1. get_trading_tickers() to return "BTC"
    2. get_trading_strategies_by_ticker() to return aroon
    3. get_position_size() to return Decimal("5500")
    4. Aroon should_buy to return True / should_sell to return True

Simply put, buy BTC for aroon strategy and sell
