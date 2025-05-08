from datetime import date
from typing import Optional

from app.lottery.domain.entities import Ballot
from app.lottery.domain.repository import AbstractLotteryRepository


class GetWinningBallotUseCase:
    def __init__(self, lottery_repo: AbstractLotteryRepository):
        self.lottery_repo = lottery_repo

    def execute(self, date_: date) -> Optional[Ballot]:
        lottery = self.lottery_repo.get_by_date(date_)
        if not lottery or not lottery.winner_ballot_id:
            return None

        ballots_by_id = {b.id: b for b in lottery.ballots}

        return ballots_by_id.get(lottery.winner_ballot_id)
