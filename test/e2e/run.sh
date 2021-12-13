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

