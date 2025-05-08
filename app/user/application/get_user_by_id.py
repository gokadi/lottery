from uuid import UUID

from app.user.domain.entities import User
from app.user.domain.repository import AbstractUserRepository


class GetUserByIdUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    def execute(self, user_id: UUID) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
