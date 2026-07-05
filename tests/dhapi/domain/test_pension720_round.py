import datetime

from dhapi.domain.pension720_round import current_pension720_round


def test_anchor_round():
    # 2024-12-26(목)에 추첨된 회차는 243회
    assert current_pension720_round(datetime.date(2024, 12, 26)) == 243


def test_known_round_from_real_purchase():
    # 실제 구매 내역 기준: 2026-07-09(목) 추첨 회차는 323회
    assert current_pension720_round(datetime.date(2026, 7, 5)) == 323
    assert current_pension720_round(datetime.date(2026, 7, 9)) == 323


def test_round_increments_after_draw_day():
    assert current_pension720_round(datetime.date(2026, 7, 10)) == 324
    assert current_pension720_round(datetime.date(2026, 7, 16)) == 324


def test_returns_int_for_today():
    assert isinstance(current_pension720_round(), int)
