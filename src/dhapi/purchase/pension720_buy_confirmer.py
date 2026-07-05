import logging

logger = logging.getLogger(__name__)


class Pension720BuyConfirmer:
    def confirm(self, round_number: int, always_yes: bool = False):
        print(f"🎯 연금복권720+ {round_number}회 자동번호 1세트(1~5조 동일번호, 5장, 5,000원)를 구매합니다.")
        print("❓ 위와 같이 구매하시겠습니까? [Y/n] ", end="")

        if always_yes:
            print("\n✅ --yes 플래그가 주어져 자동으로 구매를 진행합니다.")
            return True
        if input().strip().lower() in ["y", "yes", ""]:
            return True

        print("❗️구매를 취소했습니다.")
        return False
