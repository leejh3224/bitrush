import logging as sentry_logger
from loguru import logger


def info(msg: str):
    logger.info(msg)


def error(msg: str):
    logger.error(msg)

    # to trigger error alerts
    sentry_logger.error(msg, exc_info=True, stack_info=True)
