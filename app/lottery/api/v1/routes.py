import os
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.lottery.api.v1.dependencies import (
    get_close_lottery_use_case,
    get_create_lottery_use_case,
    get_get_winner_use_case,
    get_submit_ballot_use_case,
)
from app.lottery.api.v1.dtos import BallotResponseDto
from app.lottery.application.close_lottery import CloseLotteryUseCase
from app.lottery.application.create_lottery import CreateLotteryUseCase
from app.lottery.application.get_winner import GetWinningBallotUseCase
from app.lottery.application.submit_ballot import SubmitBallotUseCase

router = APIRouter(prefix="/lotteries", tags=["lotteries"])


@router.post("/submit", status_code=status.HTTP_204_NO_CONTENT)
def submit_ballot(
    user_id: UUID,
    date_: date,
    use_case: SubmitBallotUseCase = Depends(get_submit_ballot_use_case),
):
    try:
        use_case.execute(user_id=user_id, date_=date_)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_lottery(
    date_: date,
    use_case: CreateLotteryUseCase = Depends(get_create_lottery_use_case),
):
    try:
        use_case.execute(date_)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/close", status_code=status.HTTP_204_NO_CONTENT)
def close_lottery(
    date_: date,
    x_internal_token: str = Header(...),
    use_case: CloseLotteryUseCase = Depends(get_close_lottery_use_case),
):
    if x_internal_token != os.getenv("INTERNAL_CLOSE_TOKEN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        use_case.execute(date_=date_)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/lotteries/winner", response_model=BallotResponseDto)
def get_winner(
    date_: date = Query(..., alias="date"),
    use_case: GetWinningBallotUseCase = Depends(get_get_winner_use_case),
):
    result = use_case.execute(date_)
    if not result:
        raise HTTPException(status_code=404, detail="No winner for this date")
    return result
