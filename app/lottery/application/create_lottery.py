from datetime import date

from sqlalchemy.orm import Session

from app.lottery.domain.entities import Lottery
from app.lottery.domain.repository import AbstractLotteryRepository


class CreateLotteryUseCase:
    def __init__(
        self,
        repo: AbstractLotteryRepository,
        session: Session,
    ):
        self.repo = repo
        self.session = session

    def execute(self, date_: date) -> None:
        if self.repo.exists_for_date(date_):
            raise ValueError("Lottery already exists for this date")

        lottery = Lottery.create(date=date_)
        self.repo.save(lottery)
        self.session.commit()
