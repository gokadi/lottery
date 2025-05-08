from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.lottery.domain.entities import Lottery
from app.shared.repository import AbstractRepository


class AbstractLotteryRepository(AbstractRepository[Lottery], ABC):
    @abstractmethod
    def get_by_date(self, date: date) -> Optional[Lottery]:
        pass

    @abstractmethod
    def exists_for_date(self, date: date) -> bool:
        pass

    @abstractmethod
    def get_open_lotteries(self) -> list[Lottery]:
        pass
