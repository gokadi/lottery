from dataclasses import dataclass, field
from datetime import date as date_type
from datetime import datetime, timezone
from typing import List, Optional, Self
from uuid import UUID, uuid4


@dataclass
class Ballot:
    id: UUID
    user_id: UUID
    lottery_id: UUID
    submitted_at: datetime

    @staticmethod
    def create(user_id: UUID, lottery_id: UUID) -> "Ballot":
        return Ballot(
            id=uuid4(),
            user_id=user_id,
            lottery_id=lottery_id,
            submitted_at=datetime.now(timezone.utc),
        )


@dataclass
class Lottery:
    id: UUID
    date: date_type
    ballots: List[Ballot] = field(default_factory=list)
    winner_ballot_id: Optional[UUID] = None

    @classmethod
    def create(cls, date: date_type) -> "Lottery":
        return cls(
            id=uuid4(),
            date=date,
            ballots=[],
            winner_ballot_id=None,
        )

    def add_ballot(self, ballot: Ballot) -> None:
        if ballot.lottery_id != self.id:
            raise ValueError("Ballot does not match lottery ID.")
        self.ballots.append(ballot)

    @property
    def is_closed(self) -> bool:
        return datetime.now(timezone.utc).date() > self.date
