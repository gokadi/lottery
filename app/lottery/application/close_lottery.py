from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.lottery.domain.repository import AbstractLotteryRepository
from app.lottery.domain.service import LotteryService


class CloseLotteryUseCase:
    def __init__(
        self,
        lottery_repo: AbstractLotteryRepository,
        session: Session,
    ):
        self.lottery_repo = lottery_repo
        self.session = session

    def execute(self, date_: Optional[date] = None) -> None:
        date_ = date_ or datetime.now(timezone.utc).date()

        lottery = self.lottery_repo.get_by_date(date_)
        if not lottery:
            raise ValueError("No lottery exists for the given date.")

        winner = LotteryService.draw_winner(lottery)
        lottery.winner_ballot_id = winner.id

        self.lottery_repo.save(lottery)
        self.session.commit()
