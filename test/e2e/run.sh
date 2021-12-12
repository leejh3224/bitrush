#!/bin/bash

docker compose -f docker-compose.e2e-test.yml build --build-arg NO_CACHE_TIMESTAMP="$(date +%Y-%m-%d:%H:%M:%S)"

docker compose -f docker-compose.e2e-test.yml up --abort-on-container-exit --exit-code-from e2e-test
exit_code=$?

docker compose -f docker-compose.e2e-test.yml down -v

if [ $exit_code -eq 0 ]; then
    echo "test passed"
    exit 0;
else
    echo "test failed"
    exit 1;
fi

# 1. get_trading_tickers() to return "BTC"
# 2. get_trading_strategies_by_ticker() to return aroon
# 3. get_position_size() to return Decimal("5500")
# 4. Aroon should_buy to return True / should_sell to return True
