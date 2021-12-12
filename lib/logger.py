from os import environ

from loguru import logger
from sentry_sdk import capture_exception


def info(msg: str):
    logger.info(msg)


def error(exception: Exception):
    logger.exception(exception)

    # to trigger error alerts
    if environ.get("STAGE") == "prod":
        capture_exception(exception)
