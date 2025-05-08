from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.shared.repository import AbstractRepository
from app.user.domain.entities import User


class AbstractUserRepository(AbstractRepository[User], ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def exists(self, user_id: UUID) -> bool:
        pass
