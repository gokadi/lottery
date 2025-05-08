from fastapi import Depends
from sqlalchemy.orm import Session

from app.lottery.application.close_lottery import CloseLotteryUseCase
from app.lottery.application.create_lottery import CreateLotteryUseCase
from app.lottery.application.get_winner import GetWinningBallotUseCase
from app.lottery.application.submit_ballot import SubmitBallotUseCase
from app.lottery.infrastructure.repository import SqlAlchemyLotteryRepository
from app.shared.database import get_session
from app.user.api.v1.dependencies import get_user_repository
from app.user.infrastructure.repository import SqlAlchemyUserRepository


def get_lottery_repository(
    session: Session = Depends(get_session),
) -> SqlAlchemyLotteryRepository:
    return SqlAlchemyLotteryRepository(session)


def get_submit_ballot_use_case(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    lottery_repo: SqlAlchemyLotteryRepository = Depends(
        get_lottery_repository
    ),
    session: Session = Depends(get_session),
) -> SubmitBallotUseCase:
    return SubmitBallotUseCase(user_repo, lottery_repo, session)


def get_close_lottery_use_case(
    lottery_repo: SqlAlchemyLotteryRepository = Depends(
        get_lottery_repository
    ),
    session: Session = Depends(get_session),
) -> CloseLotteryUseCase:
    return CloseLotteryUseCase(lottery_repo, session)


def get_get_winner_use_case(
    lottery_repo: SqlAlchemyLotteryRepository = Depends(
        get_lottery_repository
    ),
) -> GetWinningBallotUseCase:
    return GetWinningBallotUseCase(lottery_repo)


def get_create_lottery_use_case(
    repo: SqlAlchemyLotteryRepository = Depends(get_lottery_repository),
    session: Session = Depends(get_session),
) -> CreateLotteryUseCase:
    return CreateLotteryUseCase(repo, session)
