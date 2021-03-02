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


def is_trade_completed(order) -> bool:
    """해당 주문의 거래가 완료되었는지를 확인

    주문 : 거래 = 1 : N 관계이며, 한 주문이 여러 개의 거래를 발생시킬 수 있다.
    해당 함수는 인자로 들어온 주문과 관련된 거래가 모두 완료되었는지를 검사한다.

    Args:
        order (dict): 업비트 주문
    """
    return order["state"] != "wait"
