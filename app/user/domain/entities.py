from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    name: Optional[str] = None
    banned_at: Optional[datetime] = None

    def is_banned(self) -> bool:
        return self.banned_at is not None

    def ban(self):
        if self.is_banned():
            raise RuntimeError("User is already banned.")
        self.banned_at = datetime.now(timezone.utc)

    def unban(self):
        self.banned_at = None
