from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.user.domain.entities import User
from app.user.domain.repository import AbstractUserRepository
from app.user.infrastructure.models import UserModel


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        row = self.session.get(UserModel, user_id)
        return self._to_entity(row) if row else None

    def exists(self, user_id: UUID) -> bool:
        return (
            self.session.query(UserModel.id).filter_by(id=user_id).first()
            is not None
        )

    def save(self, user: User) -> None:
        model = self._to_model(user)
        self.session.merge(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            name=model.name,
            banned_at=model.banned_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            name=entity.name,
            banned_at=entity.banned_at,
        )
