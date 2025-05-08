from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.user.api.v1.dependencies import (
    get_ban_user_use_case,
    get_get_user_by_id_use_case,
    get_unban_user_use_case,
)
from app.user.api.v1.dtos import UserResponseDto
from app.user.application.ban_user import BanUserUseCase
from app.user.application.get_user_by_id import GetUserByIdUseCase
from app.user.application.unban_user import UnbanUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponseDto)
def get_user(
    user_id: UUID,
    use_case: GetUserByIdUseCase = Depends(get_get_user_by_id_use_case),
):
    try:
        return use_case.execute(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/{user_id}/ban", status_code=status.HTTP_204_NO_CONTENT)
def ban_user(
    user_id: UUID,
    use_case: BanUserUseCase = Depends(get_ban_user_use_case),
):
    try:
        use_case.execute(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{user_id}/unban", status_code=status.HTTP_204_NO_CONTENT)
def unban_user(
    user_id: UUID,
    use_case: UnbanUserUseCase = Depends(get_unban_user_use_case),
):
    try:
        use_case.execute(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
