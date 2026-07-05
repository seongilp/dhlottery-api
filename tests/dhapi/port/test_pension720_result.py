from dhapi.port.lottery_client import LotteryClient


def test_current_api_success_response():
    # 2026-07-05 실제 구매 성공 응답 형태
    response = {
        "resultCode": "100",
        "resultMessage": None,
        "resultMessageCode": None,
        "data": {"ltPrchsQty": 5, "prchsLtNoInfoLstCn": "104347|202607059027673|100000914946059|323|1"},
    }
    assert LotteryClient._is_pension720_success(response)


def test_legacy_api_success_response():
    assert LotteryClient._is_pension720_success({"loginYn": "Y", "result": {"resultMsg": "SUCCESS"}})


def test_failure_responses():
    assert not LotteryClient._is_pension720_success({"resultCode": "300", "resultMessage": "예치금이 부족합니다."})
    assert not LotteryClient._is_pension720_success({"loginYn": "N"})
    assert not LotteryClient._is_pension720_success({})


def test_failure_reason():
    assert LotteryClient._pension720_failure_reason({"resultCode": "300", "resultMessage": "예치금이 부족합니다."}) == "예치금이 부족합니다."
    assert LotteryClient._pension720_failure_reason({"loginYn": "Y", "result": {"resultMsg": "FAILURE"}}) == "FAILURE"
