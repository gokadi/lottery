from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.lottery.domain.entities import Ballot, Lottery
from app.lottery.domain.repository import AbstractLotteryRepository
from app.user.domain.entities import User
from app.user.domain.repository import AbstractUserRepository


class SubmitBallotUseCase:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        lottery_repo: AbstractLotteryRepository,
        session: Session,
    ):
        self.user_repo = user_repo
        self.lottery_repo = lottery_repo
        self.session = session

    def execute(self, user_id: UUID, date_: date | None = None) -> None:
        date_ = date_ or datetime.now(timezone.utc).date()

        user: User | None = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user.is_banned():
            raise PermissionError("User is banned")

        lottery = self.lottery_repo.get_by_date(date_)
        if lottery is None:
            lottery = Lottery.create(date=date_)

        ballot = Ballot.create(user_id=user.id, lottery_id=lottery.id)
        lottery.add_ballot(ballot)

        self.lottery_repo.save(lottery)
        self.session.commit()
