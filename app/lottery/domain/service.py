import random

from app.lottery.domain.entities import Ballot, Lottery


class LotteryService:
    @staticmethod
    def draw_winner(lottery: Lottery) -> Ballot:
        if not lottery.is_closed:
            raise RuntimeError("Cannot draw winner before lottery closes.")

        if lottery.winner_ballot_id is not None:
            raise RuntimeError("Winner already drawn.")

        if not lottery.ballots:
            raise RuntimeError("No ballots submitted.")

        winner = random.choice(lottery.ballots)
        lottery.winner_ballot_id = winner.id
        return winner
