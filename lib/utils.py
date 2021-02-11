from datetime import timedelta
from decimal import *
from datetime import timedelta


def find(list, func):
    return ([item for idx, item in enumerate(list) if func(item, idx, list)] or [None])[
        0
    ]


def missing_days(days):
    """API에서 받아온 데이터에 구멍이 있을 경우 디비와 대조해서 빠진 날짜를 계산"""
    date_set = set(days[0] + timedelta(x) for x in range((days[-1] - days[0]).days))
    return sorted(date_set - set(days))
