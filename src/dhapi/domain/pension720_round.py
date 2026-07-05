import datetime
from typing import Optional

import pytz

# 2024-12-26(목)에 추첨된 회차는 243회. 연금복권720+는 매주 목요일 추첨.
_ANCHOR_DRAW_DATE = datetime.date(2024, 12, 26)
_ANCHOR_ROUND = 243


def current_pension720_round(today: Optional[datetime.date] = None) -> int:
    """현재 판매 중인 연금복권720+ 회차 (다가오는 목요일에 추첨되는 회차)"""
    if today is None:
        today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).date()
    days_until_thursday = (3 - today.weekday()) % 7
    next_thursday = today + datetime.timedelta(days=days_until_thursday)
    weeks_passed = (next_thursday - _ANCHOR_DRAW_DATE).days // 7
    return _ANCHOR_ROUND + weeks_passed
