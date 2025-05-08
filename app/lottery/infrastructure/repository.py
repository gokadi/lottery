from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.lottery.domain.entities import Ballot, Lottery
from app.lottery.domain.repository import AbstractLotteryRepository
from app.lottery.infrastructure.models import BallotModel, LotteryModel


class SqlAlchemyLotteryRepository(AbstractLotteryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_date(self, date_: date) -> Optional[Lottery]:
        row = (
            self.session.query(LotteryModel)
            .options(joinedload(LotteryModel.ballots))
            .filter(LotteryModel.date == date_)
            .first()
        )
        return self._to_entity(row) if row else None

    def save(self, lottery: Lottery) -> None:
        model = self._to_model(lottery)
        self.session.merge(model)

    def exists_for_date(self, date_: date) -> bool:
        return (
            self.session.query(LotteryModel).filter_by(date=date_).first()
            is not None
        )

    def get_open_lotteries(self) -> List[Lottery]:
        rows = (
            self.session.query(LotteryModel)
            .filter_by(winner_ballot_id=None)
            .all()
        )
        return [self._to_entity(row) for row in rows]

    def _to_entity(self, model: LotteryModel) -> Lottery:
        return Lottery(
            id=model.id,
            date=model.date,
            ballots=self._to_ballot_entities(model.ballots, model.id),
            winner_ballot_id=model.winner_ballot_id,
        )

    def _to_model(self, entity: Lottery) -> LotteryModel:
        return LotteryModel(
            id=entity.id,
            date=entity.date,
            winner_ballot_id=entity.winner_ballot_id,
            ballots=self._to_ballot_models(entity.ballots, entity.id),
        )

    def _to_ballot_entities(
        self, ballots: List[BallotModel], lottery_id: UUID
    ) -> List[Ballot]:
        return [
            Ballot(
                id=b.id,
                user_id=b.user_id,
                lottery_id=lottery_id,
                submitted_at=b.submitted_at,
            )
            for b in ballots
        ]

    def _to_ballot_models(
        self, ballots: List[Ballot], lottery_id: UUID
    ) -> List[BallotModel]:
        return [
            BallotModel(
                id=b.id,
                user_id=b.user_id,
                lottery_id=lottery_id,
                submitted_at=b.submitted_at,
            )
            for b in ballots
        ]
