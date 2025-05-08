from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.database import get_session
from app.user.application.ban_user import BanUserUseCase
from app.user.application.get_user_by_id import GetUserByIdUseCase
from app.user.application.unban_user import UnbanUserUseCase
from app.user.infrastructure.repository import SqlAlchemyUserRepository


def get_user_repository(
    session: Session = Depends(get_session),
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


def get_ban_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    session: Session = Depends(get_session),
) -> BanUserUseCase:
    return BanUserUseCase(repo, session)


def get_unban_user_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
    session: Session = Depends(get_session),
) -> UnbanUserUseCase:
    return UnbanUserUseCase(repo, session)


def get_get_user_by_id_use_case(
    repo: SqlAlchemyUserRepository = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repo)
