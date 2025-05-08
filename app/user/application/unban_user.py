from uuid import UUID

from sqlalchemy.orm import Session

from app.user.domain.repository import AbstractUserRepository


class UnbanUserUseCase:
    def __init__(self, repo: AbstractUserRepository, session: Session):
        self.repo = repo
        self.session = session

    def execute(self, user_id: UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.unban()
        self.repo.save(user)
        self.session.commit()
