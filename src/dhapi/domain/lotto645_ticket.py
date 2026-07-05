import random
from enum import Enum
from typing import Iterable, List, Optional


class Lotto645Mode(str, Enum):
    AUTO = "auto"
    SEMIAUTO = "semiauto"
    MANUAL = "manual"


class Lotto645Ticket:
    def __init__(self, numbers: Optional[str] = None):
        try:
            if not numbers:
                self.numbers = []
            else:
                self.numbers = sorted(list(map(int, numbers.split(","))))
        except ValueError:
            raise ValueError(f"숫자를 입력하세요 (입력된 값: {numbers}).")

        if len(self.numbers) != len(set(self.numbers)):
            raise ValueError(f"중복되지 않도록 숫자들을 입력하세요 (입력된 값: {numbers}).")

        for n in self.numbers:
            if not 1 <= n <= 45:
                raise ValueError(f"각 번호는 1부터 45까지의 숫자만 사용할 수 있습니다 (입력된 값: {n}).")

        if len(self.numbers) == 6:
            self.mode = Lotto645Mode.MANUAL
        elif 1 <= len(self.numbers) <= 5:
            self.mode = Lotto645Mode.SEMIAUTO
        elif len(self.numbers) == 0:
            self.mode = Lotto645Mode.AUTO
        else:
            raise ValueError(f"숫자는 0개 이상 6개 이하의 숫자를 입력해야 합니다 (입력된 값: {numbers}).")

    @property
    def mode_kor(self):
        if self.mode == Lotto645Mode.AUTO:
            return "자동"
        elif self.mode == Lotto645Mode.SEMIAUTO:
            return "반자동"
        elif self.mode == Lotto645Mode.MANUAL:
            return "수동"
        else:
            raise RuntimeError("지원하지 않는 게임 타입입니다.")

    @staticmethod
    def create_auto_tickets(count: int):
        return [Lotto645Ticket() for _ in range(count)]

    @staticmethod
    def create_tickets(numbers_list: List[str]):
        return [Lotto645Ticket(numbers) for numbers in numbers_list]

    @staticmethod
    def create_tickets_excluding(excluded_numbers: Iterable[int], count: int = 5):
        """제외할 번호들을 뺀 풀에서 랜덤 6개씩 뽑아 수동모드 티켓을 생성

        확률적 이득은 없지만(매 회차 독립 시행) 직전 회차 당첨번호를 피하고 싶을 때 사용한다.
        """
        pool = [n for n in range(1, 46) if n not in set(excluded_numbers)]
        if len(pool) < 6:
            raise ValueError(f"제외 후 남은 번호가 6개 미만입니다 (남은 개수: {len(pool)}).")

        rng = random.SystemRandom()
        return [Lotto645Ticket(",".join(map(str, rng.sample(pool, 6)))) for _ in range(count)]
